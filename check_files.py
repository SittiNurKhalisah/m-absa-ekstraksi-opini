import os

files = os.listdir('models/')
print("File di folder models:")
for f in sorted(files):
    print(f"  - {f}")