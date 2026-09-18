"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Kleza AI Assistant — a site-wide, text-only Q&A concierge.
 *
 * Mounted once in the root layout, it:
 *   1. renders a floating launcher pinned to the bottom-right of every page,
 *      plus a nudge bubble that appears 30s after landing and returns every
 *      2 minutes until the visitor opens the panel (or dismisses it),
 *   2. stays closed on landing — it never opens by itself, and
 *   3. opens a plain chat panel that answers questions with information drawn
 *      from the site's own content. Answers are text only: no voice, no link
 *      cards, and it never navigates the visitor away. The thread is kept in
 *      localStorage, so history survives page loads and return visits, and is
 *      cleared only by "New conversation".
 */

interface Intent {
  keys: string[];
  say: string;
  route?: string;
}

// Detailed, professional answers. The assistant explains these in the chat;
// `route` is only used when the visitor explicitly asks to open/go to a page.
// More specific, info-style answers are matched first.
const INFO: Intent[] = [
  {
    keys: ["what do you do", "what does kleza", "what is kleza", "who are you", "about kleza", "tell me about kleza", "about the company"],
    say: "Kleza is a healthcare-first AI company. We design AI products, agentic companions, and digital services that help healthcare organizations move faster, decide smarter, and serve patients better — about 75% of our work is in healthcare. You'll find our story and mission on the About page.",
    route: "/about",
  },
  {
    keys: ["healthcare", "hipaa", "clinical", "patient", "care", "medical"],
    say: "Healthcare is roughly 75% of what we do. We build HIPAA-aligned AI for patient intake, clinical documentation, scheduling, and care coordination — designed to fit real clinical workflows rather than add to them.",
    route: "/about#healthcare",
  },
  {
    keys: ["contact information", "contact info", "contact details", "reach you", "your email", "email address", "phone number", "your number", "call you", "your address", "how do i contact", "how to contact", "get in touch"],
    say: "Here's how to reach us. Email us at hello@kleza.io. In the US, call +1 913-800-2728 — our office is in Overland Park, Kansas. In India, call +91 7396146227 — we're in Madhapur, HITEC City, Hyderabad. You can also send a message or book a call from the Contact page.",
    route: "/contact",
  },
  {
    keys: ["location", "located", "office", "where are you", "address", "kansas", "hyderabad", "madhapur", "india", "usa", "headquarter"],
    say: "We operate from two offices. In the USA we're in Overland Park, Kansas, and in India we're in Madhapur, HITEC City, Hyderabad. Our Hyderabad center coordinates engineering and operations for clients.",
  },
  {
    keys: ["price", "pricing", "cost", "how much", "quote", "budget"],
    say: "We don't publish fixed pricing because every engagement is scoped to your needs — the size of the system, integrations, and timeline all matter. The best next step is a short call so we can give you an accurate estimate; you can reach us at hello@kleza.io or through the Contact page.",
    route: "/contact",
  },
];

// Topic / page knowledge. Each answer explains what the section covers.
const NAV: Intent[] = [
  {
    keys: ["home", "homepage", "main page", "start page"],
    say: "The home page gives an overview of everything Kleza does — our AI products, services, enterprise offerings, and the healthcare focus that runs through all of it.",
    route: "/",
  },
  {
    keys: ["about", "company", "story", "team", "mission", "vision", "values"],
    say: "The About section covers our story, mission, and the team behind Kleza — who we are, why we focus on healthcare, and how we work with clients.",
    route: "/about",
  },
  {
    keys: ["career", "careers", "job", "jobs", "hiring", "work here", "open role", "vacanc", "apply", "openings"],
    say: "We're growing! The Careers page lists our current open roles across engineering and operations and explains how to apply. You can also email careers@kleza.io.",
    route: "/about/careers",
  },
  {
    keys: ["product", "products", "voica", "docui", "pulse", "companion", "agentic", "ai product"],
    say: "Our AI Products are agentic companions built for healthcare workflows — including Voica for voice-driven interactions, DocUI for document intelligence, and Pulse for monitoring and insights. The AI Products page details each one and who it's for.",
    route: "/ai-products",
  },
  {
    keys: ["service", "services", "training", "fine tun", "rag", "support assistant", "ai service", "model"],
    say: "Our AI Services cover the full build: model training, fine-tuning, retrieval-augmented generation (RAG), and support assistants. In short, we build and deploy custom AI on your own data, validated against your standards. The AI Services page goes into detail.",
    route: "/ai-services",
  },
  {
    keys: ["enterprise", "website", "web development", "marketing", "seo", "it service", "outsourc", "automation", "digital marketing"],
    say: "Enterprise Services span web development, digital marketing, SEO, IT services, operational outsourcing, and automation tools — the digital backbone organizations need alongside their AI. The Enterprise Services page lists the full range.",
    route: "/enterprise-services",
  },
  {
    keys: ["resource", "resources", "blog", "article", "insight", "newsletter", "read", "case study", "case studies"],
    say: "The Resources section is where we share our thinking — blog posts, in-depth articles, client case studies, and our newsletter, mostly focused on applying AI in healthcare.",
    route: "/resources",
  },
  {
    keys: ["demo", "consultation", "book a", "schedule", "free consult", "book a call", "meeting"],
    say: "Happy to set you up with a free consultation. You can book a time on the Schedule page, or email hello@kleza.io and we'll find a slot that works.",
    route: "/contact/schedule",
  },
  {
    keys: ["contact", "talk", "reach", "email", "phone", "call", "consult", "connect", "speak to"],
    say: "Happy to connect you with our team. You can reach us at hello@kleza.io, or use the Contact page to send a message or book a call.",
    route: "/contact",
  },
];

// Detailed, specific knowledge — individual products, services, and company
// facts drawn from the site's own content, so the assistant can answer
// "anything asked" with real detail (matched ahead of the broad NAV topics).
const DETAIL: Intent[] = [
  // --- AI Products ---
  {
    keys: ["voica", "voice ai", "voice intelligence", "voice product"],
    say: "Voica is our voice-intelligence product — real-time conversational AI for patient intake, support, and care coordination. It handles natural turn-taking and live transcription, and escalates to a human the moment it's unsure.",
    route: "/ai-products/voica",
  },
  {
    keys: ["docui", "document ai", "document intelligence", "paperwork", "pdf"],
    say: "DocUI is our document-intelligence product. It reads, classifies, and routes paperwork automatically — with e-signature, batch approval, and a full audit trail — turning an inbox of PDFs into a clean, auditable pipeline.",
    route: "/ai-products/docui",
  },
  {
    keys: ["pulse", "pulse board", "ops dashboard", "operations dashboard", "kpi"],
    say: "Pulse Board is our real-time operations dashboard — live KPI tiles, anomaly detection, and smart alerts in one role-based view, so leaders catch what's slipping before it slips.",
    route: "/ai-products/pulse",
  },
  {
    keys: ["assessment app", "assessment", "digital assessment"],
    say: "The Assessment App delivers digital assessments that adapt to the responder, score instantly, and route results automatically — replacing paper forms with a clean audit trail.",
    route: "/ai-products/assessment",
  },
  {
    keys: ["onboarding app", "onboarding"],
    say: "The Onboarding App runs onboarding end to end — document collection, ID verification, e-signature, and status tracking — to get new staff, caregivers, and clients productive faster.",
    route: "/ai-products/onboarding",
  },
  {
    keys: ["3 llms", "three llms", "multi-model", "multi model", "reasoning", "triangulat"],
    say: "Our 3 LLMs system triangulates reasoning across multiple models and reconciles their outputs into a single, confidence-scored answer — so you're never relying on a single-point bet.",
    route: "/ai-products/llms",
  },
  {
    keys: ["marketplace", "integration", "integrations", "connector", "template"],
    say: "The Marketplace offers ready-to-deploy integrations, connectors, and templates that link Kleza products to the tools you already use — installable in minutes.",
    route: "/ai-products/marketplace",
  },
  {
    keys: ["companion", "companions", "hr companion", "admin companion", "scheduler", "caregiver", "client companion", "workforce", "comes360", "agentic"],
    say: "Our Comes360 companions are agentic assistants for your teams — HR, Admin, and Scheduler companions for workforce operations, plus Caregiver and Client companions for direct care and engagement.",
    route: "/ai-products",
  },
  // --- AI Services ---
  {
    keys: ["fine tun", "fine-tun", "custom model", "train a model", "rag pipeline", "bespoke model", "data curation", "mlops"],
    say: "We build business-specific AI — data curation, fine-tuning, RAG pipelines, evaluation suites, and MLOps — so your models reflect how your business actually operates, validated against your standards.",
    route: "/ai-services/training",
  },
  {
    keys: ["support assistant", "customer support", "24/7", "chatbot", "conversational ai", "help desk"],
    say: "Our AI Support Assistant is 24/7 conversational AI trained on your knowledge base — tone-matched, multi-channel, with smart escalation to a human and analytics built in.",
    route: "/ai-services/assistant",
  },
  // --- Enterprise Services ---
  {
    keys: ["website", "web development", "web design", "build a site", "build a website"],
    say: "Our Website Development team builds modern, high-performance, SEO-ready sites — design systems, accessibility, CMS integration, and performance budgets included.",
    route: "/enterprise-services/website-development",
  },
  {
    keys: ["ppc", "paid ads", "google ads", "meta ads", "campaign", "growth marketing"],
    say: "Our Digital Marketing covers paid and organic growth — campaigns, content, analytics, A/B testing, and automation that turns spend into pipeline.",
    route: "/enterprise-services/digital-marketing",
  },
  {
    keys: ["seo", "search ranking", "rank", "serp", "search visibility", "indexing"],
    say: "We handle SEO and search visibility — technical and content SEO, rank tracking with our SERP Agent, and instant indexing so your freshest content gets seen.",
    route: "/enterprise-services/search-visibility",
  },
  {
    keys: ["it service", "managed it", "infrastructure", "remote it", "patching", "backup"],
    say: "Remote IT Services give you 24/7 infrastructure care — monitoring, patching, backups, security hardening, and remote support with response times you can count on.",
    route: "/enterprise-services/remote-it-services",
  },
  {
    keys: ["outsourc", "back office", "back-office", "operations support", "managed operations"],
    say: "Operational Outsourcing gives you a trained, SLA-backed team that runs your repeatable operations with documented processes and AI tooling — quality stays high as you scale.",
    route: "/enterprise-services/operational-outsourcing",
  },
  {
    keys: ["blog automation", "social media", "content automation", "scheduling tool"],
    say: "Our automation tools run content and marketing on autopilot — AI drafting with a human review gate, multi-channel social scheduling, and best-time posting.",
    route: "/enterprise-services/automation-tools",
  },
  {
    keys: ["uptime", "domain expiry", "performance monitoring", "website performance", "monitoring"],
    say: "Monitoring & Verification keeps your digital surface reliable — uptime and Core Web Vitals checks, plus domain and SSL expiry alerts so nothing lapses.",
    route: "/enterprise-services/monitoring-verification",
  },
  // --- Company facts ---
  {
    keys: ["founded", "since", "how long", "experience", "established", "how old", "years in business"],
    say: "Kleza was founded in 2016. We're a team of 40-plus specialists operating across the USA and India, with about 75% of our work in healthcare.",
    route: "/about",
  },
  {
    keys: ["why kleza", "why choose", "different", "what makes", "why you", "advantage", "stand out"],
    say: "What sets Kleza apart is healthcare depth plus human-in-the-loop AI — we build precise, domain-specific systems that augment your teams rather than replace them, and we stay accountable at every step.",
    route: "/about",
  },
  {
    keys: ["security", "compliance", "data privacy", "secure", "hipaa compliant", "is it safe"],
    say: "Security and privacy are built in. Our healthcare work is HIPAA-aligned, with audit trails, human oversight, and privacy-by-design across every deployment.",
    route: "/about#healthcare",
  },
  {
    keys: ["industries", "industry", "sectors", "who do you work with", "your clients", "type of clients"],
    say: "About 75% of our work is in healthcare — home care, hospitals, pharmacies, and health-tech — but we also serve businesses that need digital and AI services across other sectors.",
    route: "/about",
  },
];

function matchIntent(raw: string): Intent | null {
  const q = raw.toLowerCase().trim();
  if (!q) return null;
  let best: { intent: Intent; score: number } | null = null;
  for (const intent of [...INFO, ...DETAIL, ...NAV]) {
    for (const key of intent.keys) {
      if (q.includes(key)) {
        // Specific INFO/DETAIL answers outrank the broad NAV topics; among
        // equals, the longest matched keyword wins.
        const bonus = INFO.includes(intent) ? 100 : DETAIL.includes(intent) ? 60 : 0;
        const score = key.length + bonus;
        if (!best || score > best.score) best = { intent, score };
      }
    }
  }
  return best?.intent ?? null;
}

interface Message {
  id: number;
  role: "user" | "ai";
  text: string;
}

/** Where the conversation is kept, so history survives page loads. */
const STORE = "kleza-ai-msgs";

export default function VoiceAssistant() {
  const [open, setOpen] = useState(false);
  const [typed, setTyped] = useState("");
  const [teaser, setTeaser] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);
  const [listening, setListening] = useState(false);
  // Book-a-demo picker (UI only — nothing is sent anywhere yet).
  const [demoOpen, setDemoOpen] = useState(false);
  // The Start chat / Book a Demo row hides once the visitor starts chatting.
  const [showActions, setShowActions] = useState(true);
  const [demoMonth, setDemoMonth] = useState<{ y: number; m: number } | null>(null);
  const [demoDay, setDemoDay] = useState<number | null>(null);
  const [demoSlot, setDemoSlot] = useState<string | null>(null);
  // Step 1 = pick date & time, step 2 = who the demo is for.
  const [demoStep, setDemoStep] = useState<1 | 2>(1);
  const [demoName, setDemoName] = useState("");
  const [demoEmail, setDemoEmail] = useState("");
  const [demoPhone, setDemoPhone] = useState("");

  const thinkTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const recogRef = useRef<any>(null);
  const idRef = useRef(0);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const nextId = () => ++idRef.current;
  const inChat = messages.length > 0;

  /* ----- restore the conversation across page loads -----
     The site uses full page loads, so React state resets on every route
     change. History is kept in localStorage so the thread is still there when
     the visitor comes back, and is only ever cleared by "New conversation". */
  useEffect(() => {
    let restored: Message[] = [];
    try {
      const raw = localStorage.getItem(STORE);
      if (raw) {
        const arr = JSON.parse(raw);
        if (Array.isArray(arr)) restored = arr as Message[];
      }
    } catch {
      /* ignore */
    }
    idRef.current = restored.reduce((m, x) => Math.max(m, x?.id ?? 0), 0);
    if (restored.length) setMessages(restored);

    let wasOpen = false;
    try {
      wasOpen = sessionStorage.getItem("kleza-ai-openstate") === "1";
    } catch {
      /* ignore */
    }
    if (wasOpen) setOpen(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ----- persist the conversation + open state ----- */
  useEffect(() => {
    try {
      localStorage.setItem(STORE, JSON.stringify(messages));
    } catch {
      /* ignore */
    }
  }, [messages]);

  useEffect(() => {
    try {
      sessionStorage.setItem("kleza-ai-openstate", open ? "1" : "0");
    } catch {
      /* ignore */
    }
  }, [open]);

  /* ----- wire global open event ----- */
  useEffect(() => {
    const openHandler = () => setOpen(true);
    window.addEventListener("kleza-ai-open", openHandler);
    return () => window.removeEventListener("kleza-ai-open", openHandler);
  }, []);

  /* ----- the nudge -----
     The assistant never opens by itself. The bubble shows as soon as the page
     loads, stays for 30s, closes itself, then reopens every 2 minutes until the
     visitor uses it. "Used" is tracked per page view only (a ref, not storage):
     a stored flag meant that opening the panel once silenced the nudge for the
     whole tab. */
  const NUDGE_FIRST = 1_000; // ~immediately on load (lets the panel animate in)
  const NUDGE_VISIBLE = 30_000; // then it closes itself
  const NUDGE_REPEAT = 120_000; // and comes back every 2 minutes
  const nudgeDone = useRef(false);

  useEffect(() => {
    if (open) nudgeDone.current = true;
    if (open || nudgeDone.current) return;

    const timers: ReturnType<typeof setTimeout>[] = [];
    const cycle = (delay: number) => {
      timers.push(
        setTimeout(() => {
          setTeaser(true);
          timers.push(
            setTimeout(() => {
              setTeaser(false);
              // ...and comes back 2 minutes after closing, until it's used.
              cycle(NUDGE_REPEAT);
            }, NUDGE_VISIBLE)
          );
        }, delay)
      );
    };
    cycle(NUDGE_FIRST);
    return () => timers.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  function dismissTeaser() {
    setTeaser(false);
    nudgeDone.current = true;
  }

  function launch() {
    dismissTeaser();
    setOpen(true);
  }

  /* ----- dictation -----
     The mic only fills the input box; the visitor still presses Enter (or the
     send button) to ask. The assistant never speaks its answers aloud.
     The button always renders — feature detection happens on click, so it can
     never silently disappear (it used to be hidden until a client-side check
     ran, which meant it sometimes never showed at all). ----- */
  function toggleDictation() {
    if (listening) {
      try {
        recogRef.current?.stop();
      } catch {
        /* ignore */
      }
      setListening(false);
      return;
    }
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      pushAI({
        text:
          "Dictation isn't supported in this browser — please type your question below instead. (It works in Chrome and Edge.)",
      });
      return;
    }
    const recog = new SR();
    recog.lang = "en-US";
    recog.interimResults = true;
    recog.continuous = false;
    let finalText = "";
    recog.onresult = (e: any) => {
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const r = e.results[i];
        if (r.isFinal) finalText += r[0].transcript;
        else interim += r[0].transcript;
      }
      setTyped((finalText + interim).trimStart());
    };
    recog.onerror = () => setListening(false);
    recog.onend = () => setListening(false);
    recogRef.current = recog;
    setListening(true);
    try {
      recog.start();
    } catch {
      setListening(false);
    }
  }

  /* ----- grow the input with the question (up to the CSS max-height) -----
     `scrollHeight` excludes the border, and box-sizing is border-box, so the
     border width has to be added back or the last line gets clipped. */
  useEffect(() => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    const border = el.offsetHeight - el.clientHeight;
    el.style.height = `${el.scrollHeight + border}px`;
  }, [typed]);

  /* ----- auto-scroll chat to bottom ----- */
  useEffect(() => {
    if (messages.length === 0) return;
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, thinking]);

  /* ----- always start the home view scrolled to the top when opening ----- */
  useEffect(() => {
    if (!open) return;
    const el = scrollRef.current;
    if (el && messages.length === 0) el.scrollTop = 0;
  }, [open, messages.length]);

  function pushAI(msg: Omit<Message, "id" | "role">) {
    setMessages((m) => [...m, { id: nextId(), role: "ai", ...msg }]);
  }

  /* ----- core: answer a typed question, in text, from the site's own content.
     Information only — the assistant never navigates the visitor away. ----- */
  function send(raw: string) {
    const text = raw.trim();
    if (!text) return;
    setMessages((m) => [...m, { id: nextId(), role: "user", text }]);
    setThinking(true);
    if (thinkTimer.current) clearTimeout(thinkTimer.current);
    thinkTimer.current = setTimeout(() => {
      setThinking(false);
      const intent = matchIntent(text);
      pushAI({
        text:
          intent?.say ??
          "I can tell you about Kleza's AI products, AI services, enterprise services, resources, careers, or our contact details and locations. What would you like to know?",
      });
    }, 700);
  }

  /* ----- book a demo -----
     A small inline calendar. The month is only computed on open, never during
     render, so the server and client can't disagree about "today". ----- */
  const DEMO_SLOTS = ["09:30", "11:00", "13:30", "15:00", "16:30"];
  const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];

  function openDemo() {
    const now = new Date();
    setDemoMonth({ y: now.getFullYear(), m: now.getMonth() });
    setDemoDay(null);
    setDemoSlot(null);
    setDemoStep(1);
    setDemoName("");
    setDemoEmail("");
    setDemoPhone("");
    setDemoOpen(true);
  }

  /** Human-readable form of the chosen slot, e.g. "Wed, 29 Jul at 13:30". */
  function demoWhen(): string {
    if (!demoMonth || !demoDay || !demoSlot) return "";
    const d = new Date(demoMonth.y, demoMonth.m, demoDay);
    return `${d.toLocaleDateString(undefined, {
      weekday: "short",
      day: "numeric",
      month: "short",
    })} at ${demoSlot}`;
  }

  const emailLooksValid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(demoEmail.trim());
  const phoneLooksValid = demoPhone.replace(/\D/g, "").length >= 7;
  const detailsReady = demoName.trim().length >= 2 && emailLooksValid && phoneLooksValid;

  function shiftMonth(step: number) {
    setDemoMonth((cur) => {
      if (!cur) return cur;
      const d = new Date(cur.y, cur.m + step, 1);
      return { y: d.getFullYear(), m: d.getMonth() };
    });
    setDemoDay(null);
    setDemoSlot(null);
  }

  /** Day cells for the visible month, padded so the 1st lands on its weekday. */
  function monthCells(y: number, m: number): (number | null)[] {
    const lead = new Date(y, m, 1).getDay();
    const total = new Date(y, m + 1, 0).getDate();
    const cells: (number | null)[] = Array(lead).fill(null);
    for (let d = 1; d <= total; d++) cells.push(d);
    return cells;
  }

  /** Past days (and Sundays) can't be booked. */
  function dayDisabled(y: number, m: number, d: number): boolean {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const cell = new Date(y, m, d);
    return cell < today || cell.getDay() === 0;
  }

  function confirmDemo() {
    if (!demoMonth || !demoDay || !demoSlot || !detailsReady) return;
    const name = demoName.trim().split(/\s+/)[0];
    pushAI({
      text: `Thanks ${name} — your demo is requested for ${demoWhen()}. We'll send the confirmation and joining details to ${demoEmail.trim()}, and call you if we need anything before then.`,
    });
    setDemoOpen(false);
  }

  /* Clears the thread deliberately — the button is labelled "New conversation"
     so it can't be mistaken for a back arrow (which used to erase silently). */
  function newConversation() {
    if (thinkTimer.current) clearTimeout(thinkTimer.current);
    setThinking(false);
    setMessages([]);
    setShowActions(true);
    try {
      localStorage.removeItem(STORE);
    } catch {
      /* ignore */
    }
  }

  function close() {
    setOpen(false);
  }

  /* ----- Esc to close ----- */
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  const SPARKLE = (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M10.5 4.5C10.5 9.2 14.3 13 19 13C14.3 13 10.5 16.8 10.5 21.5C10.5 16.8 6.7 13 2 13C6.7 13 10.5 9.2 10.5 4.5Z" />
      <path d="M18.5 2.5C18.5 4.2 19.8 5.5 21.5 5.5C19.8 5.5 18.5 6.8 18.5 8.5C18.5 6.8 17.2 5.5 15.5 5.5C17.2 5.5 18.5 4.2 18.5 2.5Z" />
    </svg>
  );

  return (
    <>
      {/* Floating launcher — premium, highlighted, bottom-right */}
      <div className={"ai-va-dock" + (open ? " hidden" : "")}>
        <div className={"ai-va-teaser" + (teaser ? " show" : "")} role="status" aria-hidden={!teaser}>
          <button className="ai-va-teaser-x" onClick={dismissTeaser} aria-label="Dismiss">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round">
              <line x1="6" y1="6" x2="18" y2="18" />
              <line x1="18" y1="6" x2="6" y2="18" />
            </svg>
          </button>
          <button className="ai-va-teaser-body" onClick={launch}>
            <span className="ai-va-teaser-wave" aria-hidden="true">👋</span>
            <span>
              <strong>Need a hand?</strong> Ask me anything about Kleza — our products, services or how to reach us.
            </span>
          </button>
        </div>

        <button className="ai-va-fab" onClick={launch} aria-label="Open Kleza AI assistant">
          <span className="ai-va-fab-ring" aria-hidden="true" />
          <span className="ai-va-fab-ring two" aria-hidden="true" />
          <span className="ai-va-fab-icon">{SPARKLE}</span>
          <span className="ai-va-fab-label">Ask&nbsp;KI</span>
        </button>
      </div>

      <div
        className={"ai-va-overlay" + (open ? " open" : "")}
        onMouseDown={(e) => {
          if (e.target === e.currentTarget) close();
        }}
        aria-hidden={!open}
      >
        <div
          className={"ai-va-panel" + (demoOpen ? " demo" : "")}
          role="dialog"
          aria-modal="true"
          aria-label="Kleza AI Assistant"
        >
          {/* Header */}
          <div className="ai-va-head">
            <span className="ai-va-brand">
              <span className="ai-va-brand-ic">{SPARKLE}</span>
              <span className="ai-va-brand-name">Kleza AI Assistant</span>
            </span>
            {inChat && (
              <button
                className="ai-va-new"
                onClick={newConversation}
                aria-label="New conversation"
                title="New conversation"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 12a9 9 0 1 1-3.5-7.1" />
                  <polyline points="21 3 21 9 15 9" />
                </svg>
              </button>
            )}
            <button className="ai-va-close" onClick={close} aria-label="Close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round">
                <line x1="6" y1="6" x2="18" y2="18" />
                <line x1="18" y1="6" x2="6" y2="18" />
              </svg>
            </button>
          </div>

          {/* Scrollable middle — the chat thread, or the demo picker */}
          <div className="ai-va-scroll" ref={scrollRef}>
            {demoOpen && demoMonth ? (
              <div className="ai-va-demo">
                <div className="ai-va-demo-top">
                  <button className="ai-va-demo-back" onClick={() => setDemoOpen(false)} aria-label="Back to chat">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="15 18 9 12 15 6" />
                    </svg>
                  </button>
                  <strong>Book a demo</strong>
                </div>

                {demoStep === 1 ? (
                  <>
                    <div className="ai-va-cal-head">
                      <button onClick={() => shiftMonth(-1)} aria-label="Previous month">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="15 18 9 12 15 6" />
                        </svg>
                      </button>
                      <span>{MONTHS[demoMonth.m]} {demoMonth.y}</span>
                      <button onClick={() => shiftMonth(1)} aria-label="Next month">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="9 18 15 12 9 6" />
                        </svg>
                      </button>
                    </div>

                    <div className="ai-va-cal-dow" aria-hidden="true">
                      {["S", "M", "T", "W", "T", "F", "S"].map((d, i) => (
                        <span key={i}>{d}</span>
                      ))}
                    </div>
                    <div className="ai-va-cal-grid" role="grid">
                      {monthCells(demoMonth.y, demoMonth.m).map((d, i) =>
                        d === null ? (
                          <span key={`x${i}`} />
                        ) : (
                          <button
                            key={d}
                            className={"ai-va-cal-day" + (demoDay === d ? " sel" : "")}
                            disabled={dayDisabled(demoMonth.y, demoMonth.m, d)}
                            onClick={() => {
                              setDemoDay(d);
                              setDemoSlot(null);
                            }}
                          >
                            {d}
                          </button>
                        )
                      )}
                    </div>

                    {demoDay && (
                      <>
                        <div className="ai-va-demo-label">Pick a time</div>
                        <div className="ai-va-slots">
                          {DEMO_SLOTS.map((s) => (
                            <button
                              key={s}
                              className={"ai-va-slot" + (demoSlot === s ? " sel" : "")}
                              onClick={() => setDemoSlot(s)}
                            >
                              {s}
                            </button>
                          ))}
                        </div>
                      </>
                    )}

                    <button
                      className="ai-va-demo-confirm"
                      disabled={!demoDay || !demoSlot}
                      onClick={() => setDemoStep(2)}
                    >
                      Continue
                    </button>
                  </>
                ) : (
                  <>
                    {/* Chosen slot stays visible, and can be changed. */}
                    <div className="ai-va-demo-when">
                      <span>{demoWhen()}</span>
                      <button onClick={() => setDemoStep(1)}>Change</button>
                    </div>

                    <div className="ai-va-demo-label">Your details</div>
                    <div className="ai-va-demo-fields">
                      <input
                        className="ai-va-field"
                        type="text"
                        value={demoName}
                        onChange={(e) => setDemoName(e.target.value)}
                        placeholder="Full name"
                        aria-label="Full name"
                        autoComplete="name"
                      />
                      <input
                        className="ai-va-field"
                        type="email"
                        value={demoEmail}
                        onChange={(e) => setDemoEmail(e.target.value)}
                        placeholder="Work email"
                        aria-label="Work email"
                        autoComplete="email"
                      />
                      <input
                        className="ai-va-field"
                        type="tel"
                        value={demoPhone}
                        onChange={(e) => setDemoPhone(e.target.value)}
                        placeholder="Phone number"
                        aria-label="Phone number"
                        autoComplete="tel"
                      />
                    </div>

                    <button className="ai-va-demo-confirm" disabled={!detailsReady} onClick={confirmDemo}>
                      Confirm demo
                    </button>
                  </>
                )}
              </div>
            ) : (
            <div className="ai-va-chat">
              {messages.map((m) =>
                m.role === "user" ? (
                  <div key={m.id} className="ai-va-msg user">
                    <div className="ai-va-bubble">{m.text}</div>
                  </div>
                ) : (
                  <div key={m.id} className="ai-va-msg ai">
                    <span className="ai-va-avatar">{SPARKLE}</span>
                    <div className="ai-va-ai-body">
                      <div className="ai-va-bubble">{m.text}</div>
                    </div>
                  </div>
                )
              )}
              {thinking && (
                <div className="ai-va-msg ai">
                  <span className="ai-va-avatar">{SPARKLE}</span>
                  <div className="ai-va-typing">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              )}
            </div>
            )}
          </div>

          {/* Two actions: start chatting, or book a demo. Hidden once the
              visitor taps Start chat or the conversation is under way. */}
          {!demoOpen && showActions && !inChat && (
            <div className="ai-va-actions">
              <button
                className="ai-va-act primary"
                onClick={() => {
                  setShowActions(false);
                  inputRef.current?.focus();
                }}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
                </svg>
                Start chat
              </button>
              <button className="ai-va-act" onClick={openDemo}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
                Book a Demo
              </button>
            </div>
          )}

          {/* Footer input */}
          <form
            className="ai-va-foot"
            onSubmit={(e) => {
              e.preventDefault();
              if (!typed.trim()) return;
              send(typed.trim());
              setTyped("");
            }}
          >
            {/* A textarea, not an input: long questions wrap and stay readable
                instead of scrolling out of sight. Enter sends, Shift+Enter
                starts a new line. */}
            <textarea
              ref={inputRef}
              rows={1}
              value={typed}
              onChange={(e) => setTyped(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  if (!typed.trim()) return;
                  send(typed.trim());
                  setTyped("");
                }
              }}
              placeholder="Ask anything…"
              aria-label="Ask anything"
            />
            {/* Enter hint, then the mic (dictates into the box), then send. */}
            <span className="ai-va-enter" aria-hidden="true" title="Press Enter to send">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 10 4 15 9 20" />
                <path d="M20 4v7a4 4 0 0 1-4 4H4" />
              </svg>
            </span>
            <button
              type="button"
              className={"ai-va-foot-mic" + (listening ? " on" : "")}
              onClick={toggleDictation}
              aria-label={listening ? "Stop dictation" : "Dictate your question"}
              title={listening ? "Listening — tap to stop" : "Speak your question"}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 1.5a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0v-7a3 3 0 0 0-3-3z" />
                <path d="M5 11a7 7 0 0 0 14 0" />
                <line x1="12" y1="18" x2="12" y2="22" />
                <line x1="8" y1="22" x2="16" y2="22" />
              </svg>
            </button>
            <button type="submit" className="ai-va-send" aria-label="Send">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
