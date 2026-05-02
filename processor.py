# processor.py
import re
import string

def clean_text(text):
    """Logika bisnis: Pembersihan teks"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Hapus URL
    text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)
    # Hapus Tanda Baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Hapus Angka
    text = re.sub(r'\d+', '', text)
    # Hapus spasi ganda
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def validate_input(text):
    """Logika bisnis: Validasi input"""
    if not text or not isinstance(text, str):
        return False
    if len(text.strip()) < 3:
        return False
    return True