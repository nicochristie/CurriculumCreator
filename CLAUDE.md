1. Project Setup

```
mkdir cv-converter
cd cv-converter
python -m venv venv
venv\Scripts\activate
pip install python-docx jinja2 playwright
```

2. Architecture
```
cv-converter/
├── cv_parser.py          # Extract structure from .docx
├── html_generator.py     # Generate HTML from parsed data
├── templates/
│   └── cv_template.html  # Jinja2 template with CSS
├── input/
│   └── cv.docx          # Source document
└── output/
    ├── cv.html          # Generated HTML
    └── cv.pdf           # Final PDF (optional)
```


3. Development Steps
Step 1: Parse Word document

Extract paragraphs, runs (text formatting)
Identify structure (headings, bullets, bold/italic)
Store in data structure (dict/class)

Step 2: Generate HTML

Map Word styles to semantic HTML tags
Apply custom CSS for precise formatting
Use Jinja2 for template rendering

Step 3: Convert to PDF (optional)

Use Playwright's PDF export
Maintains CSS exactly as browser renders

4. Key Parsing Considerations

Word paragraph styles → HTML semantic tags (h1, h2, p)
Bold/italic runs → <strong>, <em>
Tables → <table>
Bullets/numbering → <ul>, <ol>

5. Alternative: C# approach
Would use DocumentFormat.OpenXml + Razor templates, but more setup overhead on Windows.