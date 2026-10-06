"""Shells for the news pages.

The posts themselves are Markdown under news/posts/ and are rendered in the
browser by news/news.js. All this produces is the page around them: the site's
own chrome, an empty container for the script to fill, and the title and
preview tags, which have to be in the HTML because the services that unfurl a
shared link do not run scripts.

Adding a post is a Markdown file and a line in news/posts.json. Running the
build again gives it its shell.
"""
import json
import pathlib
import re

import yaml

BASE = 'https://scotmesh.net'

CSS = '''<style>
  /* News. The site's own tokens throughout; nothing here introduces a colour. */
  .news-head { display: grid; gap: 10px; justify-items: start; padding-block: 10px 24px; }
  .news-head h1 { margin: 0; }
  .news-head p { margin: 0; color: var(--muted); max-width: 60ch; }
  .news-list { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); }
  .post-card { display: grid; border: 1px solid var(--line); border-radius: 12px; background: var(--card);
    overflow: hidden; text-decoration: none; color: inherit; }
  .post-card:hover { border-color: color-mix(in srgb, var(--saltire) 45%, var(--line)); }
  .post-card .cover { display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; }
  .post-card .in { padding: 15px 16px 17px; display: grid; gap: 8px; align-content: start; }
  .post-card h2 { font-size: 18px; line-height: 1.2; margin: 0; }
  .post-card p { margin: 0; font-size: 14.5px; color: var(--muted); }
  .eyebrow { display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    font-family: var(--mono); font-size: 11.5px; color: var(--muted); }
  .eyebrow .pip { width: 8px; height: 8px; border-radius: 50%; background: var(--tint); flex: none; }
  .byline { font-family: var(--mono); font-size: 11.5px; color: var(--muted); }
  .tint-meshcore { --tint: var(--meshcore); } .tint-meshtastic { --tint: var(--meshtastic); }
  .tint-reticulum { --tint: var(--reticulum); } .tint-all { --tint: var(--saltire); }

  .article { max-width: 70ch; margin-inline: auto; display: grid; gap: 16px; padding-block: 10px 12px; }
  .article .head { display: grid; gap: 9px; }
  .article .head .lead { margin-top: 5px; }
  /* The site's base h1 caps at 18ch, which is right for the front page and
     wrong here: it broke a six-word headline over three lines. */
  .article h1 { margin: 0; max-width: none; font-size: clamp(24px, 3.4vw, 32px);
    line-height: 1.18; letter-spacing: -.015em; text-wrap: balance; }
  .article h2 { font-size: clamp(19px, 2.6vw, 24px); margin: 14px 0 -4px; }
  .article p { margin: 0; font-size: 16.5px; line-height: 1.7; }
  .article .lead { font-size: 18.5px; color: var(--muted); }
  .article .credit { font-family: var(--mono); font-size: 11.5px; color: var(--muted); margin-top: -8px; }
  .article figure { margin: 0; }
  .article figure svg, .article figure img { display: block; width: 100%; height: auto; border-radius: 12px; }
  .article .cover-fig svg, .article .cover-fig img { aspect-ratio: 16 / 9; }
  .article figcaption { margin-top: 9px; font-size: 14px; color: var(--muted); }
  .article ul { margin: 0; padding-left: 20px; display: grid; gap: 7px; }
  .article pre.cli { margin: 0; padding: 14px 16px; border-radius: 10px; overflow-x: auto;
    background: #0B1526; border: 1px solid var(--line); color: #D6E2F2;
    font-family: var(--mono); font-size: 14px; line-height: 1.7; }
  .article code { background: color-mix(in srgb, var(--line) 45%, transparent); padding: 1px 5px;
    border-radius: 4px; font-family: var(--mono); font-size: .9em; }
  .article .tablewrap { border: 1px solid var(--line); border-radius: 10px; overflow-x: auto; }
  .article table { width: 100%; border-collapse: collapse; font-size: 15px; }
  .article th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: .05em;
    text-transform: uppercase; color: var(--muted); font-weight: 400; padding: 11px 14px;
    border-bottom: 1px solid var(--line); }
  .article td { padding: 11px 14px; border-bottom: 1px solid color-mix(in srgb, var(--line) 55%, transparent); }
  .article tr:last-child td { border-bottom: 0; }
  .article td.mono { font-family: var(--mono); color: var(--muted); font-variant-numeric: tabular-nums; }
  .article hr { border: 0; border-top: 1px solid var(--line); margin: 6px 0; }
  .article .tags { display: flex; gap: 7px; flex-wrap: wrap; font-family: var(--mono); font-size: 12px; }
  .article .tags span { border: 1px solid var(--line); border-radius: 999px; padding: 3px 10px; color: var(--muted); }
  .back { font-family: var(--mono); font-size: 12.5px; color: var(--muted); text-decoration: none; }
  .back:hover { color: var(--ink); }
</style>'''

RESET = '''<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>'''


def chrome(page):
    """The whole stylesheet, the nav and the footer, from the page the build
    just made, so a news page cannot drift from the site around it."""
    styles = re.findall(r'<style>.*?</style>', page, re.S)
    if not styles:
        raise SystemExit('news: no stylesheet in page.html')
    nav = page[page.index('<header class="nav">'):page.index('<main')]
    foot = page[page.index('<footer>'):]
    foot = re.sub(r'<script[^>]*src="/app\.js"[^>]*>\s*</script>\s*', '', foot)
    return ''.join(styles), nav, foot


def front_matter(path):
    text = path.read_text()
    if not text.startswith('---'):
        return {}
    end = text.index('\n---', 3)
    return yaml.safe_load(text[4:end]) or {}


def shell(seo, styles, nav, foot, title, desc, url, inner):
    return ('<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n'
            + seo.page_head(title, desc, url) + styles + '\n' + RESET + CSS
            + '\n</head>\n<body>\n' + nav + inner + foot
            + '\n<script src="/news/news.js" defer></script>\n</body>\n</html>\n')


def build(page, seo, out):
    styles, nav, foot = chrome(page)
    news = out / 'news'
    slugs = json.loads((news / 'posts.json').read_text())
    paths = ['/news/']

    index = ('<main><section><div class="wrap">'
             '<div class="news-head"><h1>News</h1>'
             '<p>What is going up, what is going down, and what changed on the three networks '
             'ScotMesh runs.</p></div>'
             '<div class="news-list" id="news-list"></div>'
             '</div></section></main>')
    (news / 'index.html').write_text(shell(
        seo, styles, nav, foot, 'News',
        'Announcements and changes across the three mesh networks ScotMesh runs in Scotland: '
        'MeshCore, Meshtastic and Reticulum.', BASE + '/news/', index))

    for slug in slugs:
        meta = front_matter(news / 'posts' / slug / 'index.md')
        url = BASE + '/news/' + slug + '/'
        art = ('<main><section><div class="wrap">'
               '<article class="article" id="news-post" data-post="' + slug + '"></article>'
               '</div></section></main>')
        d = news / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(shell(
            seo, styles, nav, foot,
            meta.get('title', slug), meta.get('summary', ''), url, art))
        paths.append('/news/%s/' % slug)

    print('news: %d shells' % len(paths))
    return paths
