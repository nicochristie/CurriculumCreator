"""
PDF Generator - Convert HTML CV to PDF using Playwright

This module uses Playwright's Chromium browser to render the HTML CV
and export it as a high-quality PDF suitable for printing.
"""

import os
import asyncio
from playwright.async_api import async_playwright


class PDFGenerator:
    def __init__(self):
        pass

    async def generate_pdf(self, html_path, pdf_path):
        """Generate PDF from HTML file"""
        # Convert to absolute path
        html_path = os.path.abspath(html_path)
        pdf_path = os.path.abspath(pdf_path)

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Load the HTML file
            await page.goto(f'file:///{html_path}'.replace('\\', '/'))

            # Generate PDF with print-optimized settings
            await page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '0mm',
                    'right': '0mm',
                    'bottom': '0mm',
                    'left': '0mm'
                }
            )

            await browser.close()

        print(f"PDF generated successfully: {pdf_path}")
        return pdf_path

    def generate_pdf_sync(self, html_path, pdf_path):
        """Synchronous wrapper for generate_pdf"""
        return asyncio.run(self.generate_pdf(html_path, pdf_path))


async def main():
    """Generate PDF from existing HTML"""
    html_path = 'output/cv.html'
    pdf_path = 'output/cv.pdf'

    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        print("Please run html_generator.py first to generate the HTML.")
        return

    print(f"Generating PDF from {html_path}...")
    generator = PDFGenerator()
    await generator.generate_pdf(html_path, pdf_path)

    print(f"\nPDF generation complete!")
    print(f"  Input:  {html_path}")
    print(f"  Output: {pdf_path}")


if __name__ == '__main__':
    asyncio.run(main())
