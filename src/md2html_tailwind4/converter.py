import markdown
import re
from bs4 import BeautifulSoup


class Converter:
    _ADMONITION_STYLES = {
        'note':      ('border-blue-400 bg-blue-50 dark:bg-blue-950/30 dark:border-blue-600',    'text-blue-800 dark:text-blue-300'),
        'info':      ('border-blue-400 bg-blue-50 dark:bg-blue-950/30 dark:border-blue-600',    'text-blue-800 dark:text-blue-300'),
        'tip':       ('border-green-400 bg-green-50 dark:bg-green-950/30 dark:border-green-600', 'text-green-800 dark:text-green-300'),
        'hint':      ('border-green-400 bg-green-50 dark:bg-green-950/30 dark:border-green-600', 'text-green-800 dark:text-green-300'),
        'success':   ('border-green-400 bg-green-50 dark:bg-green-950/30 dark:border-green-600', 'text-green-800 dark:text-green-300'),
        'warning':   ('border-amber-400 bg-amber-50 dark:bg-amber-950/30 dark:border-amber-600', 'text-amber-800 dark:text-amber-300'),
        'caution':   ('border-amber-400 bg-amber-50 dark:bg-amber-950/30 dark:border-amber-600', 'text-amber-800 dark:text-amber-300'),
        'attention': ('border-amber-400 bg-amber-50 dark:bg-amber-950/30 dark:border-amber-600', 'text-amber-800 dark:text-amber-300'),
        'danger':    ('border-red-400 bg-red-50 dark:bg-red-950/30 dark:border-red-600',         'text-red-800 dark:text-red-300'),
        'error':     ('border-red-400 bg-red-50 dark:bg-red-950/30 dark:border-red-600',         'text-red-800 dark:text-red-300'),
        'important': ('border-purple-400 bg-purple-50 dark:bg-purple-950/30 dark:border-purple-600', 'text-purple-800 dark:text-purple-300'),
    }
    _ADMONITION_DEFAULT = (
        'border-neutral-400 bg-neutral-50 dark:bg-neutral-800/30 dark:border-neutral-600',
        'text-neutral-800 dark:text-neutral-200',
    )

    _SIZE_SCALES = {
        'sm': {
            'h1_size': 'text-xl sm:text-2xl lg:text-3xl',
            'h2_size': 'text-lg sm:text-xl lg:text-2xl',
            'h3_size': 'text-base sm:text-lg lg:text-xl',
            'h4_size': 'text-sm sm:text-base',
            'h5_size': 'text-sm',
            'h6_size': 'text-xs',
            'body_size': 'text-sm',
            'pre_size': 'text-xs',
            'code_size': 'text-[0.85em]',
        },
        'base': {
            'h1_size': 'text-2xl sm:text-3xl lg:text-4xl',
            'h2_size': 'text-xl sm:text-2xl lg:text-3xl',
            'h3_size': 'text-lg sm:text-xl lg:text-2xl',
            'h4_size': 'text-base sm:text-lg',
            'h5_size': 'text-base',
            'h6_size': 'text-sm',
            'body_size': 'text-base',
            'pre_size': 'text-sm',
            'code_size': 'text-[0.9em]',
        },
        'lg': {
            'h1_size': 'text-3xl sm:text-4xl lg:text-5xl',
            'h2_size': 'text-2xl sm:text-3xl lg:text-4xl',
            'h3_size': 'text-xl sm:text-2xl lg:text-3xl',
            'h4_size': 'text-lg sm:text-xl',
            'h5_size': 'text-lg',
            'h6_size': 'text-base',
            'body_size': 'text-lg',
            'pre_size': 'text-base',
            'code_size': 'text-[0.95em]',
        },
    }

    def __init__(self, font_size='base'):
        if font_size not in self._SIZE_SCALES:
            raise ValueError(f"font_size must be one of: {', '.join(self._SIZE_SCALES)}")
        self._s = self._SIZE_SCALES[font_size]

    def convert_md_to_html(self, markdown_content):
        # Ensure blank lines before list/blockquote markers so nl2br doesn't swallow them.
        spaced = self._ensure_list_spacing(markdown_content)
        # Inject markdown="1" so md_in_html processes content inside HTML blocks.
        preprocessed = self._inject_markdown_attr(spaced)
        # Convert Markdown to HTML with richer extensions for broader content support.
        html_content = markdown.markdown(
            preprocessed,
            extensions=[
                'tables', 'attr_list', 'fenced_code', 'sane_lists', 'nl2br', 'md_in_html',
                'abbr', 'def_list', 'footnotes', 'admonition', 'toc',
            ],
            extension_configs={
                'toc': {'marker': '', 'permalink': False},
            },
        )

        # Parse the HTML content and convert tables to custom divs
        soup = BeautifulSoup(html_content, 'html.parser')

        # Add Tailwind classes to various elements
        self.add_tailwind_classes(soup)

        # Convert tables to custom divs
        self.convert_tables(soup)

        # Escape Django template delimiters in code examples so they render literally.
        self.escape_django_template_syntax_in_code_blocks(soup)

        # Create the full HTML content with JavaScript for play/pause toggle
        full_html_content = self.create_full_html(soup)

        return full_html_content

    def add_tailwind_classes(self, soup):
        s = self._s
        for h1 in soup.find_all('h1'):
            h1['class'] = f'{s["h1_size"]} font-bold tracking-tight mb-4 sm:mb-5 text-neutral-900 dark:text-neutral-100'

        for h2 in soup.find_all('h2'):
            h2['class'] = f'{s["h2_size"]} font-bold tracking-tight mt-8 mb-3 text-neutral-900 dark:text-neutral-100'

        for h3 in soup.find_all('h3'):
            h3['class'] = f'{s["h3_size"]} font-semibold mt-6 mb-3 text-neutral-900 dark:text-neutral-100'

        for h4 in soup.find_all('h4'):
            h4['class'] = f'{s["h4_size"]} font-semibold mt-5 mb-2 text-neutral-800 dark:text-neutral-200'

        for h5 in soup.find_all('h5'):
            h5['class'] = f'{s["h5_size"]} font-semibold mt-4 mb-2 text-neutral-800 dark:text-neutral-200'

        for h6 in soup.find_all('h6'):
            h6['class'] = f'{s["h6_size"]} font-semibold uppercase tracking-wide mt-4 mb-2 text-neutral-700 dark:text-neutral-300'

        for p in soup.find_all('p'):
            if self._is_badge_paragraph(p):
                p['class'] = 'flex flex-wrap gap-2 items-center justify-center mb-4'
            else:
                p['class'] = f'mb-4 {s["body_size"]} leading-7 text-pretty text-justify text-neutral-800 dark:text-neutral-200'

        for ul in soup.find_all('ul'):
            ul['class'] = f'list-disc list-outside pl-6 mb-4 space-y-1 {s["body_size"]} leading-7 text-justify text-neutral-800 dark:text-neutral-200'

        for ol in soup.find_all('ol'):
            ol['class'] = f'list-decimal list-outside pl-6 mb-4 space-y-1 {s["body_size"]} leading-7 text-justify text-neutral-800 dark:text-neutral-200'

        for li in soup.find_all('li'):
            li['class'] = 'leading-7'

        for blockquote in soup.find_all('blockquote'):
            blockquote['class'] = f'mb-5 p-4 sm:p-5 rounded-r-xl border-l-4 bg-neutral-100 text-neutral-700 border-neutral-400 italic {s["body_size"]} leading-7 quote dark:bg-neutral-900/60 dark:text-neutral-300 dark:border-neutral-600'

        for img in soup.find_all('img'):
            if img.parent and img.parent.name == 'a':
                img['class'] = 'inline h-5 align-middle'
            else:
                img['class'] = 'mx-auto my-5 w-full max-w-4xl h-auto rounded-xl border border-neutral-200 shadow-sm dark:border-neutral-700 dark:shadow-neutral-950/30'

        for pre in soup.find_all('pre'):
            pre['class'] = f'my-5 overflow-x-auto rounded-xl border border-neutral-200 bg-neutral-950 p-4 {s["pre_size"]} leading-6 text-neutral-100 dark:border-neutral-700 dark:bg-neutral-950 dark:text-neutral-100'

        for code in soup.find_all('code'):
            if code.parent and code.parent.name == 'pre':
                code['class'] = 'bg-transparent p-0 text-inherit font-mono'
            else:
                code['class'] = f'px-1.5 py-0.5 rounded-md bg-neutral-100 {s["code_size"]} font-mono text-neutral-900 dark:bg-neutral-800 dark:text-neutral-100'

        for strong in soup.find_all('strong'):
            strong['class'] = 'font-semibold text-neutral-900 dark:text-neutral-100'

        for em in soup.find_all('em'):
            em['class'] = 'italic text-neutral-700 dark:text-neutral-300'

        for a in soup.find_all('a'):
            a_cls = a.get('class') or []
            if isinstance(a_cls, str):
                a_cls = a_cls.split()
            if 'footnote-ref' in a_cls or 'footnote-backref' in a_cls:
                continue
            children = [c for c in a.children if getattr(c, 'name', None) or str(c).strip()]
            if not (len(children) == 1 and getattr(children[0], 'name', None) == 'img'):
                a['class'] = 'text-sky-700 underline decoration-sky-300 underline-offset-2 hover:text-sky-900 transition-colors dark:text-sky-300 dark:decoration-sky-600 dark:hover:text-sky-200'
            if a.get('href', '').startswith(('http://', 'https://')):
                a['target'] = '_blank'
                a['rel'] = 'noopener noreferrer'

        for hr in soup.find_all('hr'):
            hr['class'] = 'my-8 border-neutral-300 dark:border-neutral-700'

        for abbr in soup.find_all('abbr'):
            abbr['class'] = 'underline decoration-dotted cursor-help'

        for dl in soup.find_all('dl'):
            dl['class'] = f'mb-4 space-y-3 {s["body_size"]}'

        for dt in soup.find_all('dt'):
            dt['class'] = 'font-semibold text-neutral-900 dark:text-neutral-100'

        for dd in soup.find_all('dd'):
            dd['class'] = f'ml-6 {s["body_size"]} text-neutral-700 dark:text-neutral-300'

        for div in soup.find_all('div', class_='admonition'):
            div_classes = div.get('class') or []
            adm_type = div_classes[1] if len(div_classes) > 1 else ''
            box_cls, title_cls = self._ADMONITION_STYLES.get(adm_type, self._ADMONITION_DEFAULT)
            div['class'] = f'my-5 rounded-xl border-l-4 p-4 sm:p-5 {box_cls}'
            title_p = div.find('p', class_='admonition-title')
            if title_p:
                title_p['class'] = f'font-semibold mb-2 {title_cls}'

        footnote_div = soup.find('div', class_='footnote')
        if footnote_div:
            footnote_div['class'] = 'mt-8 pt-4 border-t border-neutral-200 dark:border-neutral-700'
            hr_tag = footnote_div.find('hr')
            if hr_tag:
                hr_tag.decompose()
            ol_tag = footnote_div.find('ol')
            if ol_tag:
                ol_tag['class'] = f'list-decimal pl-6 space-y-1 {s["body_size"]} text-neutral-600 dark:text-neutral-400'
            for li_tag in footnote_div.find_all('li'):
                li_tag['class'] = 'leading-6'
            for back in footnote_div.find_all('a', class_='footnote-backref'):
                back['class'] = 'text-sky-600 no-underline hover:text-sky-800 dark:text-sky-400'

        align_map = {'center': 'text-center', 'right': 'text-right', 'left': 'text-left'}
        for tag in soup.find_all(align=True):
            align_val = tag.get('align', '').lower()
            tailwind_class = align_map.get(align_val)
            if tailwind_class:
                existing = tag.get('class', '')
                if isinstance(existing, list):
                    existing = ' '.join(existing)
                tag['class'] = f'{existing} {tailwind_class}'.strip()
                del tag['align']

    def convert_tables(self, soup):
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            if len(rows) == 0:
                continue

            # Check if the first row is a header
            first_row_cells = rows[0].find_all(['th', 'td'])
            has_headers = len(first_row_cells) == 3 and all(th.name == 'th' for th in first_row_cells)

            # Only convert dedicated audio tables; keep all other tables semantic/responsive.
            if not has_headers or not self._is_audio_table(rows):
                self._style_as_responsive_table(soup, table)
                continue

            start_index = 1 if has_headers else 0
            divs = []

            for row in rows[start_index:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:  # Ensure there are at least two cells per row
                    div = soup.new_tag('div', **{'class': 'my-3 rounded-xl border border-neutral-200 bg-white p-3 sm:p-4 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-center gap-2 sm:gap-3 dark:border-neutral-700 dark:bg-neutral-900 dark:shadow-neutral-950/30'})
                    span1 = soup.new_tag('span', **{'class': 'font-semibold rounded-lg bg-neutral-800 px-3 py-2 text-white text-sm sm:text-base dark:bg-neutral-700'})
                    span1.string = cells[0].get_text()
                    span2 = soup.new_tag('span', **{'class': 'font-semibold rounded-lg bg-neutral-700 px-3 py-2 text-white text-sm sm:text-base break-words dark:bg-neutral-600'})
                    span2_content = cells[1].get_text()
                    span2.append(soup.new_string(span2_content))
                    if len(cells) == 3 and cells[2].get_text().strip():
                        audio_button = soup.new_tag('button', **{'class': 'audio-button ml-2', 'data-state': 'play'})
                        audio_button.string = '▶️'
                        audio_url = cells[2].get_text().strip()
                        if not audio_url.startswith(('http://', 'https://', '/')):
                            continue
                        audio_id = re.sub(r'[^a-z0-9_]', '_', span2_content.lower())
                        audio = soup.new_tag('audio', **{'src': audio_url, 'class': 'hidden', 'controls': ''})
                        audio_button['onclick'] = f"togglePlayPause('{audio_id}', this);"
                        audio['id'] = audio_id
                        span2.append(audio_button)
                        span2.append(audio)
                    div.append(span1)
                    div.append(span2)
                    divs.append(div)
            if divs:
                table.replace_with(*divs)
            else:
                table.decompose()

    @staticmethod
    def _is_audio_table(rows):
        # Audio-table mode is only valid when the 3rd column consistently contains media URLs.
        data_rows = rows[1:] if len(rows) > 1 else []
        if not data_rows:
            return False

        third_values = []
        for row in data_rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 3:
                return False
            third_values.append(cells[2].get_text().strip().lower())

        if not all(third_values):
            return False

        return all(value.startswith(('http://', 'https://', '/')) for value in third_values)

    def _style_as_responsive_table(self, soup, table):
        table['class'] = 'min-w-full border-collapse text-sm sm:text-base'
        table['style'] = 'color: var(--color-base-content); border-color: var(--color-base-300);'

        thead = table.find('thead')
        if thead:
            thead['class'] = ''
            thead['style'] = 'background-color: var(--color-base-300); color: var(--color-base-content);'
        for th in table.find_all('th'):
            th['class'] = 'border px-3 py-2 text-left font-semibold whitespace-nowrap'
            th['style'] = 'border-color: var(--color-base-300); color: var(--color-base-content);'

        for td in table.find_all('td'):
            td['class'] = 'border px-3 py-2 align-top'
            td['style'] = 'border-color: var(--color-base-300); color: var(--color-base-content);'

        wrapper = soup.new_tag(
            'div',
            **{
                'class': 'my-5 overflow-x-auto rounded-xl border shadow-sm',
                'style': 'border-color: var(--color-base-300); background-color: var(--color-base-100); color: var(--color-base-content);',
            },
        )
        table.wrap(wrapper)

    def create_full_html(self, soup):
        return str(soup)

    @staticmethod
    def _is_badge_paragraph(p):
        """Return True if all meaningful children of a <p> are badge links (<a><img>) or <br> tags."""
        for child in p.children:
            name = getattr(child, 'name', None)
            if name == 'br':
                continue
            if name == 'a':
                a_children = [c for c in child.children if getattr(c, 'name', None) or str(c).strip()]
                if len(a_children) == 1 and getattr(a_children[0], 'name', None) == 'img':
                    continue
            if not name and not str(child).strip():
                continue
            return False
        return True

    @staticmethod
    def _ensure_list_spacing(text):
        """Insert a blank line before list/blockquote lines that immediately follow non-blank content.

        The nl2br extension converts single newlines to <br>, which prevents
        Python-Markdown from recognising list markers that aren't preceded by
        a blank line.  This preprocessor adds the required blank line.
        """
        _LIST_MARKER = re.compile(r'^([ \t]*([-*+]|\d+[.)])[ \t]+|>[ \t]|!!! )', re.MULTILINE)
        lines = text.splitlines(keepends=True)
        result = []
        for i, line in enumerate(lines):
            if i > 0 and _LIST_MARKER.match(line):
                prev = lines[i - 1].rstrip('\n').rstrip('\r')
                if prev.strip():  # previous line is non-empty
                    result.append('\n')  # inject blank line
            result.append(line)
        return ''.join(result)

    @staticmethod
    def _inject_markdown_attr(text):
        """Inject markdown="1" into HTML block tags so md_in_html processes inner content."""
        block_tags = r'div|section|article|header|footer|aside|main|nav|figure|figcaption|details|summary'

        def inject(m):
            if 'markdown=' in m.group(0).lower():
                return m.group(0)
            return m.group(0)[:-1] + ' markdown="1">'

        return re.sub(
            r'<(?:' + block_tags + r')(?:\s[^>]*)?(?<!/)>',
            inject,
            text,
            flags=re.IGNORECASE,
        )

    def escape_django_template_syntax_in_code_blocks(self, soup):
        for tag in soup.find_all(['code', 'pre']):
            # Skip <code> inside <pre> — the <pre> pass already covers that text.
            if tag.name == 'code' and tag.parent and tag.parent.name == 'pre':
                continue
            # Keep code samples readable while preventing Django template parsing.
            if tag.string is not None:
                tag.string.replace_with(self._escape_django_delimiters(str(tag.string)))
                continue

            for text_node in tag.find_all(string=True):
                text_node.replace_with(self._escape_django_delimiters(str(text_node)))

    @staticmethod
    def _escape_django_delimiters(text):
        token_map = {
            '{{': '{% templatetag openvariable %}',
            '}}': '{% templatetag closevariable %}',
            '{%': '{% templatetag openblock %}',
            '%}': '{% templatetag closeblock %}',
            '{#': '{% templatetag opencomment %}',
            '#}': '{% templatetag closecomment %}',
        }
        return re.sub(r'\{\{|\}\}|\{%|%\}|\{#|#\}', lambda m: token_map[m.group(0)], text)
