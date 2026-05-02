import pytest
from processor import clean_text, validate_input

# 15 Test Cases untuk Logika Bisnis
def test_clean_lowercase():
    assert clean_text("EMAS") == "emas"

def test_clean_remove_url():
    assert clean_text("beli di http://web.com") == "beli di"

def test_clean_remove_mention():
    assert clean_text("@user emas") == "emas"

def test_clean_remove_punctuation():
    assert clean_text("emas!!!") == "emas"

def test_clean_remove_numbers():
    assert clean_text("emas 123") == "emas"

def test_clean_whitespace():
    assert clean_text("  emas  ") == "emas"

def test_clean_empty():
    assert clean_text("") == ""

def test_clean_none():
    assert clean_text(None) == ""

def test_clean_double_space():
    assert clean_text("emas  naik") == "emas naik"

def test_clean_hashtag():
    assert clean_text("#investasi emas") == "emas"

def test_val_valid():
    assert validate_input("harga emas") is True

def test_val_too_short():
    assert validate_input("hi") is False

def test_val_empty():
    assert validate_input("") is False

def test_val_spaces():
    assert validate_input("   ") is False

def test_val_non_string():
    assert validate_input(123) is False