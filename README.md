# ⚡ CYBERPUNK DEVELOPER STORYTELLING PORTFOLIO

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16.2.6-black?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19.2.4-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Framer_Motion-12.x-FF0055?style=for-the-badge&logo=framer&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-4.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-Mongoose-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
</p>

<p align="center">
  <strong>An award-worthy, immersive full-stack developer portfolio with cinematic scroll storytelling, cyberpunk aesthetics, and a secure contact backend — running at a fluid 60FPS.</strong>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features Deep Dive](#features-deep-dive)
  - [Frontend Architecture](#frontend-architecture)
  - [UI Component System](#ui-component-system)
  - [Animation System](#animation-system)
  - [Performance & Accessibility Hooks](#performance--accessibility-hooks)
  - [Backend API](#backend-api)
  - [Database Layer](#database-layer)
  - [Email Notification System](#email-notification-system)
  - [Security & Validation](#security--validation)
- [Page Sections](#page-sections)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Design System](#design-system)
- [Code Quality Notes](#code-quality-notes)

---

## Overview

This is a **production-grade, full-stack cyberpunk-themed developer portfolio** built with Next.js 15+. It goes far beyond a static portfolio — it's an immersive, scroll-driven narrative experience designed to make a lasting impression.

The portfolio guides visitors through a developer's identity, skills, projects, and experience using:

- **Cinematic scroll-based transitions** powered by Framer Motion
- **Matrix rain canvas animation** with FPS-adaptive rendering
- **Glitch typography** with layered CSS clip-path effects
- **Neon holographic card UI** with light glow interactions
- **Secure contact modal** with real-time validation, MongoDB persistence, and SMTP email delivery

The entire system is built with modularity, type-safety, and accessibility as first-class concerns.

---

## Live Demo

> Replace with your deployed URL after setup.

```
https://your-domain.com
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16.2.6 (App Router) |
| UI Library | React 19.2.4 |
| Language | TypeScript 5.x (strict) |
| Styling | Tailwind CSS 4.x with custom `@theme` tokens |
| Animation | Framer Motion 12.x |
| Icons | Lucide React |
| Fonts | Oxanium (display) + Space Mono (monospace) via `next/font` |
| Backend | Next.js API Routes (serverless) |
| Database | MongoDB via Mongoose 9.x |
| Email | Nodemailer 8.x |
| Validation | validator.js 13.x |

---

## Project Structure

```
cyberpunk-portfolio/
├── .env.local                        # Environment variables (never commit this)
├── next.config.ts                    # Next.js configuration
├── tailwind.config / postcss.config  # Tailwind + PostCSS pipeline
├── tsconfig.json                     # TypeScript strict mode config
├── eslint.config.mjs                 # ESLint configuration
│
└── src/
    ├── app/                          # Next.js App Router
    │   ├── layout.tsx                # Root HTML shell: fonts, metadata, nav, overlay effects
    │   ├── page.tsx                  # Main orchestrator: section layout + modal state
    │   ├── globals.css               # Tailwind @theme tokens, keyframes, scrollbar styling
    │   ├── sitemap.ts                # Auto-generated XML sitemap for SEO
    │   └── api/
    │       └── contact/
    │           └── route.ts          # POST endpoint: rate limiting, validation, DB save, email
    │
    ├── components/
    │   ├── layout/
    │   │   ├── CyberNav.tsx          # Fixed navbar with scroll-detect + mobile drawer
    │   │   └── ScrollProgress.tsx    # Spring-physics scroll progress bar
    │   │
    │   ├── sections/
    │   │   ├── Hero.tsx              # Fullscreen hero with parallax, glitch title, CTAs
    │   │   ├── About.tsx             # Animated bio with staggered text reveals
    │   │   ├── SkillsMatrix.tsx      # 3-column skill grid with animated progress bars
    │   │   ├── ProjectShowcase.tsx   # Cyberpunk project cards with hover effects
    │   │   ├── Timeline.tsx          # Vertical experience/education timeline
    │   │   └── ContactModal.tsx      # Full-featured animated contact form modal
    │   │
    │   └── ui/
    │       ├── CyberButton.tsx       # Reusable motion button with neon variants
    │       ├── GlitchText.tsx        # Multi-layer glitch typography effect
    │       ├── MatrixRain.tsx        # Canvas-based Matrix falling characters
    │       └── NeonCard.tsx          # Holographic card with glow borders and corner accents
    │
    ├── hooks/
    │   ├── useReducedMotion.ts       # Respects `prefers-reduced-motion` media query
    │   └── usePerformance.ts         # Live FPS counter to detect low-performance devices
    │
    └── lib/
        ├── db.ts                     # MongoDB connection with Next.js hot-reload safety
        ├── mailer.ts                 # Nodemailer SMTP with 3-attempt retry + fallback logging
        └── validations.ts            # Input sanitization and XSS prevention via validator.js
```

---

## Features Deep Dive

### Frontend Architecture

**`src/app/page.tsx`** — The root page is a client component that manages a single piece of state: whether the `ContactModal` is open. All sections are composed sequentially. The modal is passed a trigger callback from the `Hero` component's CTA button, ensuring clean one-way data flow.

**`src/app/layout.tsx`** — Handles:
- Google Font loading via `next/font` with CSS variable injection (`--font-oxanium`, `--font-space-mono`)
- Full SEO metadata including Open Graph and Twitter Card tags
- Fixed CRT scanline overlay using a `pointer-events-none` div at `z-50`
- Global ambient gradient overlay for the cyberpunk atmosphere
- Mounting `CyberNav` and `ScrollProgress` outside the page content tree

---

### UI Component System

#### `CyberButton.tsx`
A `motion.button` wrapper that accepts three color variants: `cyan`, `pink`, and `purple`. Key implementation details:

- Uses `clipPath: polygon(...)` to produce the characteristic cut-corner cyberpunk shape
- `whileHover` and `whileTap` scale animations are conditionally disabled via `useReducedMotion()`
- Renders decorative glitch-blink accent lines at all four corners using absolutely positioned spans
- Spreads `HTMLMotionProps<"button">` to support all native button attributes including `type`, `disabled`, and `aria-*` props

#### `GlitchText.tsx`
Implements a three-layer glitch effect:

1. **Pink layer** — absolutely positioned, clips to the top 33% of the text using `clipPath`, animates `x`/`y` offsets and multi-color `textShadow` on a loop
2. **Base layer** — the actual readable white text with a soft white `drop-shadow`
3. **Cyan layer** — clips to the bottom 33%, animates at 75% of the primary layer's speed to create desynchronized drift

When `prefers-reduced-motion` is set, the component renders a plain `<span>` with no animation.

#### `MatrixRain.tsx`
Canvas-based falling character animation:

- Dynamically sizes the canvas to its parent container using a debounced resize observer
- Character set is `010101ABCDEF//[]{}<>_+$#@!%&*()-+=`
- Renders at **24FPS** normally; degrades to **12FPS** if `usePerformance()` detects FPS below 45
- Uses `rgba` fill with low opacity (`0.12`) to create the characteristic trailing glow
- Cycles through four palette colors (cyan, purple, pink, dark blue) in a deterministic round-robin per column
- Fully cleaned up on unmount: cancels `animationFrame` and removes resize listener

#### `NeonCard.tsx`
Reusable holographic card component featuring:

- `clipPath` cut-corner on the bottom-right
- Border glow transitions on hover and focus-within for keyboard accessibility
- Micro-grid background overlay (16×16px `repeating-linear-gradient`)
- Animated pulse dots in the top-left and bottom-right corners
- Cybernetic corner accent lines in cyan and pink
- Lift animation (`y: -6`) on hover, disabled under `prefers-reduced-motion`

---

### Animation System

All animations use **only `transform` and `opacity`** CSS properties — zero layout-affecting properties are animated. This is critical for maintaining 60FPS by keeping animations entirely on the compositor thread.

**Scroll-linked animations in `Hero.tsx`:**
```ts
const yBg = useTransform(scrollY, [0, 800], [0, 220]);       // Parallax grid layer
const opacityContent = useTransform(scrollY, [0, 450], [1, 0]); // Fade out on scroll
const scaleContent = useTransform(scrollY, [0, 450], [1, 0.96]); // Subtle scale down
```
These are applied as `motion.div` style props — they update via Framer's internal scheduler, **not React re-renders**, meaning zero React reconciliation cost during scroll.

**Entrance animations** use `variants` with `staggerChildren` so each child reveals sequentially:
```ts
containerVariants = { visible: { transition: { staggerChildren: 0.18, delayChildren: 0.2 } } }
itemVariants = { hidden: { y: 25, opacity: 0 }, visible: { y: 0, opacity: 1, duration: 0.8 } }
```

**Scroll-triggered section reveals** use `whileInView` with `viewport={{ once: true, margin: "-100px" }}` — sections animate in only once, 100px before they enter the viewport. Skill progress bars additionally use `whileInView` with per-bar stagger delays (`delay: skillIdx * 0.04`).

**`ScrollProgress.tsx`** uses `useSpring(scrollYProgress, { stiffness: 120, damping: 25 })` to decouple the progress bar from raw scroll position, adding satisfying spring physics that makes the bar feel responsive without being jittery.

---

### Performance & Accessibility Hooks

#### `useReducedMotion.ts`
Listens to the `(prefers-reduced-motion: reduce)` media query via `addEventListener("change", ...)`. Every animated component consumes this hook and conditionally disables all motion. This is implemented at the component level, not globally, so non-animated components are unaffected.

#### `usePerformance.ts`
Runs a `requestAnimationFrame` loop, counting frames per second using `performance.now()` delta timing. Exposes `{ fps, isLowPerformance: fps < 45 }`. The `MatrixRain` canvas uses this to halve its draw rate on devices that can't sustain 24FPS, preventing the canvas from becoming a performance bottleneck.

---

### Backend API

**`src/app/api/contact/route.ts`** — Next.js Route Handler (serverless-compatible POST endpoint).

**In-memory rate limiting:**
```ts
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();
```
Uses an IP-keyed map with a 1-minute sliding window and a hard cap of 3 requests. On breach, returns HTTP `429` with a structured JSON error body. Security warnings are logged via `console.warn`.

**Request pipeline:**
1. Extract IP from `x-forwarded-for` header (proxy-safe)
2. Rate limit check → 429 if exceeded
3. Parse JSON body
4. Run `sanitizeAndValidateContact()` → throws on invalid input
5. `connectToDatabase()` → saves `Contact` document to MongoDB
6. `sendNotificationEmail()` → SMTP delivery with fallback logging
7. Return `{ status: "TRANSMITTED", recipient: email }` with HTTP 200

All responses include security headers: `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.

---

### Database Layer

**`src/lib/db.ts`** — Implements connection caching via `globalThis.mongoose` to prevent multiple connections during Next.js hot module reloading in development:

```ts
let cached = globalThis.mongoose; // { conn: null, promise: null }
if (!cached.conn) {
  cached.promise = mongoose.connect(MONGODB_URI, { bufferCommands: false });
  cached.conn = await cached.promise;
}
```

**Contact Schema:**

| Field | Type | Notes |
|---|---|---|
| `fullName` | String | required, trimmed |
| `email` | String | required, trimmed, lowercased |
| `phone` | String | optional, trimmed |
| `message` | String | required |
| `ipAddress` | String | optional, logged from request |
| `userAgent` | String | optional, logged from request |
| `createdAt` | Date | auto via `timestamps: true` |
| `updatedAt` | Date | auto via `timestamps: true` |

Model is exported safely for hot-reload: `mongoose.models.Contact || mongoose.model("Contact", ...)`.

---

### Email Notification System

**`src/lib/mailer.ts`** — Nodemailer-based SMTP dispatcher with resilience features:

- Reads all credentials from environment variables (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `CONTACT_NOTIFICATION_EMAIL`)
- **Fallback logging mode:** If SMTP credentials are absent or contain placeholder values, the function logs the formatted email payload to `console.log` instead of throwing. This prevents development environments from timing out on email attempts.
- **3-attempt retry loop:** If SMTP delivery fails, it retries up to 3 times before throwing a descriptive error
- **Dual format email:** Sends both a plain text version and a styled HTML version with cyberpunk branding (dark background, neon borders, monospace font)

---

### Security & Validation

**`src/lib/validations.ts`** — Uses the `validator` library for all sanitization:

- `validator.escape()` on all string fields to prevent XSS via HTML entity encoding
- `validator.isEmail()` + `validator.normalizeEmail()` for email fields
- `validator.isMobilePhone(phone, "any")` for E.164 international phone format
- `validator.isLength(message, { min: 10, max: 2000 })` for message body
- All validation failures throw descriptive `Error` objects caught by the API route's try/catch

**Frontend validation in `ContactModal.tsx`:**
- Real-time field-level validation on `onBlur` (validates touched fields only)
- Full form validation on submit (validates all fields simultaneously)
- Error state reflected by border color change (gray → pink) and `aria-invalid` attribute
- Each error message is linked to its input via `aria-describedby` for screen readers
- Keyboard focus trap implemented manually via `querySelectorAll` of focusable elements + Tab/Shift+Tab handling
- Escape key closes the modal
- Body scroll locked via `document.body.style.overflow = "hidden"` when open

---

## Page Sections

### Hero (`id="home"`)
Full-viewport section with:
- MatrixRain canvas background at 15% opacity in `screen` blend mode
- Parallax CSS grid that drifts upward at 27.5% of scroll speed
- Ambient radial glow blobs (cyan bottom-left, pink top-right)
- Staggered entrance animation for badge, headline, subtext, and CTA buttons
- Fixed status readouts in the bottom corners (desktop only)
- Bouncing scroll indicator arrow

### About (`id="about"`)
Developer bio with story-driven narrative, animated text reveal on scroll entry, floating NeonCards for personal stats, and holographic section dividers.

### Skills Matrix (`id="skills"`)
Three-column responsive grid of NeonCards (Frontend, Backend, DevOps/AI). Each card contains animated progress bars that fill from 0% to the skill level when scrolled into view, with staggered delays per bar. Cards lift on hover with neon glow transitions.

### Project Showcase (`id="projects"`)
Grid of project cards built with NeonCard, each featuring:
- Project title, description, and tech tag list
- GitHub and Live Demo icon links
- Cyberpunk sector tag badge
- Hover motion lift and border glow

### Timeline (`id="experience"`)
Vertical timeline for work experience, education, and certifications. Each node has a neon pulse indicator, animated line connector, and scroll-triggered reveal. Supports multiple entry types with distinct visual treatment.

### Contact Modal
Triggered by the Hero's "INITIALIZE_HANDSHAKE" button. Features:
- Framer Motion `AnimatePresence` for enter/exit animations with scale + translate
- Backdrop blur overlay
- Fully accessible: ARIA roles, focus trap, Escape to close, auto-focus first input
- Real-time form validation with animated error states
- Success screen with animated checkmark on submission
- POSTs to `/api/contact` and handles loading/success/error states

---

## Environment Variables

Create a `.env.local` file in the project root:

```env
# MongoDB
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/cyber_portfolio

# SMTP Email (example: Gmail, SendGrid, Resend)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Notification recipient
CONTACT_NOTIFICATION_EMAIL=your-email@gmail.com

# Site URL for sitemap generation
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

> **Note:** If SMTP credentials are missing or left as placeholders, the mailer gracefully falls back to logging the message payload in the console. The app will not crash.

---

## Getting Started

### Prerequisites
- Node.js 18.17+ or 20+
- npm or yarn
- A MongoDB Atlas cluster (or local MongoDB instance)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cyberpunk-portfolio.git
cd cyberpunk-portfolio

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Then fill in your values in .env.local

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Available Scripts

```bash
npm run dev      # Start development server with hot reload
npm run build    # Production build
npm run start    # Start production server
npm run lint     # ESLint code check
```

---

## Deployment

### Vercel (Recommended)

1. Push your repository to GitHub
2. Connect it to [Vercel](https://vercel.com)
3. Add all environment variables in the Vercel dashboard under **Settings → Environment Variables**
4. Deploy — Next.js API routes are automatically deployed as serverless functions

### Other Platforms (Render, Railway, etc.)

Ensure your deployment platform supports:
- Node.js 18+
- Environment variable injection
- Persistent file system is **not** required (MongoDB is remote)

---

## Design System

The cyberpunk theme is defined entirely in `src/app/globals.css` using Tailwind 4's `@theme` directive:

```css
@theme {
  --color-cyber-bg:     #05050a;   /* Near-black deep space background */
  --color-cyber-darker: #020204;   /* Even darker for modal/card surfaces */
  --color-cyber-cyan:   #00f0ff;   /* Primary neon accent */
  --color-cyber-purple: #9d4edd;   /* Secondary accent */
  --color-cyber-pink:   #ff007f;   /* Highlight / error / warning */
  --color-cyber-blue:   #004bba;   /* Deep blue accent */

  --shadow-neon-cyan:   0 0 10px rgba(0,240,255,0.5), 0 0 20px rgba(0,240,255,0.2);
  --shadow-neon-pink:   0 0 10px rgba(255,0,127,0.5), 0 0 20px rgba(255,0,127,0.2);
  --shadow-neon-purple: 0 0 10px rgba(157,78,221,0.5), 0 0 20px rgba(157,78,221,0.2);
}
```

**Typography:**
- Display headings: **Oxanium** (futuristic variable weight sans)
- Code / monospace labels: **Space Mono** (bitmap-influenced monospace)
- Both loaded via `next/font/google` with `display: "swap"` for zero layout shift

**Custom scrollbar:** Styled in neon cyan with a pink hover state, matching the overall palette.

---

## Code Quality Notes

- **TypeScript strict mode** is enabled — all props, API payloads, and hook return values are fully typed
- **Component-driven architecture** — all UI is broken into reusable atoms (`CyberButton`, `NeonCard`, `GlitchText`) and composed into section-level organisms
- **Separation of concerns** — business logic (validation, DB, email) is fully isolated in `src/lib/`, never mixed into components
- **No layout thrashing** — animations exclusively use `transform` and `opacity`; scroll transforms run on Framer's internal tick, not React's render cycle
- **Accessibility-first** — ARIA labels on all interactive elements, focus trapping in modal, keyboard navigation, `useReducedMotion` honored throughout
- **Hot-reload safe** — MongoDB connection and Mongoose models are cached on `globalThis` to survive Next.js HMR without spawning duplicate connections
- **Graceful degradation** — SMTP failure does not crash the API; low FPS devices get a reduced-frame canvas animation; reduced-motion users get static layouts

---

## License

MIT License — see [LICENSE](Golden%20Response/LICENSE) for full terms.

---

<p align="center">Built by <strong>Arun Pratap Singh</strong> · Prompt Analysis Submission</p>