# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.1] - 2026-04-19

### Fixed

- `_ensure_list_spacing` was inserting a blank line before every list item (including items 2, 3, 4…), causing each `* item` to become a separate `<ul>` block. It now only inserts a blank line before the **first** item of a list block (i.e. when the preceding line is not itself a list marker).

## [1.4.0] - 2026-04-19

### Added

- Support for 5 new Markdown extensions: `abbr` (abbreviations with `<abbr>` tooltip), `def_list` (definition lists `<dl>/<dt>/<dd>`), `footnotes` (`[^1]` syntax), `admonition` (`!!! note/warning/danger/...` callout boxes), `toc` (auto-generates `id` attributes on headings for anchor links)
- Tailwind classes for all new elements: `<abbr>`, `<dl>/<dt>/<dd>`, admonition boxes (color-coded by type), footnote section
- Admonition color scheme: `note`/`info` → blue, `tip`/`hint`/`success` → green, `warning`/`caution`/`attention` → amber, `danger`/`error` → red, `important` → purple

### Fixed

- List items (`* item`, `- item`, `1. item`) and blockquotes immediately following a paragraph (no blank line) were not rendered as HTML lists due to the `nl2br` extension consuming the newline. A new `_ensure_list_spacing` preprocessor inserts the required blank line automatically.

## [1.3.0] - 2026-04-19

### Added

- `font_size` parameter on `Converter` (`'sm'`, `'base'`, `'lg'`; default `'base'`) to control the typographic scale of all rendered elements
- `--font-size` CLI flag (`sm` | `base` | `lg`) passed through to `Converter`

## [1.2.0] - 2026-04-17

### Fixed

- Badge paragraphs now render inline with `flex flex-wrap gap-2 items-center justify-center` instead of stacked with full line-height spacing
- Deprecated `align="center/left/right"` HTML attributes are now translated to Tailwind `text-center/left/right` classes and removed from output

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
