"""
Complete CV Conversion Pipeline

Converts a Word CV document to HTML and PDF in one command.
Usage: python convert_cv.py [input.docx] [--html-only]
"""

import sys
import os
import asyncio
from cv_parser import CVParser
from html_generator import HTMLGenerator
from pdf_generator import PDFGenerator


async def convert_cv(input_docx='input/cv.docx', output_html='output/cv.html',
                     output_pdf='output/cv.pdf', html_only=False):
    """Complete conversion pipeline"""

    print("=" * 60)
    print("CV Converter - Word to HTML/PDF")
    print("=" * 60)

    # Step 1: Parse Word document
    print("\n[1/3] Parsing Word document...")
    parser = CVParser(input_docx)
    cv_data = parser.parse()
    print(f"  - Found {len(cv_data['sections'])} sections")

    # Step 2: Generate HTML
    print("\n[2/3] Generating HTML...")
    generator = HTMLGenerator()
    generator.generate(cv_data, output_html)
    print(f"  - HTML saved to: {output_html}")

    # Step 3: Generate PDF (if requested)
    if not html_only:
        print("\n[3/3] Generating PDF...")
        pdf_gen = PDFGenerator()
        await pdf_gen.generate_pdf(output_html, output_pdf)
        print(f"  - PDF saved to: {output_pdf}")
    else:
        print("\n[3/3] Skipping PDF generation (HTML only mode)")

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)
    print(f"\nOutput files:")
    print(f"  HTML: {os.path.abspath(output_html)}")
    if not html_only:
        print(f"  PDF:  {os.path.abspath(output_pdf)}")
    print()


def main():
    """Main entry point"""
    # Parse command line arguments
    input_docx = 'input/cv.docx'
    html_only = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '--html-only':
            html_only = True
        else:
            input_docx = sys.argv[1]

    if '--html-only' in sys.argv:
        html_only = True

    # Check if input file exists
    if not os.path.exists(input_docx):
        print(f"Error: Input file not found: {input_docx}")
        print("\nUsage: python convert_cv.py [input.docx] [--html-only]")
        sys.exit(1)

    # Run conversion
    asyncio.run(convert_cv(
        input_docx=input_docx,
        html_only=html_only
    ))


if __name__ == '__main__':
    main()
