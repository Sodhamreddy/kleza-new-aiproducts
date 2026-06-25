import Link from "next/link";
import { notFound } from "next/navigation";
import Chrome from "./Chrome";
import { getItem, getParent } from "@/lib/menu";

function Arrow() {
  return (
    <svg
      className="arrow"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  );
}

export default async function SubPage({
  parentKey,
  slug,
}: {
  parentKey: string;
  slug: string;
}) {
  const parent = getParent(parentKey);
  const item = getItem(parentKey, slug);
  if (!parent || !item) notFound();

  return (
    <Chrome>
      <div className="breadcrumb-bar">
        <div className="container">
          <nav className="breadcrumb" aria-label="Breadcrumb">
            <Link href="/">Home</Link>
            <span className="sep">&raquo;</span>
            <Link href={parent.route}>{parent.label}</Link>
            <span className="sep">&raquo;</span>
            <span className="current">{item.name}</span>
          </nav>
        </div>
      </div>

      <section className="inner-hero">
        <div className="container">
          <span className="eyebrow">{item.eyebrow}</span>
          <h1>
            {item.name} <span className="ital">{item.italTail}</span>
          </h1>
          <p className="lede">{item.lede}</p>
          <div className="hero-ctas">
            <Link
              className="btn btn-accent"
              href="/contact"
              style={{ backgroundColor: "rgb(30, 170, 220)" }}
            >
              {item.cta} <Arrow />
            </Link>
            <Link className="btn btn-ghost" href={parent.route}>
              Back to {parent.label}
            </Link>
          </div>
        </div>
      </section>

      <section className="inner-section band-white">
        <div className="container">
          <div className="feature-block">
            <div className="feature-text">
              <span className="eyebrow">{item.sectionEyebrow}</span>
              <h2>
                {item.name}
                <span className="ital">.</span>
              </h2>
              <p>{item.body}</p>
              <ul className="feature-list">
                {item.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <Link className="btn btn-dark" href="/contact">
                {item.cta} <Arrow />
              </Link>
            </div>
            <div className="feature-visual">
              <div className="blob" />
              <div className="tile">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="9" />
                  <path d="M12 3a15 15 0 0 1 4 9 15 15 0 0 1-4 9 15 15 0 0 1-4-9 15 15 0 0 1 4-9z" />
                  <line x1="3" y1="12" x2="21" y2="12" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="inner-section band-light">
        <div className="container">
          <div className="cta">
            <h2>
              Ready to get started with{" "}
              <span className="ital">{item.name}?</span>
            </h2>
            <p>
              Tell us what you&rsquo;re working on and we&rsquo;ll show you what
              Kleza can do.
            </p>
            <div className="cta-buttons">
              <Link className="btn btn-accent" href="/contact">
                {item.cta} <Arrow />
              </Link>
              <Link className="btn btn-ghost" href={parent.route}>
                Explore {parent.label}
              </Link>
            </div>
          </div>
        </div>
      </section>
    </Chrome>
  );
}
