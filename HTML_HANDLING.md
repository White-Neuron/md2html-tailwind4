# Hướng dẫn xử lý HTML output từ md2html-tailwind4

## 1. Tổng quan

`Converter` sinh ra HTML hoàn chỉnh với:
- **Tailwind CSS 4** classes (không cần build step)
- **MathJax 3** auto-injected khi có công thức toán
- **Dark mode support** via `dark:` variants
- **Responsive design** cho tất cả elements

## 2. Sử dụng HTML output

### 2.1 HTML có sẵn MathJax

HTML được sinh từ converter **đã bao gồm** MathJax loader:

```html
<!-- Tự động chèn vào cuối nếu có toán học -->
<script>
window.MathJax = window.MathJax || {
  tex: {inlineMath: [['\\(', '\\)'], ['$', '$']]},
  svg: {fontCache: 'global'}
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
```

**Khi nào được inject:**
- Nếu markdown chứa `$...$` hay `\(...\)` → MathJax được inject
- Nếu không có toán học → MathJax không được thêm (tiết kiệm bandwidth)

### 2.2 Cách sử dụng với Django/FastAPI

```python
from md2html_tailwind4 import Converter

# Trong view/handler
converter = Converter(font_size='base')
html = converter.convert_md_to_html(markdown_content)

# Truyền vào template
return render(request, 'template.html', {'content': html | safe})
```

**Template (Django):**
```html
{% extends "base.html" %}
{% block content %}
<div class="bg-white dark:bg-neutral-900 p-4">
    {{ content | safe }}
</div>
{% endblock %}
```

## 3. Công thức toán học (Math expressions)

### 3.1 Format hỗ trợ

| Format | Ví dụ | Kết quả |
|--------|-------|--------|
| Inline $ | `$\rightarrow$` | → |
| Inline \(\) | `\(\rightarrow\)` | → |
| Display $$ | `$$\sum x$$` | ∑ x (trên dòng riêng) |
| Display \[\] | `\[E=mc^2\]` | E=mc² (trên dòng riêng) |

### 3.2 Pattern hỗ trợ đặc biệt

Converter tự động gom các math fragment thành 1 expression:

```markdown
# Input
Price: $4.99 \rightarrow $14.99

# Converter xử lý thành
Price: $4.99 \rightarrow 14.99$

# HTML output
Price: <span class="arithmatex">\(4.99 \rightarrow 14.99\)</span>
```

**Hỗ trợ patterns:**
- `$num1 \cmd $num2` → `$num1 \cmd num2$` ✓
- `$num1$ \cmd $num2$` → `$num1 \cmd num2$` ✓
- `$num1 $num2` → No merge (must have LaTeX command)

### 3.3 Best practices

✅ **Tốt:**
```markdown
- Tiền tệ: $4.99 \rightarrow $14.99
- Công thức: $E=mc^2$
- Khoa học: $\alpha + \beta = \gamma$
```

❌ **Tránh:**
```markdown
- Tiền tệ viết liên tục: $4.99$14.99 (không parse)
- Mix ké: $4.99 text $text (confusing)
- Không escape khi cần: $abc$def (sẽ parse $abc$ riêng)
```

## 4. CSS & Tailwind classes

### 4.1 Các class được áp dụng tự động

**Headings:**
```
h1: text-2xl sm:text-3xl lg:text-4xl font-bold
h2: text-xl sm:text-2xl lg:text-3xl font-bold
h3: text-lg sm:text-xl lg:text-2xl font-semibold
```

**Paragraphs:**
```
text-base leading-7 text-justify text-neutral-800 dark:text-neutral-200
```

**Code blocks:**
```
rounded-xl border bg-neutral-950 p-4 dark:border-neutral-700
```

**Admonitions:**
```
note/info:   border-blue-400 bg-blue-50
warning:     border-amber-400 bg-amber-50
danger/error: border-red-400 bg-red-50
```

### 4.2 Font size scales

```python
converter = Converter(font_size='sm')   # Nhỏ
converter = Converter(font_size='base') # Mặc định
converter = Converter(font_size='lg')   # Lớn
```

## 5. Dark mode

HTML được sinh **tự động hỗ trợ dark mode**. Để kích hoạt:

```html
<!-- HTML đã có dark: classes -->
<!-- Kích hoạt bằng JS: -->
<script>
  document.documentElement.classList.add('dark');
  // Hoặc toggle
  document.documentElement.classList.toggle('dark');
</script>

<!-- Hoặc CSS -->
@media (prefers-color-scheme: dark) {
  html { @apply dark; }
}
```

## 6. Tích hợp với frameworks

### 6.1 Django

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'builtins': ['django.template.defaulttags'],
        },
    },
]

# views.py
from md2html_tailwind4 import Converter
from django.utils.safestring import mark_safe

def article_view(request, slug):
    article = Article.objects.get(slug=slug)
    converter = Converter()
    html_content = converter.convert_md_to_html(article.markdown_text)
    return render(request, 'article.html', {
        'content': mark_safe(html_content)
    })

# template.html
<div class="prose prose-sm md:prose-base max-w-4xl">
    {{ content }}
</div>
```

### 6.2 FastAPI

```python
from fastapi import FastAPI, Response
from md2html_tailwind4 import Converter

app = FastAPI()

@app.get("/article/{article_id}")
def get_article(article_id: int):
    # Fetch article from DB
    converter = Converter()
    html = converter.convert_md_to_html(article.content)
    return Response(content=html, media_type="text/html")
```

### 6.3 Static site generators

```python
# build.py
from pathlib import Path
from md2html_tailwind4 import Converter

converter = Converter(font_size='base')
md_dir = Path('content')
html_dir = Path('output')

for md_file in md_dir.glob('*.md'):
    with open(md_file) as f:
        content = f.read()
    
    html = converter.convert_md_to_html(content)
    
    output_file = html_dir / md_file.stem / 'index.html'
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(html)
```

## 7. Performance & optimization

### 7.1 MathJax loading

- **MathJax được inject từ CDN** (618 kB gzipped)
- **Auto-inject chỉ khi cần**: Không có toán → không load MathJax
- **Async loading**: `<script async>` không block page render

### 7.2 Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_convert(markdown_text):
    converter = Converter()
    return converter.convert_md_to_html(markdown_text)
```

### 7.3 Production notes

- HTML đã bao gồm Tailwind classes → **không cần JIT compiler**
- MathJax từ CDN → đảm bảo **CORS allowed** trên production
- Django/FastAPI xử lý xây dựng HTML nhanh → **no build step**

## 8. Xử lý lỗi & edge cases

### 8.1 Django template delimiters

```markdown
# Input
{% if condition %}...{% endif %}

# Converter tự động escape
{% templatetag openblock %} if condition {% templatetag closeblock %}...
```

**Lý do:** Tránh Django parse lại khi render

### 8.2 External links

```markdown
# Input
[Link](https://example.com)

# Output
<a href="..." target="_blank" rel="noopener noreferrer">Link</a>
```

**Tự động thêm:**
- `target="_blank"` (mở tab mới)
- `rel="noopener noreferrer"` (security)

### 8.3 Tables

**Audio tables** (3 cột, cột 3 = media URL):
```
| Tên | URL | Audio |
|-----|-----|-------|
| Song 1 | /path/song.mp3 | [play] |
```
→ Chuyển thành interactive audio player

**Bảng thường:**
```
| Col1 | Col2 |
|------|------|
| Data | Data |
```
→ Responsive table với scroll trên mobile

## 9. Changelog toán học

- **v1.4.2+**: Thêm pymdownx.arithmatex để parse `$...$` expressions
- **v1.4.3+**: Auto-inject MathJax 3 khi phát hiện toán học
- **v1.5.0+**: Smart merge của math fragments (e.g., `$4.99 \rightarrow $14.99`)

## 10. Troubleshooting

### Toán học không hiển thị

**Nguyên nhân 1: CSP (Content Security Policy)**
```html
<!-- Header cần allow CDN -->
<meta http-equiv="Content-Security-Policy" 
      content="script-src 'unsafe-inline' https://cdn.jsdelivr.net">
```

**Nguyên nhân 2: Format không đúng**
```markdown
# ❌ Lỗi
$4.99 \rightarrow $14.99
→ Phải có LaTeX command giữa hai $

# ✅ Đúng
$4.99 \rightarrow 14.99$
```

**Nguyên nhân 3: JS không chạy**
```python
# Đảm bảo output được mark as safe
from django.utils.safestring import mark_safe
html = mark_safe(converter.convert_md_to_html(content))
```

### HTML không style

- Đảm bảo Tailwind CSS 4 được load trên page
- HTML đã bao gồm class names, không phải inline styles
- Framework phải compile Tailwind hoặc dùng CDN

### Performance chậm

- Kiểm tra MathJax loading time (DevTools → Network)
- Disable MathJax nếu không cần toán: tự remove `<script>` tags
- Dùng `font_size='sm'` cho mobile

---

**Hỏi thêm?** Tham khảo README.md hoặc file này!
