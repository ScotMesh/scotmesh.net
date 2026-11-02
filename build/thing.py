"""The "What's this thing?" page, for people who find a repeater.

Takes its chrome and styles from the built news page, so run this after news.py.
Writes whatisthisthing/index.html.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://scotmesh.net/whatisthisthing/'
TITLE = "What's this thing?"
DESC = 'Found a small antenna and solar panel on a post or a tree? It is a ScotMesh radio repeater. Here is what it does and who to tell if there is a problem.'

CSS = '''<style>
  /* What's this thing. The site's own tokens; nothing here introduces a colour. */
  .thing { max-width: 720px; margin: 0 auto; display: grid; gap: 40px; padding-block: 8px 48px; }
  .thing-hero { position: relative; aspect-ratio: 16 / 7; min-height: 240px; border-radius: 12px; overflow: hidden;
    background: url("/whatisthisthing/repeater-in-the-mist.jpg") center 30% / cover; }
  .thing-title { display: grid; gap: 12px; }
  .thing-title h1 { margin: 0; }
  .thing-title .lead { margin: 0; font-size: 1.3rem; line-height: 1.38; }
  .thing h2 { margin: 0 0 10px; }
  .thing p { margin: 0; }
  .parts { display: grid; grid-template-columns: minmax(0, 280px) minmax(0, 1fr); gap: 24px; align-items: center; }
  .parts .photo { position: relative; }
  .parts img { display: block; width: 100%; height: auto; border-radius: 12px; }
  .pin, .key li::before { width: 26px; height: 26px; border-radius: 50%; background: var(--bg); border: 2px solid var(--chrome-ink);
    color: var(--ink); font: 600 13px/22px var(--mono); text-align: center; }
  .pin { position: absolute; margin: -13px 0 0 -13px; }
  .key { list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; counter-reset: k; }
  .key li { display: grid; grid-template-columns: 26px minmax(0, 1fr); gap: 12px; counter-increment: k; }
  .key li::before { content: counter(k); }
  .key b { display: block; }
  .key span { color: var(--muted); }
  @media (max-width: 560px) { .parts { grid-template-columns: minmax(0, 1fr); } .parts .photo { max-width: 300px; } }
  .ticks { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .ticks li { padding-left: 22px; position: relative; }
  .ticks li::before { content: ""; position: absolute; left: 2px; top: .7em; width: 9px; height: 2px; background: var(--chrome-ink); }
  .did { border-left: 3px solid var(--signal); padding: 2px 0 2px 16px; font-size: 1.15rem; }
  .did b { display: block; font: 600 12px/1.6 var(--mono); color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
  .problem { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 22px; display: grid; gap: 12px; }
  .problem h2 { margin: 0; }
  .join { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
  .join a { padding: 9px 16px; border-radius: 6px; font-weight: 600; text-decoration: none; border: 1px solid var(--line); color: var(--ink); }
  .join a.main { background: var(--saltire); border-color: var(--saltire); color: #fff; }
  .join a:hover { border-color: var(--chrome-ink); }
</style>'''

MAIN = '''<main><section><div class="wrap"><div class="thing">
  <div class="thing-hero" role="img" aria-label="A small antenna and solar panel on top of a tree in the mist"></div>

  <div class="thing-title">
    <h1>What's this thing?</h1>
    <p class="lead">You've found a radio repeater. Don't worry, it's just us nerds, wanting to text each other without the internet.</p>
    <p>It passes data from node to node across Scotland, which gives us texting, telemetry and weather information. Mostly, though, it's fun.</p>
  </div>

  <p class="did"><b>Did you know?</b> Some of our communications stretch from Inverness to the south of the island of Ireland.</p>

  <section>
    <h2>When there's no signal</h2>
    <p>It also works where there's no mobile signal, and it doesn't need mains power. Some of the community see it as a backup radio service for emergencies, such as a big storm or a long power cut.</p>
  </section>

  <section class="parts" aria-label="The parts of a repeater">
    <figure class="photo" style="margin:0">
      <img src="/whatisthisthing/repeater-on-a-post.jpg" alt="An antenna, a small black box and a solar panel fixed to a wooden fence post" width="760" height="1351" loading="lazy">
      <span class="pin" style="left:52%;top:22%" aria-hidden="true">1</span>
      <span class="pin" style="left:47%;top:51%" aria-hidden="true">2</span>
      <span class="pin" style="left:42%;top:69%" aria-hidden="true">3</span>
    </figure>
    <ol class="key">
      <li><div><b>Antenna</b><span>Sends and receives the messages.</span></div></li>
      <li><div><b>Radio</b><span>A small box that passes messages on.</span></div></li>
      <li><div><b>Solar panel</b><span>Keeps it running, with no mains power.</span></div></li>
    </ol>
  </section>

  <section>
    <h2>Is it safe?</h2>
    <ul class="ticks">
      <li>It uses less radio power than a mobile phone.</li>
      <li>It has no camera and no microphone.</li>
    </ul>
  </section>

  <section>
    <h2>Who put it there?</h2>
    <p>Anyone in the community can place one, and we advise them to get the landowner's permission first.</p>
  </section>

  <section class="problem" id="problem">
    <h2>Seen a problem?</h2>
    <p>If one has fallen, looks damaged or shouldn't be there, please tell us where it is. We'll find its owner as soon as possible and get back to you. Don't climb up to it or try to move it.</p>
    <ul class="ticks">
      <li>Where you saw it: the nearest place, road or a map pin</li>
      <li>What's wrong</li>
      <li>A photo, if you can</li>
    </ul>
    <p>Email <a href="mailto:contact@scotmesh.net">contact@scotmesh.net</a>.</p>
  </section>

  <section>
    <h2>Get involved</h2>
    <p>Anyone can join in. You can use the network with a cheap radio, or put up a repeater of your own.</p>
    <div class="join">
      <a class="main" href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Join us on Discord</a>
      <a href="https://scotmesh.net/">About ScotMesh</a>
    </div>
  </section>
</div></div></section></main>'''


def build():
    s = (ROOT / 'news/index.html').read_text(encoding='utf-8')
    s = re.sub(r'<title>.*?</title>', f'<title>{TITLE} — ScotMesh</title>', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', rf'\g<1>{DESC}', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', rf'\g<1>{DESC}', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\g<1>{TITLE}', s, count=1)
    s = s.replace('https://scotmesh.net/news/', URL)
    s = s.replace('content="https://scotmesh.net/og.png"', f'content="{URL}repeater-in-the-mist.jpg"')
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = re.sub(r'<main.*?</main>', lambda _: MAIN, s, count=1, flags=re.S)
    s = re.sub(r'<script src="/news/news\.js"[^>]*></script>\n?', '', s)
    (ROOT / 'whatisthisthing/index.html').write_text(s, encoding='utf-8')


if __name__ == '__main__':
    build()
