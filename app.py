import nltk
import os
import shutil

# Set NLTK data path
nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')

def download_nltk_data():
    """Download required NLTK data with cleanup on failure"""
    required_packages = ['stopwords', 'punkt', 'punkt_tab', 'averaged_perceptron_tagger']
    
    for package in required_packages:
        try:
            # Check if already exists
            if package == 'stopwords':
                nltk.data.find(f'corpora/{package}')
            elif 'punkt' in package:
                nltk.data.find(f'tokenizers/{package}')
            else:
                nltk.data.find(f'taggers/{package}')
        except LookupError:
            # Try to download
            try:
                print(f"Downloading {package}...")
                nltk.download(package, quiet=True, raise_on_error=True)
            except Exception as e:
                # If download fails, try to clean up corrupted files
                print(f"Error downloading {package}: {e}")
                corrupted_paths = [
                    os.path.join(nltk_data_dir, 'corpora', package),
                    os.path.join(nltk_data_dir, 'tokenizers', package),
                    os.path.join(nltk_data_dir, 'taggers', package),
                ]
                for path in corrupted_paths:
                    if os.path.exists(path):
                        shutil.rmtree(path, ignore_errors=True)
                # Retry download
                try:
                    nltk.download(package, quiet=True, raise_on_error=True)
                except:
                    pass

# Download NLTK data
download_nltk_data()
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_models, load_dictionary
from utils.normalisasi import normalize_text
from utils.pos_tagging import pos_tagging
from utils.ekstraksi_opini import extract_opinions
from utils.preprocessing import preprocess_text
from utils.prediction import predict_aspect_sentiment


# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="M-ABSA Layanan Kesehatan",
    page_icon=" ",
    layout="wide"
)

# =====================================================
# LOAD RESOURCE
# =====================================================
@st.cache_resource
def load_resource():
    models = load_models()
    kamus = load_dictionary()
    return models, kamus

models, kamus = load_resource()

# =====================================================
# PIPELINE
# =====================================================
def process_single_review(text):
    norm = normalize_text(text, kamus)
    pos = pos_tagging(norm)
    opinions = extract_opinions(pos)
    processed = preprocess_text(opinions)
    results = predict_aspect_sentiment(processed, models)
    return results

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Home", "Prediksi Ulasan Tunggal", "Prediksi CSV"]
)

# =====================================================
# HOME PAGE
# =====================================================
if menu == "Home":

    st.markdown(
        """
        <h1 style='text-align:center;'>M-ABSA berbasis Ekstraksi Opini<br>
        untuk Ulasan Layanan Kesehatan</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Deskripsi Sistem")
    st.write(
        """
        **M-ABSA (Multiclass Aspect-Based Sentiment Analysis)** merupakan sistem analisis sentimen
        yang menerapkan **metode ekstraksi opini** untuk menganalisis ulasan layanan kesehatan.
        
        Sistem ini dirancang untuk mengidentifikasi **aspek layanan** yang dibahas dalam ulasan
        serta menentukan **sentimen (positif atau negatif)** pada setiap aspek tersebut.
        """
    )
    st.markdown("### Aspek yang Dianalisis")
    st.markdown(
        """
        - **KPMS (Kualitas Pelayanan Medis dan Staf)**  
        - **FI (Fasilitas dan Infrastruktur)**          
        - **WT (Waktu Tunggu)**  
        - **BL (Biaya Layanan)**  
        """
    )

    st.info("📂 Sistem mendukung input **ulasan tunggal** maupun **file CSV** untuk analisis massal.")

# =====================================================
# MODE 1: ULASAN TUNGGAL
# =====================================================
elif menu == "Prediksi Ulasan Tunggal":

    st.title("Prediksi Ulasan Tunggal")

    review = st.text_area(
        "Masukkan ulasan layanan kesehatan:",
        height=150,
        placeholder="Pelayanan dokter ramah tetapi waktu tunggu lama"
    )

    if st.button("Prediksi"):
        if review.strip():
            with st.spinner("Memproses ulasan..."):
                results = process_single_review(review)

            if results:
                for r in results:
                    st.markdown(
                        f"""
                        <div style="padding:15px;border-left:5px solid #00d4ff;
                        background:#1e293b;color:#e2e8f0;margin-bottom:10px;
                        border-radius:8px">
                        <b>Opini:</b> {r['opini']}<br>
                        <b>Aspek:</b> {r['aspek']}<br>
                        <b>Sentimen:</b> {r['sentimen']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("Tidak ada opini terdeteksi.")
        else:
            st.warning("Masukkan ulasan terlebih dahulu.")

# =====================================================
# MODE 2: UPLOAD CSV
# =====================================================
else:

    st.title("Prediksi CSV")

    uploaded_file = st.file_uploader(
        "Upload file CSV (berisi kolom ulasan)",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        kolom_ulasan = st.selectbox(
            "Pilih kolom ulasan:",
            df.columns
        )

        if st.button(" Analisis CSV"):
            with st.spinner("Memproses seluruh ulasan..."):
                all_results = []

                for ulasan in df[kolom_ulasan].dropna():
                    results = process_single_review(ulasan)
                    for r in results:
                        all_results.append({
                            "Ulasan": ulasan,
                            "Opini": r["opini"],
                            "Aspek": r["aspek"],
                            "Sentimen": r["sentimen"]
                        })

            if all_results:
                hasil_df = pd.DataFrame(all_results)

                st.subheader("Tabel Hasil Analisis")
                st.dataframe(hasil_df, use_container_width=True)

                st.subheader(" Statistik Sentimen")
                fig1 = px.bar(
                    hasil_df["Sentimen"].value_counts().reset_index(),
                    x="index", y="Sentimen",
                    labels={"index": "Sentimen", "Sentimen": "Jumlah"}
                )
                st.plotly_chart(fig1, use_container_width=True)

                st.subheader("📊 Distribusi Aspek")
                fig2 = px.pie(
                    hasil_df,
                    names="Aspek"
                )
                st.plotly_chart(fig2, use_container_width=True)

            else:
                st.warning("Tidak ada opini yang berhasil diekstraksi.")
