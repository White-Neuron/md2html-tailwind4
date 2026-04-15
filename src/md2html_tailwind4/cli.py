import argparse

from .converter import Converter


def main():
    parser = argparse.ArgumentParser(
        prog='md2html',
        description='Convert Markdown to HTML with Tailwind CSS 4 classes.',
    )
    parser.add_argument('input', help='Path to the input Markdown file')
    parser.add_argument('output', help='Path to the output HTML file')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    converter = Converter()
    html_content = converter.convert_md_to_html(markdown_content)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    main()
