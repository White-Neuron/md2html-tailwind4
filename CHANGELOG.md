# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-15

### Added

- Initial release of `md2html-tailwind4`
- `Converter` class with `convert_md_to_html()` method
- Tailwind CSS 4 class annotations for all standard HTML elements (h1–h6, p, ul, ol, li, blockquote, img, pre, code, strong, em, a, hr)
- Responsive table styling with overflow scrolling
- Audio table support: 3-column tables with media URLs are converted to interactive audio player widgets
- Django template delimiter escaping (`{{ }}`, `{% %}`, `{# #}`) inside code blocks
- External links automatically get `target="_blank"` and `rel="noopener noreferrer"`
- Dark mode support via Tailwind `dark:` variants
- CLI entry point: `md2html input.md output.html`
- `src/` layout for clean PyPI packaging with `hatchling` build backend
