import subprocess
import sys

# Gerekli kütüphaneleri kontrol edip yükleyin
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

# Gerekli kütüphanelerin yüklenmesi
install_and_import("hashlib")
install_and_import("cryptography")

import hashlib
from cryptography.fernet import Fernet

with open("Albil_staj.txt", "w") as dosya:
    dosya.write("Bu bir deneme yazısıdır.")

def dosya_hash_hesapla(dosya_yolu):
    sha256 = hashlib.sha256()
    with open(dosya_yolu, "rb") as f:
        for veri_blok in iter(lambda: f.read(4096), b""):
            sha256.update(veri_blok)
    return sha256.hexdigest()

ilk_hash = dosya_hash_hesapla("Albil_staj.txt")

with open("Albil_staj_hash.txt", "w") as dosya:
    dosya.write(ilk_hash)

anahtar = Fernet.generate_key()
sifreleyici = Fernet(anahtar)

with open("Albil_staj_hash.txt", "rb") as dosya:
    hash_verisi = dosya.read()

sifrelenmis_hash = sifreleyici.encrypt(hash_verisi)

with open("Albil_staj_hash.enc", "wb") as dosya:
    dosya.write(sifrelenmis_hash)

with open("Albil_staj.txt", "w") as dosya:
    dosya.write("Bu yazı değiştirilmiştir.")

degisen_hash = dosya_hash_hesapla("Albil_staj.txt")

with open("Albil_staj_hash_2.txt", "w") as dosya:
    dosya.write(degisen_hash)

with open("Albil_staj_hash.enc", "rb") as dosya:
    sifrelenmis_veri = dosya.read()

cozulmus_hash = sifreleyici.decrypt(sifrelenmis_veri).decode()

if ilk_hash == degisen_hash:
    print("Dosya değişmemiş")
else:
    print("Dosyanız değiştirilmiştir")