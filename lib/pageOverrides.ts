/**
 * Mega-menu slugs that now have a full prototype page of their own
 * (second design handoff). These render the real designed page instead of
 * the generic hand-built SubPage template.
 */
export const PAGE_OVERRIDES: Record<string, Record<string, string>> = {
  about: { careers: "careers.html", partners: "partners.html" },
  "ai-services": {
    training: "ai-training.html",
    assistant: "ai-assistant.html",
    automation: "ai-automation.html",
  },
  resources: { articles: "Blog.html" },
  "enterprise-services": {
    "website-development": "Website Development.html",
    "digital-marketing": "Digital Marketing.html",
    "operational-outsourcing": "Operational Outsourcing.html",
    "remote-it-services": "Remote IT Services.html",
    "automation-tools": "Automation Tools.html",
    "search-visibility": "Search Visibility.html",
    "monitoring-verification": "Monitoring Verification.html",
  },
};

export function overrideFile(parentKey: string, slug: string): string | undefined {
  return PAGE_OVERRIDES[parentKey]?.[slug];
}

export function overrideSlugs(parentKey: string): string[] {
  return Object.keys(PAGE_OVERRIDES[parentKey] ?? {});
}
