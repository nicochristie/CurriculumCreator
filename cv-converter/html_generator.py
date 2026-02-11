"""
HTML Generator - Convert parsed CV data to HTML using Jinja2 template

This module takes the structured CV data from cv_parser and renders
it into a professional HTML document using a Jinja2 template.
"""

import os
import shutil
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from cv_parser import CVParser


class HTMLGenerator:
    def __init__(self, template_dir='templates'):
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Add custom filters if needed
        self.env.filters['render_runs'] = self._render_runs_filter

    def generate(self, cv_data, output_path):
        """Generate HTML from CV data"""
        # Load the template
        template = self.env.get_template('cv_template.html')

        # Add the render_runs function to the context
        cv_data['render_runs'] = self._render_runs

        # Render the template
        html_content = template.render(**cv_data)

        # Prettify the HTML
        html_content = self._prettify_html(html_content)

        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Copy assets (photo, CSS) to output directory
        output_dir = os.path.dirname(output_path)

        # Copy photo
        photo_src = 'templates/header-photo.jpg'
        photo_dst = os.path.join(output_dir, 'header-photo.jpg')
        if os.path.exists(photo_src):
            shutil.copy2(photo_src, photo_dst)

        # Copy CSS if it exists
        css_src = 'templates/cv_styles.css'
        css_dst = os.path.join(output_dir, 'cv_styles.css')
        if os.path.exists(css_src):
            shutil.copy2(css_src, css_dst)

        print(f"HTML generated successfully: {output_path}")
        return output_path

    def _prettify_html(self, html):
        """Clean up and properly indent HTML"""
        # Remove all existing whitespace and newlines to start fresh
        html = re.sub(r'>\s+<', '><', html)

        # Tags that should increase indent
        indent_tags = ['html', 'head', 'body', 'div', 'ul', 'ol', 'li', 'h1', 'h2', 'h3',
                       'span', 'a', 'section', 'header', 'footer', 'nav']
        # Self-closing or inline tags that don't need newlines
        inline_tags = ['br', 'img', 'input', 'meta', 'link']

        indent_level = 0
        result = []
        tag_stack = []

        # Split by tags
        parts = re.split(r'(<[^>]+>)', html)

        for part in parts:
            if not part:
                continue

            # Check if it's a tag
            if part.startswith('<'):
                # Comment
                if part.startswith('<!--'):
                    result.append('    ' * indent_level + part)
                # Closing tag
                elif part.startswith('</'):
                    indent_level = max(0, indent_level - 1)
                    tag_name = re.search(r'</(\w+)', part)
                    if tag_name:
                        tag_name = tag_name.group(1)
                        # Only add newline for block elements
                        if tag_name in indent_tags:
                            result.append('    ' * indent_level + part)
                        else:
                            result.append(part)
                # Self-closing or inline tag
                elif part.endswith('/>') or any(f'<{tag}' in part for tag in inline_tags):
                    result.append('    ' * indent_level + part)
                # Opening tag
                else:
                    tag_name = re.search(r'<(\w+)', part)
                    if tag_name:
                        tag_name = tag_name.group(1)
                        result.append('    ' * indent_level + part)
                        if tag_name in indent_tags:
                            indent_level += 1
            # Text content
            else:
                # Only add non-empty text
                text = part.strip()
                if text:
                    result.append('    ' * indent_level + text)

        return '\n'.join(result)

    def _render_runs(self, runs):
        """Render text runs with formatting"""
        if not runs:
            return ''

        result = []
        for run in runs:
            text = run['text']
            classes = []

            if run.get('bold'):
                classes.append('bold')
            if run.get('italic'):
                classes.append('italic')
            if run.get('underline'):
                classes.append('underline')

            if classes:
                class_str = ' '.join(classes)
                result.append(f'<span class="{class_str}">{text}</span>')
            else:
                result.append(text)

        return ''.join(result)

    def _render_runs_filter(self, runs):
        """Jinja2 filter version of render_runs"""
        return self._render_runs(runs)


def main():
    """Main function to convert CV from Word to HTML"""
    # Parse the CV
    print("Parsing CV from Word document...")
    parser = CVParser('input/cv.docx')
    cv_data = parser.parse()

    # Generate HTML
    print("\nGenerating HTML...")
    generator = HTMLGenerator()
    output_path = 'output/cv.html'
    generator.generate(cv_data, output_path)

    print(f"\n✓ Conversion complete!")
    print(f"  Input:  input/cv.docx")
    print(f"  Output: {output_path}")
    print(f"\nOpen {output_path} in your browser to view the result.")


if __name__ == '__main__':
    main()
