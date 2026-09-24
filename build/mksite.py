"""Turn build/page.html into the document served at scotmesh.net.

The artifact host supplies a document skeleton; here we supply our own. The
site also self-hosts IBM Plex under /fonts rather than pulling it from Google,
which is how the previous page already worked.
"""
import pathlib, re

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

page = page.replace('<title>ScotMesh</title>',
                    '<title>ScotMesh — community mesh networks in Scotland</title>', 1)

HEAD_EXTRA = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="https://scotmesh.net/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="description" content="ScotMesh: the community mesh networks of Scotland. MeshCore, Meshtastic and Reticulum — what each one is, where the nodes are, and how to join.">
<meta name="theme-color" content="#0A1424">
<meta name="color-scheme" content="dark light">
<meta property="og:title" content="ScotMesh">
<meta property="og:description" content="The community mesh networks of Scotland: MeshCore, Meshtastic and Reticulum. What each one is, where the nodes are, and how to join.">
<meta property="og:image" content="https://scotmesh.net/og.png">
<meta property="og:url" content="https://scotmesh.net/">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/ibm-plex-mono-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-sans-condensed-400.woff2" as="font" type="font/woff2" crossorigin>
'''

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
print('index.html %.0f KB, app.js %.1f KB' %
      (len(doc) / 1024, len((out / 'app.js').read_text()) / 1024))
