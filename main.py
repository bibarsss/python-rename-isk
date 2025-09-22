from pathlib import Path
import unicodedata
from pypdf import PdfReader
import sys, io

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer, 
    encoding="utf-8", 
    line_buffering=True
)

def read(file_path: str)->str:
    reader = PdfReader(file_path)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    return full_text

print('Парсим все иски где в наз вании есть слово "суд", и содержит слово "ИСКОВОЕ ЗАЯВЛЕНИЕ" и переименовывает')

for path in Path(".").rglob("*.pdf"):
    filename = unicodedata.normalize("NFC", path.name).lower()
    if "суд" in filename:
        text = read(str(path))
        if "исковое заявление" in text.lower():
            try:
                new_path = path.with_name("Иск (1).pdf")
                path.rename(new_path)
                print(f"✅ Renamed: {path.name} -> {new_path.name}")
            except Exception:
                print(f"[ERROR]: {path.name} -> {new_path.name}")
                continue