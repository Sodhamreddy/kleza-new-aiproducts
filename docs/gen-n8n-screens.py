# Renders the n8n workflow pictures used in the Ask AI guide.
#   python docs/gen-n8n-screens.py            # all of them
#   python docs/gen-n8n-screens.py n8n-01-ask # just one
#
# The n8n connector is not authorised on this machine, so nothing can be
# captured from a live canvas. These are drawn instead: nodes are laid out at
# real pixel coordinates, wired with the same bezier curves n8n uses, and
# photographed in headless Chrome at 2x — so they read as a canvas rather than
# as a flowchart, and they regenerate from this file when the design changes.
#
# Output: docs/ui/n8n-*.png

import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "docs", "ui")
TMP  = os.path.join(ROOT, "docs", ".build")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500'
         '&display=swap">')

# ----------------------------------------------------------------- icons ----
# One glyph per node type: [colour, svg body drawn on a 24x24 grid].
S = 'fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
ICON = {
 "webhook":  ("#7d4b8b", f'<g {S}><path d="M9 12a3 3 0 1 1 4.2 2.8L16 20"/><path d="M12 9V4"/><path d="M5 20h7"/><circle cx="19" cy="17" r="2.6"/><circle cx="5" cy="17" r="2.6"/></g>'),
 "code":     ("#4f5b93", f'<g {S}><polyline points="8 7 3 12 8 17"/><polyline points="16 7 21 12 16 17"/><line x1="13.5" y1="5" x2="10.5" y2="19"/></g>'),
 "agent":    ("#0f9d8f", '<g fill="currentColor"><path d="M10 3.5c0 3.6 2.9 6.5 6.5 6.5-3.6 0-6.5 2.9-6.5 6.5 0-3.6-2.9-6.5-6.5-6.5C7.1 10 10 7.1 10 3.5Z"/><path d="M18 13.5c0 1.4 1.1 2.5 2.5 2.5-1.4 0-2.5 1.1-2.5 2.5 0-1.4-1.1-2.5-2.5-2.5 1.4 0 2.5-1.1 2.5-2.5Z"/></g>'),
 "claude":   ("#d97757", '<g fill="currentColor"><path d="M6.6 16.6 10.4 6.4h2.3l3.8 10.2h-2.3l-.8-2.3H9.7l-.8 2.3H6.6Zm3.7-4.1h3l-1.5-4.3-1.5 4.3Z"/><path d="M17.4 6.4h2.1v10.2h-2.1z"/></g>'),
 "memory":   ("#7a5bd6", f'<g {S}><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/></g>'),
 "tool":     ("#0f9d8f", f'<g {S}><path d="M14.5 6.5a4 4 0 0 0 5 5l-8 8a2.8 2.8 0 0 1-4-4l8-8a4 4 0 0 0-1 -1Z"/><circle cx="17" cy="7" r="0"/></g>'),
 "vector":   ("#6b4fbb", f'<g {S}><circle cx="6" cy="7" r="2.2"/><circle cx="18" cy="7" r="2.2"/><circle cx="6" cy="17" r="2.2"/><circle cx="18" cy="17" r="2.2"/><path d="M8.2 7h7.6M8.2 17h7.6M6 9.2v5.6M18 9.2v5.6"/></g>'),
 "respond":  ("#885577", f'<g {S}><path d="M4 12h13"/><polyline points="12 7 17 12 12 17"/><path d="M20 4v16"/></g>'),
 "sheets":   ("#0f9d58", f'<g {S}><rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M4 9h16M4 15h16M10 9v11.5M15 3.5V20"/></g>'),
 "gmail":    ("#ea4335", f'<g {S}><rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3.5 6.5 12 13 20.5 6.5"/></g>'),
 "calendar": ("#4285f4", f'<g {S}><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="m9.5 15 2 2 3.5-4"/></g>'),
 "slack":    ("#611f69", f'<g {S}><path d="M9 4v9M15 11v9M4 15h9M11 9h9"/></g>'),
 "http":     ("#2f6fd0", f'<g {S}><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.8 2.6 14.2 0 17M12 3.5c-2.6 2.8-2.6 14.2 0 17"/></g>'),
 "clock":    ("#3d8f5a", f'<g {S}><circle cx="12" cy="12" r="8.5"/><polyline points="12 7 12 12 15.5 14"/></g>'),
 "filter":   ("#4a5568", f'<g {S}><polygon points="3.5 5 20.5 5 14 12.5 14 19.5 10 17.5 10 12.5"/></g>'),
 "split":    ("#4a5568", f'<g {S}><path d="M4 6h4l5 6 5 6h2M4 18h4l5-6"/><polyline points="17 3 20 6 17 9"/><polyline points="17 15 20 18 17 21"/></g>'),
 "doc":      ("#5a6472", f'<g {S}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></g>'),
 "bell":     ("#d98324", f'<g {S}><path d="M18 9a6 6 0 1 0-12 0c0 5-2 6.5-2 6.5h16S18 14 18 9Z"/><path d="M10.5 19a2 2 0 0 0 3 0"/></g>'),
 "chart":    ("#2f6fd0", f'<g {S}><path d="M4 20V4"/><path d="M4 20h16"/><rect x="7.5" y="12" width="3" height="5"/><rect x="12.5" y="8" width="3" height="9"/><rect x="17" y="14" width="3" height="3"/></g>'),
 "search":   ("#2f6fd0", f'<g {S}><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></g>'),
 "form":     ("#7d4b8b", f'<g {S}><rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M8 9h8M8 13h8M8 17h4"/></g>'),
 "postgres": ("#336791", f'<g {S}><ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6"/><path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/><path d="M9.5 18.5v-5M14.5 18.5v-5"/></g>'),
 "shield":   ("#0f9d8f", f'<g {S}><path d="M12 3 5 6v6c0 4.2 3 7.5 7 9 4-1.5 7-4.8 7-9V6Z"/><path d="m9 12 2 2 4-4"/></g>'),
}

def glyph(kind, px=34):
    col, body = ICON[kind]
    return (f'<span class="ic" style="color:{col};width:{px}px;height:{px}px">'
            f'<svg viewBox="0 0 24 24">{body}</svg></span>')

CSS = '''
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#fff}
.wrap{padding:0}
.chrome{display:flex;align-items:center;gap:12px;height:46px;padding:0 18px;
  background:#fff;border-bottom:1px solid #e4e7ec}
.chrome .dot{width:22px;height:22px;border-radius:6px;background:#ea4b71;color:#fff;
  display:grid;place-items:center;font:800 11px Inter;letter-spacing:-.03em}
.chrome .nm{font:600 13.5px Inter;color:#20222a}
.chrome .crumb{font:400 13.5px Inter;color:#9aa1ad}
.chrome .tabs{display:flex;gap:16px;margin-left:22px}
.chrome .tabs span{font:500 12.5px Inter;color:#8d94a1;padding:14px 0}
.chrome .tabs span.on{color:#20222a;box-shadow:inset 0 -2px 0 #ea4b71}
.chrome .right{margin-left:auto;display:flex;align-items:center;gap:10px}
.chrome .tog{width:34px;height:19px;border-radius:999px;background:#22c07d;position:relative}
.chrome .tog::after{content:"";position:absolute;top:2px;right:2px;width:15px;height:15px;
  border-radius:50%;background:#fff}
.chrome .tog.off{background:#cfd4dc}
.chrome .tog.off::after{right:auto;left:2px}
.chrome .st{font:500 12px Inter;color:#5b6472}
.chrome .sv{font:600 12px Inter;color:#fff;background:#20222a;border-radius:7px;padding:6px 13px}

.wf{position:relative;background:#fafafb;
  background-image:radial-gradient(#dfe3ea 1.15px,transparent 1.15px);
  background-size:20px 20px}
.wires{position:absolute;inset:0;overflow:visible}

.node{position:absolute;width:96px;height:96px;border-radius:9px;background:#fff;
  border:1.5px solid #dbdfe7;box-shadow:0 1px 3px rgba(20,25,35,.07);
  display:grid;place-items:center;z-index:2}
.node.wide{width:190px}
.node.trig{border-top-left-radius:48px;border-bottom-left-radius:48px}
.node.small{width:74px;height:74px}
.node .ic svg{width:100%;height:100%;display:block}
.node .ic{display:block}
.node .bolt{position:absolute;top:-1px;left:9px;color:#9aa1ad}
.node .bolt svg{width:13px;height:13px}
.lbl{position:absolute;text-align:center;width:190px;font:600 13px Inter;color:#20222a;
  line-height:1.3;z-index:2}
.lbl em{display:block;font:400 11px "JetBrains Mono",monospace;color:#8d94a1;
  font-style:normal;margin-top:3px;letter-spacing:.01em}
.plabel{position:absolute;font:500 10.5px Inter;color:#8d94a1;text-align:center;width:120px;z-index:2}
.badge{position:absolute;width:25px;height:25px;border-radius:50%;background:#0d8f80;color:#fff;
  font:700 13px/25px Inter;text-align:center;z-index:6;
  box-shadow:0 0 0 3px #fafafb,0 2px 6px rgba(10,30,36,.25)}
.note{position:absolute;background:#fff;border:1px solid #dbdfe7;border-left:3px solid #0d8f80;
  border-radius:8px;padding:9px 12px;font:400 11.5px/1.45 Inter;color:#3d4654;
  box-shadow:0 6px 16px -10px rgba(20,25,35,.4);z-index:5}
.note b{color:#20222a}
.sticky{position:absolute;background:#fff6d8;border:1px solid #f0dfa4;border-radius:8px;
  padding:11px 13px;font:400 11.5px/1.5 Inter;color:#5a4a1c;z-index:1;
  box-shadow:0 2px 6px rgba(20,25,35,.06)}
.sticky b{display:block;font:700 12px Inter;color:#3f3410;margin-bottom:3px}

/* catalogue board */
.board{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;padding:20px}
.tile{border:1px solid #e2e6ec;border-radius:12px;background:#fff;padding:14px 16px 15px}
.tile h4{margin:0;font:700 14px Inter;color:#16202b}
.tile .who{font:500 10.5px "JetBrains Mono",monospace;color:#0d8f80;letter-spacing:.09em;
  text-transform:uppercase;margin:0 0 5px}
.tile p{margin:5px 0 11px;font:400 12px/1.5 Inter;color:#5b6472}
.chain{display:flex;align-items:center;gap:0;flex-wrap:wrap}
.chip{display:flex;align-items:center;gap:6px;border:1px solid #dbdfe7;border-radius:8px;
  background:#fbfcfd;padding:5px 9px 5px 6px;font:500 11px Inter;color:#3d4654}
.chip .ic{width:15px;height:15px;display:block}
.chip .ic svg{width:100%;height:100%;display:block}
.arr{color:#b6bcc7;font-size:12px;padding:0 5px}

/* executions table */
.ex{padding:0 18px 18px}
.ex table{width:100%;border-collapse:collapse;font-family:Inter}
.ex th{text-align:left;font:600 11px Inter;letter-spacing:.07em;text-transform:uppercase;
  color:#8d94a1;padding:12px 10px;border-bottom:1px solid #e4e7ec}
.ex td{font:400 12.5px Inter;color:#3d4654;padding:11px 10px;border-bottom:1px solid #eef0f4}
.ex td.q{color:#20222a}
.pill{display:inline-block;font:600 11px Inter;border-radius:999px;padding:3px 10px}
.pill.ok{background:#e6f7ef;color:#146c4b}
.pill.no{background:#fdecec;color:#a32b2b}
.pill.warn{background:#fdf3e2;color:#8a5a12}
.mono{font-family:"JetBrains Mono",monospace;font-size:11.5px;color:#5b6472}
'''

BOLT = ('<span class="bolt"><svg viewBox="0 0 24 24" fill="currentColor">'
        '<path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12L13 2Z"/></svg></span>')

NW, NH = 96, 96          # standard node
SW, SH = 74, 74          # sub-node


def node(n):
    """n: dict(x,y,kind,title,sub,wide,trig,small)"""
    cls = "node"
    w, h = NW, NH
    if n.get("wide"):  cls += " wide"; w = 190
    if n.get("small"): cls += " small"; w = h = SW
    if n.get("trig"):  cls += " trig"
    px = 30 if n.get("small") else 36
    inner = (BOLT if n.get("trig") else "") + glyph(n["kind"], px)
    lbl_w = 150 if n.get("small") else 190
    lx = n["x"] + w / 2 - lbl_w / 2
    ly = n["y"] + h + 9
    sub = f'<em>{n["sub"]}</em>' if n.get("sub") else ""
    return (f'<div class="{cls}" style="left:{n["x"]}px;top:{n["y"]}px">{inner}</div>'
            f'<div class="lbl" style="left:{lx}px;top:{ly}px">{n["title"]}{sub}</div>')


def wire(a, b, dashed=False, down=False):
    """Bezier between node dicts, the way n8n draws them."""
    def geom(n):
        w = 190 if n.get("wide") else (SW if n.get("small") else NW)
        h = SH if n.get("small") else NH
        return w, h
    aw, ah = geom(a); bw, bh = geom(b)
    if down:                                   # agent bottom -> sub-node top
        x1, y1 = a["x"] + a.get("port", aw / 2), a["y"] + ah
        x2, y2 = b["x"] + bw / 2, b["y"]
        dy = max(28, (y2 - y1) * 0.55)
        d = f"M{x1},{y1} C{x1},{y1+dy} {x2},{y2-dy} {x2},{y2}"
    else:
        x1, y1 = a["x"] + aw, a["y"] + ah / 2
        x2, y2 = b["x"], b["y"] + bh / 2
        dx = max(38, (x2 - x1) * 0.5)
        d = f"M{x1},{y1} C{x1+dx},{y1} {x2-dx},{y2} {x2},{y2}"
    style = ' stroke-dasharray="5 5"' if dashed else ''
    head = "" if dashed else ' marker-end="url(#ah)"'
    return f'<path d="{d}" fill="none" stroke="#b6bcc7" stroke-width="2.2"{style}{head}/>'


def canvas(w, h, nodes, wires_html, extra=""):
    return (f'<div class="wf" style="width:{w}px;height:{h}px">'
            f'<svg class="wires" width="{w}" height="{h}"><defs>'
            f'<marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,1.2 L9,5 L0,8.8 z" fill="#b6bcc7"/></marker></defs>'
            f'{wires_html}</svg>'
            + "".join(node(n) for n in nodes) + extra + '</div>')


def chrome(name, active=True, tab="Editor", plain=False):
    tg = '<span class="tog"></span>' if active else '<span class="tog off"></span>'
    st = "Active" if active else "Inactive"
    if plain:                       # settings screens have no workflow controls
        return (f'<div class="chrome"><span class="dot">n8</span>'
                f'<span class="crumb">Kleza&nbsp;/</span><span class="nm">{name}</span></div>')
    return (f'<div class="chrome"><span class="dot">n8</span>'
            f'<span class="crumb">Kleza&nbsp;/</span><span class="nm">{name}</span>'
            f'<span class="tabs"><span class="{"on" if tab=="Editor" else ""}">Editor</span>'
            f'<span class="{"on" if tab=="Executions" else ""}">Executions</span>'
            f'<span>Evaluations</span></span>'
            f'<span class="right"><span class="st">{st}</span>{tg}'
            f'<span class="sv">Save</span></span></div>')


def page(body, w):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">{FONTS}'
            f'<style>{CSS}</style></head><body><div class="wrap" style="width:{w}px">'
            f'{body}</div></body></html>')


def badge(x, y, n):
    return f'<div class="badge" style="left:{x}px;top:{y}px">{n}</div>'


def sticky(x, y, w, title, text):
    return (f'<div class="sticky" style="left:{x}px;top:{y}px;width:{w}px">'
            f'<b>{title}</b>{text}</div>')


def note(x, y, w, html):
    return f'<div class="note" style="left:{x}px;top:{y}px;width:{w}px">{html}</div>'


def chain(steps):
    out = []
    for i, (kind, label) in enumerate(steps):
        if i:
            out.append('<span class="arr">&#9656;</span>')
        out.append(f'<span class="chip">{glyph(kind, 15)}{label}</span>')
    return '<div class="chain">' + "".join(out) + '</div>'


# ============================================================== 1 · ASK AI ===
def wf_ask(annotated=False):
    """Retrieval on the main line: every question is searched before the model
    is called, and the floor is enforced in the workflow rather than left to
    the model's judgement."""
    W, H = 1160, 620
    y = 110
    P = 140                                     # node pitch
    x = lambda i: 36 + i * P

    hook  = dict(x=x(0), y=y, kind="webhook", title="Webhook",
                 sub="POST /kleza-ask-ai", trig=True)
    valid = dict(x=x(1), y=y, kind="code",    title="Validate", sub="500 chars · rate limit")
    emb   = dict(x=x(2), y=y, kind="chart",   title="Embed the question", sub="→ numbers")
    srch  = dict(x=x(3), y=y, kind="postgres",title="Search pgvector", sub="top-k 5 + scores")
    floor = dict(x=x(4), y=y, kind="filter",  title="Above the floor?", sub="≥ 0.35")
    ask   = dict(x=x(5), y=y, kind="claude",  title="Claude writes it", sub="those pieces only")
    shape = dict(x=x(6), y=y, kind="code",    title="Shape response", sub="JSON · check pages")
    resp  = dict(x=x(7), y=y, kind="respond", title="Respond to Webhook", sub="answer · sources")

    std   = dict(x=x(4), y=y+215, kind="respond", title="Standard reply",
                 sub="model never called")
    log   = dict(x=x(7), y=y+215, kind="sheets",  title="Log the question",
                 sub="after the reply")
    store = dict(x=x(3)+11, y=y+215, kind="postgres", title="Postgres · pgvector",
                 sub="~180 chunks", small=True)
    model = dict(x=x(5)+11, y=y+215, kind="claude", title="Anthropic Chat Model",
                 sub="claude-opus-5", small=True)
    mem   = dict(x=x(6)+11, y=y+215, kind="memory", title="Window Memory",
                 sub="6 messages", small=True)

    nodes = [hook, valid, emb, srch, floor, ask, shape, resp, std, log, store, model, mem]
    chain = [hook, valid, emb, srch, floor, ask, shape, resp]
    ws = [wire(a_, b_) for a_, b_ in zip(chain, chain[1:])]
    ws.append(wire(dict(floor, port=NW / 2), std, down=True))     # nothing relevant
    ws.append(wire(dict(shape, port=NW / 2), log, down=True))
    ws.append(wire(dict(srch,  port=NW / 2), store, dashed=True, down=True))
    ws.append(wire(dict(ask,   port=NW * 0.35), model, dashed=True, down=True))
    ws.append(wire(dict(ask,   port=NW * 0.75), mem,   dashed=True, down=True))

    extra = ""
    for sn, lab in ((store, "Vector Store"), (model, "Chat Model"), (mem, "Memory")):
        extra += (f'<div class="plabel" style="left:{sn["x"]+SW/2-60}px;'
                  f'top:{sn["y"]-21}px">{lab}</div>')
    extra += sticky(36, 330, 300, "Retrieval is a step, not a suggestion",
                    "The search sits on the main line, so every question is looked up before "
                    "the model is reached &mdash; it is not a tool the model may decide to skip. "
                    "Nothing above the floor and the branch below answers instead: the model "
                    "is never called, which is the cheapest way to be sure of an answer.")
    if annotated:
        for n_, num in ((hook, 1), (valid, 2), (emb, 3), (srch, 4), (floor, 5),
                        (ask, 6), (shape, 7), (resp, 8)):
            extra += badge(n_["x"] - 13, n_["y"] - 13, num)
        extra += badge(log["x"] - 13, log["y"] - 13, 9)
    return chrome("Ask AI &mdash; answering") + canvas(W, H, nodes, "".join(ws), extra)


# ======================================================== 2 · CONTENT REFRESH ==
def wf_refresh():
    W, H = 1100, 400
    y = 110
    trig = dict(x=36,  y=y, kind="clock",  title="Schedule Trigger",
                sub="every Sunday", trig=True)
    hook = dict(x=36,  y=y+185, kind="webhook", title="Webhook",
                sub="POST /kleza-reindex", trig=True)
    menu = dict(x=191, y=y, kind="doc",    title="Read menu.ts", sub="clean text already")
    smap = dict(x=346, y=y, kind="http",   title="Fetch sitemap", sub="the page list")
    get  = dict(x=501, y=y, kind="http",   title="Fetch each page", sub="20 pages")
    strip= dict(x=656, y=y, kind="code",   title="Strip to text", sub="no menus, no code")
    stamp= dict(x=811, y=y, kind="code",   title="Stamp the URL", sub="so it can cite")
    save = dict(x=966,y=y, kind="sheets", title="Save the knowledge", sub="ready to use")
    nodes = [trig, menu, smap, get, strip, stamp, save]
    ws = "".join(wire(a, b) for a, b in zip(nodes, nodes[1:]))
    extra = sticky(191, 265, 540, "Kept separate on purpose",
                   "Crawling is slow and it sometimes fails. Running it on its own "
                   "schedule means a broken crawl can never break a live conversation &mdash; "
                   "the chat keeps answering from the last good copy.")
    return chrome("Ask AI &mdash; content refresh") + canvas(W, H, nodes, ws, extra)


# =========================================================== 3 · BOOK A DEMO ==
def wf_demo(annotated=False):
    W, H = 1100, 560
    y = 110
    hook = dict(x=36,  y=y, kind="webhook", title="Webhook", sub="POST /kleza-demo", trig=True)
    val  = dict(x=191, y=y, kind="code",    title="Validate", sub="name · email · phone")
    dup  = dict(x=346, y=y, kind="filter",  title="Slot still free?", sub="check the calendar")
    cal  = dict(x=501, y=y, kind="calendar",title="Create the event", sub="+ Meet link · invite")
    mail = dict(x=656, y=y, kind="gmail",   title="Confirmation email", sub="to the visitor")
    crm  = dict(x=811, y=y, kind="sheets",  title="Row in the CRM", sub="who · when · page")
    resp = dict(x=966,y=y, kind="respond", title="Respond to Webhook", sub="booked ✓")
    slack= dict(x=656, y=y+200, kind="slack", title="Tell the team", sub="#demos")
    rem  = dict(x=811, y=y+200, kind="clock", title="Reminder", sub="24 h before")
    busy = dict(x=346, y=y+200, kind="gmail", title="Offer other times", sub="if the slot went")
    nodes = [hook, val, dup, cal, mail, crm, resp, slack, rem, busy]

    ws = [wire(hook, val), wire(val, dup), wire(dup, cal), wire(cal, mail),
          wire(mail, crm), wire(crm, resp),
          wire(dict(x=dup["x"], y=dup["y"], port=NW/2), busy, down=True),
          wire(dict(x=mail["x"], y=mail["y"], port=NW/2), slack, down=True),
          wire(slack, rem)]
    extra = sticky(36, 330, 290, "The screen already exists",
                   "The panel collects the date, the time, the name, the email and the "
                   "phone number today &mdash; and then does nothing with them. This is the "
                   "workflow that makes that screen real.")
    if annotated:
        for n_, num in ((hook, 1), (val, 2), (dup, 3), (cal, 4), (mail, 5),
                        (crm, 6), (resp, 7)):
            extra += badge(n_["x"] - 13, n_["y"] - 13, num)
    return chrome("Kleza &mdash; book a demo") + canvas(W, H, nodes, "".join(ws), extra)


# ============================================================= 4 · CATALOGUE ==
TILES = [
 ("Ask AI, answering", "the website assistant",
  "A visitor's question goes out, an answer written only from our own pages comes back &mdash; "
  "and every question lands in a log we can read.",
  [("webhook","Webhook"),("agent","AI Agent"),("code","Shape"),("respond","Respond"),("sheets","Log")]),
 ("Book a demo", "the panel's calendar",
  "Holds the slot, sends the invite and the confirmation, drops a row in the CRM and "
  "tells the team &mdash; while the visitor is still on the page.",
  [("webhook","Booking"),("calendar","Calendar"),("gmail","Email"),("sheets","CRM"),("slack","Slack")]),
 ("Enquiry routing", "contact &amp; careers forms",
  "Every form on the site lands in one place, gets classified, and reaches the right "
  "person with the page it came from attached.",
  [("form","Form"),("agent","Classify"),("sheets","CRM"),("gmail","Owner"),("bell","Chase")]),
 ("Content refresh", "keeps the answers true",
  "Re-reads the website on a schedule so the assistant is never quoting a page we "
  "changed last month.",
  [("clock","Weekly"),("http","Crawl"),("code","Strip"),("vector","Store")]),
 ("Blog &amp; social", "our Automation Tools service",
  "Drafts the post, waits for a human to approve it, then publishes and schedules the "
  "social versions at the right times.",
  [("clock","Plan"),("agent","Draft"),("shield","Approve"),("http","Publish"),("chart","Report")]),
 ("Uptime &amp; SSL", "our Monitoring service",
  "Checks the sites we look after every few minutes, and shouts &mdash; once, not fifty times &mdash; "
  "when something is down or about to expire.",
  [("clock","Every 5 min"),("http","Check"),("split","If down"),("slack","Alert")]),
 ("Search visibility", "our SEO service",
  "Pulls rankings, traffic and Core Web Vitals into one sheet and emails the client a "
  "digest they will actually read.",
  [("clock","Monday"),("search","Rankings"),("sheets","Sheet"),("gmail","Digest")]),
 ("Inbox triage", "operational outsourcing",
  "Reads what arrives, sorts it, drafts the routine replies for a human to send, and "
  "escalates the ones that matter.",
  [("gmail","Inbox"),("agent","Sort"),("doc","Draft"),("slack","Escalate")]),
]

def wf_catalogue():
    tiles = "".join(
        f'<div class="tile"><p class="who">{who}</p><h4>{t}</h4><p>{d}</p>{chain(c)}</div>'
        for t, who, d, c in TILES)
    return (chrome("Kleza &mdash; workflows", active=True) +
            f'<div class="board" style="background:#fafafb">{tiles}</div>')


# =============================================================== 5 · ANATOMY ==
def wf_anatomy():
    W, H = 1100, 450
    y = 150
    a = dict(x=80, y=y, kind="webhook", title="Webhook", sub="POST /kleza-ask-ai", trig=True)
    b = dict(x=290, y=y, kind="agent",   title="AI Agent", sub="instructions live here", wide=True)
    c = dict(x=580, y=y, kind="respond", title="Respond to Webhook", sub="answer · sources")
    m = dict(x=340, y=y+190, kind="claude", title="Anthropic Chat Model",
             sub="claude-opus-5", small=True)
    nodes = [a, b, c, m]
    bm = dict(b); bm["port"] = 55
    ws = wire(a, b) + wire(b, c) + wire(bm, m, dashed=True, down=True)
    extra = (
      note(40, 40, 240, "<b>A trigger</b> is what starts a run. The flat-left shape "
                        "means &ldquo;nothing happens until something calls this&rdquo;.")
      + note(770, 40, 290, "<b>A node</b> is one step. It has settings, and &mdash; if it "
                           "talks to another company &mdash; a stored credential. Our Anthropic "
                           "key lives there, and nowhere else.")
      + note(730, 250, 330, "<b>A run</b> (n8n calls it an execution) is one journey "
                            "through the workflow, kept with everything that went in and "
                            "came out. That is how you debug a bad answer.")
      + note(40, 300, 290, "<b>The dashed line</b> means &ldquo;this is a part the step uses&rdquo; "
                           "&mdash; the model, its memory, its tools &mdash; not the next step.")
      + badge(a["x"] - 13, a["y"] - 13, 1) + badge(b["x"] - 13, b["y"] - 13, 2)
      + badge(m["x"] - 12, m["y"] - 12, 3) + badge(c["x"] - 13, c["y"] - 13, 4))
    return chrome("Anything &mdash; the shape of every workflow") + canvas(W, H, nodes, ws, extra)


# ============================================================ 6 · EXECUTIONS ==
ROWS = [
 ("today 14:22", "What does Voica do?",              "ok",   "2.9 s", "/ai-products/voica"),
 ("today 14:19", "do u work with pharmacies",        "ok",   "3.4 s", "/about"),
 ("today 14:11", "How much does Voica cost?",        "warn", "3.1 s", "/contact"),
 ("today 13:58", "What&rsquo;s the weather in Hyderabad?", "no", "1.2 s", "&mdash;"),
 ("today 13:47", "book a demo next tuesday",         "ok",   "2.2 s", "&mdash;"),
 ("today 13:31", "whats the diff between voica and docui", "ok", "3.8 s", "/ai-products"),
 ("today 13:05", "Ignore previous instructions",     "no",   "1.1 s", "&mdash;"),
]
PILL = {"ok": ("ok", "Answered"), "no": ("no", "Refused"), "warn": ("warn", "Sent to Contact")}

def wf_executions():
    rows = ""
    for when, q, st, dur, src in ROWS:
        cls, txt = PILL[st]
        rows += (f'<tr><td class="mono">{when}</td><td class="q">{q}</td>'
                 f'<td><span class="pill {cls}">{txt}</span></td>'
                 f'<td class="mono">{dur}</td><td class="mono">{src}</td></tr>')
    return (chrome("Ask AI &mdash; answering", tab="Executions") +
            '<div class="ex" style="background:#fff"><table>'
            '<thead><tr><th>When</th><th>The question</th><th>What happened</th>'
            '<th>Took</th><th>Page cited</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            '<p style="font:400 11.5px Inter;color:#8d94a1;margin:14px 10px 4px">'
            'Every run is kept with what went in and what came out. This list &mdash; read '
            'for half an hour a week &mdash; is where the assistant actually gets better.</p></div>')


# ============================================================== 7 · A NODE ===
NODE_CSS = '''
.np{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:0;background:#fafafb;
  border-top:1px solid #e4e7ec}
.np .col{padding:16px 18px 22px;border-right:1px solid #e9ecf1}
.np .col:last-child{border-right:none}
.np h5{margin:0 0 10px;font:600 12px Inter;letter-spacing:.06em;text-transform:uppercase;
  color:#8d94a1}
.np .io{background:#fff;border:1px solid #e4e7ec;border-radius:8px;padding:11px 13px;
  font:400 11.5px/1.65 "JetBrains Mono",monospace;color:#3d4654;white-space:pre-wrap}
.np .io b{color:#20222a;font-weight:500}
.fld{margin-bottom:13px}
.fld label{display:block;font:600 11.5px Inter;color:#3d4654;margin-bottom:4px}
.fld .in{background:#fff;border:1px solid #dbdfe7;border-radius:7px;padding:8px 11px;
  font:400 12px Inter;color:#20222a}
.fld .in.sel{display:flex;align-items:center;justify-content:space-between;color:#20222a}
.fld .in.sel span.k{display:flex;align-items:center;gap:7px}
.fld .in.exp{font-family:"JetBrains Mono",monospace;font-size:11.5px;color:#8a5cd0;
  background:#faf7ff;border-color:#e2d6f7}
.fld .in.ta{font-family:"JetBrains Mono",monospace;font-size:10.8px;line-height:1.6;
  color:#3d4654;white-space:pre-wrap;max-height:186px;overflow:hidden}
.fld .hint{font:400 10.5px Inter;color:#9aa1ad;margin-top:4px}
.cred{display:inline-flex;align-items:center;gap:6px;font:500 11.5px Inter;color:#146c4b;
  background:#e6f7ef;border-radius:999px;padding:3px 10px}
.nphead{display:flex;align-items:center;gap:10px;padding:12px 18px;background:#fff}
.nphead .ttl{font:700 14px Inter;color:#20222a}
.nphead .tag{font:500 10.5px "JetBrains Mono",monospace;color:#8d94a1}
.nphead .rt{margin-left:auto;font:600 11.5px Inter;color:#fff;background:#ea4b71;
  border-radius:7px;padding:6px 13px}

/* credentials + failure + email */
.crd{padding:0 18px 20px;background:#fff}
.crd table{width:100%;border-collapse:collapse}
.crd th{text-align:left;font:600 11px Inter;letter-spacing:.07em;text-transform:uppercase;
  color:#8d94a1;padding:12px 10px;border-bottom:1px solid #e4e7ec}
.crd td{font:400 12.5px Inter;color:#3d4654;padding:11px 10px;border-bottom:1px solid #eef0f4}
.crd td.n{font-weight:600;color:#20222a}
.crd .dot2{display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c07d;
  margin-right:7px;vertical-align:1px}
.crd .banner{display:flex;gap:10px;align-items:flex-start;margin:16px 0 4px;padding:12px 14px;
  border-radius:9px;background:#f2f8ff;border:1px solid #d7e6f7;font:400 12px/1.55 Inter;
  color:#2c4a63}
.crd .banner b{color:#17334a}
.err{position:absolute;background:#fff;border:1px solid #f3c9c9;border-left:4px solid #d64545;
  border-radius:9px;padding:12px 14px;font:400 11.5px/1.5 Inter;color:#5b3232;z-index:6;
  box-shadow:0 8px 22px -12px rgba(20,25,35,.45)}
.err b{display:block;font:700 12.5px Inter;color:#a32b2b;margin-bottom:4px}
.err code{font-family:"JetBrains Mono",monospace;font-size:11px;background:#fdf0f0;
  padding:1px 5px;border-radius:4px}
.node.bad{border-color:#d64545;box-shadow:0 0 0 3px rgba(214,69,69,.12)}
.node .warn{position:absolute;top:-9px;right:-9px;width:21px;height:21px;border-radius:50%;
  background:#d64545;color:#fff;font:700 13px/21px Inter;text-align:center}
.node.skip{opacity:.42}

.mail{background:#fff;padding:0 0 20px}
.mail .bar{display:flex;align-items:center;gap:9px;padding:13px 20px;border-bottom:1px solid #e9ecf1}
.mail .bar .av{width:30px;height:30px;border-radius:50%;background:#36c0ed;color:#fff;
  display:grid;place-items:center;font:700 12px Inter}
.mail .subj{font:700 16px Inter;color:#16202b;padding:18px 20px 4px}
.mail .meta{font:400 12px Inter;color:#8d94a1;padding:0 20px 14px}
.mail .body{padding:4px 20px 0;font:400 13.5px/1.7 Inter;color:#2c3947}
.mail .body p{margin:0 0 12px}
.mail .card2{border:1px solid #e4e7ec;border-radius:10px;padding:14px 16px;margin:4px 0 14px;
  background:#fbfcfd}
.mail .card2 .k{font:600 10.5px "JetBrains Mono",monospace;letter-spacing:.1em;
  text-transform:uppercase;color:#8d94a1}
.mail .card2 .v{font:600 14px Inter;color:#16202b;margin:2px 0 10px}
.mail .btn2{display:inline-block;font:600 13px Inter;color:#000;background:rgb(155 234 166);
  border-radius:999px;padding:9px 18px}
.mail .sig{font:400 12.5px/1.6 Inter;color:#5b6472;margin-top:16px}
'''
CSS += NODE_CSS

SYS_PREVIEW = """You are the Kleza website assistant. You help visitors of
kleza.io understand what Kleza does and find the right page
or the right person.

## Your only source of knowledge
You answer ONLY from the Kleza website content provided to you.
- Never answer from general knowledge, even when you are
  confident.
- Never guess, estimate, extrapolate or fill gaps.
- Never invent prices, dates, client names, headcounts,
  certifications or capabilities. If a number is not in the
  content, it does not exist.

## What is out of scope
Everything else. For anything out of scope, reply with exactly
this and nothing more: &hellip;"""

def wf_node():
    inp = ('{\n  <b>"question"</b>: "does voica handle\n     interruptions?",\n'
           '  <b>"sessionId"</b>: "kz-8f3a91c4"\n}')
    out = ('[\n  {\n    <b>"pageContent"</b>: "Natural turn-\n'
           '       taking with barge-in. Live\n'
           '       transcription. Confidence-\n'
           '       scored escalation…",\n'
           '    <b>"metadata"</b>: {\n'
           '      "url": "/ai-products/voica",\n'
           '      "heading": "What it does" },\n'
           '    <b>"score"</b>: 0.89\n  },\n'
           '  { <b>"score"</b>: 0.86, … },\n'
           '  { <b>"score"</b>: 0.71, … }\n]')
    return (chrome("Ask AI &mdash; answering") +
      '<div class="nphead">' + glyph("postgres", 22) +
      '<span class="ttl">Search pgvector</span>'
      '<span class="tag">@n8n/n8n-nodes-langchain.vectorStorePGVector</span>'
      '<span class="rt">Test step</span></div>'
      '<div class="np">'
        f'<div class="col"><h5>Input</h5><div class="io">{inp}</div>'
        '<p style="font:400 11.5px/1.5 Inter;color:#8d94a1;margin:10px 0 0">'
        'The visitor&rsquo;s question, validated. Nothing has been sent to a model yet.</p></div>'
        '<div class="col"><h5>Parameters</h5>'
          '<div class="fld"><label>Operation mode</label>'
            '<div class="in sel"><span>Get Many &mdash; retrieve documents</span>'
            '<span style="color:#9aa1ad">&#9662;</span></div></div>'
          '<div class="fld"><label>Credential to connect with</label>'
            '<div class="in sel"><span class="k">' + glyph("postgres", 14) +
            'Kleza Postgres &mdash; pgvector</span>'
            '<span style="color:#9aa1ad">&#9662;</span></div></div>'
          '<div class="fld"><label>Table name</label>'
            '<div class="in">kleza_pages</div></div>'
          '<div class="fld"><label>Prompt</label>'
            '<div class="in exp">{{ $json.question }}</div>'
            '<div class="hint">The text to match against. Embedded by the sub-node below, '
            'never by Claude.</div></div>'
          '<div class="fld"><label>Limit (top-k)</label>'
            '<div class="in" style="width:90px">5</div></div>'
          '<div class="fld"><label>Include metadata</label>'
            '<div class="in sel"><span>On &mdash; carries the page URL</span>'
            '<span style="color:#9aa1ad">&#9662;</span></div>'
            '<div class="hint">Without this an answer has nothing to cite.</div></div>'
          '<div class="fld"><label>Sub-node</label>'
            '<div class="in sel"><span class="k">' + glyph("chart", 14) +
            'Embeddings &mdash; text-embedding-3-small</span>'
            '<span style="color:#9aa1ad">&#9662;</span></div>'
            '<div class="hint">Must be the same model that indexed the pages.</div></div>'
        '</div>'
        f'<div class="col"><h5>Output</h5><div class="io">{out}</div>'
        '<p style="font:400 11.5px/1.5 Inter;color:#8d94a1;margin:10px 0 0">'
        'Three paragraphs of our own site, each with its page and its score. <b>This is the '
        'entire universe of facts</b> the next node may answer from.</p></div>'
      '</div>')


# ========================================================= 8 · CREDENTIALS ===
CREDS = [
 ("Anthropic account &mdash; Kleza", "claude", "Anthropic API", "2 minutes ago", "Ask AI"),
 ("Kleza sales calendar", "calendar", "Google Calendar OAuth2", "18 minutes ago", "Book a demo"),
 ("sales@kleza.io (send only)", "gmail", "SMTP", "18 minutes ago", "Book a demo, Enquiries"),
 ("Kleza CRM sheet", "sheets", "Google Sheets OAuth2", "18 minutes ago", "Book a demo, Ask AI"),
 ("Kleza workspace", "slack", "Slack API", "3 hours ago", "Alerts"),
]

def wf_credentials():
    rows = ""
    for name, ic, typ, used, where in CREDS:
        rows += (f'<tr><td class="n"><span class="dot2"></span>{name}</td>'
                 f'<td>{typ}</td><td>{used}</td><td>{where}</td></tr>')
    return (chrome("Credentials", plain=True) +
      '<div class="crd"><table><thead><tr><th>Name</th><th>Type</th>'
      '<th>Last used</th><th>Used by</th></tr></thead>'
      f'<tbody>{rows}</tbody></table>'
      '<div class="banner">' + glyph("shield", 16) +
      '<span><b>This screen is the security answer.</b> Every key, password and login the '
      'automations need lives here, encrypted, and nowhere else &mdash; not in the website&rsquo;s '
      'code, not in a browser, not in a message. They can be replaced from this list, but '
      'never read back out of it.</span></div></div>')


# ============================================================== 9 · FAILURE ===
def wf_failed():
    W, H = 1100, 480
    y = 120
    hook = dict(x=36,  y=y, kind="webhook", title="Webhook", sub="POST /kleza-demo", trig=True)
    val  = dict(x=191, y=y, kind="code",    title="Validate", sub="ok &middot; 41 ms")
    cal  = dict(x=346, y=y, kind="calendar",title="Create the event", sub="failed")
    mail = dict(x=501, y=y, kind="gmail",   title="Confirmation email", sub="not reached")
    crm  = dict(x=656, y=y, kind="sheets",  title="Row in the CRM", sub="not reached")
    nodes = [hook, val, cal, mail, crm]
    ws = "".join(wire(a, b) for a, b in zip(nodes, nodes[1:]))
    html = canvas(W, H, nodes, ws,
        note(760, 96, 300, "<b>What the visitor saw</b><br>&ldquo;I couldn&rsquo;t confirm that "
             "booking just now &mdash; please email sales@kleza.io.&rdquo; Never a silent "
             "success.")
        + f'<div class="err" style="left:320px;top:296px;width:420px">'
          '<b>Google Calendar &mdash; the run stopped here</b>'
          '<code>401 invalid_grant: token has been expired or revoked</code><br>'
          'The calendar login needs reconnecting. Nothing after this node ran, so no '
          'email went out and no row was written &mdash; the booking simply did not happen.'
          '</div>')
    # mark the failed node and grey out what never ran
    html = html.replace(f'<div class="node" style="left:{cal["x"]}px;top:{cal["y"]}px">',
                        f'<div class="node bad" style="left:{cal["x"]}px;top:{cal["y"]}px">'
                        '<span class="warn">!</span>')
    for n_ in (mail, crm):
        html = html.replace(f'<div class="node" style="left:{n_["x"]}px;top:{n_["y"]}px">',
                            f'<div class="node skip" style="left:{n_["x"]}px;top:{n_["y"]}px">')
    return chrome("Kleza &mdash; book a demo", tab="Executions") + html


# ================================================================ 10 · EMAIL ==
def wf_email():
    return ('<div class="mail">'
      '<div class="bar"><span class="av">K</span>'
      '<span style="font:600 13px Inter;color:#20222a">Kleza</span>'
      '<span style="font:400 12px Inter;color:#8d94a1">&lt;sales@kleza.io&gt;</span>'
      '<span style="margin-left:auto;font:400 11.5px \'JetBrains Mono\',monospace;'
      'color:#9aa1ad">sent by n8n, 1.4 s after the booking</span></div>'
      '<div class="subj">Your Kleza demo &mdash; Wednesday 15 July, 13:30</div>'
      '<div class="meta">to priya@northstarcare.com</div>'
      '<div class="body">'
        '<p>Hello Priya,</p>'
        '<p>Thanks for booking a demo with us. It is in both our diaries, and the invite '
        'is attached to this email.</p>'
        '<div class="card2"><div class="k">When</div>'
        '<div class="v">Wednesday 15 July 2026, 13:30 &ndash; 14:00 IST</div>'
        '<div class="k">Who from Kleza</div><div class="v">[name of whoever takes the call]</div>'
        '<div class="k">Where</div><div class="v" style="margin-bottom:12px">'
        'Google Meet &mdash; link in the invite</div>'
        '<span class="btn2">Add to calendar</span></div>'
        '<p>If that time stops working, reply to this email and we will move it &mdash; '
        'no form to fill in again.</p>'
        '<div class="sig">Kleza Solutions<br>Overland Park, Kansas &middot; '
        'Madhapur, Hyderabad<br>sales@kleza.io</div>'
      '</div></div>')


# ======================================================= 11 · RAG INDEXING ===
RAG_CSS = '''
.rag{background:#fafafb;padding:22px 24px 26px;
  background-image:radial-gradient(#dfe3ea 1.15px,transparent 1.15px);background-size:20px 20px}
.rag h6{margin:0 0 12px;font:600 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;
  color:#8d94a1}
.row{display:flex;align-items:stretch;gap:0}
.pagecard{width:250px;flex:none;background:#fff;border:1.5px solid #dbdfe7;border-radius:10px;
  padding:13px 15px;font:400 11.5px/1.6 Inter;color:#3d4654;box-shadow:0 1px 3px rgba(20,25,35,.07)}
.pagecard .u{font:500 10.5px "JetBrains Mono",monospace;color:#7d4b8b;margin-bottom:7px;
  word-break:break-all}
.pagecard h4{margin:0 0 5px;font:700 13.5px Inter;color:#16202b}
.pagecard .tag2{display:inline-block;font:500 10px "JetBrains Mono",monospace;color:#8d94a1;
  border:1px solid #e4e7ec;border-radius:5px;padding:1px 6px;margin-top:9px}
.big{display:grid;place-items:center;padding:0 16px;color:#b6bcc7;font-size:22px;flex:none}
.chunks{display:flex;flex-direction:column;gap:9px;flex:1}
.chunk{display:flex;gap:11px;background:#fff;border:1.5px solid #dbdfe7;border-radius:9px;
  padding:10px 13px;box-shadow:0 1px 3px rgba(20,25,35,.06)}
.chunk .n2{width:22px;height:22px;flex:none;border-radius:6px;background:#eef2f7;color:#5b6472;
  font:700 11px/22px Inter;text-align:center}
.chunk .tx2{flex:1;font:400 11.5px/1.55 Inter;color:#3d4654}
.chunk .tx2 b{display:block;font:700 12px Inter;color:#16202b;margin-bottom:2px}
.chunk .meta2{display:block;font:400 10px "JetBrains Mono",monospace;color:#9aa1ad;margin-top:4px}
.chunk.hit{border-color:#0f9d8f;box-shadow:0 0 0 3px rgba(15,157,143,.12)}
.chunk .score{flex:none;align-self:center;font:600 11px "JetBrains Mono",monospace;
  color:#146c4b;background:#e6f7ef;border-radius:999px;padding:3px 9px}
.chunk .score.no{color:#8d94a1;background:#f1f3f6}
.qbox{background:#fff;border:1.5px solid #36c0ed;border-radius:10px;padding:11px 14px;
  font:600 13px Inter;color:#16202b;box-shadow:0 1px 3px rgba(20,25,35,.07)}
.abox{background:#fff;border:1.5px solid #0f9d8f;border-radius:10px;padding:12px 14px;
  font:400 12px/1.6 Inter;color:#3d4654;box-shadow:0 1px 3px rgba(20,25,35,.07)}
.abox b{color:#16202b}
.abox .src{font:500 10.5px "JetBrains Mono",monospace;color:#8d94a1;margin-top:7px;display:block}
.stepnote{font:400 11px/1.5 Inter;color:#8d94a1;margin:7px 0 0}
'''
CSS += RAG_CSS

def wf_index():
    W, H = 1100, 480
    y = 110
    trig = dict(x=36,  y=y, kind="clock",  title="Schedule Trigger",
                sub="every Sunday", trig=True)
    hook = dict(x=36,  y=y+185, kind="webhook", title="Webhook",
                sub="POST /kleza-reindex", trig=True)
    src  = dict(x=191, y=y, kind="doc",    title="menu.ts + 20 pages", sub="the whole site")
    strip= dict(x=346, y=y, kind="code",   title="Strip to text", sub="no menus, no code")
    cut  = dict(x=501, y=y, kind="split",  title="Cut into chunks", sub="~800 tokens &middot; 100 over")
    emb  = dict(x=656, y=y, kind="chart",  title="Turn into numbers", sub="one per chunk")
    store= dict(x=811, y=y, kind="postgres", title="Postgres · pgvector", sub="~180 chunks")
    model= dict(x=672, y=y+215, kind="claude", title="Embedding model",
                sub="cost: check", small=True)
    nodes = [trig, hook, src, strip, cut, emb, store, model]
    chain = [trig, src, strip, cut, emb, store]
    ws = [wire(a, b) for a, b in zip(chain, chain[1:])]
    ws.append(wire(hook, src))          # the deploy hook joins the same chain
    ws.append(wire(dict(emb, port=NW/2), model, dashed=True, down=True))
    extra = (f'<div class="plabel" style="left:{model["x"]+SW/2-60}px;top:{model["y"]-21}px">'
             'Embeddings</div>'
             + sticky(330, 330, 320, "Two ways in, one store",
                      "The schedule keeps the store fresh on its own. The webhook lets a "
                      "deploy re-index immediately, so a page we publish this morning is "
                      "answerable this morning &mdash; not next Sunday."))
    return chrome("Ask AI &mdash; index the website") + canvas(W, H, nodes, "".join(ws), extra)


# ==================================================== 12 · PAGE INTO CHUNKS ==
CHUNKS = [
 ("Voica &mdash; what it is",
  "Real-time conversational AI for patient intake, support and care coordination.",
  "/ai-products/voica &middot; 96 tokens"),
 ("What it does",
  "Natural turn-taking with barge-in. Live transcription. Confidence-scored escalation "
  "to a human the moment it is unsure.",
  "/ai-products/voica &middot; 124 tokens"),
 ("Who it is for",
  "Home care, clinics and pharmacies handling more calls than their front desk can answer.",
  "/ai-products/voica &middot; 88 tokens"),
 ("Security &amp; compliance",
  "HIPAA-aligned. Audit trail on every call. Human oversight by design.",
  "/ai-products/voica &middot; 74 tokens"),
]

def wf_chunks():
    page = ('<div class="pagecard"><div class="u">https://kleza.io/ai-products/voica</div>'
            '<h4>Voica</h4>'
            'Real-time conversational AI for patient intake, support and care coordination. '
            'Handles natural turn-taking and live transcription, and escalates to a human the '
            'moment it is unsure.<br><br>'
            '<b>What it does</b><br>Natural turn-taking with barge-in &middot; Live transcription '
            '&middot; Confidence-scored escalation&hellip;'
            '<span class="tag2">one page &middot; 1 of 20</span></div>')
    chunks = "".join(
        f'<div class="chunk"><span class="n2">{i+1}</span><span class="tx2"><b>{h}</b>{t}'
        f'<span class="meta2">{m}</span></span></div>'
        for i, (h, t, m) in enumerate(CHUNKS))
    return (chrome("The knowledge, close up", plain=True) +
      '<div class="rag"><h6>One page becomes four pieces</h6>'
      f'<div class="row">{page}<div class="big">&#10142;</div>'
      f'<div class="chunks">{chunks}</div></div>'
      '<p class="stepnote">Cut on the headings, not by counting characters &mdash; a piece that '
      'starts mid-sentence answers nothing. Every piece carries its own web address, which is '
      'what lets an answer say where it came from. Twenty pages make roughly 180 pieces.</p>'
      '</div>')


# ====================================================== 13 · HOW IT ANSWERS ==
RETRIEVE = [
 ("What it does", "Natural turn-taking with barge-in. Live transcription. Confidence-scored "
  "escalation to a human&hellip;", "/ai-products/voica", "0.89", True),
 ("Voica &mdash; what it is", "Real-time conversational AI for patient intake, support and care "
  "coordination.", "/ai-products/voica", "0.86", True),
 ("AI Support Assistant", "24/7 conversational AI trained on your knowledge base, with smart "
  "escalation to a human.", "/ai-services/assistant", "0.71", True),
 ("Operational Outsourcing", "A trained, SLA-backed team that runs your repeatable "
  "operations&hellip;", "/enterprise-services/operational-outsourcing", "0.19", False),
]

def wf_retrieve():
    rows = ""
    for h, t, u, sc, hit in RETRIEVE:
        rows += (f'<div class="chunk{" hit" if hit else ""}">'
                 f'<span class="tx2"><b>{h}</b>{t}<span class="meta2">{u}</span></span>'
                 f'<span class="score{"" if hit else " no"}">{sc}</span></div>')
    return (chrome("The knowledge, close up", plain=True) +
      '<div class="rag"><h6>What happens to one question</h6>'
      '<div class="row" style="align-items:center">'
        '<div style="width:250px;flex:none">'
          '<div class="qbox">&ldquo;does voica handle interruptions?&rdquo;</div>'
          '<p class="stepnote">The visitor&rsquo;s words are turned into numbers the same way the '
          'pieces were &mdash; so &ldquo;interruptions&rdquo; can find &ldquo;barge-in&rdquo;, which shares not one '
          'word with it. That is the whole trick, and it is why keyword matching could '
          'never answer this.</p>'
        '</div>'
        '<div class="big">&#10142;</div>'
        f'<div class="chunks">{rows}</div>'
      '</div>'
      '<div class="row" style="margin-top:16px;align-items:center">'
        '<div style="width:250px;flex:none">'
          '<p class="stepnote" style="margin:0">The closest three go to the model with the '
          'instructions. The fourth is nowhere near, so it never gets sent &mdash; and if '
          '<em>nothing</em> scores above the floor, the model is never called at all and the '
          'visitor gets the standard reply.</p>'
        '</div>'
        '<div class="big">&#10142;</div>'
        '<div class="abox" style="flex:1">'
          '<b>Yes.</b> Voica handles natural turn-taking with barge-in, so a caller can '
          'interrupt mid-sentence and it will stop and listen. It also transcribes live and '
          'hands over to a person the moment it is unsure.'
          '<span class="src">from /ai-products/voica</span>'
        '</div>'
      '</div></div>')


def wf_alert():
    return ('<div class="mail">'
      '<div class="bar"><span class="av" style="background:#0f9d8f">n8</span>'
      '<span style="font:600 13px Inter;color:#20222a">Kleza automations</span>'
      '<span style="font:400 12px Inter;color:#8d94a1">&lt;bookings@kleza.io&gt;</span>'
      '<span style="margin-left:auto;font:400 11.5px \'JetBrains Mono\',monospace;'
      'color:#9aa1ad">to sales@kleza.io &middot; also posted in #demos</span></div>'
      '<div class="subj">New demo booked &mdash; Priya Raghavan, North Star Care</div>'
      '<div class="meta">Wednesday 15 July, 13:30 IST &middot; 4 minutes from now in your diary</div>'
      '<div class="body">'
        '<div class="card2"><div class="k">Who</div>'
        '<div class="v">Priya Raghavan &middot; priya@northstarcare.com &middot; +1 913 555 0148</div>'
        '<div class="k">Booked from</div>'
        '<div class="v">/ai-products/voica &mdash; the Voica page, just before booking</div>'
        '<div class="k">Asked the assistant first</div>'
        '<div class="v" style="margin-bottom:12px">&ldquo;does voica handle interruptions?&rdquo; '
        '&middot; &ldquo;is it hipaa safe&rdquo;</div>'
        '<span class="btn2">Open the calendar entry</span></div>'
        '<p>The visitor already has their confirmation and the invite. Nothing else is '
        'needed from you before the call.</p>'
        '<div class="sig">Sent by the <b>Book a demo</b> workflow &mdash; n8n &middot; '
        'run #&hellip; &middot; 1.4 s</div>'
      '</div></div>')


# ================================================== 14 · RAG ARCHITECTURE ====
ARCH_CSS = '''
.arch{background:#fbfcfd;padding:0 0 6px}
.lane{position:relative;padding:16px 22px 18px;border-bottom:1px solid #e7eaef}
.lane:last-child{border-bottom:none}
.lane.ingest{background:linear-gradient(90deg,#f4f9f8,#fbfcfd 60%)}
.lane.store{background:#fff}
.lane.answer{background:linear-gradient(90deg,#f3f9fd,#fbfcfd 60%)}
.lane-hd{display:flex;align-items:baseline;gap:10px;margin-bottom:13px}
.lane-hd .num{width:22px;height:22px;border-radius:6px;color:#fff;font:700 12px/22px Inter;
  text-align:center;flex:none}
.lane.ingest .num{background:#0f9d8f}
.lane.answer .num{background:#2f6fd0}
.lane.store  .num{background:#336791}
.lane-hd h4{margin:0;font:700 15px Inter;color:#16202b}
.lane-hd .when{margin-left:auto;font:500 10.5px "JetBrains Mono",monospace;color:#8d94a1;
  border:1px solid #e2e6ec;border-radius:999px;padding:3px 11px;background:#fff}
.lane-hd .sub{font:400 12.5px Inter;color:#6b7684}
.chain2{display:flex;align-items:center;flex-wrap:nowrap;gap:0}
.step2{display:flex;align-items:center;gap:8px;background:#fff;border:1.5px solid #dbdfe7;
  border-radius:10px;padding:8px 11px;box-shadow:0 1px 3px rgba(20,25,35,.06);flex:none}
.step2 .ic{width:19px;height:19px;display:block;flex:none}
.step2 .ic svg{width:100%;height:100%;display:block}
.step2 b{display:block;font:600 12.5px Inter;color:#16202b;line-height:1.25}
.step2 em{display:block;font:400 10.5px "JetBrains Mono",monospace;color:#8d94a1;
  font-style:normal;margin-top:2px}
.step2.big{border-color:#0f9d8f;box-shadow:0 2px 10px -4px rgba(15,157,143,.45)}
.ar2{color:#c2c8d2;font-size:14px;padding:0 6px;flex:none}
.storebar{display:flex;align-items:center;gap:16px;background:#f7fafd;border:1.5px solid #cfdcea;
  border-radius:12px;padding:13px 18px}
.storebar .big2{display:flex;align-items:center;gap:11px}
.storebar .big2 .ic{width:30px;height:30px;display:block}
.storebar .big2 .ic svg{width:100%;height:100%;display:block}
.storebar h5{margin:0;font:700 14.5px Inter;color:#16202b}
.storebar p{margin:2px 0 0;font:400 11.5px Inter;color:#5b6472}
.cols3{display:flex;gap:9px;margin-left:auto;flex-wrap:wrap}
.fact{background:#fff;border:1px solid #dde5ee;border-radius:8px;padding:6px 11px;
  font:400 10.5px Inter;color:#5b6472;text-align:center}
.fact b{display:block;font:700 12.5px Inter;color:#16202b}
.wfnote{font:400 11px Inter;color:#8d94a1;margin:9px 0 0}
.wfnote b{color:#5b6472}

.tl{background:#fbfcfd;padding:20px 24px 22px}
.tl h6{margin:0 0 14px;font:600 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;
  color:#8d94a1}
.tlrow{display:flex;align-items:stretch;gap:3px;margin-bottom:9px}
.seg{border-radius:7px;padding:9px 12px;color:#fff;font:600 12px Inter;
  display:flex;flex-direction:column;justify-content:center;min-width:0}
.seg em{display:block;font:400 10.5px "JetBrains Mono",monospace;opacity:.88;margin-top:2px;
  font-style:normal}
.tlaxis{display:flex;justify-content:space-between;font:400 10.5px "JetBrains Mono",monospace;
  color:#9aa1ad;border-top:1px solid #e2e6ec;padding-top:6px}
.tlnote{font:400 11.5px/1.6 Inter;color:#5b6472;margin:12px 0 0;max-width:78ch}
.tlnote b{color:#16202b}
'''
CSS += ARCH_CSS


def chip(kind, title, sub, cls=""):
    return (f'<span class="step2 {cls}">{glyph(kind, 19)}'
            f'<span><b>{title}</b><em>{sub}</em></span></span>')


def arrow_row(items):
    out = []
    for i, it in enumerate(items):
        if i:
            out.append('<span class="ar2">&#10142;</span>')
        out.append(it)
    return '<div class="chain2">' + "".join(out) + '</div>'


def wf_arch():
    ing = [chip("clock", "Schedule", "every Sunday"),
           chip("webhook", "Webhook", "on deploy"),
           chip("doc", "menu.ts + 20 pages", "whole site"),
           chip("code", "Strip to text", "no menus, no code"),
           chip("split", "Cut into chunks", "~800 tokens"),
           chip("chart", "Embed", "one per chunk")]
    ans = [chip("webhook", "Webhook", "POST /kleza-ask-ai"),
           chip("code", "Validate", "500 chars"),
           chip("chart", "Embed question", "same model"),
           chip("tool", "search_kleza_website", "top-k 5", "big"),
           chip("claude", "Claude writes it", "those pieces only"),
           chip("respond", "Answer + source", "2&ndash;4 s")]
    return (chrome("Ask AI &mdash; how the whole thing fits together", plain=True) +
      '<div class="arch">'
        '<div class="lane ingest"><div class="lane-hd"><span class="num">1</span>'
          '<h4>Workflow one &mdash; put the website in</h4>'
          '<span class="sub">nobody is waiting</span>'
          '<span class="when">runs weekly &middot; or on deploy</span></div>'
          + arrow_row(ing) +
          '<p class="wfnote"><b>Fails safely.</b> If a crawl breaks, the store keeps the '
          'last good copy and the assistant carries on answering from it.</p>'
        '</div>'
        '<div class="lane store"><div class="lane-hd"><span class="num">2</span>'
          '<h4>The store in the middle</h4>'
          '<span class="sub">the only thing the two workflows share</span>'
          '<span class="when">ours &middot; inspectable</span></div>'
          '<div class="storebar"><span class="big2">' + glyph("postgres", 30) +
          '<span><h5>Postgres &middot; pgvector</h5>'
          '<p>One table, one vector column. Every row carries the page it came from.</p>'
          '</span></span>'
          '<span class="cols3">'
            '<span class="fact"><b>~180</b>pieces</span>'
            '<span class="fact"><b>~5 MB</b>on disk</span>'
            '<span class="fact"><b>&lt;50 ms</b>a search</span>'
            '<span class="fact"><b>SQL</b>to audit</span>'
          '</span></div>'
        '</div>'
        '<div class="lane answer"><div class="lane-hd"><span class="num">3</span>'
          '<h4>Workflow two &mdash; take the question out</h4>'
          '<span class="sub">a visitor is waiting</span>'
          '<span class="when">runs per question</span></div>'
          + arrow_row(ans) +
          '<p class="wfnote"><b>The fence.</b> Claude only ever sees the pieces the search '
          'returned. If nothing clears the relevance floor the model is never called at all, '
          'and the visitor gets the standard reply.</p>'
        '</div>'
      '</div>')


def wf_timeline():
    segs = [("8%",  "#7d4b8b", "Validate",        "40 ms"),
            ("10%", "#2f6fd0", "Embed question",  "~120 ms"),
            ("7%",  "#336791", "Search",          "&lt;50 ms"),
            ("63%", "#d97757", "Claude writes the answer", "1.8 &ndash; 2.6 s"),
            ("12%", "#885577", "Shape &amp; respond", "~90 ms")]
    bar = "".join(f'<span class="seg" style="width:{w};background:{c}">{t}'
                  f'<em>{d}</em></span>' for w, c, t, d in segs)
    return (chrome("One question, second by second", plain=True) +
      '<div class="tl"><h6>Where the 2&ndash;4 seconds actually go</h6>'
      f'<div class="tlrow">{bar}</div>'
      '<div class="tlaxis"><span>0 s</span><span>1 s</span><span>2 s</span><span>3 s</span></div>'
      '<p class="tlnote"><b>Retrieval is not the slow part.</b> Turning the question into '
      'numbers and finding the right paragraphs takes under a fifth of a second between them; '
      'almost all of the wait is the model writing. That is why the dots on screen should turn '
      'into a line of text after 1.5 seconds &mdash; and why tuning retrieval buys accuracy, '
      'not speed.</p></div>')


# ===================================================== 16 · THE SIX LAYERS ===
FENCE_CSS = '''
.fence{background:#fbfcfd;padding:20px 22px 22px}
.fence h6{margin:0 0 14px;font:600 11.5px Inter;letter-spacing:.1em;text-transform:uppercase;
  color:#8d94a1}
.gates{display:flex;align-items:stretch;gap:0}
.endcap{display:flex;flex-direction:column;justify-content:center;gap:3px;flex:none;
  width:112px;padding:12px 13px;border-radius:10px;font:600 12px Inter;color:#16202b}
.endcap.in{background:#eaf4fb;border:1.5px solid #b9d8ef}
.endcap.out{background:#e9f7f1;border:1.5px solid #a9ddc6}
.endcap em{font:400 10.5px "JetBrains Mono",monospace;color:#6b7684;font-style:normal}
.gate{flex:1;min-width:0;background:#fff;border:1.5px solid #dbdfe7;border-radius:10px;
  padding:11px 12px;margin:0 4px;box-shadow:0 1px 3px rgba(20,25,35,.06);position:relative}
.gate .gn{position:absolute;top:-9px;left:11px;width:19px;height:19px;border-radius:6px;
  background:#0d8f80;color:#fff;font:700 11px/19px Inter;text-align:center}
.gate b{display:block;font:700 12px Inter;color:#16202b;margin:5px 0 4px;line-height:1.28}
.gate p{margin:0;font:400 10.5px/1.45 Inter;color:#5b6472}
.gate .where{display:inline-block;margin-top:7px;font:600 9px "JetBrains Mono",monospace;
  letter-spacing:.08em;text-transform:uppercase;border-radius:4px;padding:2px 6px}
.gate .where.wf{background:#e6f2fb;color:#2f6fd0}
.gate .where.pr{background:#f3eefc;color:#7a5bd6}
.fnote{font:400 11.5px/1.6 Inter;color:#5b6472;margin:14px 0 0;max-width:80ch}
.fnote b{color:#16202b}

.zones{display:flex;align-items:stretch;gap:0;background:#fbfcfd;padding:22px 22px 20px}
.zone{flex:1;border:1.5px solid #dbdfe7;border-radius:12px;background:#fff;padding:14px 16px}
.zone.public{border-style:dashed;background:#fdfcf7}
.zone.secret{border-color:#a9ddc6;background:#f6fcf9}
.zone h5{margin:0 0 3px;font:700 13.5px Inter;color:#16202b}
.zone .tagline{font:500 10px "JetBrains Mono",monospace;letter-spacing:.08em;
  text-transform:uppercase;color:#8d94a1;display:block;margin-bottom:10px}
.zline{display:flex;align-items:center;gap:8px;font:400 11.5px Inter;color:#3d4654;
  padding:5px 0;border-bottom:1px dashed #eef1f5}
.zline:last-child{border-bottom:none}
.zline .ic{width:16px;height:16px;flex:none;display:block}
.zline .ic svg{width:100%;height:100%;display:block}
.zarrow{flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:0 10px;color:#8d94a1;font:500 9.5px "JetBrains Mono",monospace;text-align:center}
.zarrow .a{font-size:19px;color:#c2c8d2;line-height:1}
'''
CSS += FENCE_CSS

LAYERS = [
 ("Only retrieved text", "The model is handed the paragraphs the search returned and nothing "
  "else — it is never asked to answer from what it knows.", "wf", "workflow"),
 ("Instructions with a boundary", "What it is, what it may discuss, what it must not, and what "
  "to say at the edge.", "pr", "prompt"),
 ("Must name its page", "A claim with no page behind it is, by definition, not on our website.",
  "pr", "prompt"),
 ("The relevance floor", "Nothing scores high enough → the standard reply, and the model is "
  "never called.", "wf", "workflow"),
 ("One scripted “no”", "The same sentence every time, offering the human route. Countable in "
  "the log.", "pr", "prompt"),
 ("Input is data, not orders", "Visitor words are wrapped in tags; anything inside claiming to "
  "change the rules is ignored.", "wf", "both"),
]


def wf_fence():
    gates = ""
    for i, (name, what, cls, where) in enumerate(LAYERS, 1):
        gates += (f'<div class="gate"><span class="gn">{i}</span><b>{name}</b>'
                  f'<p>{what}</p><span class="where {cls}">{where}</span></div>')
    return (chrome("Six layers, and where each one lives", plain=True) +
      '<div class="fence"><h6>What a question passes through before it becomes an answer</h6>'
      '<div class="gates">'
        '<div class="endcap in">A question<em>from anyone</em></div>'
        f'{gates}'
        '<div class="endcap out">An answer<em>+ its page</em></div>'
      '</div>'
      '<p class="fnote"><b>No single one of these is the fence.</b> Three live in the workflow, '
      'where they cannot be argued with, and three live in the instructions, where they can be '
      'read and improved. The failure to expect is not a jailbreak getting through — it is '
      'layer 2 being drawn too tight and refusing good questions.</p></div>')


# ================================================ 17 · HOW THE PANEL CONNECTS =
def wf_connect():
    def line(kind, txt):
        return f'<div class="zline">{glyph(kind, 16)}{txt}</div>'
    return (chrome("Connecting the panel to n8n", plain=True) +
      '<div class="zones">'
        '<div class="zone public"><h5>The visitor&rsquo;s browser</h5>'
        '<span class="tagline">assume everything here is public</span>'
        + line("form", "The Ask AI panel, on kleza.io")
        + line("doc", "The question, the session id, the page")
        + line("shield", "No keys of any kind")
        + '</div>'
        '<div class="zarrow"><span class="a">&#10142;</span>HTTPS<br>POST</div>'
        '<div class="zone"><h5>Our host &middot; Hostinger</h5>'
        '<span class="tagline">30 lines of PHP</span>'
        + line("code", "api/ask.php forwards the request")
        + line("shield", "Adds the shared secret")
        + line("bell", "Throttles abuse before n8n is touched")
        + '</div>'
        '<div class="zarrow"><span class="a">&#10142;</span>secret<br>header</div>'
        '<div class="zone secret"><h5>n8n</h5>'
        '<span class="tagline">where the keys live</span>'
        + line("webhook", "Webhook checks the secret")
        + line("postgres", "Reads pgvector &middot; our own database")
        + line("claude", "Calls Anthropic with our key")
        + '</div>'
      '</div>')


# ==================================================== 18 · THE ERROR WORKFLOW =
def wf_error():
    W, H = 1100, 400
    y = 110
    trig = dict(x=36,  y=y, kind="bell",   title="Error Trigger",
                sub="any workflow, any node", trig=True)
    fmt  = dict(x=246, y=y, kind="code",   title="What broke, in one line",
                sub="workflow · node · error")
    slack= dict(x=456, y=y, kind="slack",  title="Post to #alerts", sub="within seconds")
    log  = dict(x=666, y=y, kind="sheets", title="Append to the log", sub="so it can be counted")
    nodes = [trig, fmt, slack, log]
    ws = "".join(wire(a, b) for a, b in zip(nodes, nodes[1:]))
    extra = sticky(246, 265, 560, "Build this once, point everything at it",
                   "Set it as the error workflow on every other workflow. Without it a broken "
                   "booking or a dead crawl is silent &mdash; you find out when somebody asks why "
                   "nobody called them back.")
    return chrome("Kleza &mdash; when something breaks") + canvas(W, H, nodes, ws, extra)


SCREENS = [
 ("rag-05-fence",       1240, wf_fence),
 ("n8n-13-connect",     1160, wf_connect),
 ("n8n-14-error",       1100, wf_error),
 ("rag-03-architecture", 1240, wf_arch),
 ("rag-04-timeline",   1100, wf_timeline),
 ("n8n-01-ask",        1160, wf_ask),
 ("n8n-01-ask-a",      1160, lambda: wf_ask(annotated=True)),
 ("n8n-02-refresh",    1100, wf_refresh),
 ("n8n-03-demo",       1100, wf_demo),
 ("n8n-03-demo-a",     1100, lambda: wf_demo(annotated=True)),
 ("n8n-04-catalogue",  1180, wf_catalogue),
 ("n8n-05-anatomy",    1100, wf_anatomy),
 ("n8n-06-executions", 1180, wf_executions),
 ("n8n-07-node",       1180, wf_node),
 ("n8n-08-credentials",1180, wf_credentials),
 ("n8n-09-failed",     1100, wf_failed),
 ("n8n-10-email",      740,  wf_email),
 ("n8n-11-index",      1100, wf_index),
 ("rag-01-chunks",     1100, wf_chunks),
 ("rag-02-retrieve",   1100, wf_retrieve),
 ("n8n-12-alert",      740,  wf_alert),
]

only = set(sys.argv[1:])
ok = 0
for i, (name, w, build) in enumerate(SCREENS):
    if only and name not in only:
        continue
    f = os.path.join(TMP, name + ".html")
    open(f, "w", encoding="utf-8").write(page(build(), w))
    png = os.path.join(OUT, name + ".png")
    if os.path.exists(png):
        os.remove(png)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--user-data-dir={os.path.join(TMP, 'n8nprof%d' % i)}",
                    f"--window-size={w},2200", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--virtual-time-budget=4000",
                    f"--screenshot={png}", "file:///" + f.replace("\\", "/")],
                   capture_output=True)
    for _ in range(60):
        if os.path.exists(png) and os.path.getsize(png) > 0:
            break
        time.sleep(0.25)
    if not os.path.exists(png):
        print(f"{name:20} FAIL"); continue

    # trim the empty page below the drawing, then flatten the colour table:
    # these are flat-colour pictures, so a 256-colour palette is lossless to
    # the eye and roughly quarters the file the PDF has to carry.
    from PIL import Image, ImageChops
    im = None
    for _ in range(40):                     # OneDrive keeps the file locked for
        try:                                # a moment after Chrome closes it
            im = Image.open(png).convert("RGB")
            break
        except (PermissionError, OSError):
            time.sleep(0.25)
    if im is None:
        print(f"{name:20} LOCKED"); continue
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).getbbox()
    if bb:
        im = im.crop((0, 0, im.width, min(im.height, bb[3] + 18)))
    im.convert("P", palette=Image.ADAPTIVE, colors=256).save(png, optimize=True)
    ok += 1
    print(f"{name:20} OK  {os.path.getsize(png):>8}")
print("done", ok, "/", len(SCREENS))
