# md2html-tailwind4

A Python package that converts Markdown to clean, styled HTML using **Tailwind CSS 4** classes.

Designed for projects that render HTML inside a Tailwind-powered frontend (Django, FastAPI, static sites, etc.). No build step required — just pass in Markdown, get back ready-to-render HTML.

## Features

- Converts Markdown to HTML with full Tailwind CSS 4 class annotations
- Configurable font size scale (`sm`, `base`, `lg`)
- Abbreviations (`abbr`) with dotted underline tooltip
- Definition lists (`dl`/`dt`/`dd`)
- Footnotes (`[^1]` syntax)
- Admonition callout boxes (`!!! note`, `!!! warning`, `!!! danger`, etc.) with color-coded Tailwind styling
- Heading anchor IDs auto-generated via `toc` extension
- List items immediately following a paragraph (no blank line) render correctly
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

# font_size: 'sm' | 'base' (default) | 'lg'
converter = Converter(font_size='sm')
html = converter.convert_md_to_html("# Hello\n\nThis is **Markdown**.")
print(html)
```

### Command Line

```bash
md2html input.md output.html

# Use a smaller font size
md2html input.md output.html --font-size sm
```

### Font Size Scales

| Scale | Heading 1 | Body text | Code block |
|-------|-----------|-----------|------------|
| `sm` | `text-xl` → `text-3xl` | `text-sm` | `text-xs` |
| `base` *(default)* | `text-2xl` → `text-4xl` | `text-base` | `text-sm` |
| `lg` | `text-3xl` → `text-5xl` | `text-lg` | `text-base` |

## Requirements

- Python >= 3.11

## License

MIT — White Neuron Co., Ltd.
