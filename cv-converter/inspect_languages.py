"""Check where Languages appears"""
from docx import Document

doc = Document('input/cv.docx')

print("Searching for 'Languages' in document:")
print("=" * 60)

for i, para in enumerate(doc.paragraphs):
    if 'language' in para.text.lower():
        print(f"\n[{i}] Style: {para.style.name}")
        print(f"    Text: {para.text}")
        print(f"    Alignment: {para.alignment}")
        if para.runs:
            print(f"    First run - Bold: {para.runs[0].bold}, Italic: {para.runs[0].italic}")
