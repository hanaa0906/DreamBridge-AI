import os
import tempfile
from app.services.extraction_service import extract_text


def test_extract_text_from_txt_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Hello lesson content.")
        path = f.name
    try:
        result = extract_text(path)
        assert "Hello lesson content." in result
    finally:
        os.remove(path)


def test_extract_text_unsupported_extension_raises():
    try:
        extract_text("somefile.xyz")
        assert False, "should have raised"
    except ValueError:
        pass
