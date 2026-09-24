import json, pathlib

A = json.loads(pathlib.Path('assets.json').read_text())

HEAD = '''<title>ScotMesh</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@400;600&display=swap">
<script>
  (function () {
    try {
      var t = localStorage.getItem('scotmesh-theme');
      if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    } catch (e) {}
  })();
</script>
<style>
  /* ScotMesh brand tokens. This is the one page where all three network tints
     appear together, so Saltire stays the page's own chrome and each tint
     belongs strictly to its network's section. */
  :root {
    --night: #0A1424; --saltire: #005EB8; --mist: #E6EDF7; --signal: #F2B33D;
    --meshcore: #56B4F5;   --meshcore-deep: #0069A6;
    --meshtastic: #65C281; --meshtastic-deep: #05773B;
    --reticulum: #B199F4;  --reticulum-deep: #6A51A4;

    --bg: var(--night); --well: #0C1729; --card: #101C30; --line: #22324D;
    --ink: var(--mist); --muted: #8FA2BD; --link: #7FB2EE;
    --chrome: var(--saltire); --chrome-ink: #7FB2EE;
    --good: #65C281; --bad: #E4707A;

    --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
    --sans: "IBM Plex Sans Condensed", "Roboto Condensed", "Arial Narrow", system-ui, sans-serif;
    --shadow: 0 1px 0 rgba(255,255,255,.03), 0 12px 32px -18px rgba(0,0,0,.9);
  }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) {
      --bg: #F4F7FC; --well: #EAF0F9; --card: #FFF; --line: #D3DEEE;
      --ink: var(--night); --muted: #5A6B85; --link: var(--saltire); --chrome-ink: var(--saltire);
      --meshcore: var(--meshcore-deep); --meshtastic: var(--meshtastic-deep); --reticulum: var(--reticulum-deep);
      --good: #05773B; --bad: #A61B28;
      --shadow: 0 1px 0 rgba(255,255,255,.7), 0 12px 28px -20px rgba(10,20,36,.45);
    }
  }
  :root[data-theme="light"] {
    --bg: #F4F7FC; --well: #EAF0F9; --card: #FFF; --line: #D3DEEE;
    --ink: var(--night); --muted: #5A6B85; --link: var(--saltire); --chrome-ink: var(--saltire);
    --meshcore: var(--meshcore-deep); --meshtastic: var(--meshtastic-deep); --reticulum: var(--reticulum-deep);
    --good: #05773B; --bad: #A61B28;
    --shadow: 0 1px 0 rgba(255,255,255,.7), 0 12px 28px -20px rgba(10,20,36,.45);
  }

  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink);
    font-family: var(--sans); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1140px; margin-inline: auto; padding-inline: 20px; }
  h1, h2, h3 { font-family: var(--mono); font-weight: 600; margin: 0; text-wrap: balance; }
  a { color: var(--link); }
  code { font-family: var(--mono); font-size: .92em; }

  .nav { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20;
    background: color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--line); }
  .nav .wrap { display: flex; align-items: center; gap: 12px; min-height: 60px; flex-wrap: wrap; }
  .lockup { display: block; margin-right: auto; }
  .lockup svg { display: block; height: 30px; width: auto; }
  .lockup .on-light { display: none; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .lockup .on-light { display: block; }
    :root:not([data-theme="dark"]) .lockup .on-dark { display: none; }
  }
  :root[data-theme="light"] .lockup .on-light { display: block; }
  :root[data-theme="light"] .lockup .on-dark { display: none; }
  .nav nav { display: flex; align-items: center; gap: 3px; flex-wrap: wrap; }
  .nav nav a { font-family: var(--mono); font-size: 13.5px; text-decoration: none; color: var(--muted);
    padding: 7px 10px; border-radius: 6px; }
  .nav nav a:hover { color: var(--ink); background: var(--well); }
  .theme-toggle { display: inline-flex; align-items: center; justify-content: center; width: 34px;
    height: 32px; padding: 0; color: var(--muted); background: none; border: 1px solid transparent;
    border-radius: 6px; cursor: pointer; }
  .theme-toggle:hover { color: var(--ink); background: var(--well); }
  .theme-toggle .t-light { display: none; } .theme-toggle .t-dark { display: block; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .theme-toggle .t-dark { display: none; }
    :root:not([data-theme="dark"]) .theme-toggle .t-light { display: block; }
  }
  :root[data-theme="light"] .theme-toggle .t-dark { display: none; }
  :root[data-theme="light"] .theme-toggle .t-light { display: block; }
  :root[data-theme="dark"] .theme-toggle .t-dark { display: block; }
  :root[data-theme="dark"] .theme-toggle .t-light { display: none; }

  /* ------------------------------------------------------------------ hero
     Always dark, like the sibling sites' banners: the tokens below pin the
     Night palette, so it must paint its own background or light mode puts
     this ink on a light page. */
  .hero { position: relative; overflow: hidden; border-bottom: 1px solid #22324D;
    color: var(--ink); background: var(--bg);
    --bg: #0A1424; --ink: #E6EDF7; --muted: #8FA2BD; --line: #22324D; --card: #101C30;
    --meshcore: #56B4F5; --meshtastic: #65C281; --reticulum: #B199F4; --chrome-ink: #7FB2EE; }
  .hero-grid { position: relative; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 560px);
    gap: 40px; align-items: center; padding-block: 56px 26px; }
  h1 { font-size: clamp(30px, 4.4vw, 46px); line-height: 1.07; letter-spacing: -0.01em; max-width: 18ch; }
  .lede { font-size: clamp(16px, 2vw, 19px); color: var(--muted); max-width: 54ch; margin: 16px 0 0; }
  .hero-links { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }
  .btn { display: inline-flex; align-items: center; font-family: var(--mono); font-size: 14px;
    font-weight: 600; text-decoration: none; padding: 11px 17px; border-radius: 8px;
    border: 1px solid var(--line); color: var(--ink); background: var(--card); }
  .btn-primary { background: var(--saltire); border-color: var(--saltire); color: #fff; }
  /* the map: one Scotland, three networks */
  .scotmap { display: block; width: 100%; height: auto; max-height: 600px; margin-inline: auto; }
  .scotmap .coast { fill: none; stroke: var(--saltire); stroke-opacity: .95; stroke-width: 1.15;
    stroke-linejoin: round; stroke-linecap: round; }
  .scotmap .inset-box { fill: rgba(0,94,184,.10); stroke: var(--saltire); stroke-opacity: .7; stroke-width: .8; }
  .scotmap .inset-label { fill: var(--muted); font-family: var(--mono); font-size: 9.5px; }
  .scotmap text { font-family: var(--mono); }
  .legend { display: flex; gap: 18px; flex-wrap: wrap; justify-content: center; margin-top: 10px;
    font-size: 13px; color: var(--muted); }
  .legend span { display: inline-flex; align-items: center; gap: 7px; }
  .legend i { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
  .legend b { color: var(--ink); font-weight: 600; font-family: var(--mono); }
  @keyframes ring { from { r: 4; opacity: .55; } to { r: 26; opacity: 0; } }
  .scotmap .ring { animation: ring 3.2s ease-out infinite; }
  @media (prefers-reduced-motion: reduce) { .scotmap .ring, .scotmap .pulse { display: none; } }
  .hero .nets { position: relative; padding-top: 6px; }

  /* The three networks, side by side. This is the page's argument: the only
     place all three exist together, each answering "is this the one for me?"
     with a live figure rather than a claim. */
  .nets { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; padding-block: 34px 52px; }
  .net { position: relative; display: flex; flex-direction: column; gap: 12px; padding: 22px;
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    box-shadow: var(--shadow); text-decoration: none; color: inherit;
    border-top: 3px solid var(--tint); }
  .net:hover { border-color: color-mix(in srgb, var(--tint) 55%, var(--line)); border-top-color: var(--tint); }
  .net-head { display: flex; align-items: center; gap: 11px; }
  .net-head svg { width: 34px; height: 34px; border-radius: 7px; display: block; }
  .net-name { font-family: var(--mono); font-weight: 600; font-size: 17px; }
  .net-for { font-size: 13px; color: var(--tint); font-family: var(--mono); }
  .net p { margin: 0; font-size: 14.5px; color: var(--muted); }
  .vitals { display: flex; gap: 18px; flex-wrap: wrap; margin-top: auto; padding-top: 14px;
    border-top: 1px solid var(--line); }
  .vital .n { font-family: var(--mono); font-size: 22px; font-weight: 600; line-height: 1.1;
    font-variant-numeric: tabular-nums; color: var(--tint); }
  .vital .l { font-size: 12.5px; color: var(--muted); }
  .go { font-family: var(--mono); font-size: 13.5px; color: var(--tint); }

  .live-note { grid-column: 1 / -1; margin: 0; font-size: 13px; color: var(--muted); }

  /* --------------------------------------------------------------- sections */
  section { border-bottom: 1px solid var(--line); }
  section.alt { background: var(--well); }
  .sec { padding-block: 50px; }
  .sec-head { display: flex; align-items: baseline; gap: 13px; flex-wrap: wrap; margin-bottom: 24px; }
  .sec-head h2 { font-size: clamp(20px, 2.6vw, 26px); }
  .sec-head .rule { font-family: var(--mono); font-size: 12px; letter-spacing: .05em;
    text-transform: uppercase; color: var(--tint, var(--muted)); }
  .sec-head p { margin: 0; color: var(--muted); font-size: 14.5px; }

  /* explainers: words one side, the mechanism moving on the other */
  .explain { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); gap: 36px; align-items: center; }
  .explain.flip .words { order: 2; }
  .explain .words p { margin: 0; font-size: 16px; color: var(--muted); max-width: 46ch; }
  .explain .words p + p { margin-top: 10px; }
  .facts { list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 7px; font-size: 14.5px; }
  .facts li { display: flex; gap: 10px; align-items: baseline; }
  .facts li::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--tint); flex: none; transform: translateY(-1px); }
  .diagram { display: block; width: 100%; height: auto; background: var(--card); border: 1px solid var(--line);
    border-radius: 14px; box-shadow: var(--shadow); }
  .diagram text { font-family: var(--mono); fill: var(--muted); }
  @media (prefers-reduced-motion: reduce) { .diagram .anim { display: none; } }
  @media (max-width: 880px) { .explain { grid-template-columns: 1fr; } .explain.flip .words { order: 0; } }
  .tools { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 12px; }
  .tool { display: flex; flex-direction: column; gap: 6px; padding: 17px 18px; background: var(--card);
    border: 1px solid var(--line); border-radius: 11px; text-decoration: none; color: inherit;
    box-shadow: var(--shadow); }
  .tool:hover { border-color: color-mix(in srgb, var(--tint) 50%, var(--line)); }
  .tool h3 { font-size: 15px; }
  .tool .q { font-size: 13.5px; color: var(--tint); font-family: var(--mono); }
  .tool p { margin: 0; font-size: 14px; color: var(--muted); }
  .tool .host { font-family: var(--mono); font-size: 11.5px; color: var(--muted); margin-top: 4px; }

  pre { margin: 0; background: var(--well); border: 1px solid var(--line); border-radius: 8px;
    padding: 12px 13px; overflow-x: auto; font-family: var(--mono); font-size: 12.5px; line-height: 1.55; }
  :root:not([data-theme="light"]) pre { background: #0A1424; }
  .panel { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px;
    box-shadow: var(--shadow); display: grid; gap: 12px; }

  footer { padding-block: 34px 44px; font-size: 14px; color: var(--muted); }
  .foot-grid { display: grid; grid-template-columns: 1.5fr repeat(2, minmax(0,1fr)); gap: 26px; }
  .foot-grid ul { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 6px; }
  .foot-grid a { color: var(--muted); text-decoration: none; }
  .foot-grid a:hover { color: var(--ink); }
  .lbl { font-family: var(--mono); font-size: 11.5px; letter-spacing: .05em; text-transform: uppercase; }
  .lockup-scotmesh svg { display: block; height: 26px; width: auto; }
  .lockup-scotmesh .on-light { display: none; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .lockup-scotmesh .on-light { display: block; }
    :root:not([data-theme="dark"]) .lockup-scotmesh .on-dark { display: none; }
  }
  :root[data-theme="light"] .lockup-scotmesh .on-light { display: block; }
  :root[data-theme="light"] .lockup-scotmesh .on-dark { display: none; }
  .foot-bar { grid-column: 1 / -1; display: flex; justify-content: space-between; gap: 14px;
    flex-wrap: wrap; margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 13.5px; }

  section[id] { scroll-margin-top: 72px; }
  a:focus-visible, button:focus-visible { outline: 2px solid var(--chrome-ink); outline-offset: 2px; }

  @media (max-width: 880px) {
    .nets { grid-template-columns: 1fr; }
    .foot-grid { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 520px) { .foot-grid { grid-template-columns: 1fr; } }
</style>'''

NETS = [
    dict(id='meshcore', name='MeshCore', tint='var(--meshcore)', href='https://meshcore.scotmesh.net/',
         who='Held Up by Repeaters',
         blurb='Long-range LoRa messaging on cheap radios, with an app on your phone and '
               'repeaters on the hills doing the carrying. The mesh reaches from the top of '
               'Scotland down through the Isles and across to the south of the Republic of '
               'Ireland, with a live map, coverage built from real packets, and alerts when a '
               'repeater goes quiet.',
         vitals=[('repeaters', '109', 'repeaters'), ('packets', '741', 'packets today'), ('observers', '13', 'observers')]),
    dict(id='meshtastic', name='Meshtastic', tint='var(--meshtastic)', href='https://meshtastic.scotmesh.net/',
         who="Scotland's Original Mesh",
         blurb='Long-range LoRa messaging on cheap radios, with an app on your phone and '
               'the community\'s longest-running mesh behind it. Scotland only, with a wide '
               'choice of hardware, plenty of documentation, and hundreds of nodes already on air.',
         vitals=[('nodes', '293', 'nodes heard'), ('routers', '17', 'routers'), ('packets', '63', 'packets today')]),
    dict(id='reticulum', name='Reticulum', tint='var(--reticulum)', href='https://rns.scotmesh.net/',
         who='No Radio Needed',
         blurb='An encrypted network with no accounts and no central authority, carried over LoRa, '
               'I2P or plain internet. The only one of the three you can join without buying '
               'anything: connect over the internet, and add a radio later if you want one.',
         vitals=[('clients', '155', 'clients'), ('peers', '4/4', 'peers linked'), ('uptime', '15d', 'uptime')]),
]


def traffic(P):
    """Illustrative traffic over the real node positions, shaped like each
    network's actual behaviour rather than a generic sparkle.

    Map scale is ~0.8 km per unit. MeshCore routes chain repeater to repeater
    at up to ~50 km a hop, starting from a companion where one is close; that
    is how a MeshCore message crosses the country. Meshtastic bursts flood
    two or three neighbours within a few km and stop, as a hop limit does.
    Reticulum has one gateway here, so it rings; nothing else is invented.
    """
    import math, random
    rnd = random.Random(2026)
    def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
    def near(p, pool, lo, hi):
        return [q for q in pool if q is not p and lo <= dist(p, q) <= hi]

    mc = [(x, y, r) for x, y, r in P['mc']]
    reps = [n for n in mc if n[2] == 'repeater']
    comps = [n for n in mc if n[2] != 'repeater']
    mt = [(x, y, r) for x, y, r in P['mt']]
    out = []

    # --- MeshCore: long relayed chains ------------------------------------
    routes, tries = [], 0
    while len(routes) < 6 and tries < 3000:
        tries += 1
        start = rnd.choice(comps) if comps and rnd.random() < 0.7 else rnd.choice(reps)
        chain = [start]
        for _ in range(rnd.choice([3, 4, 5, 6])):
            cand = [q for q in near(chain[-1], reps, 10, 62) if q not in chain]
            if len(chain) > 1:  # keep heading away from where we came from
                prev = chain[-2]
                cand = [q for q in cand if dist(q, prev) > dist(chain[-1], prev)] or cand
            if not cand: break
            chain.append(rnd.choice(cand))
        if len(chain) >= 4 and dist(chain[0], chain[-1]) > 70:
            routes.append(chain)
    for i, chain in enumerate(routes):
        d = 'M' + ' L'.join('%.1f %.1f' % (q[0], q[1]) for q in chain)
        dur, begin = 5.5 + 0.9 * len(chain), i * 1.7
        motion = '<animateMotion dur="%.1fs" begin="%.1fs" repeatCount="indefinite" path="%s"/>' % (dur, begin, d)
        fade = '<animate attributeName="opacity" dur="%.1fs" begin="%.1fs" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.06;.9;1"/>' % (dur, begin)
        out.append('<circle class="pulse" r="7" fill="var(--meshcore)" fill-opacity=".22" opacity="0">%s%s</circle>' % (motion, fade))
        out.append('<circle class="pulse" r="2.8" fill="#FFFFFF" opacity="0">%s%s</circle>' % (motion, fade))

    # --- Meshtastic: short local floods ------------------------------------
    bursts, tries = [], 0
    while len(bursts) < 7 and tries < 3000:
        tries += 1
        o = rnd.choice(mt)
        nb = near(o, mt, 5, 26)
        if len(nb) < 2: continue
        rnd.shuffle(nb)
        first = nb[:rnd.choice([2, 3])]
        # a second hop from one of them, so it reads as a flood not a star
        second = []
        for f in first:
            more = [q for q in near(f, mt, 5, 26) if q is not o and q not in first]
            if more and rnd.random() < 0.6: second.append((f, rnd.choice(more)))
        bursts.append((o, first, second))
    CYCLE = 9.0
    for i, (o, first, second) in enumerate(bursts):
        t0 = (i * 1.3) % CYCLE
        def pulse(a, b, start, hop):
            d = 'M%.1f %.1f L%.1f %.1f' % (a[0], a[1], b[0], b[1])
            k0 = start / CYCLE; k1 = min(0.999, (start + hop) / CYCLE)
            return ('<circle class="pulse" r="2.4" fill="var(--meshtastic)" stroke="#0A1424" stroke-width=".8" paint-order="stroke" opacity="0">'
                    '<animateMotion dur="%.1fs" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;%.4f;%.4f;1" path="%s"/>'
                    '<animate attributeName="opacity" dur="%.1fs" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;%.4f;%.4f;%.4f;%.4f;1"/></circle>'
                    % (CYCLE, k0, k1, d, CYCLE, max(0, k0 - .002), k0, k1, min(1, k1 + .004)))
        # the origin rings once, then the hops leave
        out.append('<circle class="pulse" cx="%.1f" cy="%.1f" r="2" fill="none" stroke="var(--meshtastic)" stroke-width="1.2" opacity="0">'
                   '<animate attributeName="r" dur="%.1fs" repeatCount="indefinite" values="2;2;18;18" keyTimes="0;%.4f;%.4f;1"/>'
                   '<animate attributeName="opacity" dur="%.1fs" repeatCount="indefinite" values="0;0;.8;0;0" keyTimes="0;%.4f;%.4f;%.4f;1"/></circle>'
                   % (o[0], o[1], CYCLE, t0/CYCLE, min(.999,(t0+1.0)/CYCLE), CYCLE, max(0,t0/CYCLE-.002), min(.998,(t0+.05)/CYCLE), min(.999,(t0+1.0)/CYCLE)))
        for f in first: out.append(pulse(o, f, t0 + 0.2, 0.7))
        for f, q in second: out.append(pulse(f, q, t0 + 1.0, 0.7))

    # --- Reticulum: the gateway announces ---------------------------------
    gx, gy = P['rns'][0]
    out.append('<circle class="pulse ring" cx="%.1f" cy="%.1f" r="4" fill="none" stroke="var(--reticulum)" stroke-width="1.2"/>' % (gx, gy))
    return ''.join(out)


def scotmap():
    """One Scotland, all three networks on it, from each network's own data.

    MeshCore and Meshtastic are real node positions (CoreScope and the
    Meshtastic site's feed), projected with the coastline's own maths.
    Reticulum is honest about what it is: one LoRa gateway at Cadham, with
    the network itself reached over the internet rather than the air.
    """
    P = json.loads(pathlib.Path('points.json').read_text())
    coast = pathlib.Path('coast.txt').read_text()
    land = pathlib.Path('land-path.txt').read_text()
    inset = pathlib.Path('inset.txt').read_text()
    X0, Y0, W, H = -8, -8, 536, 679
    band = H / 5 * 0.62
    o = ['<svg class="scotmap" viewBox="%d %d %d %d" role="img" aria-label="Map of Scotland with every MeshCore and Meshtastic node heard, in each network\'s colour, and the Reticulum gateway at Cadham">' % (X0, Y0, W, H)]
    # the saltire on the land, quiet, as on the sibling sites
    o.append('<defs><clipPath id="scot-clip"><path d="%s"/></clipPath></defs>' % land)
    o.append('<g clip-path="url(#scot-clip)"><rect x="%d" y="%d" width="%d" height="%d" fill="#122140"/>'
             '<path d="M%d %d L%d %d M%d %d L%d %d" stroke="#FFFFFF" stroke-width="%g" fill="none" stroke-opacity=".10"/></g>'
             % (X0, Y0, W, H, X0, Y0, X0+W, Y0+H, X0+W, Y0, X0, Y0+H, band))
    o.append('<path class="coast" d="%s"/>' % coast)
    o.append(inset)
    halo = ' stroke="#0A1424" stroke-width="0.8" paint-order="stroke"'
    # MeshCore first, then Meshtastic on top: both dense in the central belt,
    # and drawing order is not a ranking — the smaller set reads better above.
    o.append('<g class="mc">')
    for x, y, role in P['mc']:
        r = 2.6 if role == 'repeater' else 1.9
        o.append('<circle cx="%s" cy="%s" r="%s" fill="var(--meshcore)"%s/>' % (x, y, r, halo))
    o.append('</g><g class="mt">')
    for x, y, role in P['mt']:
        r = 2.6 if role in ('ROUTER', 'ROUTER_LATE') else 1.9
        o.append('<circle cx="%s" cy="%s" r="%s" fill="var(--meshtastic)"%s/>' % (x, y, r, halo))
    o.append('</g>')
    gx, gy = P['rns'][0]
    o.append('<g class="rns"><circle cx="%.1f" cy="%.1f" r="4" fill="var(--reticulum)"%s/></g>' % (gx, gy, halo))
    o.append('<g class="traffic">%s</g>' % traffic(P))
    o.append('</svg>')
    return ''.join(o)


def net_cards():
    out = []
    for n in NETS:
        vit = ''.join('<div class="vital"><div class="n" data-vital="%s">%s</div><div class="l">%s</div></div>' % v
                      for v in n['vitals'])
        out.append(
            '<a class="net" style="--tint: %s" href="%s" data-net="%s">'
            '<div class="net-head">%s<div><div class="net-name">%s</div>'
            '<div class="net-for">%s</div></div></div>'
            '<p>%s</p><div class="vitals">%s</div><div class="go">%s &rarr;</div></a>'
            % (n['tint'], n['href'], n['id'], A[n['id']], n['name'], n['who'], n['blurb'], vit,
               n['href'].replace('https://', '').rstrip('/')))
    return ''.join(out)

def diagram_meshcore():
    """Fixed repeaters on high ground relay a message hop by hop."""
    masts = [(130, 118), (270, 100), (405, 112)]
    o = ['<svg class="diagram" viewBox="0 0 520 240" role="img" aria-label="A message travels from one radio to another by hopping between repeaters placed on hills">']
    o.append('<path d="M0 205 Q 70 160 130 178 T 270 162 T 405 172 T 520 200 L520 240 L0 240 Z" fill="#0A1424" stroke="#22324D"/>')
    for x, y in masts:
        base = {130: 178, 270: 162, 405: 172}[x]
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--muted)" stroke-width="2"/>' % (x, base, x, y + 6))
        o.append('<circle cx="%d" cy="%d" r="5" fill="var(--meshcore)"/>' % (x, y))
        o.append('<text x="%d" y="%d" text-anchor="middle" font-size="10">repeater</text>' % (x, base + 16))
    for x in (34, 486):
        o.append('<rect x="%d" y="192" width="18" height="30" rx="4" fill="#101C30" stroke="var(--muted)"/>' % (x - 9))
        o.append('<circle cx="%d" cy="214" r="2.2" fill="var(--ink)"/>' % x)
    o.append('<text x="34" y="236" text-anchor="middle" font-size="10">you</text><text x="486" y="236" text-anchor="middle" font-size="10">them</text>')
    path = 'M34 190 L130 118 L270 100 L405 112 L486 190'
    o.append('<defs><path id="mc-route" d="%s"/></defs>' % path)
    o.append('<path d="%s" fill="none" stroke="var(--meshcore)" stroke-opacity=".25" stroke-width="1.2" stroke-dasharray="3 4"/>' % path)
    o.append('<g class="anim">')
    o.append('<circle r="5" fill="var(--meshcore)"><animateMotion dur="5s" repeatCount="indefinite"><mpath href="#mc-route"/></animateMotion></circle>')
    # each repeater flashes as the packet reaches it (times from the path's segment lengths)
    for (x, y), t in zip(masts, (1.15, 2.35, 3.55)):
        o.append('<circle cx="%d" cy="%d" r="5" fill="none" stroke="var(--meshcore)" stroke-width="2" opacity="0">'
                 '<animate attributeName="r" values="5;22" dur="1s" begin="%.2fs;%.2fs" repeatCount="indefinite" fill="freeze"/>'
                 '<animate attributeName="opacity" values=".8;0" dur="1s" begin="%.2fs" repeatCount="indefinite"/></circle>'
                 % (x, y, t, t + 5, t))
    o.append('</g></svg>')
    return ''.join(o)


def diagram_meshtastic():
    """Every node repeats what it hears, a few hops out."""
    nodes = [(80, 120), (160, 70), (170, 165), (250, 110), (260, 195), (330, 60), (345, 140), (420, 95), (430, 185), (480, 130)]
    links = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(3,6),(4,6),(5,7),(6,7),(6,8),(7,9),(8,9)]
    hop = {0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5}
    o = ['<svg class="diagram" viewBox="0 0 520 240" role="img" aria-label="A message spreads outward from one radio as each neighbour repeats it, a few hops in every direction">']
    for a, b in links:
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#22324D" stroke-width="1.2"/>' % (*nodes[a], *nodes[b]))
    for i, (x, y) in enumerate(nodes):
        o.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x, y, 'var(--meshtastic)' if i == 0 else 'var(--muted)'))
    o.append('<text x="80" y="142" text-anchor="middle" font-size="10">you</text>')
    o.append('<g class="anim">')
    # the message ripples: hop n lights up at n seconds, then everything fades and it repeats
    for i, (x, y) in enumerate(nodes):
        if i == 0: continue
        t = hop[i] * 0.75
        o.append('<circle cx="%d" cy="%d" r="5" fill="var(--meshtastic)" opacity="0">'
                 '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.7;1" dur="6s" begin="%.2fs" repeatCount="indefinite"/></circle>' % (x, y, t))
    # a packet crosses every link, leaving when its sender has the message and
    # arriving as the receiver lights. Several are in flight at once, and some
    # nodes are reached twice — which is what flooding actually does.
    CYCLE, STEP = 6.0, 0.75
    for a, b in links:
        if hop[a] > hop[b]: a, b = b, a
        t0 = hop[a] * STEP; t1 = t0 + STEP
        k0, k1 = t0 / CYCLE, t1 / CYCLE
        if t0 == 0:
            kp, kt = '0;1;1', '0;%.4f;1' % k1
            ov, ot = '1;1;0;0', '0;%.4f;%.4f;1' % (k1, k1 + 0.004)
        else:
            kp, kt = '0;0;1;1', '0;%.4f;%.4f;1' % (k0, k1)
            ov, ot = '0;0;1;1;0;0', '0;%.4f;%.4f;%.4f;%.4f;1' % (k0 - 0.002, k0, k1, k1 + 0.004)
        o.append('<circle r="3.4" fill="var(--meshtastic)" stroke="#0A1424" stroke-width="1" paint-order="stroke" opacity="0">'
                 '<animateMotion dur="%.1fs" repeatCount="indefinite" calcMode="linear" keyPoints="%s" keyTimes="%s" path="M%d %d L%d %d"/>'
                 '<animate attributeName="opacity" dur="%.1fs" repeatCount="indefinite" values="%s" keyTimes="%s"/></circle>'
                 % (CYCLE, kp, kt, *nodes[a], *nodes[b], CYCLE, ov, ot))
    o.append('<circle cx="80" cy="120" r="5" fill="none" stroke="var(--meshtastic)" stroke-width="1.5">'
             '<animate attributeName="r" values="5;70" dur="1.6s" begin="0s;6s;12s;18s;24s;30s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".8;0" dur="1.6s" begin="0s;6s;12s;18s;24s;30s" repeatCount="indefinite"/></circle>')
    o.append('</g></svg>')
    return ''.join(o)


def diagram_reticulum():
    """Encrypted end to end, over whatever bearer is there — and there are many.

    A graph rather than a line: two routes from you to them, crossing seven
    different bearers, including the two meshes on this page (RNS runs over
    both, via ScotMesh's own forks). Two sealed packets take different routes
    at once, which is the point: the network finds a way, and does not care
    which links it used.
    """
    N = {'you': (36, 136), 'A': (150, 78), 'D': (150, 196), 'S': (258, 24), 'B': (330, 78),
         'E': (290, 204), 'C': (400, 136), 'them': (484, 136)}
    # edge: (from, to, bearer, style)
    E = [('you', 'A', 'LoRa', 'wave'), ('you', 'D', 'MeshCore', 'dash6'), ('A', 'S', 'satellite', 'dot'),
         ('S', 'B', 'satellite', 'dot'), ('A', 'B', 'Wi-Fi', 'dash2'), ('D', 'E', 'Meshtastic', 'dash6'),
         ('B', 'C', 'internet', 'solid'), ('E', 'C', 'internet', 'solid'), ('C', 'them', 'I2P', 'dash4'),
         ('E', 'them', 'radio', 'wave')]
    dash = {'wave': '', 'solid': '', 'dot': ' stroke-dasharray="2 4"', 'dash2': ' stroke-dasharray="2 2"',
            'dash4': ' stroke-dasharray="5 4"', 'dash6': ' stroke-dasharray="8 3"'}
    def wave(x1, y1, x2, y2):
        # a LoRa link drawn as a wave along the straight line between the nodes
        import math
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
        n = max(3, int(L / 22)); d = 'M%.1f %.1f' % (x1, y1)
        for i in range(1, n + 1):
            t = i / n; px, py = x1 + dx * t, y1 + dy * t
            cx, cy = x1 + dx * (t - 0.5 / n), y1 + dy * (t - 0.5 / n)
            amp = 6 if i % 2 else -6
            d += ' Q%.1f %.1f %.1f %.1f' % (cx + nx * amp, cy + ny * amp, px, py)
        return d
    o = ['<svg class="diagram" viewBox="0 0 520 250" role="img" aria-label="Two encrypted messages cross a small network from you to them by different routes, over LoRa, MeshCore, Meshtastic, satellite, Wi-Fi, the internet and I2P">']
    for f, t, name, st in E:
        (x1, y1), (x2, y2) = N[f], N[t]
        if st == 'wave':
            o.append('<path d="%s" fill="none" stroke="var(--reticulum)" stroke-opacity=".45" stroke-width="1.5"/>' % wave(x1, y1, x2, y2))
        else:
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--reticulum)" stroke-opacity=".45" stroke-width="1.5"%s/>' % (x1, y1, x2, y2, dash[st]))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # nudge labels off the line
        off = -7 if (f, t) not in (('you', 'D'), ('D', 'E'), ('E', 'them')) else 13   # E->C stays above its line, clear of 'radio'
        o.append('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="9.5">%s</text>' % (mx, my + off, name))
    # the satellite
    sx, sy = N['S']
    o.append('<g transform="translate(%d %d)"><rect x="-5" y="-5" width="10" height="10" fill="#101C30" stroke="var(--reticulum)" stroke-width="1.4"/>'
             '<line x1="-16" y1="0" x2="-6" y2="0" stroke="var(--reticulum)" stroke-width="3"/><line x1="6" y1="0" x2="16" y2="0" stroke="var(--reticulum)" stroke-width="3"/></g>' % (sx, sy))
    for k in ('A', 'B', 'C', 'D', 'E'):
        x, y = N[k]
        o.append('<circle cx="%d" cy="%d" r="8" fill="#101C30" stroke="var(--reticulum)" stroke-width="1.6"/>' % (x, y))
    for k, lbl in (('you', 'you'), ('them', 'them')):
        x, y = N[k]
        o.append('<rect x="%d" y="%d" width="22" height="16" rx="3" fill="#101C30" stroke="var(--muted)"/>' % (x - 11, y - 8))
        o.append('<text x="%d" y="%d" text-anchor="middle" font-size="10">%s</text>' % (x, y + 24, lbl))
    o.append('<text x="400" y="118" text-anchor="middle" font-size="9.5">transport node</text>')
    # two routes, two sealed packets, offset so they are never in step
    r1 = 'M36 136 L150 78 Q258 24 330 78 L400 136 L484 136'
    r2 = 'M36 136 L150 196 L290 204 L484 136'
    o.append('<defs><path id="rns-r1" d="%s"/><path id="rns-r2" d="%s"/></defs>' % (r1, r2))
    o.append('<g class="anim">')
    for rid, dur, begin in (('rns-r1', 7.0, 0.0), ('rns-r2', 6.2, 3.1)):
        for r, extra in ((8, ' fill="none" stroke="var(--reticulum)" stroke-width="1.6"'), (3.2, ' fill="var(--reticulum)"')):
            o.append('<circle r="%s"%s><animateMotion dur="%.1fs" begin="%.1fs" repeatCount="indefinite"><mpath href="#%s"/></animateMotion></circle>' % (r, extra, dur, begin, rid))
    o.append('</g></svg>')
    return ''.join(o)



EXPLAIN = [
    ('meshcore', 'MeshCore', 'var(--meshcore)', 'Repeaters carry the message', diagram_meshcore,
     ['Long-range LoRa messaging on cheap radios. What makes it MeshCore is the <b>repeater</b>: '
      'a radio left on a hill, a mast or a roof whose only job is to pass messages on.',
      'Your radio just has to reach one repeater. From there the message hops repeater to '
      'repeater across the country, and each hop is recorded, so the route it took can be seen.'],
     ['Fixed repeaters on high ground do the carrying', 'Every hop is recorded in the packet', 'Reach depends on where the repeaters are']),
    ('meshtastic', 'Meshtastic', 'var(--meshtastic)', 'Every radio repeats what it hears', diagram_meshtastic,
     ['Long-range LoRa messaging with an app on your phone. There is no special infrastructure: '
      '<b>every radio is also a relay</b>, and repeats what it hears to everyone in range.',
      'A message ripples outward a few hops in every direction and stops. The more radios there '
      'are in an area, the further a message can travel.'],
     ['No dedicated infrastructure needed', 'A message floods a few hops, then stops', 'Reach depends on how many radios are about']),
    ('reticulum', 'Reticulum', 'var(--reticulum)', 'Any link will do', diagram_reticulum,
     ['Not tied to any one radio, or to radio at all: a way of moving <b>encrypted</b> messages over whatever is '
      'available — LoRa, the internet, I2P, satellite, even MeshCore or Meshtastic — without caring which.',
      'A message is sealed at your end and opened only at theirs. Everything in between, '
      'including our transport node, carries it without being able to read it.'],
     ['Encrypted end to end, by default', 'Runs over LoRa, the internet, I2P, satellite — even the other two meshes', 'No accounts, no central authority']),
]


def explainers():
    out = []
    for i, (key, name, tint, title, draw, paras, facts) in enumerate(EXPLAIN):
        words = ''.join('<p>%s</p>' % t for t in paras)
        fl = ''.join('<li>%s</li>' % f for f in facts)
        out.append(
            '<section id="%s"%s><div class="wrap sec" style="--tint: %s">'
            '<div class="sec-head"><span class="rule">%s</span><h2>%s</h2></div>'
            '<div class="explain%s"><div class="words">%s<ul class="facts">%s</ul></div><div>%s</div></div>'
            '</div></section>'
            % (key, ' class="alt"' if i % 2 else '', tint, name, title, ' flip' if i % 2 else '', words, fl, draw()))
    return ''.join(out)



BODY = '''
<header class="nav">
  <div class="wrap">
    <a class="lockup" href="#top" aria-label="ScotMesh — home">__SM_DARK____SM_LIGHT__</a>
    <nav aria-label="Primary">
      <a href="https://meshcore.scotmesh.net/" data-net="meshcore">MeshCore</a>
      <a href="https://meshtastic.scotmesh.net/" data-net="meshtastic">Meshtastic</a>
      <a href="https://rns.scotmesh.net/" data-net="reticulum">Reticulum</a>
      <a href="https://scotmesh.uk/" target="_blank" rel="noopener">Forum</a>
      <a href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Discord</a>
      <button type="button" id="theme-toggle" class="theme-toggle" aria-label="Switch to light theme" title="Switch theme">
        <svg class="t-dark" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.2 4.2l1.6 1.6M18.2 18.2l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.2 19.8l1.6-1.6M18.2 5.8l1.6-1.6"/></svg>
        <svg class="t-light" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4 8.3 8.3 0 1 0 20 14.5Z"/></svg>
      </button>
    </nav>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Three meshes across Scotland, one community.</h1>
      <p class="lede">
        ScotMesh people run three separate radio networks. They do not talk to each
        other, and you do not have to pick just one — but you do have to start
        somewhere. Here is what each is for, and what all three are doing right now.
      </p>
      <div class="hero-links">
        <a class="btn btn-primary" href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Join the community</a>
        <a class="btn" href="https://scotmesh.uk/" target="_blank" rel="noopener">Forum</a>
      </div>
    </div>
    <div>
      __MAP__
      <div class="legend">
        <span><i style="background:var(--meshcore)"></i>MeshCore</span>
        <span><i style="background:var(--meshtastic)"></i>Meshtastic</span>
        <span><i style="background:var(--reticulum)"></i>Reticulum gateway</span>
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="nets">
      __NETS__
      <p class="live-note">
        Node positions on the map are real; the moving traffic is illustrative, shaped like each network's behaviour. Figures come from each network's own tools, refreshed every few minutes. They are not
        the same measure — a MeshCore repeater, a Meshtastic node and a Reticulum client are
        different things — so read them as signs of life, not a league table.
      </p>
    </div>
  </div>
</section>

__TOOLS__
<script>
  /* MeshCore and Meshtastic are equals here, so neither gets to be permanently
     first: the pair is swapped at random on each load. Reticulum stays last —
     it is the odd one out, being the only one you can join with no radio.
     This runs during parse, before first paint, so nothing visibly reorders. */
  (function () {
    if (!(Math.random() < 0.5)) return;
    var swap = function (a, b) {
      if (a && b && a.parentNode) a.parentNode.insertBefore(b, a);
    };
    swap(document.querySelector('.net[data-net="meshcore"]'),
         document.querySelector('.net[data-net="meshtastic"]'));
    swap(document.getElementById('meshcore'), document.getElementById('meshtastic'));
    swap(document.querySelector('.nav nav a[data-net="meshcore"]'),
         document.querySelector('.nav nav a[data-net="meshtastic"]'));
    /* On the mark the two top corners are positions, not ranks: exchange the
       tint and the label between them, and leave the geometry alone. */
    var mc = document.querySelector('.corner[data-net="meshcore"]');
    var mt = document.querySelector('.corner[data-net="meshtastic"]');
    if (mc && mt) {
      var t = mc.style.getPropertyValue('--tint');
      mc.style.setProperty('--tint', mt.style.getPropertyValue('--tint'));
      mt.style.setProperty('--tint', t);
      var ta = mc.querySelector('text'), tb = mt.querySelector('text');
      var tx = ta.textContent; ta.textContent = tb.textContent; tb.textContent = tx;
    }
    /* The striped background belongs to the position, not the section, so it
       has to be reapplied once the order has changed. */
    var secs = document.querySelectorAll('main section[id]');
    for (var i = 0; i < secs.length; i++) {
      secs[i].classList.toggle('alt', i % 2 === 1);
      /* the diagram alternates sides by position too, not by network */
      var ex = secs[i].querySelector('.explain');
      if (ex) ex.classList.toggle('flip', i % 2 === 1);
    }
  })();
</script>

</main>

<footer>
  <div class="wrap foot-grid">
    <div>
      <a class="lockup-scotmesh" href="https://scotmesh.uk/" aria-label="ScotMesh main site">__SM_DARK____SM_LIGHT__</a>
      <p style="margin:12px 0 0; max-width:36ch">
        Community-run radio networks across Scotland. The forum, the guides and the people are on
        the main site; this page is the live tools and infrastructure behind them.
      </p>
    </div>
    <div>
      <span class="lbl">Community</span>
      <ul>
        <li><a href="https://scotmesh.uk/" target="_blank" rel="noopener">Main site &amp; forum</a></li>
        <li><a href="https://wiki.scotmesh.uk/" target="_blank" rel="noopener">Community wiki</a></li>
        <li><a href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Discord</a></li>
        <li><a href="https://www.facebook.com/groups/26406719398968062" target="_blank" rel="noopener">Facebook group</a></li>
      </ul>
    </div>
    <div>
      <span class="lbl">Networks</span>
      <ul>
        <li><a href="https://meshcore.scotmesh.net/">MeshCore in Scotland</a></li>
        <li><a href="https://meshtastic.scotmesh.net/">Meshtastic in Scotland</a></li>
        <li><a href="https://rns.scotmesh.net/">Reticulum in Scotland</a></li>
      </ul>
    </div>
    <div class="foot-bar">
      <span>ScotMesh &middot; EDI Region &middot; hosted by <a href="https://www.oarc.uk/" target="_blank" rel="noopener">OARC</a></span>
      <span class="mono">Service administration by Alex (MM7ROQ)</span>
    </div>
  </div>
</footer>

<script>
  (function () {
    var root = document.documentElement;
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    function current() {
      var set = root.getAttribute('data-theme');
      if (set === 'light' || set === 'dark') return set;
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    function label() {
      btn.setAttribute('aria-label', current() === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    }
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('scotmesh-theme', next); } catch (e) {}
      label();
    });
    label();
  })();
</script>
'''

body = BODY
for token, value in (('__SM_DARK__', A['sm_dark']), ('__SM_LIGHT__', A['sm_light']),
                     ('__MAP__', scotmap()),
                     ('__NETS__', net_cards()), ('__TOOLS__', explainers())):
    assert token in body, token
    body = body.replace(token, value)

pathlib.Path('page.html').write_text(HEAD + body)
print('written %.0f KB' % (len(HEAD + body) / 1024))
