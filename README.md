# md2html-tailwind4

A Python package that converts Markdown to clean, styled HTML using **Tailwind CSS 4** classes.

Designed for projects that render HTML inside a Tailwind-powered frontend (Django, FastAPI, static sites, etc.). No build step required — just pass in Markdown, get back ready-to-render HTML.

## Features

- Converts Markdown to HTML with full Tailwind CSS 4 class annotations
- Responsive tables with overflow scrolling
- Audio table support (3-column tables with media URLs become interactive audio players)
- Automatically escapes Django template delimiters (`{{ }}`, `{% %}`) inside code blocks
- External links get `target="_blank"` and `rel="noopener noreferrer"` automatically
- Dark mode support via Tailwind's `dark:` variants
- CLI tool included

## Installation

```bash
pip install md2html-tailwind4
```

## Usage

### Python API

```python
from md2html_tailwind4 import Converter

converter = Converter()
html = converter.convert_md_to_html("# Hello\n\nThis is **Markdown**.")
print(html)
```

### Command Line

```bash
md2html input.md output.html
```

## Requirements

- Python >= 3.11

## License

MIT — White Neuron Co., Ltd.
