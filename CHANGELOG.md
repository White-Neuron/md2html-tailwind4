# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-17

### Fixed

- `md_in_html` extension was a no-op; added `_inject_markdown_attr` preprocessor to inject `markdown="1"` into block-level HTML tags so inner markdown (bold, links, badges) renders correctly
- Double-escaping of Django template delimiters in `<pre><code>` blocks; `<code>` inside `<pre>` is now skipped
- XSS: `audio_id` now sanitized with `re.sub(r'[^a-z0-9_]', '_', ...)` to strip all non-safe characters from inline JS
- XSS: `audio_url` validated to only accept `http://`, `https://`, or `/`-prefixed paths; `javascript:` and other schemes are rejected
- URL allowlist mismatch between `_is_audio_table` and `convert_tables`; both now require the same prefixes, eliminating silent row loss
- Badge images (inside `<a>`) no longer inherit the full-width block image classes; they receive `inline h-5 align-middle` instead
- Badge links (sole child is `<img>`) no longer receive text/underline Tailwind classes
- Removed dead `media_suffixes` variable from `_is_audio_table`

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
