---
title: "Keep Scotland's traffic in Scotland"
date: 2026-10-06T21:30:00+01:00
author: Alex
network: meshcore
summary: "Scotland is adding sco-admin, a region for the traffic that keeps the mesh running rather than the traffic people send each other. Every repeater should carry it, whether or not you ever use MeshMapper."
banner:
  src: images/cover.svg
  alt: "The MeshMapper mark and the ScotMesh mark side by side"
tags: [meshcore, scopes, repeaters]
draft: false
---

## What to do

Two lines on the repeater console. This applies to every Scottish repeater, not only to people who wardrive:

```
region put sco-admin *
region save
```

That is the whole change for most repeaters. If yours carries a local region code as well, or you would rather have the full configuration in the order the wiki uses, the [script builder](https://meshcore.scotmesh.net/repeater/) writes it out for you.

Do it now rather than when the switch happens. A repeater filtering on `sco` that has not been told about `sco-admin` will quietly drop everything scoped to it, and it will look perfectly healthy while doing it.

## What the region is for

A mesh carries two sorts of traffic. There is what people send each other, and there is everything that exists to keep the thing running: mapping, bots, utilities, the measurements that tell us where coverage actually reaches. The second sort has always gone out under `sco` alongside the first, which means it travels everywhere `sco` travels.

`sco-admin` separates them. It sits beside `sco` rather than underneath it, every Scottish repeater carries it, and it is never handed to a peering partner. Traffic scoped to it crosses Scotland and stops at the water.

MeshMapper is the first thing to move onto it. It will not be the last, which is the other reason to add it now rather than when you happen to need it.

## Why MeshMapper is moving first

Scotland and the Island of Ireland carry each other's scopes. That peering agreement is what lets a message scoped `sco` reach Ireland and one scoped `ioi` reach us, and it works independently of channels: anything carrying the `sco` scope crosses between the two meshes whatever hashtag it was sent on.

MeshMapper sends three kinds of packet, and they do not behave the same way. Discovery requests and traces are zero hop, so they reach the repeater in front of you and go no further. TX pings are different. They are ordinary channel messages on `#wardriving` and they flood, because whether one arrives anywhere is the measurement.

Those pings go out carrying the `sco` scope, and Irish repeaters carry `sco`. So every ping sent while wardriving in Scotland is also repeated across Ireland, spending Irish airtime on a measurement that Scottish observers have already heard.

The Island of Ireland asked us to stop that happening. We have agreed, and a region of our own for this kind of traffic is how we are doing it.

## What it looks like in the data

Between 22 August and 6 October, CoreScope recorded 283 wardriving messages scoped to `sco`. An observer in Ireland heard 117 of them, which is 41 in every hundred.

They were not creeping over the water either. The median message reached that observer after ten hops and the longest took twenty-one, and every hop is a repeater transmitting.

| Month | Messages | Heard in Ireland |
| --- | --- | --- |
| August | 60 | 5% |
| September | 179 | 45% |
| October, to the 6th | 44 | 75% |

The share has gone up every month as the mesh has filled in. That is the problem getting worse on its own rather than anyone doing anything wrong.

<figure><svg viewBox="0 0 640 560" role="img" aria-label="A diagram of one wardriving ping leaving the central belt, passing ten repeaters and crossing the Irish Sea to an observer in Ireland, with a branch carrying on into Wales"><rect x="0" y="0" width="640" height="302" rx="10" fill="var(--well)"/><rect x="0" y="302" width="640" height="258" rx="10" fill="var(--card)"/><line x1="0" y1="302" x2="640" y2="302" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="6 7"/><text x="22" y="36" text-anchor="start" font-family="var(--mono)" font-size="12" font-weight="400" fill="var(--muted)">SCOTLAND</text><text x="22" y="328" text-anchor="start" font-family="var(--mono)" font-size="12" font-weight="400" fill="var(--muted)">IRELAND</text><text x="618" y="288" text-anchor="end" font-family="var(--sans)" font-size="13" font-weight="400" fill="var(--muted)">the Irish Sea</text><line x1="168" y1="72" x2="168" y2="504" stroke="#56B4F5" stroke-width="2.5" stroke-opacity=".55"/><circle cx="168" cy="56" r="30" fill="none" stroke="#5BD7F2" stroke-opacity=".16" stroke-width="2"/><circle cx="168" cy="56" r="20" fill="none" stroke="#5BD7F2" stroke-opacity=".38" stroke-width="2"/><circle cx="168" cy="56" r="10" fill="#5BD7F2"/><text x="214" y="52" text-anchor="start" font-family="var(--sans)" font-size="16" font-weight="600" fill="var(--ink)">Wardriver</text><text x="214" y="72" text-anchor="start" font-family="var(--sans)" font-size="13.5" font-weight="400" fill="var(--muted)">between Glasgow and Falkirk</text><circle cx="168" cy="112" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="116" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">1</text><circle cx="168" cy="150" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="154" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">2</text><circle cx="168" cy="188" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="192" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">3</text><circle cx="168" cy="226" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="230" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">4</text><circle cx="168" cy="264" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="268" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">5</text><circle cx="168" cy="302" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="306" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">6</text><circle cx="168" cy="340" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="344" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">7</text><circle cx="168" cy="378" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="382" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">8</text><circle cx="168" cy="416" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="420" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">9</text><circle cx="168" cy="454" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5"/><text x="148" y="458" text-anchor="end" font-family="var(--mono)" font-size="12.5" font-weight="400" fill="var(--muted)">10</text><text x="214" y="193" text-anchor="start" font-family="var(--sans)" font-size="13.5" font-weight="400" fill="var(--muted)">every one of these is a repeater</text><text x="214" y="231" text-anchor="start" font-family="var(--sans)" font-size="13.5" font-weight="400" fill="var(--muted)">transmitting the ping again</text><path d="M168,264 C268,264 338,298 392,342" fill="none" stroke="#56B4F5" stroke-width="2.5" stroke-opacity=".45" stroke-dasharray="8 7"/><circle cx="392" cy="342" r="7" fill="var(--bg)" stroke="#56B4F5" stroke-width="2.5" stroke-opacity=".6"/><text x="374" y="366" text-anchor="middle" font-family="var(--sans)" font-size="13.5" font-weight="400" fill="var(--muted)">and on into Wales</text><circle cx="168" cy="504" r="13" fill="#56B4F5"/><circle cx="168" cy="504" r="23" fill="none" stroke="#56B4F5" stroke-opacity=".35" stroke-width="2"/><text x="214" y="500" text-anchor="start" font-family="var(--sans)" font-size="16" font-weight="600" fill="var(--ink)">Observer in Ireland</text><text x="214" y="521" text-anchor="start" font-family="var(--sans)" font-size="13.5" font-weight="400" fill="var(--muted)">ten hops from where it was sent</text></svg>
<figcaption>One ping, drawn to the measured median: out from between Glasgow and Falkirk, ten repeaters, across the Irish Sea to an observer in Ireland, and on into Wales. The longest in the period took twenty-one hops.</figcaption>
</figure>

## What it does not change

Wardriving carries on working, and BIDIR and TX results keep coming back, because the pings still flood across Scotland. They just stop crossing to Ireland. Discovery and trace were never part of this: they never left the repeater in front of you in the first place.

A date for the switch will go out on Discord once enough repeaters are carrying `sco-admin` for it to be safe. Adding it early costs nothing.
