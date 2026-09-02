# Regenerates docs/ui/*.png from the live component styles.
#   python docs/gen-ui-screens.py                 # all of them
#   python docs/gen-ui-screens.py 03-home         # just one
#
# Each Ask AI state is rebuilt from the component's own markup (see
# app/_components/VoiceAssistant.tsx) and styled with the real .ai-va-* rules
# read straight out of app/globals.css, then captured in headless Chrome at 2x.
# Two variants per state: a clean shot, and an annotated one whose numbered
# badges are positioned from the live DOM (getBoundingClientRect), so a badge
# always lands on the real control.
#
# The CSS is sliced by comment markers, not line numbers, so it survives the
# stylesheet growing: design tokens from the top of the file, the assistant
# block, and the brand-palette overrides at the bottom (which is what makes the
# launcher blue and the buttons green).

import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "docs", "ui")
TMP  = os.path.join(ROOT, "docs", ".build")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

lines = open(os.path.join(ROOT, "app", "globals.css"), encoding="utf-8").read().splitlines()

def find(marker, start=0):
    for i in range(start, len(lines)):
        if marker in lines[i]:
            return i
    raise SystemExit("marker not found in app/globals.css: " + marker)

def comment_start(i):                      # step back onto the comment opener
    while i > 0 and "/*" not in lines[i]:
        i -= 1
    return i

TOKENS_END = comment_start(find("Eyebrow / monospace label"))
VA_START   = comment_start(find("KLEZA AI ASSISTANT"))
VA_END     = comment_start(find("BRAND PALETTE OVERRIDES"))

base = "\n".join(lines[0:TOKENS_END])          # :root tokens + resets
va   = "\n".join(lines[VA_START:VA_END])       # the assistant block
ovr  = "\n".join(lines[VA_END:])               # palette overrides (blue fab etc.)

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1'
         '&family=JetBrains+Mono:wght@400;500&display=swap">')

SPARKLE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
  '<path d="M10.5 4.5C10.5 9.2 14.3 13 19 13C14.3 13 10.5 16.8 10.5 21.5C10.5 16.8 6.7 13 2 13C6.7 13 10.5 9.2 10.5 4.5Z"/>'
  '<path d="M18.5 2.5C18.5 4.2 19.8 5.5 21.5 5.5C19.8 5.5 18.5 6.8 18.5 8.5C18.5 6.8 17.2 5.5 15.5 5.5C17.2 5.5 18.5 4.2 18.5 2.5Z"/></svg>')
MIC = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
  '<path d="M12 1.5a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0v-7a3 3 0 0 0-3-3z"/><path d="M5 11a7 7 0 0 0 14 0"/>'
  '<line x1="12" y1="18" x2="12" y2="22"/><line x1="8" y1="22" x2="16" y2="22"/></svg>')
X = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">'
     '<line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>')
NEW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M21 12a9 9 0 1 1-3.5-7.1"/><polyline points="21 3 21 9 15 9"/></svg>')
SEND = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>')
ENTER = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
         '<polyline points="9 10 4 15 9 20"/><path d="M20 4v7a4 4 0 0 1-4 4H4"/></svg>')
CAL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
       '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>'
       '<line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>')
CHATIC = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
  '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>')
CHEVL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
         '<polyline points="15 18 9 12 15 6"/></svg>')
CHEVR = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
         '<polyline points="9 18 15 12 9 6"/></svg>')

# ------------------------------------------------------------- the launcher --
def dock(teaser=False):
    t = " show" if teaser else ""
    return f'''<div class="ai-va-dock">
  <div class="ai-va-teaser{t}" role="status">
    <button class="ai-va-teaser-x" aria-label="Dismiss"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg></button>
    <button class="ai-va-teaser-body"><span class="ai-va-teaser-wave">&#128075;</span><span><strong>Need a hand?</strong> Ask me anything about Kleza &mdash; our products, services or how to reach us.</span></button>
  </div>
  <button class="ai-va-fab" aria-label="Open Kleza AI assistant">
    <span class="ai-va-fab-ring"></span><span class="ai-va-fab-ring two"></span>
    <span class="ai-va-fab-icon">{SPARKLE}</span><span class="ai-va-fab-label">Ask&nbsp;AI</span>
  </button>
</div>'''

# ----------------------------------------------------------------- the panel --
def head(new=False):
    n = f'<button class="ai-va-new" aria-label="New conversation">{NEW}</button>' if new else ''
    return f'''<div class="ai-va-head"><span class="ai-va-brand">
    <span class="ai-va-brand-ic">{SPARKLE}</span><span class="ai-va-brand-name">Kleza AI Assistant</span></span>
    {n}<button class="ai-va-close" aria-label="Close">{X}</button></div>'''

def foot(text="", listening=False):
    mic = " on" if listening else ""
    return f'''<form class="ai-va-foot">
  <textarea rows="1" placeholder="Ask anything&hellip;" aria-label="Ask anything">{text}</textarea>
  <span class="ai-va-enter">{ENTER}</span>
  <button type="button" class="ai-va-foot-mic{mic}" aria-label="Dictate your question">{MIC}</button>
  <button type="submit" class="ai-va-send" aria-label="Send">{SEND}</button></form>'''

ACTIONS = (f'<div class="ai-va-actions">'
           f'<button class="ai-va-act primary">{CAL}Book Demo</button>'
           f'<button class="ai-va-act">{CHATIC}Start Chat</button></div>')

def user(t):
    return f'<div class="ai-va-msg user"><div class="ai-va-bubble">{t}</div></div>'

def ai(t):
    return (f'<div class="ai-va-msg ai"><span class="ai-va-avatar">{SPARKLE}</span>'
            f'<div class="ai-va-ai-body"><div class="ai-va-bubble">{t}</div></div></div>')

TYPING = (f'<div class="ai-va-msg ai"><span class="ai-va-avatar">{SPARKLE}</span>'
          '<div class="ai-va-typing"><span></span><span></span><span></span></div></div>')

def chat(msgs=()):
    return f'<div class="ai-va-scroll"><div class="ai-va-chat">{"".join(msgs)}</div></div>'

def panel(body, new=False, actions=False, footer_text="", listening=False, demo=False):
    cls = "ai-va-panel demo" if demo else "ai-va-panel"
    return (f'<div class="ai-va-overlay open"><div class="{cls}" role="dialog" aria-modal="true">'
            f'{head(new)}{body}{ACTIONS if actions else ""}'
            f'{foot(footer_text, listening)}</div></div>')

# ------------------------------------------------------------ book a demo ----
def cal_grid(sel=None):
    # July 2026: the 1st is a Wednesday, so three blank cells lead the month.
    cells = ['<span></span>'] * 3
    for d in range(1, 32):
        c = "ai-va-cal-day" + (" sel" if d == sel else "")
        dis = ' disabled' if d < 6 or (d + 2) % 7 == 0 else ''
        cells.append(f'<button class="{c}"{dis}>{d}</button>')
    dow = "".join(f"<span>{d}</span>" for d in "SMTWTFS")
    return (f'<div class="ai-va-cal-dow">{dow}</div>'
            f'<div class="ai-va-cal-grid" role="grid">{"".join(cells)}</div>')

DEMO_TOP = (f'<div class="ai-va-demo-top">'
            f'<button class="ai-va-demo-back" aria-label="Back to chat">{CHEVL}</button>'
            f'<strong>Book a demo</strong></div>')

def demo_date(sel_day=15, sel_slot="13:30"):
    slots = "".join(f'<button class="ai-va-slot{" sel" if s == sel_slot else ""}">{s}</button>'
                    for s in ["09:30", "11:00", "13:30", "15:00", "16:30"])
    return ('<div class="ai-va-scroll"><div class="ai-va-demo">' + DEMO_TOP +
            f'<div class="ai-va-cal-head"><button aria-label="Previous month">{CHEVL}</button>'
            f'<span>July 2026</span><button aria-label="Next month">{CHEVR}</button></div>'
            + cal_grid(sel_day) +
            '<div class="ai-va-demo-label">Pick a time</div>'
            f'<div class="ai-va-slots">{slots}</div>'
            '<button class="ai-va-demo-confirm">Continue</button></div></div>')

POPULAR = ["What does Kleza do?", "Tell me about Voica",
           "Do you do SEO?", "Where are your offices?"]

def home_proposed():
    """§04's fix, built only from styling the sheet already carries."""
    pills = "".join(f'<button class="ai-va-slot">{q}</button>' for q in POPULAR)
    return ('<div class="ai-va-scroll"><div class="ai-va-home" style="padding-bottom:6px">'
            '<p class="ai-va-greet">Hi! How can I help you today?</p>'
            '<p class="ai-va-greet-sub">Ask me about our AI products, our services, '
            'or how to reach the right person.</p>'
            '<div class="ai-va-section">Popular</div>'
            f'<div class="ai-va-slots">{pills}</div>'
            '</div></div>')

def ai_sourced(t, src):
    """An answer with the one line §05 asks for."""
    return (f'<div class="ai-va-msg ai"><span class="ai-va-avatar">{SPARKLE}</span>'
            f'<div class="ai-va-ai-body"><div class="ai-va-bubble">{t}</div>'
            f'<span style="font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;'
            f'color:var(--muted-2);padding-left:2px">From our {src} page</span>'
            f'</div></div>')

def slot_taken():
    pills = "".join(f'<button class="ai-va-slot">{s}</button>'
                    for s in ["Wed 15:00", "Thu 09:30", "Thu 13:30"])
    return ('<div class="ai-va-scroll"><div class="ai-va-chat">'
            + ai("That time was taken while you were filling this in &mdash; sorry. "
                 "Here are the next three that are free, or email sales@kleza.io and "
                 "we&rsquo;ll find one that works.")
            + f'<div class="ai-va-slots" style="padding-left:37px">{pills}</div>'
            '</div></div>')

WEEK_CSS = '''
.wk-nav{display:flex;align-items:center;justify-content:space-between;margin:2px 0 10px;
  font-family:var(--sans);font-weight:600;font-size:13.5px;color:var(--ink)}
.wk-nav button{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;color:var(--muted)}
.wk-nav svg{width:14px;height:14px}
.wk-row{display:grid;grid-template-columns:52px 1fr;gap:10px;align-items:center;
  padding:7px 0;border-bottom:1px solid var(--line)}
.wk-row:last-of-type{border-bottom:none}
.wk-day{font-family:var(--sans);font-size:12px;line-height:1.2;color:var(--ink)}
.wk-day b{display:block;font-weight:700;font-size:13px}
.wk-day span{color:var(--muted-2);font-size:11px}
.ai-va-slot.gone{color:var(--line-2);border-color:var(--line-2);text-decoration:line-through;
  background:transparent}
.wk-none{font-family:var(--sans);font-size:12px;color:var(--muted-2);font-style:italic}
.wk-foot{margin-top:12px;font-family:var(--sans);font-size:11.5px;color:var(--muted-2);
  text-align:center}
'''

# (day, [(time, taken?), ...]) — one working week, as the calendar really is
WEEK = [
 ("Mon", "14 Jul", [("09:30", True), ("11:00", False), ("13:30", True), ("15:00", False)]),
 ("Tue", "15 Jul", [("09:30", True), ("11:00", True), ("13:30", True), ("15:00", True)]),
 ("Wed", "16 Jul", [("09:30", False), ("11:00", False), ("13:30", False), ("15:00", True)]),
 ("Thu", "17 Jul", [("09:30", True), ("11:00", False), ("13:30", False), ("15:00", False)]),
 ("Fri", "18 Jul", [("09:30", True), ("11:00", True), ("13:30", False), ("15:00", True)]),
]

def week_nav(label):
    return (f'<div class="wk-nav"><button aria-label="Previous week">{CHEVL}</button>'
            f'<span>{label}</span>'
            f'<button aria-label="Next week">{CHEVR}</button></div>')

def demo_week(full=False, sel="13:30", sel_day=2):
    rows = ""
    for i, (d, dt, slots) in enumerate(WEEK):
        if full:
            cells = '<span class="wk-none">fully booked</span>'
        else:
            free = [(t, taken) for t, taken in slots]
            cells = "".join(
                f'<button class="ai-va-slot{" gone" if taken else ""}'
                f'{" sel" if (not taken and i == sel_day and t == sel) else ""}">{t}</button>'
                for t, taken in free)
            if all(taken for _, taken in slots):
                cells = '<span class="wk-none">fully booked</span>'
            else:
                cells = f'<div class="ai-va-slots">{cells}</div>'
        rows += (f'<div class="wk-row"><span class="wk-day"><b>{d}</b>'
                 f'<span>{dt}</span></span>{cells}</div>')
    foot = ('<button class="ai-va-demo-confirm">Next week has 14 free &rsaquo;</button>'
            if full else '<button class="ai-va-demo-confirm">Continue</button>')
    note = ("Checked against the sales calendar a second ago."
            if not full else "Nothing free this week &mdash; so we do not pretend there is.")
    return (f'<style>{WEEK_CSS}</style>'
            '<div class="ai-va-scroll"><div class="ai-va-demo">' + DEMO_TOP +
            week_nav("14 &ndash; 18 July 2026") + rows +
            f'{foot}<p class="wk-foot">{note}</p></div></div>')

def demo_details(filled=True):
    v = (("Priya Raghavan", "priya@northstarcare.com", "+1 913 555 0148") if filled
         else ("", "", ""))
    ph = ("Full name", "Work email", "Phone number")
    fields = "".join(
        f'<input class="ai-va-field" value="{v[i]}" placeholder="{ph[i]}">' for i in range(3))
    return ('<div class="ai-va-scroll"><div class="ai-va-demo">' + DEMO_TOP +
            '<div class="ai-va-demo-when"><span>Wed, 15 Jul at 13:30</span>'
            '<button>Change</button></div>'
            '<div class="ai-va-demo-label">Your details</div>'
            f'<div class="ai-va-demo-fields">{fields}</div>'
            '<button class="ai-va-demo-confirm">Confirm demo</button></div></div>')

# ------------------------------------------------------------- the harness ---
TIGHT = '''
.pgbg{display:none}
.ai-va-overlay{position:static;padding:34px;opacity:1;justify-content:flex-start}
.ai-va-panel{transform:none;opacity:1;
  box-shadow:0 18px 40px -22px rgba(10,19,22,.35)}
'''

CALLOUT_CSS = '''
.co{position:absolute;width:26px;height:26px;border-radius:50%;
  background:#0d8f80;color:#fff;font:700 14px/26px var(--sans);text-align:center;
  box-shadow:0 0 0 3px #fff,0 3px 8px rgba(10,30,36,.3);z-index:9999}
'''
CALLOUT_JS = '''
<script>
(function(){
  var spec = %s;
  spec.forEach(function(s){
    var el = document.querySelectorAll(s[0])[s[3] || 0];
    if (!el) return;
    var r = el.getBoundingClientRect();
    var b = document.createElement('div');
    b.className = 'co'; b.textContent = s[1];
    var y = r.top + window.scrollY + Math.min(14, r.height / 2) - 13;
    var x = r.left + window.scrollX - 31;
    if (s[2] === 'right') x = r.right + window.scrollX + 5;
    if (s[2] === 'mid')   { x = r.left + window.scrollX + r.width / 2 - 13;
                            y = r.top + window.scrollY + r.height / 2 - 13; }
    if (s[2] === 'top' || s[2] === 'bottom') {
      x = r.left + window.scrollX + r.width / 2 - 13;
      y = (s[2] === 'top') ? r.top + window.scrollY - 33
                           : r.bottom + window.scrollY + 7;
    }
    b.style.left = Math.round(x) + 'px';
    b.style.top  = Math.round(y) + 'px';
    document.body.appendChild(b);
  });
})();
</script>'''

def page(body, w, tight=False, callouts=None):
    extra = (TIGHT if tight else "") + CALLOUT_CSS
    js = (CALLOUT_JS % repr(callouts).replace("'", '"')) if callouts else ""
    size = "" if tight else "height:100%;overflow:hidden;"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">{FONTS}
<style>{base}
{va}
{ovr}
html,body{{margin:0;padding:0}}
body{{width:{w}px;{size}background:var(--bg);position:relative}}
button{{font-family:var(--sans);border:none;background:none;cursor:pointer;color:inherit;padding:0}}
input,textarea{{font-family:var(--sans)}}
.pgbg{{position:fixed;inset:0;padding:28px 30px}}
.pgbg h4{{font-family:var(--serif);font-size:30px;color:#c9d6d9;margin:0 0 8px;font-weight:400}}
.pgbg p{{font-size:13px;color:#d4dee0;margin:0;max-width:300px;line-height:1.6}}
{extra}</style></head><body>
<div class="pgbg"><h4>Intelligence, engineered</h4><p>Page content sits behind the assistant. The overlay background is transparent, so the site stays visible and readable.</p></div>
{body}{js}</body></html>'''

# ------------------------------------------------------------ the content ----
A_VOICA = ("Voica is our voice-intelligence product &mdash; real-time conversational AI for "
           "patient intake, support, and care coordination. It handles natural turn-taking "
           "and live transcription, and escalates to a human the moment it&rsquo;s unsure.")
A_OFFICES = ("We operate from two offices. In the USA we&rsquo;re in Overland Park, Kansas, and "
             "in India we&rsquo;re in Madhapur, HITEC City, Hyderabad. Our Hyderabad centre "
             "coordinates engineering and operations for clients.")
A_FALLBACK = ("I can tell you about Kleza&rsquo;s AI products, AI services, enterprise services, "
              "resources, careers, or our contact details and locations. What would you like "
              "to know?")
A_REFUSAL = ("I can only help with questions about Kleza &mdash; our products, services, company "
             "and how to get in touch. For anything else, email sales@kleza.io and a human "
             "will help.")
A_BOOKED = ("Thanks Priya &mdash; your demo is requested for Wed, 15 Jul at 13:30. We&rsquo;ll send "
            "the confirmation and joining details to priya@northstarcare.com, and call you if "
            "we need anything before then.")

STRIP_CSS = '''
.strip{display:flex;align-items:stretch;gap:0}
.strip .cell{flex:none;display:flex;flex-direction:column}
.strip .cap{margin-top:auto;font:700 32px var(--sans);color:#0d8f80;text-align:center;
  padding:10px 22px 0;letter-spacing:.01em;line-height:1.25}
.strip .cap em{display:block;font-style:normal;font-weight:400;font-size:25px;
  color:var(--muted-2);margin-top:6px;line-height:1.3}
'''

def strip(cells):
    """A filmstrip of panels, for the opening spread."""
    out = []
    for body, title, sub in cells:
        out.append(f'<div class="cell">{body}'
                   f'<div class="cap">{title}<em>{sub}</em></div></div>')
    return f'<style>{STRIP_CSS}</style><div class="strip">{"".join(out)}</div>'

CHAT_ANSWER   = chat([user("What does Voica do?"), ai(A_VOICA)])
CHAT_THINK    = chat([user("Do you work with pharmacies?"), TYPING])
CHAT_FALLBACK = chat([user("Do you work with hospitals in Texas?"), ai(A_FALLBACK)])
CHAT_REFUSAL  = chat([user("What&rsquo;s the weather in Hyderabad?"), ai(A_REFUSAL)])
CHAT_BOOKED   = chat([ai(A_BOOKED)])
CHAT_MOBILE   = chat([user("Where are your offices?"), ai(A_OFFICES)])

# name, viewport width, tight?, body, callouts: [selector, label, side, nth?]
STATES = [
 ("01-launcher",   560, False, dock(), None),
 ("01-launcher-a", 560, False, dock(),
    [[".ai-va-fab", "1", "left"], [".ai-va-fab-label", "2", "right"]]),

 ("02-nudge",      560, False, dock(teaser=True), None),
 ("02-nudge-a",    560, False, dock(teaser=True),
    [[".ai-va-teaser-body", "1", "left"], [".ai-va-teaser-x", "2", "right"],
     [".ai-va-fab", "3", "left"]]),

 ("03-home",   440, True, panel(chat(), actions=True), None),
 ("03-home-a", 440, True, panel(chat(), actions=True),
    [[".ai-va-brand", "1", "left"], [".ai-va-close", "2", "right"],
     [".ai-va-scroll", "3", "mid"], [".ai-va-act.primary", "4", "left"],
     [".ai-va-act", "5", "right", 1], [".ai-va-foot textarea", "6", "left"],
     [".ai-va-foot-mic", "7", "top"], [".ai-va-send", "8", "right"]]),

 ("04-chat",   440, True, panel(CHAT_ANSWER, new=True), None),
 ("04-chat-a", 440, True, panel(CHAT_ANSWER, new=True),
    [[".ai-va-new", "1", "left"], [".ai-va-close", "2", "right"],
     [".ai-va-msg.user .ai-va-bubble", "3", "left"],
     [".ai-va-msg.ai", "4", "left"]]),

 ("05-thinking",   440, True, panel(CHAT_THINK, new=True), None),
 ("05-thinking-a", 440, True, panel(CHAT_THINK, new=True),
    [[".ai-va-typing", "1", "left"]]),

 ("06-dictation",   440, True,
    panel(chat(), actions=True, footer_text="where are your offices",
          listening=True), None),
 ("06-dictation-a", 440, True,
    panel(chat(), actions=True, footer_text="where are your offices",
          listening=True),
    [[".ai-va-foot-mic", "1", "top"], [".ai-va-foot textarea", "2", "left"],
     [".ai-va-send", "3", "right"]]),

 ("07-fallback",   440, True, panel(CHAT_FALLBACK, new=True), None),
 ("07-fallback-a", 440, True, panel(CHAT_FALLBACK, new=True),
    [[".ai-va-msg.ai", "1", "left"]]),

 ("08-demo-date",   440, True, panel(demo_date(), demo=True), None),
 ("08-demo-date-a", 440, True, panel(demo_date(), demo=True),
    [[".ai-va-demo-back", "1", "left"], [".ai-va-cal-head", "2", "left"],
     [".ai-va-cal-day.sel", "3", "right"], [".ai-va-slot.sel", "4", "top"],
     [".ai-va-demo-confirm", "5", "left"]]),

 ("09-demo-details",   440, True, panel(demo_details(), demo=True), None),
 ("09-demo-details-a", 440, True, panel(demo_details(), demo=True),
    [[".ai-va-demo-when", "1", "left"], [".ai-va-demo-fields", "2", "left"],
     [".ai-va-demo-confirm", "3", "left"]]),

 ("10-demo-booked", 440, True, panel(CHAT_BOOKED, new=True), None),

 ("11-refusal",     440, True, panel(CHAT_REFUSAL, new=True), None),
 ("12-mobile",      390, True, panel(CHAT_MOBILE, new=True), None),

 # ---- proposals: what the fixes in §12 actually look like ----
 ("13-home-proposed",   440, True, panel(home_proposed(), actions=True), None),
 ("13-home-proposed-a", 440, True, panel(home_proposed(), actions=True),
    [[".ai-va-greet", "1", "left"], [".ai-va-section", "2", "left"],
     [".ai-va-slots", "3", "left"], [".ai-va-act.primary", "4", "left"]]),

 ("14-answer-sourced", 440, True,
    panel(chat([user("What does Voica do?"), ai_sourced(A_VOICA, "Voica")]), new=True), None),

 ("15-slot-taken",  440, True, panel(slot_taken(), new=True), None),
 ("16-mobile-demo", 390, True, panel(demo_date(), demo=True), None),

 # ---- real availability, once the calendar is connected ----
 ("17-demo-week",   440, True, panel(demo_week(), demo=True), None),
 ("17-demo-week-a", 440, True, panel(demo_week(), demo=True),
    [[".wk-nav", "1", "left"], [".ai-va-slot.gone", "2", "top"],
     [".ai-va-slot.sel", "3", "top"], [".ai-va-demo-confirm", "4", "left"]]),
 ("18-demo-week-full", 440, True, panel(demo_week(full=True), demo=True), None),

 # ---- the opening filmstrip ----
 ("00-journey", 2340, True, strip([
     (panel(chat(), actions=True),        "1 &middot; It opens",   "empty, and two buttons"),
     (panel(CHAT_THINK, new=True),        "2 &middot; They ask",   "typed or dictated"),
     (panel(CHAT_ANSWER, new=True),       "3 &middot; It answers", "text, and nothing else"),
     (panel(demo_date(), demo=True),      "4 &middot; Or they book", "date, then time"),
     (panel(CHAT_BOOKED, new=True),       "5 &middot; And are told", "&hellip;nothing is sent"),
   ]), None),
]

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
only = set(sys.argv[1:])
ok = 0
for i, (name, w, tight, body, co) in enumerate(STATES):
    if only and name not in only:
        continue
    f = os.path.join(TMP, name + ".html")
    open(f, "w", encoding="utf-8").write(page(body, w, tight, co))
    png = os.path.join(OUT, name + ".png")
    if os.path.exists(png):
        os.remove(png)
    h = 1700 if tight else (340 if name.startswith("02") else 300)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--user-data-dir={os.path.join(TMP, 'prof%d' % i)}",
                    f"--window-size={w},{h}", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--virtual-time-budget=3000",
                    f"--screenshot={png}", "file:///" + f.replace("\\", "/")],
                   capture_output=True)
    for _ in range(40):
        if os.path.exists(png) and os.path.getsize(png) > 0:
            break
        time.sleep(0.25)
    if not os.path.exists(png):
        print(f"{name:20} FAIL"); continue
    if tight:                                   # trim the flat background
        from PIL import Image, ImageChops
        im = None
        for _ in range(40):                     # OneDrive holds the file briefly
            try:
                im = Image.open(png).convert("RGB")
                break
            except (PermissionError, OSError):
                time.sleep(0.25)
        if im is None:
            print(f"{name:20} LOCKED"); continue
        bg = im.getpixel((1, 1))
        bb = ImageChops.difference(im, Image.new("RGB", im.size, bg)).getbbox()
        if bb:
            p = 14
            im = im.crop((max(0, bb[0] - p), max(0, bb[1] - p),
                          min(im.width, bb[2] + p), min(im.height, bb[3] + p)))
        im.save(png)
    ok += 1
    print(f"{name:20} OK  {os.path.getsize(png):>8}")
print("done", ok, "/", len(STATES))
