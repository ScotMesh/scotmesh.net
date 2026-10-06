/* ScotMesh news, rendered in the browser.
 *
 * A post is a Markdown file with YAML-ish front matter under /news/posts/.
 * This script renders the index from posts.json and a post from its own file,
 * so publishing is adding a Markdown file and one line to the list. The small
 * HTML stub each post ships with exists only for its title and link preview:
 * the services that unfurl a link do not run scripts.
 */
(function () {
  'use strict';

  var TINT = { meshcore: 'var(--meshcore)', meshtastic: 'var(--meshtastic)',
               reticulum: 'var(--reticulum)', all: 'var(--saltire)' };
  var LABEL = { meshcore: 'MeshCore', meshtastic: 'Meshtastic',
                reticulum: 'Reticulum', all: 'All networks' };
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];

  /* ---- front matter ---------------------------------------------------- */

  /* The subset a post needs: scalars, one level of nesting, and inline lists.
   * Anything cleverer belongs in the body, not the header. */
  function frontMatter(text) {
    if (text.slice(0, 3) !== '---') return { meta: {}, body: text };
    var end = text.indexOf('\n---', 3);
    if (end < 0) return { meta: {}, body: text };
    var head = text.slice(4, end), body = text.slice(end + 4).replace(/^\s*\n/, '');
    var meta = {}, parent = null;
    head.split('\n').forEach(function (line) {
      if (!line.trim() || line.trim()[0] === '#') return;
      var indented = /^\s+\S/.test(line);
      var m = line.match(/^\s*([A-Za-z0-9_-]+):\s*(.*)$/);
      if (!m) return;
      var key = m[1], val = m[2].trim();
      if (val === '') {                       // a block of its own
        if (!indented) { meta[key] = {}; parent = meta[key]; }
        return;
      }
      val = val.replace(/^["']|["']$/g, '');
      if (val[0] === '[') {
        val = val.slice(1, -1).split(',').map(function (s) {
          return s.trim().replace(/^["']|["']$/g, '');
        }).filter(Boolean);
      }
      (indented && parent ? parent : meta)[key] = val;
      if (!indented) parent = null;
    });
    return { meta: meta, body: body };
  }

  /* ---- markdown -------------------------------------------------------- */

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function inline(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>');
  }

  function table(rows) {
    var head = rows[0], body = rows.slice(2);
    var cells = function (r) { return r.replace(/^\||\|$/g, '').split('|'); };
    var th = cells(head).map(function (c) { return '<th>' + inline(c.trim()) + '</th>'; }).join('');
    var tr = body.map(function (r) {
      return '<tr>' + cells(r).map(function (c, i) {
        var t = c.trim();
        return '<td' + (i ? ' class="mono"' : '') + '>' + inline(t) + '</td>';
      }).join('') + '</tr>';
    }).join('');
    return '<div class="tablewrap"><table><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>';
  }

  /* Enough Markdown for an announcement: headings, paragraphs, fenced code,
   * tables, lists, rules, images and raw HTML for a diagram. */
  function markdown(src) {
    var lines = src.replace(/\r\n/g, '\n').split('\n');
    var out = [], i = 0;
    while (i < lines.length) {
      var line = lines[i];

      if (!line.trim()) { i++; continue; }

      if (line.slice(0, 3) === '```') {
        var buf = [];
        i++;
        while (i < lines.length && lines[i].slice(0, 3) !== '```') buf.push(lines[i++]);
        i++;
        out.push('<pre class="cli" tabindex="0">' + esc(buf.join('\n')) + '</pre>');
        continue;
      }

      if (line[0] === '<') {                  // raw block, straight through
        var raw = [];
        while (i < lines.length && lines[i].trim()) raw.push(lines[i++]);
        out.push(raw.join('\n'));
        continue;
      }

      var h = line.match(/^(#{2,3})\s+(.*)$/);
      if (h) { out.push('<h' + h[1].length + '>' + inline(h[2]) + '</h' + h[1].length + '>'); i++; continue; }

      if (/^---+$/.test(line.trim())) { out.push('<hr>'); i++; continue; }

      if (line.indexOf('|') === 0) {
        var rows = [];
        while (i < lines.length && lines[i].indexOf('|') === 0) rows.push(lines[i++]);
        out.push(rows.length > 2 ? table(rows) : '');
        continue;
      }

      var img = line.match(/^!\[([^\]]*)\]\(([^)\s]+)\)\s*$/);
      if (img) {
        out.push('<figure><img src="' + img[2] + '" alt="' + esc(img[1]) + '">' +
                 (img[1] ? '<figcaption>' + inline(img[1]) + '</figcaption>' : '') + '</figure>');
        i++;
        continue;
      }

      if (/^[-*]\s+/.test(line)) {
        var items = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i])) items.push(lines[i++].replace(/^[-*]\s+/, ''));
        out.push('<ul>' + items.map(function (t) { return '<li>' + inline(t) + '</li>'; }).join('') + '</ul>');
        continue;
      }

      var para = [];
      while (i < lines.length && lines[i].trim() && lines[i][0] !== '<' && !/^(#{2,3}\s|```|\||[-*]\s)/.test(lines[i])) {
        para.push(lines[i++]);
      }
      out.push('<p>' + inline(para.join(' ')) + '</p>');
    }
    return out.join('\n');
  }

  /* ---- covers ---------------------------------------------------------- */

  /* A post with no banner of its own gets one of six, chosen from its slug so
   * it never changes once published, and tinted to its network. */
  function pick(slug) {
    var n = 0;
    for (var i = 0; i < slug.length; i++) n = (n * 31 + slug.charCodeAt(i)) % 1000003;
    return n % 6;
  }

  var W = 1600, H = 900;

  function hills(seed, bases) {
    return bases.map(function (b, layer) {
      var pts = [];
      for (var k = 0; k <= 12; k++) {
        var x = k * W / 12;
        var y = H * b[1] - Math.sin(k * 0.8 + seed + layer) * H * 0.07 - Math.cos(k * 0.45 + seed) * H * 0.035;
        pts.push(x.toFixed(0) + ',' + y.toFixed(0));
      }
      return '<polygon points="0,' + H + ' ' + pts.join(' ') + ' ' + W + ',' + H +
             '" fill="var(--night)" fill-opacity="' + b[0] + '"/>';
    }).join('');
  }

  function mast(x, ground, height, tint, w) {
    var top = ground - height;
    return '<g stroke="var(--night)" stroke-width="' + w + '" fill="none" stroke-linecap="round">' +
      '<line x1="' + x.toFixed(0) + '" y1="' + ground.toFixed(0) + '" x2="' + x.toFixed(0) + '" y2="' + top.toFixed(0) + '"/>' +
      '<line x1="' + (x - height * 0.33).toFixed(0) + '" y1="' + ground.toFixed(0) + '" x2="' + x.toFixed(0) + '" y2="' + (top + height * 0.42).toFixed(0) + '"/>' +
      '<line x1="' + (x + height * 0.33).toFixed(0) + '" y1="' + ground.toFixed(0) + '" x2="' + x.toFixed(0) + '" y2="' + (top + height * 0.42).toFixed(0) + '"/>' +
      '</g><circle cx="' + x.toFixed(0) + '" cy="' + top.toFixed(0) + '" r="9" fill="' + tint + '"/>';
  }

  function dots(tint, n, seed) {
    var out = '';
    for (var i = 0; i < n; i++) {
      out += '<circle cx="' + ((i * 211 + seed * 97) % W) + '" cy="' + (H * 0.1 + (i * 71 + seed * 31) % (H * 0.3)).toFixed(0) +
             '" r="' + (2 + (i % 3) * 0.7).toFixed(1) + '" fill="' + tint + '" fill-opacity=".5"/>';
    }
    return out;
  }

  var ALT = ['A mast on a hill ridge at dusk',
             'Two masts on facing hills with the hop drawn between them',
             'A trig pillar on a summit',
             'A rooftop antenna above a town skyline',
             'A mast on the far shore across open water',
             'A mesh of nodes over low hills'];

  function cover(slug, network) {
    var tint = TINT[network] || TINT.all;
    var v = pick(slug);
    var id = 'cv' + v + slug.length + (network || '').length;
    var body = '';
    if (v === 0) {
      body = dots(tint, 9, 1) + hills(1.0, [[.36, .62], [.58, .75], [1, .88]]) +
        mast(W * 0.68, H * 0.88, H * 0.56, tint, 8) +
        '<rect x="' + (W * 0.68 + 14).toFixed(0) + '" y="' + (H * 0.34).toFixed(0) + '" width="84" height="52" rx="5" fill="var(--night)"/>';
    } else if (v === 1) {
      body = dots(tint, 7, 4) + hills(2.4, [[.32, .60], [.58, .74], [1, .87]]) +
        mast(W * 0.22, H * 0.80, H * 0.34, tint, 6) + mast(W * 0.78, H * 0.87, H * 0.52, tint, 7) +
        '<path d="M' + (W * 0.22).toFixed(0) + ' ' + (H * 0.46).toFixed(0) + ' Q' + (W * 0.5).toFixed(0) + ' ' +
        (H * 0.16).toFixed(0) + ' ' + (W * 0.78).toFixed(0) + ' ' + (H * 0.35).toFixed(0) +
        '" fill="none" stroke="' + tint + '" stroke-width="4" stroke-opacity=".65" stroke-dasharray="14 12"/>';
    } else if (v === 2) {
      var px = W * 0.30, pg = H * 0.72;
      body = dots(tint, 11, 7) + hills(0.3, [[.30, .58], [.55, .72], [1, .86]]) +
        '<path d="M' + (px - 34).toFixed(0) + ' ' + pg.toFixed(0) + ' L' + (px - 26).toFixed(0) + ' ' + (pg - 118).toFixed(0) +
        ' L' + (px + 26).toFixed(0) + ' ' + (pg - 118).toFixed(0) + ' L' + (px + 34).toFixed(0) + ' ' + pg.toFixed(0) +
        ' Z" fill="var(--night)"/><rect x="' + (px - 36).toFixed(0) + '" y="' + (pg - 132).toFixed(0) +
        '" width="72" height="16" rx="3" fill="var(--night)"/><circle cx="' + px.toFixed(0) + '" cy="' + (pg - 150).toFixed(0) +
        '" r="8" fill="' + tint + '"/>';
    } else if (v === 3) {
      body = dots(tint, 6, 2) + hills(3.1, [[.28, .56], [.5, .68]]);
      [[.04, .17, .22], [.22, .13, .30], [.36, .20, .25], [.57, .15, .34], [.73, .12, .27], [.86, .16, .31]]
        .forEach(function (r, i) {
          body += '<rect x="' + (W * r[0]).toFixed(0) + '" y="' + (H * (1 - r[2])).toFixed(0) +
                  '" width="' + (W * r[1]).toFixed(0) + '" height="' + (H * r[2]).toFixed(0) + '" fill="var(--night)"/>';
          if (i === 3) {
            var cx = W * (r[0] + r[1] / 2), cy = H * (1 - r[2]);
            body += '<g stroke="var(--night)" stroke-width="6" stroke-linecap="round">' +
              '<line x1="' + cx.toFixed(0) + '" y1="' + cy.toFixed(0) + '" x2="' + cx.toFixed(0) + '" y2="' + (cy - 130).toFixed(0) + '"/>' +
              '<line x1="' + (cx - 42).toFixed(0) + '" y1="' + (cy - 74).toFixed(0) + '" x2="' + (cx + 42).toFixed(0) + '" y2="' + (cy - 74).toFixed(0) + '"/>' +
              '<line x1="' + (cx - 32).toFixed(0) + '" y1="' + (cy - 100).toFixed(0) + '" x2="' + (cx + 32).toFixed(0) + '" y2="' + (cy - 100).toFixed(0) + '"/></g>' +
              '<circle cx="' + cx.toFixed(0) + '" cy="' + (cy - 130).toFixed(0) + '" r="8" fill="' + tint + '"/>';
          }
        });
    } else if (v === 4) {
      body = dots(tint, 8, 5) + hills(1.7, [[.30, .52], [.52, .62]]) +
        '<rect x="0" y="' + (H * 0.66).toFixed(0) + '" width="' + W + '" height="' + (H * 0.34).toFixed(0) +
        '" fill="var(--night)" fill-opacity=".82"/>' + mast(W * 0.64, H * 0.66, H * 0.34, tint, 6);
      for (var k = 0; k < 5; k++) {
        var yy = H * (0.72 + k * 0.055);
        body += '<line x1="' + (W * (0.30 + k * 0.04)).toFixed(0) + '" y1="' + yy.toFixed(0) + '" x2="' +
                (W * (0.74 - k * 0.03)).toFixed(0) + '" y2="' + yy.toFixed(0) + '" stroke="' + tint +
                '" stroke-opacity="' + (0.30 - k * 0.05).toFixed(2) + '" stroke-width="3"/>';
      }
    } else {
      body = hills(4.2, [[.46, .68], [1, .80]]);
      var pts = [];
      for (var n = 0; n < 9; n++) pts.push([W * (0.08 + 0.105 * n), H * (0.20 + 0.11 * Math.sin(n * 1.3 + 2))]);
      [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[0,3],[2,5],[4,7],[1,6]].forEach(function (e) {
        body += '<line x1="' + pts[e[0]][0].toFixed(0) + '" y1="' + pts[e[0]][1].toFixed(0) + '" x2="' +
                pts[e[1]][0].toFixed(0) + '" y2="' + pts[e[1]][1].toFixed(0) + '" stroke="' + tint +
                '" stroke-opacity=".34" stroke-width="2.5"/>';
      });
      pts.forEach(function (pt, n) {
        body += '<circle cx="' + pt[0].toFixed(0) + '" cy="' + pt[1].toFixed(0) + '" r="' + (n % 3 ? 7 : 10) +
                '" fill="' + tint + '"/>';
      });
    }
    return '<svg class="cover" viewBox="0 0 ' + W + ' ' + H + '" role="img" preserveAspectRatio="xMidYMid slice" aria-label="' +
      ALT[v] + '"><defs><linearGradient id="' + id + '" x1="0" y1="0" x2="0.25" y2="1">' +
      '<stop offset="0" stop-color="' + tint + '" stop-opacity=".58"/>' +
      '<stop offset="1" stop-color="var(--night)" stop-opacity="' + (v === 5 ? '.70' : '.96') + '"/></linearGradient></defs>' +
      '<rect width="' + W + '" height="' + H + '" fill="var(--well)"/>' +
      '<rect width="' + W + '" height="' + H + '" fill="url(#' + id + ')"/>' + body + '</svg>';
  }

  /* ---- rendering ------------------------------------------------------- */

  function when(iso, long) {
    var d = new Date(iso);
    if (isNaN(d)) return iso;
    var day = d.getUTCDate(), mon = MONTHS[d.getUTCMonth()], yr = d.getUTCFullYear();
    if (!long) return day + ' ' + mon.slice(0, 3) + ' ' + yr;
    var hh = ('0' + d.getUTCHours()).slice(-2), mm = ('0' + d.getUTCMinutes()).slice(-2);
    return day + ' ' + mon + ' ' + yr + ', ' + hh + ':' + mm;
  }

  function art(meta, slug) {
    if (meta.banner && meta.banner.src) {
      return '<img class="cover" src="/news/posts/' + slug + '/' + meta.banner.src + '" alt="' +
             (meta.banner.alt || '').replace(/"/g, '&quot;') + '">';
    }
    return cover(slug, meta.network);
  }

  function eyebrow(meta, long) {
    return '<div class="eyebrow"><span class="pip"></span> ' + (LABEL[meta.network] || 'ScotMesh') +
           ' · ' + when(meta.date, long) + (long && meta.author ? ' · ' + meta.author : '') + '</div>';
  }

  function renderIndex(host, posts) {
    host.innerHTML = posts.map(function (p) {
      return '<a class="post-card tint-' + (p.meta.network || 'all') + '" href="/news/' + p.slug + '/">' +
        art(p.meta, p.slug) + '<div class="in">' + eyebrow(p.meta) +
        '<h2>' + inline(p.meta.title || p.slug) + '</h2>' +
        '<p>' + inline(p.meta.summary || '') + '</p>' +
        '<div class="byline">' + (p.meta.author || '') + '</div></div></a>';
    }).join('');
  }

  function renderPost(host, meta, body, slug) {
    host.className = 'article tint-' + (meta.network || 'all');
    host.innerHTML = '<a class="back" href="/news/">← News</a>' +
      '<figure class="cover-fig">' + art(meta, slug) + '</figure>' +
      (meta.banner && meta.banner.credit ? '<p class="credit">' + inline(meta.banner.credit) + '</p>' : '') +
      '<header class="head">' + eyebrow(meta, true) +
      '<h1>' + inline(meta.title || slug) + '</h1>' +
      '<p class="lead">' + inline(meta.summary || '') + '</p></header>' + markdown(body) +
      (meta.tags && meta.tags.length
        ? '<hr><div class="tags">' + meta.tags.map(function (t) { return '<span>' + t + '</span>'; }).join('') + '</div>'
        : '');
    if (meta.title) document.title = meta.title.replace(/<[^>]+>/g, '') + ' — ScotMesh';
  }

  function get(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error(url + ' ' + r.status);
      return r.text();
    });
  }

  function start() {
    var index = document.getElementById('news-list');
    var post = document.getElementById('news-post');

    if (index) {
      get('/news/posts.json').then(function (t) {
        var slugs = JSON.parse(t);
        return Promise.all(slugs.map(function (s) {
          return get('/news/posts/' + s + '/index.md').then(function (raw) {
            var fm = frontMatter(raw);
            return { slug: s, meta: fm.meta };
          });
        }));
      }).then(function (posts) {
        posts.sort(function (a, b) { return (b.meta.date || '').localeCompare(a.meta.date || ''); });
        renderIndex(index, posts);
      }).catch(function (e) {
        index.innerHTML = '<p class="byline">The news list could not be loaded. ' + esc(String(e.message)) + '</p>';
      });
      return;
    }

    if (post) {
      var slug = post.getAttribute('data-post');
      get('/news/posts/' + slug + '/index.md').then(function (raw) {
        var fm = frontMatter(raw);
        renderPost(post, fm.meta, fm.body, slug);
      }).catch(function (e) {
        post.innerHTML = '<p class="byline">This post could not be loaded. ' + esc(String(e.message)) + '</p>';
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
