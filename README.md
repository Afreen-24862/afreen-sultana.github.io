<div align="center">

# Afreen Sultana — Portfolio

**AI/ML · Software · DevOps** &nbsp;|&nbsp; B.Tech CSE (2023 – 2027) · Hyderabad

[**Live site →**](https://afreen-24862.github.io/afreen-sultana.github.io/)

<img src="og-image.jpg" alt="Afreen Sultana — portfolio preview" width="640">

</div>

---

## About

A fast, single-page portfolio with a clean, Apple-inspired design. Instead of only *describing* projects, every project can be **tried live** in the browser — visitors can ask questions, upload text, tap, scan and play.

Built with plain HTML, CSS and JavaScript — **no build step, no framework, no backend.**

## Highlights

- **Try-it-live project demos** — each project opens a working mini-demo with a "How it helps" 3D scene and a case study
- **Live air-quality demo** — real Hyderabad (or any city) data with plain-language health guidance
- **3D CityAir playground** — drag the city, raise the pollution, switch on actions and watch the smog clear
- **Command palette** (`Ctrl/⌘ + K`), light/dark mode that follows the system, and an *Explore* checklist
- **Responsive & accessible** — works from small phones to large screens, keyboard-friendly, respects reduced motion

## Projects

| Project | What it does | Try it |
|---|---|---|
| **CityAir AI** *(flagship)* | LLM assistant built around Hyderabad's pollution data that explains the air and how to reduce it | Ask about today's air |
| **AI Resume Screening Helper** | Python workflow that extracts skills, matches them to job-description keywords and scores relevance | Paste a resume + job description |
| **Student Performance Prediction System** | ML workflow (Pandas, NumPy, Scikit-learn) that predicts student performance from academic data | Adjust habits, see the prediction |
| **DevOps CI/CD Deployment Pipeline** | Build → test → containerize → deploy workflow with release documentation | Run the pipeline, break a test |
| **Forward Deployed Engineering Case Study** | Client workflow-automation case study: requirements → tasks → handover notes | Pick pain points, get a plan |
| **Responsive Portfolio Website** | The site you're looking at — semantic, accessible, mobile-friendly | Resize the screen |
| CampusBot · FaceMark · ReelPick · SentiScope · LibraryHub · TaskFlow | Additional mini-projects, each with a live demo | Open any card |

> The demos run entirely in the browser to show the *idea* of each project. The 3D scenes are illustrative simulations, not measured data.

## Tech

- **Front end:** HTML5, CSS3 (custom properties, fluid type), vanilla JavaScript (ES6+)
- **Motion & 3D:** [GSAP](https://gsap.com/) + ScrollTrigger, [Lenis](https://lenis.darkroom.engineering/) smooth scroll, [Three.js](https://threejs.org/)
- **Data:** [Open-Meteo](https://open-meteo.com/) Air Quality & Geocoding APIs (free, no key)
- **Hosting:** GitHub Pages

## Run locally

```bash
git clone https://github.com/Afreen-24862/afreen-sultana.github.io.git
cd afreen-sultana.github.io
python3 -m http.server 8000
```

Open <http://localhost:8000>. (Use a local server rather than double-clicking `index.html` so the live demos can load data.)

## Project structure

```
├── index.html            Page structure & SEO / share-preview tags
├── css/styles.css        Design system, layout, dark mode, responsive rules
├── js/
│   ├── data.js           ★ All content — edit this to update the site
│   ├── main.js           Rendering, navigation, popups, air-quality demo, animations
│   ├── tryit.js          Interactive project demos + Explore checklist
│   ├── mini3d.js         Per-project "without / with" 3D scenes
│   └── playground.js     CityAir 3D city playground
├── assets/afreen.jpg     Photo
└── favicon*, icon-*, apple-touch-icon.png, og-image.jpg, site.webmanifest, 404.html
```

## Update the content

Everything lives in [`js/data.js`](js/data.js): name, email, links, skills, journey, projects and education.

- Add her profile links in `links` (`linkedin`, `github`, `leetcode`, `resume`) — the buttons appear automatically.
- Replace `assets/afreen.jpg` to change the photo.
- Commit and push — GitHub Pages redeploys in about a minute.

## Deploy

Hosted with **GitHub Pages**: *Settings → Pages → Deploy from a branch → `main` / `(root)`*.
All asset paths are relative, so the site works at `username.github.io` and at project URLs like `username.github.io/repo/`.

## Contact

📧 [afreensultana24862@gmail.com](mailto:afreensultana24862@gmail.com) · 📍 Hyderabad, India

---

<sub>© 2026 Afreen Sultana. Air-quality data © Open-Meteo (CC BY 4.0).</sub>
