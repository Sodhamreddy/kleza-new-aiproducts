# Embeds docs/ui/*.png into the guide and renders the PDF.
#   python docs/build-guide.py
#
# Source text:  docs/ask-ai-guide.src.html   (uses {{IMG:name}} placeholders)
# Outputs:      docs/ask-ai-guide.html       (self-contained, shareable)
#               docs/Kleza-Ask-AI-Guide.pdf  (A4, print-ready)

import base64, os, pathlib, re, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
UI   = os.path.join(DOCS, "ui")
TMP  = os.path.join(DOCS, ".build")
os.makedirs(TMP, exist_ok=True)

ALT = {
 "01-launcher":        "The Ask AI button, bottom right of every page",
 "01-launcher-a":      "The Ask AI button with its parts numbered",
 "02-nudge":           "A nudge bubble above the Ask AI button",
 "02-nudge-a":         "The nudge bubble with its parts numbered",
 "03-home":            "The assistant's first screen, empty apart from two buttons",
 "03-home-a":          "The first screen with all eight controls numbered",
 "04-chat":            "A question and its answer",
 "04-chat-a":          "The answer screen with its four controls numbered",
 "05-thinking":        "Three dots while the answer is prepared",
 "05-thinking-a":      "The thinking dots, numbered",
 "06-dictation":       "The microphone dictating into the input box",
 "06-dictation-a":     "The dictation state with its three controls numbered",
 "07-fallback":        "The catch-all reply when nothing matched",
 "07-fallback-a":      "The catch-all reply, numbered",
 "08-demo-date":       "Book a demo, step one: the calendar and time slots",
 "08-demo-date-a":     "The demo calendar with its five controls numbered",
 "09-demo-details":    "Book a demo, step two: name, email and phone",
 "09-demo-details-a":  "The demo details step with its three controls numbered",
 "10-demo-booked":     "The message shown after confirming a demo",
 "11-refusal":         "A polite refusal with a way to reach a human",
 "12-mobile":          "The assistant on a phone-sized screen",
 "00-journey":         "Five screens showing the whole assistant, side by side",
 "13-home-proposed":   "The proposed first screen, with a greeting and four questions",
 "13-home-proposed-a": "The proposed first screen with its four parts numbered",
 "14-answer-sourced":  "An answer with a line naming the page it came from",
 "15-slot-taken":      "The reply when a demo slot was taken first, offering three others",
 "16-mobile-demo":     "Booking a demo on a phone-sized screen",
 "n8n-07-node":        "An n8n node opened, showing input, settings and output",
 "n8n-08-credentials": "The n8n credential list, where every key is stored",
 "n8n-09-failed":      "A failed run, stopped at an expired calendar login",
 "n8n-10-email":       "The confirmation email the booking workflow sends",
 "rag-05-fence":       "The six safety layers a question passes through, and whether each lives in the workflow or the prompt",
 "n8n-13-connect":     "How the panel reaches n8n: browser, our PHP file, then n8n where the keys live",
 "n8n-14-error":       "The error workflow: any failure in any workflow lands in one place",
 "rag-03-architecture":"The whole system: the indexing workflow, the pgvector store, and the answering workflow",
 "rag-04-timeline":    "Where the 2-4 seconds of a question actually go",
 "n8n-01-ask":         "The answering workflow drawn on an n8n canvas",
 "n8n-01-ask-a":       "The answering workflow with its nodes numbered",
 "n8n-02-refresh":     "The content-refresh workflow on an n8n canvas",
 "n8n-03-demo":        "The book-a-demo workflow on an n8n canvas",
 "n8n-03-demo-a":      "The book-a-demo workflow with its nodes numbered",
 "n8n-04-catalogue":   "Eight workflows Kleza could run, as cards",
 "n8n-05-anatomy":     "An annotated n8n workflow explaining triggers, nodes and runs",
 "n8n-06-executions":  "The n8n executions list, showing questions and what happened",
}

src = open(os.path.join(DOCS, "ask-ai-guide.src.html"), encoding="utf-8").read()
missing = []

def embed(m):
    key = m.group(1)
    path = os.path.join(UI, key + ".png")
    if not os.path.exists(path):
        missing.append(key)
        return "<!-- missing %s -->" % key
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return '<img src="data:image/png;base64,%s" alt="%s">' % (b64, ALT.get(key, key))

out = re.sub(r"\{\{IMG:([0-9a-z\-]+)\}\}", embed, src)
if missing:
    raise SystemExit("missing screenshots: " + ", ".join(sorted(set(missing)))
                     + "\nrun: python docs/gen-ui-screens.py")

html = os.path.join(DOCS, "ask-ai-guide.html")
open(html, "w", encoding="utf-8").write(out)
print("html %.1f MB" % (os.path.getsize(html) / 1e6))

# ---------------------------------------------------------------- render ----
# Two passes: the first tells us which page each step starts on, the second
# puts those numbers in the contents list. Then the finished PDF is stamped
# with a running head and a footer — Chrome cannot do either itself.

# (id, title for the running head, a phrase that appears ONLY on that divider —
#  matching on the title alone also matches the contents list)
STEPS = [("s1", "Know the product you are changing", "in the order a visitor meets them"),
         ("s2", "Index the website into pgvector",   "nothing downstream can be tested"),
         ("s3", "Build the answering workflow",      "Build and test it inside"),
         ("s4", "Give it the fence",                 "six ordinary controls stacked together"),
         ("s5", "Connect the panel",                 "One function in the website changes"),
         ("s6", "Make Book a demo real",             "The screen already collects everything"),
         ("s7", "Watch it, then tune",               "the step that quietly gets dropped")]

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = os.path.join(DOCS, "Kleza-Ask-AI-Guide.pdf")


def render(body_html, target):
    pr = os.path.join(TMP, "guide_print.html")
    open(pr, "w", encoding="utf-8").write(
        '<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
        + body_html + "</body></html>")
    if os.path.exists(target):
        try:
            os.remove(target)
        except PermissionError:
            time.sleep(1); os.remove(target)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--user-data-dir={os.path.join(TMP, 'profpdf')}",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={target}", pathlib.Path(pr).as_uri()],
                   capture_output=True)
    for _ in range(80):
        if os.path.exists(target) and os.path.getsize(target) > 0:
            break
        time.sleep(0.5)
    return os.path.exists(target)


def step_pages(path):
    """Which page does each step divider land on? (1-based)"""
    import fitz
    d = fitz.open(path)
    found = {}
    for i in range(1, d.page_count):
        # collapse the line breaks the renderer introduced, or a marker that
        # wraps mid-phrase will never match
        text = " ".join(d[i].get_text().split())
        for sid, _title, marker in STEPS:
            if sid not in found and marker in text:
                found[sid] = i + 1
    d.close()
    return found


# pass 1 — no page numbers yet
draft = os.path.join(TMP, "draft.pdf")
if not render(re.sub(r"\{\{PAGE:s\d\}\}", "", out), draft):
    raise SystemExit("PDF FAILED (pass 1)")
pages_of = step_pages(draft)

# pass 2 — contents list carries real page numbers
final_html = re.sub(r"\{\{PAGE:(s\d)\}\}",
                    lambda m: ("&middot; p.&nbsp;%d" % pages_of[m.group(1)]
                               if m.group(1) in pages_of else ""), out)
open(html, "w", encoding="utf-8").write(
    re.sub(r"\{\{PAGE:s\d\}\}", "", out))       # web version: no page numbers
if not render(final_html, pdf):
    raise SystemExit("PDF FAILED (pass 2)")

# ------------------------------------------------------- running head + foot --
import fitz

GREY = (0.43, 0.53, 0.58)
RULE = (0.85, 0.89, 0.90)
doc = fitz.open(pdf)
n_pages = doc.page_count
# which step owns each page
owner, cur = {}, None
by_page = {v: k for k, v in pages_of.items()}
titles = {sid: t for sid, t, _m in STEPS}
for i in range(1, n_pages + 1):
    if i in by_page:
        cur = by_page[i]
    owner[i] = cur

for i in range(1, n_pages):                 # skip the cover
    page = doc[i]
    w, h = page.rect.width, page.rect.height
    L, R = 37, w - 37
    page.draw_line((L, h - 30), (R, h - 30), color=RULE, width=0.5)
    page.insert_text((L, h - 20), "Kleza · Ask AI — build guide",
                     fontname="helv", fontsize=7.5, color=GREY)
    label = "%d / %d" % (i + 1, n_pages)
    page.insert_text((R - fitz.get_text_length(label, "helv", 7.5), h - 20),
                     label, fontname="helv", fontsize=7.5, color=GREY)
    sid = owner.get(i + 1)
    if sid:                                  # running head, once past the intro
        head_txt = "STEP %s · %s" % (sid[1], titles[sid].upper())
        page.insert_text((R - fitz.get_text_length(head_txt, "hebo", 6.5), 26),
                         head_txt, fontname="hebo", fontsize=6.5, color=GREY)

doc.saveIncr()
doc.close()

data = open(pdf, "rb").read()
pages = max([int(x) for x in re.findall(rb"/Count\s+(\d+)", data)] or [0])
print("pdf  %.1f MB, %d pages" % (len(data) / 1e6, pages))
