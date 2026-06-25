"use client";

import { useEffect, useRef } from "react";
import type { ScriptDesc } from "@/lib/loadPage";

interface Props {
  scripts: ScriptDesc[];
  bodyAttrs: Record<string, string>;
}

/**
 * Re-runs the prototype's genuine interaction scripts (sticky header, mega-menu
 * hover/click, accordion, testimonial carousel) after the static markup is in
 * the DOM, and mirrors the original <body> attributes onto the real <body> so
 * attribute-based CSS selectors keep matching.
 */
export default function PageScripts({ scripts, bodyAttrs }: Props) {
  const injected = useRef(false);

  useEffect(() => {
    // Guard against any double-injection (e.g. Strict Mode); injected inline
    // code declares top-level `const`s that must not run twice.
    if (injected.current) return;
    injected.current = true;

    const body = document.body;
    for (const [k, v] of Object.entries(bodyAttrs)) body.setAttribute(k, v);

    for (const s of scripts) {
      const el = document.createElement("script");
      el.async = false;
      if (s.src) {
        el.src = s.src;
      } else {
        // Wrap inline code in an IIFE so its top-level `const`/`let` are
        // function-scoped (no global redeclaration) and guarded early
        // `return`s remain valid.
        el.text = `(function(){\n${s.code ?? ""}\n})();`;
      }
      body.appendChild(el);
    }
    // Run once per mount; each route is a fresh document load.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}
