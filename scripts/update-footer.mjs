// One-off: replace the prototype footer in every content/*.html with the real
// Kleza Solutions footer (offices, phones, email, socials) sourced from kleza.io.
import { readFile, writeFile, readdir } from "fs/promises";
import path from "path";

const FOOTER = `<footer class="footer band-light" data-screen-label="Footer" style="padding: 56px 0px 32px">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo" aria-label="Kleza"><img src="/assets/kleza-logo.png" alt="Kleza" /></a>
        <p class="tagline" style="margin-top:22px">Clinical precision meets soft, intelligent light.</p>
        <div class="footer-social">
          <a href="https://www.linkedin.com/company/kleza-solutions-pvt-ltd/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0zM.25 8.25h4.5V24h-4.5V8.25zM8.25 8.25h4.31v2.15h.06c.6-1.14 2.07-2.34 4.26-2.34 4.56 0 5.4 3 5.4 6.9V24h-4.5v-6.75c0-1.61-.03-3.68-2.24-3.68-2.24 0-2.58 1.75-2.58 3.56V24h-4.5V8.25z"/></svg></a>
          <a href="https://twitter.com/klezasolutions" target="_blank" rel="noopener noreferrer" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24h-6.656l-5.214-6.817-5.966 6.817H1.683l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.45-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg></a>
          <a href="https://www.facebook.com/Klezasolution" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07c0 6.02 4.39 11.01 10.12 11.93v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.95.93-1.95 1.89v2.25h3.32l-.53 3.49h-2.79V24C19.61 23.08 24 18.09 24 12.07z"/></svg></a>
          <a href="https://www.instagram.com/klezasolutions/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg></a>
        </div>
      </div>
      <div class="footer-offices">
        <h5>Offices</h5>
        <address class="footer-office">
          <span class="office-tag">USA &middot; Headquarters</span>
          <span>9331 W 87th St, Overland Park, KS 66212, United States</span>
          <a href="tel:+19138002728">+1 913-800-2728</a>
        </address>
        <address class="footer-office">
          <span class="office-tag">India &middot; Delivery Center</span>
          <span>5B, Unit-2, 5th Floor, Bizness Square, Opp. Hitex Junction, Hitec City, Madhapur, Telangana 500081</span>
          <a href="tel:+917396146227">+91 7396146227</a>
        </address>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="/about">About</a></li>
          <li><a href="/ai-products">AI Products</a></li>
          <li><a href="/ai-services">AI Services</a></li>
          <li><a href="/enterprise-services">Enterprise</a></li>
          <li><a href="/resources">Resources</a></li>
        </ul>
      </div>
      <div>
        <h5>Get in touch</h5>
        <ul>
          <li><a href="mailto:info@kleza.io">info@kleza.io</a></li>
          <li><a href="/contact">Contact form</a></li>
          <li><a href="tel:+19138002728">+1 913-800-2728</a></li>
          <li><a href="tel:+917396146227">+91 7396146227</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&copy; 2026 Kleza Solutions Pvt Ltd <span style="opacity:.5;margin:0 .5em">&middot;</span> All rights reserved</div>
      <div class="right">Healthcare-grade AI <span style="opacity:.5;margin:0 .5em">&middot;</span> ISO Aligned</div>
    </div>
  </div>
</footer>`;

const dir = path.join(process.cwd(), "content");
const files = (await readdir(dir)).filter((f) => f.endsWith(".html"));
const footerRe = /<footer class="footer[\s\S]*?<\/footer>/i;

for (const f of files) {
  const p = path.join(dir, f);
  const html = await readFile(p, "utf8");
  if (!footerRe.test(html)) {
    console.log(`SKIP (no footer match): ${f}`);
    continue;
  }
  await writeFile(p, html.replace(footerRe, FOOTER), "utf8");
  console.log(`updated footer: ${f}`);
}
