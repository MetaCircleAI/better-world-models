"""Build the English page (index.html) and the Chinese page (zh/index.html) from content/.

Usage: pip install -r requirements.txt && python build.py
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
SITE = "https://metacircleai.github.io/better-world-models/"

LANGS = {
    "en": dict(
        src="content/article.en.md", out="index.html", prefix="", html_lang="en",
        figure="Figure", table="Table", sep="&ensp;",
        other_label="中文", other_href="zh/",
        cite_heading="Citation", cite_intro="If you find this post useful, please cite it as:",
        license_note='Text and figures are licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.',
        desc_len=155, url=SITE,
    ),
    "zh": dict(
        src="content/article.zh.md", out="zh/index.html", prefix="../", html_lang="zh-CN",
        figure="图", table="表", sep="　",
        other_label="English", other_href="../",
        cite_heading="引用", cite_intro="如果这篇文章对你有帮助，欢迎引用：",
        license_note='正文与图片采用 <a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">CC BY 4.0</a> 许可。',
        desc_len=110, url=SITE + "zh/",
    ),
}

BIBTEX = """@misc{huang2026betterworldmodels,
  title        = {How Much Better Can World Models Get by Changing Only the Architecture?},
  author       = {Huang, Bangzhe and Liu, Ziming},
  year         = {2026},
  month        = nov,
  howpublished = {MetaCircle AI blog},
  url          = {%s}
}""" % SITE

SUP = str.maketrans("¹²³⁴", "1234")


def sup(text):
    text = html.escape(text)
    text = re.sub(r"([¹²³⁴])(?:\s*([¹²³⁴]))?",
                  lambda m: "<sup>" + m.group(1) + ("," + m.group(2) if m.group(2) else "") + "</sup>", text)
    return text.translate(SUP)


def summary(text, limit):
    """First paragraph as plain text, cut at a word (English) or character (Chinese) boundary."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut and re.search(r"[A-Za-z]", cut):
        cut = cut[: cut.rfind(" ")].rstrip(",;:")
    return cut + "…"


def build(lang, c):
    src = (ROOT / c["src"]).read_text(encoding="utf-8")
    pre = c["prefix"]
    lines = src.split("\n")
    title = lines[0].lstrip("# ").strip()
    rest = "\n".join(lines[1:]).lstrip("\n")
    authors, rest = rest.split("\n\n", 1)
    affils, rest = rest.lstrip("\n").split("\n\n", 1)
    affils_html = "".join(f"<span>{sup(a.strip())}</span>" for a in affils.split("　") if a.strip())

    fig_label = re.escape(c["figure"])

    def figure(m):
        alt, path, label, cap = m.group(1), m.group(2), m.group(3), m.group(4)
        first = label.strip() == f"{c['figure']} 1"
        name = path.rsplit("/", 1)[1]
        stem, ext = name.rsplit(".", 1)
        small = f"{pre}figures/m/{stem}.{'gif' if ext == 'gif' else 'jpg'}"
        lazy = "" if first else ' loading="lazy"'
        img = (f'<picture><source media="(max-width: 900px)" srcset="{small}">'
               f'<img src="{pre}{path}" alt="{html.escape(alt)}"{lazy} decoding="async"></picture>')
        return (f'\n<figure class="fig{" wide" if first else ""}">{img}'
                f'<figcaption><b>{html.escape(label)}</b>{c["sep"]}{html.escape(cap.strip())}</figcaption></figure>\n')

    rest = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)\n\n\*\*(" + fig_label + r" \d+)\*\*\s*([^\n]+)", figure, rest)
    body = markdown.markdown(rest, extensions=["tables"], output_format="html5")
    body = re.sub(r"<p><strong>(" + re.escape(c["table"]) + r" \d+)</strong>",
                  r'<p class="table-caption"><strong>\1</strong>', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = body.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')

    lede = re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", body, re.S).group(1))
    desc = html.escape(summary(html.unescape(lede), c["desc_len"]))
    t = html.escape(title)

    page = f"""<!doctype html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{c['url']}">
<link rel="alternate" hreflang="en" href="{SITE}">
<link rel="alternate" hreflang="zh-CN" href="{SITE}zh/">
<meta property="og:type" content="article">
<meta property="og:url" content="{c['url']}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/social.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{pre}assets/style.css">
</head>
<body>
<main class="post">
<nav class="lang-switch"><a href="{c['other_href']}" hreflang="{'zh-CN' if lang == 'en' else 'en'}">{c['other_label']}</a></nav>
<header class="post-header">
<h1>{t}</h1>
<p class="authors">{sup(authors)}</p>
<p class="affils">{affils_html}</p>
</header>
{body}
<section class="cite">
<h2>{c['cite_heading']}</h2>
<p>{c['cite_intro']}</p>
<pre><code>{html.escape(BIBTEX)}</code></pre>
</section>
<footer class="post-footer"><p>{c['license_note']}</p></footer>
</main>
</body>
</html>
"""
    out = ROOT / c["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {c['out']} ({len(page):,} bytes)")


if __name__ == "__main__":
    for lang, config in LANGS.items():
        build(lang, config)
