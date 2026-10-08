---
title: "Back in touch with the North East"
date: 2026-10-08T00:58:00+01:00
author: Alex
network: meshcore
summary: "Yorkshire Mesh changed frequency and the North East of England was cut off from the main mesh. They have added sco to their repeaters. We are adding their region, eng-ne, to ours. Two lines on the console."
banner:
  src: images/cover.svg
  alt: "Scotland and the North East of England lit up on a map and joined across the border, with the old link south through Yorkshire broken"
tags: [meshcore, scopes, repeaters, peering]
draft: false
---

## What to do

Two lines on the repeater console. This applies to every Scottish repeater, wherever it is:

```
region put eng-ne *
region save
```

The reply to the first line should read `OK - (flood allowed)`. Then type `region` and check that `eng-ne` is in the list, sitting beside `sco` rather than underneath it, the same way `ioi` and `wls` do.

<aside role="note" aria-label="Reminder: add sco-admin" style="display:flex;gap:14px;align-items:flex-start;padding:14px 16px;border:1px solid var(--signal);border-left-width:4px;border-radius:10px;background:color-mix(in srgb, var(--signal) 10%, transparent)">
<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" style="flex:none;margin-top:2px"><path d="M12 2.8 22.4 20.8H1.6Z" fill="var(--signal)"/><path d="M12 9v5.6" stroke="#0A1424" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="17.6" r="1.3" fill="#0A1424"/></svg>
<div style="min-width:0;font-size:16px;line-height:1.65"><strong style="font-family:var(--mono);font-size:13px;letter-spacing:.06em;text-transform:uppercase">While you are on the console</strong><br>If your repeater does not carry <code>sco-admin</code> yet, add it now as well: <code>region put sco-admin *</code>, then <code>region save</code>. It keeps mapping and bot traffic inside Scotland. <a href="/news/keep-scotlands-traffic-in-scotland/">Keep Scotland's traffic in Scotland</a> explains why.</div>
</aside>

Repeaters near the border will carry most of this traffic, but every repeater a message passes through has to carry the region or the message stops there. So add it even if you are nowhere near Northumberland.

## What happened

Yorkshire Mesh changed frequencies. When they did, the North East of England was cut off from the main mesh.

That has had an upside. The mesh in the North East works, and it works well. But it is an island. The people on it have nobody to talk to but each other.

## How we are joining up again

Scopes let two meshes carry each other's traffic on purpose. That is already how Scotland works with the Island of Ireland and with Wales, and the North East is joining in the same way, in both directions:

| Region | Belongs to | What changes |
| --- | --- | --- |
| `sco` | Scotland | North East repeaters now carry it, so a message you send scoped to `sco` can reach people there. |
| `eng-ne` | North East of England | Scottish repeaters will carry it once this change is in, so their messages can reach us. |

The North East has already done its half. This change is ours.

For now the link across the border is weak, so it only works one way: messages from the North East reach Scotland, but ours do not reach them yet. We are already working on strengthening the links.

## Seeing it work

CoreScope already knows `eng-ne`, so traffic scoped to it shows up in the packet list with its region name rather than as unknown. Once your repeater carries it, you should start seeing `eng-ne` messages in the paths through it.
