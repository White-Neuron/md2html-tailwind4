import markdown
import re
from bs4 import BeautifulSoup


class Converter:
    def __init__(self):
        pass

    def convert_md_to_html(self, markdown_content):
        # Convert Markdown to HTML with richer extensions for broader content support.
        html_content = markdown.markdown(
            markdown_content,
            extensions=['tables', 'attr_list', 'fenced_code', 'sane_lists', 'nl2br'],
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
        for h1 in soup.find_all('h1'):
            h1['class'] = 'text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight mb-4 sm:mb-5 text-neutral-900 dark:text-neutral-100'

        for h2 in soup.find_all('h2'):
            h2['class'] = 'text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight mt-8 mb-3 text-neutral-900 dark:text-neutral-100'

        for h3 in soup.find_all('h3'):
            h3['class'] = 'text-lg sm:text-xl lg:text-2xl font-semibold mt-6 mb-3 text-neutral-900 dark:text-neutral-100'

        for h4 in soup.find_all('h4'):
            h4['class'] = 'text-base sm:text-lg font-semibold mt-5 mb-2 text-neutral-800 dark:text-neutral-200'

        for h5 in soup.find_all('h5'):
            h5['class'] = 'text-base font-semibold mt-4 mb-2 text-neutral-800 dark:text-neutral-200'

        for h6 in soup.find_all('h6'):
            h6['class'] = 'text-sm font-semibold uppercase tracking-wide mt-4 mb-2 text-neutral-700 dark:text-neutral-300'

        for p in soup.find_all('p'):
            p['class'] = 'mb-4 text-base leading-7 text-pretty text-justify text-neutral-800 dark:text-neutral-200'

        for ul in soup.find_all('ul'):
            ul['class'] = 'list-disc list-outside pl-6 mb-4 space-y-1 text-base leading-7 text-justify text-neutral-800 dark:text-neutral-200'

        for ol in soup.find_all('ol'):
            ol['class'] = 'list-decimal list-outside pl-6 mb-4 space-y-1 text-base leading-7 text-justify text-neutral-800 dark:text-neutral-200'

        for li in soup.find_all('li'):
            li['class'] = 'leading-7'

        for blockquote in soup.find_all('blockquote'):
            blockquote['class'] = 'mb-5 p-4 sm:p-5 rounded-r-xl border-l-4 bg-neutral-100 text-neutral-700 border-neutral-400 italic text-base leading-7 quote dark:bg-neutral-900/60 dark:text-neutral-300 dark:border-neutral-600'

        for img in soup.find_all('img'):
            img['class'] = 'mx-auto my-5 w-full max-w-4xl h-auto rounded-xl border border-neutral-200 shadow-sm dark:border-neutral-700 dark:shadow-neutral-950/30'

        for pre in soup.find_all('pre'):
            pre['class'] = 'my-5 overflow-x-auto rounded-xl border border-neutral-200 bg-neutral-950 p-4 text-sm leading-6 text-neutral-100 dark:border-neutral-700 dark:bg-neutral-950 dark:text-neutral-100'

        for code in soup.find_all('code'):
            if code.parent and code.parent.name == 'pre':
                code['class'] = 'bg-transparent p-0 text-inherit font-mono'
            else:
                code['class'] = 'px-1.5 py-0.5 rounded-md bg-neutral-100 text-[0.9em] font-mono text-neutral-900 dark:bg-neutral-800 dark:text-neutral-100'

        for strong in soup.find_all('strong'):
            strong['class'] = 'font-semibold text-neutral-900 dark:text-neutral-100'

        for em in soup.find_all('em'):
            em['class'] = 'italic text-neutral-700 dark:text-neutral-300'

        for a in soup.find_all('a'):
            a['class'] = 'text-sky-700 underline decoration-sky-300 underline-offset-2 hover:text-sky-900 transition-colors dark:text-sky-300 dark:decoration-sky-600 dark:hover:text-sky-200'
            if a.get('href', '').startswith(('http://', 'https://')):
                a['target'] = '_blank'
                a['rel'] = 'noopener noreferrer'

        for hr in soup.find_all('hr'):
            hr['class'] = 'my-8 border-neutral-300 dark:border-neutral-700'

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
                        audio_id = span2_content.lower().replace(' ', '_').replace('[', '').replace(']', '')
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
        media_suffixes = ('.mp3', '.wav', '.ogg', '.m4a', '.aac', '.webm')
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

        return all(value.startswith(('http://', 'https://', '/')) or value.endswith(media_suffixes) for value in third_values)

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

    def escape_django_template_syntax_in_code_blocks(self, soup):
        for tag in soup.find_all(['code', 'pre']):
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
