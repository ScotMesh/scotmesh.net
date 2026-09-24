![ScotMesh](https://raw.githubusercontent.com/ScotMesh/branding/main/social/readme-header.png)

# scotmesh.net

Source for [scotmesh.net](https://scotmesh.net/), the front door to the ScotMesh
community networks: MeshCore, Meshtastic and Reticulum. Static HTML served by
nginx.

## Layout

```
index.html          the page as served — generated, do not hand-edit
app.js              replaces the shipped card figures with live ones
build/build.py      the page's content, design, map and diagrams; writes build/page.html
build/mksite.py     wraps build/page.html as index.html
build/site-app.js   source of app.js
build/assets.json   the brand marks and lockups, inlined into the page
build/points.json   node positions for the map, projected to page space
build/coast.txt, inset.txt, land-path.txt   Scotland's outline, Shetland inset, land fill
fonts/, *.svg, *.png   served as-is, not generated
```

`build.py` holds the copy, the three network cards, the animated map and the
three explainer diagrams, and writes `build/page.html`. `mksite.py` turns that
into `index.html`: it adds the document skeleton, swaps Google Fonts for the
self-hosted IBM Plex in `fonts/`, and sets the title, description, canonical,
og tags and icons.

```bash
cd build && python3 build.py && python3 mksite.py
```

That reproduces `index.html` and `app.js` byte for byte, so a rebuild with no
source change is a no-op in `git status`.

## Deploying

Copy the two generated files, `index.html` and `app.js`, into the site's web
root. The fonts, icons, logos and `og.png` only need copying when they change.
Copy over the top rather than mirroring with delete: other sites load
`favicon.svg` and the `logo*.png` files straight from scotmesh.net.

Nothing is built on the server.

## Live data

Each card ships with the last known figures baked in, so the page reads
correctly before `app.js` runs and if a feed is down. `app.js` then reads the
three networks' own public JSON documents cross-origin and updates each card in
place:

- `https://meshcore.scotmesh.net/api/scotland` — repeaters, packets today, observers
- `https://meshtastic.scotmesh.net/api/summary` — nodes heard, routers, packets today
- `https://rns.scotmesh.net/status.json` — clients, peers linked, transport uptime

A feed that fails leaves its own card's shipped figures alone. All three serve
`Access-Control-Allow-Origin: *`; keep that if you move them.

## Map

The map draws real node positions from `build/points.json`, refreshed by hand
from the same three feeds. The traffic on it is illustrative, shaped like each
network's actual behaviour: MeshCore packets step repeater to repeater,
Meshtastic packets flood outward from a node, and Reticulum announces arrive at
the gateway from off the map. Nothing on the map is live packet data.

## Design

The same system as the three network sites: brand tokens, IBM Plex, and the
marks and lockups from [ScotMesh/branding](https://github.com/ScotMesh/branding).
This is the one page where all three network tints appear together, so they are
equalised in lightness and chroma and the page favours none of them. The order
of the MeshCore and Meshtastic cards, sections and nav links is shuffled on each
load for the same reason.
