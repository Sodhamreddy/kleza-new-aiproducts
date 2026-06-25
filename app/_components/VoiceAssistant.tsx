"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Kleza AI Assistant — a site-wide, voice-driven concierge.
 *
 * Mounted once in the root layout, it:
 *   1. renders a premium, highlighted floating launcher pinned to the
 *      bottom-right of every page (not a nav item — it reads as an assistant),
 *   2. proactively greets visitors with a dismissable teaser bubble shortly
 *      after they land, and
 *   3. opens a chat-style panel (docked bottom-right) that answers questions,
 *      suggests solutions, and navigates by voice or text — speaking back with
 *      a female voice (Web Speech API, with a typed fallback).
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

// The visitor explicitly wants to be taken to a page (vs. just asking about it).
function wantsNavigation(raw: string): boolean {
  return /\b(open|go to|goto|take me|bring me|navigate|visit|show me|load|jump to)\b/i.test(raw);
}

function normPath(p: string): string {
  const path = (p.split("#")[0] || "").replace(/\/+$/, "");
  return path === "" ? "/" : path;
}
function currentPath(): string {
  if (typeof window === "undefined") return "/";
  return normPath(window.location.pathname);
}

interface Action {
  key: string;
  title: string;
  sub: string;
  route: string;
}

const QUICK_ACTIONS: Action[] = [
  { key: "products", title: "AI Products", sub: "Explore our AI products", route: "/ai-products" },
  { key: "services", title: "AI Services", sub: "Discover our AI services", route: "/ai-services" },
  { key: "enterprise", title: "Enterprise Services", sub: "Solutions for enterprises", route: "/enterprise-services" },
  { key: "resources", title: "Resources", sub: "Blogs, case studies and more", route: "/resources" },
  { key: "contact", title: "Contact Team", sub: "Talk to our experts", route: "/contact" },
  { key: "demo", title: "Schedule a Demo", sub: "Book a free consultation", route: "/contact/schedule" },
];

function matchIntent(raw: string): Intent | null {
  const q = raw.toLowerCase().trim();
  if (!q) return null;
  let best: { intent: Intent; score: number } | null = null;
  for (const intent of [...INFO, ...NAV]) {
    for (const key of intent.keys) {
      if (q.includes(key)) {
        const score = key.length + (INFO.includes(intent) ? 100 : 0);
        if (!best || score > best.score) best = { intent, score };
      }
    }
  }
  return best?.intent ?? null;
}

function actionForRoute(route: string): Action {
  const hit = QUICK_ACTIONS.find(
    (a) => route === a.route || route.startsWith(a.route + "/") || route.startsWith(a.route + "#")
  );
  if (hit) return hit;
  if (route === "/") return { key: "home", title: "Home", sub: "Overview of everything Kleza", route: "/" };
  if (route.startsWith("/about")) return { key: "about", title: "About Kleza", sub: "Our story and mission", route };
  return { key: "page", title: "this page", sub: "Learn more about Kleza", route };
}

interface Message {
  id: number;
  role: "user" | "ai";
  text: string;
  cards?: Action[];
  confirm?: { route: string; title: string };
}

const GREETING_SPOKEN =
  "Hi! I'm Kleza's AI assistant. I can help you find information, explore our solutions, or connect you with the right team.";

/* ---------- icons ---------- */
const ICONS: Record<string, JSX.Element> = {
  products: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2 3 7l9 5 9-5-9-5Z" /><path d="m3 12 9 5 9-5" /><path d="m3 17 9 5 9-5" />
    </svg>
  ),
  services: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3 1.6 1.6 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-1-1.5 1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.6 1.6 0 0 0 1.5-1 1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3H9a1.6 1.6 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8V9a1.6 1.6 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1Z" />
    </svg>
  ),
  enterprise: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="8" height="8" rx="1" /><rect x="13" y="3" width="8" height="8" rx="1" /><rect x="3" y="13" width="8" height="8" rx="1" /><rect x="13" y="13" width="8" height="8" rx="1" />
    </svg>
  ),
  resources: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z" />
    </svg>
  ),
  contact: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z" />
    </svg>
  ),
  demo: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  page: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" /><path d="M14 2v6h6" />
    </svg>
  ),
};
ICONS.home = ICONS.page;
ICONS.about = ICONS.page;

export default function VoiceAssistant() {
  const [open, setOpen] = useState(false);
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);
  const [transcript, setTranscript] = useState("");
  const [typed, setTyped] = useState("");
  const [teaser, setTeaser] = useState(false);
  const [greeted, setGreeted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);

  const recogRef = useRef<any>(null);
  const navTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const thinkTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const idRef = useRef(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  const nextId = () => ++idRef.current;
  const inChat = messages.length > 0;

  /* ----- restore the conversation + state across page navigations -----
     The site uses full page loads, so React state resets on every route
     change. We persist the session so the assistant continues seamlessly
     and acknowledges each page it guides the user to (expert-guide mode). */
  useEffect(() => {
    let restored: Message[] = [];
    try {
      const raw = sessionStorage.getItem("kleza-ai-msgs");
      if (raw) {
        const arr = JSON.parse(raw);
        if (Array.isArray(arr)) restored = arr as Message[];
      }
    } catch {
      /* ignore */
    }
    idRef.current = restored.reduce((m, x) => Math.max(m, x?.id ?? 0), 0);

    // Did we just navigate the user somewhere from the assistant?
    let arrival: { title: string } | null = null;
    try {
      const a = sessionStorage.getItem("kleza-ai-arrival");
      if (a) {
        arrival = JSON.parse(a);
        sessionStorage.removeItem("kleza-ai-arrival");
      }
    } catch {
      /* ignore */
    }

    if (arrival) {
      const msg = `You're now on the ${arrival.title} page. Is there anything else I can help you with?`;
      restored = [...restored, { id: ++idRef.current, role: "ai", text: msg }];
      setMessages(restored);
      setGreeted(true);
      setOpen(true);
      // Note: no speak() here — the explanation was already spoken before the
      // navigation, so this stays text-only to avoid a second overlapping voice.
      return;
    }

    if (restored.length) {
      setMessages(restored);
      setGreeted(true);
    }
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
      sessionStorage.setItem("kleza-ai-msgs", JSON.stringify(messages));
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

  /* ----- auto-open the panel on the first landing, once per session ----- */
  useEffect(() => {
    let seen = false;
    try {
      seen = sessionStorage.getItem("kleza-ai-auto") === "1";
    } catch {
      /* ignore */
    }
    if (seen) return;
    const t = setTimeout(() => {
      setOpen(true);
      try {
        sessionStorage.setItem("kleza-ai-auto", "1");
      } catch {
        /* ignore */
      }
    }, 1100);
    return () => clearTimeout(t);
  }, []);

  /* ----- proactive teaser on later page views (after the first auto-open) ----- */
  useEffect(() => {
    let firstDone = false;
    let dismissed = false;
    try {
      firstDone = sessionStorage.getItem("kleza-ai-auto") === "1";
      dismissed = sessionStorage.getItem("kleza-ai-teaser") === "1";
    } catch {
      /* ignore */
    }
    // On the very first landing the full panel auto-opens, so skip the teaser.
    if (!firstDone || dismissed) return;
    const show = setTimeout(() => setTeaser(true), 2600);
    const hide = setTimeout(() => setTeaser(false), 12000);
    return () => {
      clearTimeout(show);
      clearTimeout(hide);
    };
  }, []);

  function dismissTeaser() {
    setTeaser(false);
    try {
      sessionStorage.setItem("kleza-ai-teaser", "1");
    } catch {
      /* ignore */
    }
  }

  function launch() {
    dismissTeaser();
    setOpen(true);
  }

  /* ----- warm up voice list (loads async) + stop speech on page unload ----- */
  useEffect(() => {
    try {
      const synth = window.speechSynthesis;
      if (!synth) return;
      synth.getVoices();
      const onVoices = () => synth.getVoices();
      const stopSpeech = () => {
        try {
          synth.cancel();
        } catch {
          /* ignore */
        }
      };
      synth.addEventListener?.("voiceschanged", onVoices);
      window.addEventListener("beforeunload", stopSpeech);
      window.addEventListener("pagehide", stopSpeech);
      return () => {
        synth.removeEventListener?.("voiceschanged", onVoices);
        window.removeEventListener("beforeunload", stopSpeech);
        window.removeEventListener("pagehide", stopSpeech);
      };
    } catch {
      /* ignore */
    }
  }, []);

  /* ----- feature-detect speech recognition ----- */
  useEffect(() => {
    const SR =
      (typeof window !== "undefined" &&
        ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)) ||
      null;
    setSupported(!!SR);
  }, []);

  /* ----- auto-scroll chat to bottom (chat view only — never the home view) ----- */
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

  function pickFemaleVoice(): SpeechSynthesisVoice | null {
    try {
      const voices = window.speechSynthesis?.getVoices?.() ?? [];
      if (!voices.length) return null;

      // Known Indian-English female voices, in order of quality/naturalness.
      const indianFemale = [
        "neerja", // Microsoft Neerja Online (Natural) — en-IN, very natural
        "heera", // Microsoft Heera — en-IN
        "priya",
        "kalpana",
        "swara",
        "aditi", // Amazon Polly (Indian English)
        "raveena", // Amazon Polly (Indian English)
        "isha",
        "ananya",
      ];
      // High-quality female voices in other English locales (fallbacks).
      const otherFemale = [
        "google uk english female",
        "google us english",
        "microsoft aria",
        "microsoft jenny",
        "microsoft michelle",
        "microsoft sonia",
        "microsoft libby",
        "microsoft zira",
        "samantha",
        "victoria",
        "karen",
        "moira",
        "tessa",
        "fiona",
        "serena",
        "female",
        "woman",
      ];

      const byName = (names: string[], list: SpeechSynthesisVoice[]) => {
        for (const n of names) {
          const hit = list.find((v) => v.name.toLowerCase().includes(n));
          if (hit) return hit;
        }
        return null;
      };

      const maleRe = /(david|mark|george|daniel|fred|alex|male|man|rishi|ravi|prabhat|hemant|guy|eric|tony)/i;
      const isNatural = (v: SpeechSynthesisVoice) => /natural|neural|online/i.test(v.name);

      const enIN = voices.filter((v) => /^en[-_]IN/i.test(v.lang));
      const enAll = voices.filter((v) => /^en(-|_|$)/i.test(v.lang));

      // 1) An explicitly-known Indian female voice.
      let pick = byName(indianFemale, voices);
      // 2) Any en-IN voice that isn't obviously male (prefer natural/neural).
      if (!pick && enIN.length) {
        const female = enIN.filter((v) => !maleRe.test(v.name));
        pick =
          female.find(isNatural) ??
          female[0] ??
          enIN.find(isNatural) ??
          enIN[0];
      }
      // 3) A known good female voice in another English locale.
      if (!pick) pick = byName(otherFemale, enAll.length ? enAll : voices);
      // 4) Any English voice that isn't obviously male.
      if (!pick) {
        const pool = enAll.length ? enAll : voices;
        pick = pool.find((v) => isNatural(v) && !maleRe.test(v.name)) ?? pool.find((v) => !maleRe.test(v.name)) ?? pool[0];
      }
      return pick ?? null;
    } catch {
      return null;
    }
  }

  function speak(text: string) {
    try {
      const synth = window.speechSynthesis;
      if (!synth) return;
      // Stop anything already speaking/queued so only one voice is ever heard.
      synth.cancel();
      const start = () => {
        synth.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.rate = 0.97;
        u.pitch = 1.05;
        const v = pickFemaleVoice();
        if (v) {
          u.voice = v;
          u.lang = v.lang;
        } else {
          u.lang = "en-US";
        }
        synth.speak(u);
      };
      // A tiny delay lets the cancel flush its queue first (prevents the
      // occasional double/overlapping utterance in Chrome & Edge).
      setTimeout(start, 60);
    } catch {
      /* ignore */
    }
  }

  function pushAI(msg: Omit<Message, "id" | "role">) {
    setMessages((m) => [...m, { id: nextId(), role: "ai", ...msg }]);
  }

  /* ----- core: respond to a user query ----- */
  function send(raw: string) {
    const text = raw.trim();
    if (!text) return;
    setTranscript("");
    setMessages((m) => [...m, { id: nextId(), role: "user", text }]);
    setThinking(true);
    if (thinkTimer.current) clearTimeout(thinkTimer.current);
    thinkTimer.current = setTimeout(() => {
      setThinking(false);
      const intent = matchIntent(text);
      if (!intent) {
        const msg =
          "I can tell you about Kleza's AI products, AI services, enterprise services, resources, careers, or our contact details and locations. What would you like to know?";
        pushAI({ text: msg });
        speak(msg);
        return;
      }

      // Always explain the answer in the chat, professionally.
      const here = currentPath();
      const navigate =
        !!intent.route && normPath(intent.route) !== here && wantsNavigation(text);

      if (navigate) {
        const card = actionForRoute(intent.route!);
        const msg = `${intent.say} Opening the ${card.title} page for you now.`;
        pushAI({ text: msg });
        speak(msg);
        go(intent.route!, 2600);
      } else {
        pushAI({ text: intent.say });
        speak(intent.say);
      }
    }, 700);
  }

  function go(route: string, delay = 900) {
    // Remember where we're sending the user so the assistant can greet them
    // on arrival and keep the conversation going across the page load.
    try {
      const title = actionForRoute(route).title;
      sessionStorage.setItem("kleza-ai-arrival", JSON.stringify({ title, route }));
      sessionStorage.setItem("kleza-ai-openstate", "1");
    } catch {
      /* ignore */
    }
    if (navTimer.current) clearTimeout(navTimer.current);
    navTimer.current = setTimeout(() => {
      window.location.href = route;
    }, delay);
  }

  function startListening() {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      setSupported(false);
      return;
    }
    try {
      window.speechSynthesis?.cancel();
    } catch {
      /* ignore */
    }
    const recog = new SR();
    recog.lang = "en-US";
    recog.interimResults = true;
    recog.continuous = false;
    recog.maxAlternatives = 1;
    let finalText = "";
    recog.onresult = (e: any) => {
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const r = e.results[i];
        if (r.isFinal) finalText += r[0].transcript;
        else interim += r[0].transcript;
      }
      setTranscript(finalText || interim);
    };
    recog.onerror = (e: any) => {
      setListening(false);
      if (e?.error === "not-allowed" || e?.error === "service-not-allowed") {
        const msg =
          "I couldn't access your microphone — please allow mic access, or just type your question below.";
        pushAI({ text: msg });
        speak(msg);
      }
    };
    recog.onend = () => {
      setListening(false);
      if (finalText.trim()) send(finalText.trim());
    };
    recogRef.current = recog;
    setTranscript("");
    setListening(true);
    try {
      recog.start();
    } catch {
      setListening(false);
    }
  }

  function stopListening() {
    try {
      recogRef.current?.stop();
    } catch {
      /* ignore */
    }
    setListening(false);
  }

  function cancelListening() {
    try {
      recogRef.current?.abort?.();
    } catch {
      /* ignore */
    }
    setTranscript("");
    setListening(false);
  }

  function resetChat() {
    cancelListening();
    try {
      window.speechSynthesis?.cancel();
    } catch {
      /* ignore */
    }
    if (navTimer.current) clearTimeout(navTimer.current);
    if (thinkTimer.current) clearTimeout(thinkTimer.current);
    setThinking(false);
    setMessages([]);
    try {
      sessionStorage.removeItem("kleza-ai-msgs");
    } catch {
      /* ignore */
    }
  }

  function close() {
    cancelListening();
    try {
      window.speechSynthesis?.cancel();
    } catch {
      /* ignore */
    }
    if (navTimer.current) clearTimeout(navTimer.current);
    setOpen(false);
  }

  /* ----- greet on first open ----- */
  useEffect(() => {
    if (!open || greeted) return;
    setGreeted(true);
    speak(GREETING_SPOKEN);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

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

  function ActionRow({ a }: { a: Action }) {
    return (
      <button className="ai-va-action" onClick={() => go(a.route)}>
        <span className="ai-va-action-ic">{ICONS[a.key] ?? ICONS.page}</span>
        <span className="ai-va-action-tx">
          <span className="ai-va-action-t">{a.title}</span>
          <span className="ai-va-action-s">{a.sub}</span>
        </span>
        <svg className="ai-va-action-go" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>
    );
  }

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
              <strong>Need a hand?</strong> Ask me anything — I can talk, search and guide you around Kleza.
            </span>
          </button>
        </div>

        <button className="ai-va-fab" onClick={launch} aria-label="Open Kleza AI assistant">
          <span className="ai-va-fab-ring" aria-hidden="true" />
          <span className="ai-va-fab-ring two" aria-hidden="true" />
          <span className="ai-va-fab-icon">{SPARKLE}</span>
          <span className="ai-va-fab-label">Ask&nbsp;AI</span>
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
          className={"ai-va-panel" + (listening ? " listening" : "")}
          role="dialog"
          aria-modal="true"
          aria-label="Kleza AI Assistant"
        >
          {/* Header */}
          <div className="ai-va-head">
            <span className="ai-va-brand">
              {inChat && (
                <button className="ai-va-back" onClick={resetChat} aria-label="Back">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="15 18 9 12 15 6" />
                  </svg>
                </button>
              )}
              <span className="ai-va-brand-ic">{SPARKLE}</span>
              <span className="ai-va-brand-name">Kleza AI Assistant</span>
            </span>
            <button className="ai-va-close" onClick={close} aria-label="Close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round">
                <line x1="6" y1="6" x2="18" y2="18" />
                <line x1="18" y1="6" x2="6" y2="18" />
              </svg>
            </button>
          </div>

          {/* Scrollable middle */}
          <div className="ai-va-scroll" ref={scrollRef}>
            {!inChat ? (
              <div className="ai-va-home">
                <p className="ai-va-greet">Hi! How can I help you today?</p>
                <p className="ai-va-greet-sub">
                  I can help you find information, explore our solutions or connect you with the right team.
                </p>

                {supported && (
                  <button className="ai-va-tap" onClick={startListening}>
                    <span className="ai-va-tap-mic">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12 1.5a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0v-7a3 3 0 0 0-3-3z" />
                        <path d="M5 11a7 7 0 0 0 14 0" />
                        <line x1="12" y1="18" x2="12" y2="22" />
                        <line x1="8" y1="22" x2="16" y2="22" />
                      </svg>
                      Tap to speak
                    </span>
                    <span className="ai-va-tap-sub">or type your question below</span>
                  </button>
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
                        {m.cards && (
                          <div className="ai-va-cards">
                            {m.cards.map((c) => (
                              <ActionRow key={c.key + m.id} a={c} />
                            ))}
                          </div>
                        )}
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
            <input
              type="text"
              value={typed}
              onChange={(e) => setTyped(e.target.value)}
              placeholder="Ask anything…"
              aria-label="Ask anything"
            />
            {supported && (
              <button
                type="button"
                className="ai-va-foot-mic"
                onClick={startListening}
                aria-label="Speak your question"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 1.5a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0v-7a3 3 0 0 0-3-3z" />
                  <path d="M5 11a7 7 0 0 0 14 0" />
                  <line x1="12" y1="18" x2="12" y2="22" />
                  <line x1="8" y1="22" x2="16" y2="22" />
                </svg>
              </button>
            )}
            <button type="submit" className="ai-va-send" aria-label="Send">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </button>
          </form>

          {/* Listening overlay (covers panel body) */}
          {listening && (
            <div className="ai-va-listen">
              <button className={"ai-va-mic on"} onClick={stopListening} aria-label="Stop listening">
                <span className="ai-va-mic-ring" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 1.5a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0v-7a3 3 0 0 0-3-3z" />
                  <path d="M5 11a7 7 0 0 0 14 0" />
                  <line x1="12" y1="18" x2="12" y2="22" />
                  <line x1="8" y1="22" x2="16" y2="22" />
                </svg>
              </button>
              <p className="ai-va-listen-title">Listening…</p>
              <p className="ai-va-listen-sub">{transcript ? `“${transcript}”` : "Speak now"}</p>
              <button className="ai-va-btn ghost" onClick={cancelListening}>
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
