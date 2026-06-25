import type { Metadata } from "next";
import SubPage from "../../_components/SubPage";
import { getItem, getParent } from "@/lib/menu";

const KEY = "contact";

export function generateStaticParams() {
  return (getParent(KEY)?.items ?? []).map((i) => ({ slug: i.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const item = getItem(KEY, params.slug);
  return { title: item ? `${item.name} — Kleza` : "Kleza" };
}

export default function Page({ params }: { params: { slug: string } }) {
  return <SubPage parentKey={KEY} slug={params.slug} />;
}
