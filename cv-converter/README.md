# CV Converter - Word to HTML/PDF

A Python tool to convert Word (.docx) CVs to clean, editable HTML and print-ready PDF format.

## Features

- Extracts CV structure from Word documents (headings, paragraphs, lists, tables, formatting)
- Generates clean, semantic HTML with professional CSS styling
- Preserves text formatting (bold, italic, underline)
- Exports to PDF using Playwright's browser rendering
- Print-optimized output suitable for job portals

## Installation

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # OR
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**
   ```bash
   pip install python-docx jinja2 playwright
   playwright install chromium
   ```

## Usage

### Quick Start

Place your CV in the `input/` directory as `cv.docx`, then run:

```bash
python convert_cv.py
```

This will generate:
- `output/cv.html` - Clean, editable HTML version
- `output/cv.pdf` - Print-ready PDF

### Advanced Usage

**Convert a specific Word file:**
```bash
python convert_cv.py path/to/your/cv.docx
```

**Generate HTML only (skip PDF):**
```bash
python convert_cv.py --html-only
```

### Individual Components

**Parse Word document only:**
```bash
python cv_parser.py
```

**Generate HTML from parsed data:**
```bash
python html_generator.py
```

**Generate PDF from HTML:**
```bash
python pdf_generator.py
```

## Project Structure

```
cv-converter/
├── cv_parser.py          # Extracts structure from .docx
├── html_generator.py     # Generates HTML from parsed data
├── pdf_generator.py      # Converts HTML to PDF
├── convert_cv.py         # Complete conversion pipeline
├── templates/
│   └── cv_template.html  # Jinja2 template with CSS
├── input/
│   └── cv.docx          # Source Word document
└── output/
    ├── cv.html          # Generated HTML
    └── cv.pdf           # Final PDF
```

## Customization

### Modify Styling

Edit `templates/cv_template.html` to customize:
- Colors and fonts (CSS section)
- Layout and spacing
- Section formatting
- Print margins and page breaks

### Parsing Logic

Edit `cv_parser.py` to adjust:
- Heading detection rules
- List item detection
- Table parsing behavior
- Header/contact extraction

## Output

The generated HTML is:
- **Editable:** Clean HTML structure for easy manual updates
- **Print-optimized:** Professional CSS with print media queries
- **A4 format:** Properly sized for standard paper
- **Semantic:** Uses proper HTML5 tags (header, sections, etc.)

## Requirements

- Python 3.7+
- python-docx
- Jinja2
- Playwright

## Notes

- The parser extracts name and contact info from document headers and tables
- All text formatting (bold, italic, underline) is preserved
- Tables in the document body are converted to HTML tables
- UTF-8 encoding ensures special characters display correctly
