"""
Simple PDF Generator for CV
Converts the HTML CV to PDF using Playwright
"""

import os
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
from io import BytesIO
try:
    import pikepdf
    HAS_PIKEPDF = True
except ImportError:
    HAS_PIKEPDF = False

try:
    from PyPDF2 import PdfReader, PdfWriter
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


async def generate_pdf(html_path, pdf_path):
    """Generate PDF from HTML file"""
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        file_url = f'file:///{os.path.abspath(html_path).replace(os.sep, "/")}'
        await page.goto(file_url, wait_until='networkidle')

        # Generate PDF with print settings
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

    return True


def optimize_image_for_pdf(image_path, target_width=400, quality=90):
    """
    Create a temporary optimized version of an image for PDF generation

    Args:
        image_path: Path to the original image
        target_width: Target width in pixels (maintains aspect ratio)
        quality: JPEG quality (0-100)

    Returns:
        Path to temporary optimized image, or None if failed
    """
    import tempfile
    import shutil

    try:
        # Create backup of original
        backup_path = image_path + '.backup'
        shutil.copy2(image_path, backup_path)

        # Open and optimize the image
        with Image.open(image_path) as img:
            # Calculate new dimensions
            aspect_ratio = img.height / img.width
            new_width = target_width
            new_height = int(new_width * aspect_ratio)

            # Resize image
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save optimized version in place
            img_resized.save(image_path, 'JPEG', quality=quality, optimize=True)

        return backup_path

    except Exception as e:
        print(f"  Warning: Could not optimize image: {e}")
        return None


async def main():
    # File paths
    html_file = 'CV Nicolas Christie (en).html'
    pdf_file = 'CV Nicolas Christie (en).pdf'
    header_image = './media/header-photo.jpg'

    # Step 1: Temporarily optimize the header image for PDF generation
    print(f"Optimizing images for PDF generation...")
    backup_path = None
    if os.path.exists(header_image):
        backup_path = optimize_image_for_pdf(header_image, target_width=400, quality=90)
        if backup_path:
            original_size = os.path.getsize(backup_path)
            optimized_size = os.path.getsize(header_image)
            print(f"  Image optimized: {original_size / 1024:.1f} KB -> {optimized_size / 1024:.1f} KB")

    try:
        # Step 2: Generate PDF with optimized image
        print(f"\nGenerating PDF from {html_file}...")
        success = await generate_pdf(html_file, pdf_file)

        if success:
            final_size = os.path.getsize(pdf_file)
            print(f"PDF generated successfully: {os.path.abspath(pdf_file)}")
            print(f"Final PDF size: {final_size / 1024 / 1024:.2f} MB")
        else:
            print("PDF generation failed!")

    finally:
        # Step 3: Restore original image
        if backup_path and os.path.exists(backup_path):
            import shutil
            print(f"\nRestoring original image...")
            shutil.move(backup_path, header_image)
            print(f"Original image restored.")


if __name__ == '__main__':
    asyncio.run(main())
