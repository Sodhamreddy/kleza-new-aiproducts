// Post-build: turn Next's static export (`out/`) into an upload-ready `dist/`
// for Hostinger shared hosting, and drop in a tuned .htaccess.
import { rm, rename, cp, writeFile, access } from "fs/promises";
import path from "path";

const root = process.cwd();
const out = path.join(root, "out");
const dist = path.join(root, "dist");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Windows + OneDrive frequently hold transient handles on these folders
// (sync, antivirus, a running `serve dist`). Retry destructive ops a few times.
async function rmrf(target) {
  for (let i = 0; i < 6; i++) {
    try {
      await rm(target, { recursive: true, force: true });
      return;
    } catch (e) {
      if (i === 5) throw e;
      await sleep(400);
    }
  }
}

try {
  await access(out);
} catch {
  console.error('No "out/" folder found. Run `next build` first.');
  process.exit(1);
}

await rmrf(dist);

// `rename` is the fast path, but it throws EPERM/ENOTEMPTY on Windows when a
// process (OneDrive, antivirus, a preview server) holds a handle on out/dist.
// Fall back to a recursive copy + delete, which tolerates those locks.
try {
  await rename(out, dist);
} catch (e) {
  if (["EPERM", "ENOTEMPTY", "EEXIST", "EBUSY", "EACCES"].includes(e.code)) {
    console.warn(`rename failed (${e.code}); falling back to copy…`);
    await rmrf(dist);
    await cp(out, dist, { recursive: true });
    await rmrf(out);
  } else {
    throw e;
  }
}

const htaccess = `# Kleza — static export for Hostinger (Apache / LiteSpeed)
Options -MultiViews

# Friendly 404 (Next exports this file)
ErrorDocument 404 /404.html

# Gzip text assets
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

# Long cache for hashed/static assets
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
</IfModule>
`;

await writeFile(path.join(dist, ".htaccess"), htaccess, "utf8");

console.log("dist/ ready (with .htaccess) — upload its contents to public_html");
