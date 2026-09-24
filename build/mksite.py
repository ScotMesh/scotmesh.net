"""Turn build/page.html into the document served at scotmesh.net.

The artifact host supplies a document skeleton; here we supply our own. The
site also self-hosts IBM Plex under /fonts rather than pulling it from Google,
which is how the previous page already worked.
"""
import pathlib, re
import seo

page = pathlib.Path('page.html').read_text()

FONTS = '''<style>
/* IBM Plex, self-hosted under /fonts. */
@font-face{font-family:"IBM Plex Mono";font-weight:400;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-mono-400.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Mono";font-weight:600;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-mono-600.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-weight:400;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-sans-condensed-400.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-weight:600;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-sans-condensed-600.woff2) format("woff2")}
</style>'''

page = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', page)
page = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">', FONTS, page, count=1)
assert 'fonts.googleapis.com' not in page, 'a Google Fonts reference survived'
assert '@font-face' in page

page = re.sub(r'<title>.*?</title>\s*', '', page, count=1)  # seo.head() supplies the title

PRELOADS = '''<link rel="preload" href="/fonts/ibm-plex-mono-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-sans-condensed-400.woff2" as="font" type="font/woff2" crossorigin>
'''
HEAD_EXTRA = seo.head('parent', extra=PRELOADS)

RESET = '''<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>'''

head_end = page.index('</style>') + len('</style>')
head, body = page[:head_end], page[head_end:]

doc = ('<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n' + HEAD_EXTRA + head + '\n' + RESET +
       '\n</head>\n<body>\n' + body.strip() +
       '\n<script src="/app.js" defer></script>\n</body>\n</html>\n')

out = pathlib.Path('..')
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(doc)
(out / 'app.js').write_text(pathlib.Path('site-app.js').read_text())
(out / 'robots.txt').write_text(seo.robots('parent'))
(out / 'sitemap.xml').write_text(seo.sitemap('parent'))
print('index.html %.0f KB, app.js %.1f KB' %
      (len(doc) / 1024, len((out / 'app.js').read_text()) / 1024))
