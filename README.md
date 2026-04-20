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
- Inline/block math parsing via `pymdownx.arithmatex` (e.g. `$\\rightarrow$`) with automatic MathJax loader injection
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

## HTML Output & Integration

The generated HTML is **production-ready** with:

- **Tailwind CSS 4** classes already applied (no build step needed)
- **MathJax 3** automatically injected when math expressions detected
- **Dark mode support** via `dark:` variants
- **Responsive design** for all elements
- **Security hardening** (Django template escaping, external link attributes)

See [HTML_HANDLING.md](HTML_HANDLING.md) for detailed integration guides with Django, FastAPI, and more.

## Math Support

Format math expressions with `$...$` or `\(...\)`:

```markdown
Pricing: $4.99 \rightarrow $14.99
Physics: $E=mc^2$
Formula: \[\sum_{i=1}^{n} x_i\]
```

Smart normalization handles split expressions:
- `$4.99 \rightarrow $14.99` → `$4.99 \rightarrow 14.99$` ✓
- MathJax loaded automatically when needed

## Requirements

- Python >= 3.11

## License

MIT — White Neuron Co., Ltd.
