// scotmesh.net — replace the shipped card figures with live ones.
//
// The page ships with the last known numbers baked in, so it reads correctly
// before this runs and if a feed is down. Each network's own site publishes a
// small JSON document; we read all three cross-origin and update the card for
// that network only. A feed that fails leaves its card's shipped figures alone.
(function () {
  'use strict';

  var EVERY = 5 * 60 * 1000;

  function set(net, key, value) {
    if (typeof value !== 'string' && typeof value !== 'number') return;
    if (value !== value) return;
    var el = document.querySelector('.net[data-net="' + net + '"] [data-vital="' + key + '"]');
    if (el) el.textContent = String(value);
  }

  function days(seconds) {
    var s = Number(seconds);
    if (!isFinite(s) || s < 0) return null;
    if (s < 3600) return Math.floor(s / 60) + 'm';
    if (s < 86400) return Math.floor(s / 3600) + 'h';
    return Math.floor(s / 86400) + 'd';
  }

  function get(url, then) {
    fetch(url, { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(then)
      .catch(function () { /* keep the shipped figures */ });
  }

  function refresh() {
    get('https://meshcore.scotmesh.net/api/scotland', function (d) {
      set('meshcore', 'repeaters', d.repeaters);
      set('meshcore', 'packets', d.packetsToday);
      set('meshcore', 'observers', d.observers);
    });
    get('https://meshtastic.scotmesh.net/api/summary', function (d) {
      set('meshtastic', 'nodes', Array.isArray(d.nodes) ? d.nodes.length : d.nodes);
      set('meshtastic', 'routers', d.roles && d.roles.ROUTER);
      set('meshtastic', 'packets', d.packets_today);
    });
    get('https://rns.scotmesh.net/status.json', function (d) {
      set('reticulum', 'clients', d.clients);
      if (d.peers && typeof d.peers === 'object') {
        var names = Object.keys(d.peers), up = 0;
        names.forEach(function (k) { if (d.peers[k]) up++; });
        if (names.length) set('reticulum', 'peers', up + '/' + names.length);
      }
      set('reticulum', 'uptime', days(d.transport_uptime_s));
    });
  }

  refresh();
  setInterval(refresh, EVERY);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') refresh();
  });
})();
