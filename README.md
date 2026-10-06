# Afreen Sultana — Portfolio

Static site (no build step). Open `index.html` locally, or deploy to GitHub Pages.

## Deploy to GitHub Pages
1. Create a GitHub repo. For a clean URL name it `<username>.github.io` (site at `https://<username>.github.io/`).
2. Upload **everything in this folder** (including the hidden `.nojekyll` file).
3. Repo → Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)` → Save.
4. Wait ~1 minute, then open the URL.

All paths are relative, so it also works from a project repo (`https://<username>.github.io/<repo>/`).

## After you know the live URL (important for link previews)
In `index.html`, replace every `afreen-24862.github.io` with the real address (5 places: canonical,
`og:url`, `og:image`, `twitter:image`). Then LinkedIn/WhatsApp previews will show `og-image.jpg`.
Tip: LinkedIn caches previews — re-scrape at https://www.linkedin.com/post-inspector/

## Edit content
Everything lives in `js/data.js` — name, email, links, skills, journey, projects, education.
- Add real links in `links` (LinkedIn / GitHub / LeetCode / Resume): buttons appear automatically.
- Replace `assets/afreen.jpg` for a new photo (and re-make `og-image.jpg` if you like).
- Demos: `js/tryit.js` · 3D scenes: `js/mini3d.js`, `js/playground.js`.

## Files
favicon.ico / favicon.svg / favicon-16|32.png / apple-touch-icon.png / icon-192|512.png — browser & phone icons
site.webmanifest — "Add to Home Screen" · og-image.jpg — share preview · 404.html · robots.txt · .nojekyll
