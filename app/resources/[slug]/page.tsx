import type { Metadata } from "next";
import SubPage from "../../_components/SubPage";
import DesignPage from "../../_components/DesignPage";
import { getItem, getParent } from "@/lib/menu";
import { overrideFile, overrideSlugs } from "@/lib/pageOverrides";
import { loadPage } from "@/lib/loadPage";

const KEY = "resources";

export function generateStaticParams() {
  const slugs = new Set([
    ...(getParent(KEY)?.items ?? []).map((i) => i.slug),
    ...overrideSlugs(KEY),
  ]);
  return Array.from(slugs).map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const file = overrideFile(KEY, params.slug);
  if (file) return { title: (await loadPage(file)).title };
  const item = getItem(KEY, params.slug);
  return { title: item ? `${item.name} — Kleza` : "Kleza" };
}

export default function Page({ params }: { params: { slug: string } }) {
  const file = overrideFile(KEY, params.slug);
  if (file) return <DesignPage file={file} />;
  return <SubPage parentKey={KEY} slug={params.slug} />;
}
