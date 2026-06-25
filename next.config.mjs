/** @type {import('next').NextConfig} */
const nextConfig = {
  // The prototype's classic scripts declare top-level `const`s (e.g. `header`).
  // Strict Mode double-invokes effects in dev, which would re-execute those
  // scripts and throw "Identifier already declared". Each route is a full page
  // load, so the dev double-invoke buys us nothing here.
  reactStrictMode: false,

  // Static HTML export for shared hosting (Hostinger). `next build` emits a
  // fully static `out/` folder (no Node server needed); make-dist.mjs renames
  // it to `dist/`. trailingSlash keeps every route directory-based so Apache /
  // LiteSpeed serve `/about/` -> `/about/index.html` without extra rules.
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },

  // Static export needs no server file-tracing. Skipping it also avoids a
  // spurious `.nft.json` ENOENT during `next build` when the project lives on
  // a OneDrive-synced path (OneDrive moves trace files mid-build).
  outputFileTracing: false,

  // Dev-only: stop Watchpack from scanning the C:\ drive root (it hits locked
  // system files like pagefile.sys -> EINVAL on Windows). Gated to `dev` so it
  // never touches the static export build.
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        ...(config.watchOptions || {}),
        ignored: [
          "**/node_modules/**",
          "**/.next/**",
          "**/.git/**",
          "**/DumpStack.log.tmp",
          "**/hiberfil.sys",
          "**/pagefile.sys",
          "**/swapfile.sys",
        ],
      };
      // The webpack filesystem cache uses atomic renames (`x.pack.gz_` ->
      // `x.pack.gz`) which fail with EPERM/ENOENT on Windows + OneDrive/Downloads
      // paths, corrupting `.next` and causing "Cannot find module './NNN.js'".
      // Use an in-memory cache in dev to avoid that entirely.
      config.cache = { type: "memory" };
    }
    return config;
  },
};

export default nextConfig;
