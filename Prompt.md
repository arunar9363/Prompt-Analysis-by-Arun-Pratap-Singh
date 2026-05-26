Prompt

Background and Position

As a Senior Full-Stack Frontend Architect & Creative UI Engineer with an expertise in cinematic web storytelling, cyberpunk graphic styling, motion design and animation, and production-ready React applications.

Your assignment is to create and build a full-stack “Cyberpunk Developer Storytelling Portfolio”, which will offer an advanced, futuristic interactive experience rather than a regular portfolio website.

This portfolio should lead the user through:
- identity
- skills
- projects
- experience
- accomplishments
- vision and,
- contact interaction,

via cinematic transitions, neon-style cyberpunk graphics, layered animations, holographic interface designs, and an immersive scroll-based storytelling experience.

Requirements for the application to include:
- responsiveness,
- accessibility,
- scalability,
- front-end architecture,
- animation optimization, and,
- back-end security.
Task Requirements

Build an end-to-end full-stack developer portfolio app that uses:
- Next.js 16.2.6 — Next.js App Router with Route Handler for APIs, next/font for font loading, Metadata API for SEO.
- Framer Motion 12.x — useScroll and useTransform hooks for parallax effect, AnimatePresence for modal transition, staggerChildren for entry animations.
- Tailwind CSS v4 — use @theme directive to define custom design tokens, without using tailwind.config.js.
- TypeScript 5.x — Use strict mode, interface defined for all props & API payload.
- Next.js API Routes — POST Route Handler with rate limiting by IP address using in-memory data structure, no Express.
- Nodemailer 8.x — Send email using SMTP with 3 retries & console fallback if credentials not provided.
- MongoDB + Mongoose 9.x — Use globalThis for caching connection, Contact schema with automatic timestamps.

The app should feature:
- animation-driven scroll storytelling
- cinematic transitions for sections
- future-themed neon UI for cyberpunk
- responsive designs
- modular component system
- secure contact form system
- email notifications
- accessibility considerations
- SEO capabilities
- frontend optimization


Scroll Animation Requirements

Apply animations via Framer Motion using:
- parallax scrolling
- delayed revelation of elements
- fade animations
- movement sequence
- perspective transformation
- animated gradient backgrounds
- cyberpunk particle effects
- hologram effect
- optimized transforms

Provide smooth transitions between:
- Hero Section
- About Section
- Skills Section
- Projects Section
- Experience Timeline
- Vision Section
- Contact Section
Animations will be required to:
- use only transform and opacity CSS properties
- prevent layout thrashing
- maintain smooth performance at 60FPS
- accommodate reduced-motion accessibility
- not affect scroll performance


Requirements for Hero Section

The Hero section should include:
- animated developer introduction
- glitch typography
- cyber-grid animation for the background
- holographic floating UI elements
- cinematic entrance animation
- interactive CTA buttons
- scroll indicator animations

The following content should be included:
- developer’s name
- developer’s role or position
- futuristic tagline
- “Explore Projects” button
- “Get in Touch” button


Requirements for About Section

Implement:
- animated text reveal
- story-based biography timeline
- floating cyberpunk-themed cards
- cinematic transitions
- holographic effects

This section should contain information about:
- developer’s journey
- love for engineering
- technical approach
- creative philosophy


Skills Section Requirements

Futuristic skills visualization system will include:
- animated progress bars
- orbiting icons for various technologies
- neon-colored interactions when hovered
- interactive skill cards
- staggered animation reveals

The skill categories should include:
- Frontend
- Backend
- AI/ML
- DevOps
- Databases
- Cloud
- UI/UX


Requirements for Projects Section

Implement:
- cyberpunk projects cards
- motion interactions when hovered
- animated projects previews
- dynamic lighting effects
- scroll-based reveals

Each project card will require:
- project title
- technologies used in this project
- GitHub link to the code
- live demo link to view the project
- animated preview modal

Use lazy loading to speed up rendering.
Timeline Experience Requirements

Design a futuristic animation for a timeline to include:
- vertical motion transitions
- neon node animations
- line animations connecting nodes
- revealing animation on scrolling
- pulse effect animations for the timeline

Requirements include:
- work experience details
- educational background
- certification details
- personal achievements


Contact System Requirements

Clicking the "Get in Touch" button should:
- trigger an animated modal opening
- blur background dynamically
- use Framer Motion to animate the modal entry/exit
- properly prevent body scroll lock
- focus trap accessibility properly maintained

Form Requirements
- Full name field
- Email address
- Mobile phone number
- Message text area

Requirements include:
- real-time validation
- regex validations
- accessible labels
- validation message pop-ups
- animated error states
- debounced form submissions
- loading state animation
- success/failure feedback animations
Backend API Requirements

The implementation of the secure backend API will be done using:
- Node.js + Express 
OR 
- Next.js API Routes 

It should have:
- input sanitization 
- XSS protection
- injection prevention
- rate limiting
- validation middleware 
- structured logging
- environment variable security
- correct HTTP status code handling

Store form data in database like:
- MongoDB
OR 
- PostgreSQL 

Store: 
- name 
- email 
- phone number 
- message 
- timestamp 
- optionally IP 

Utilize: 
- dotenv
- helmet 
- express-rate-limit 
- validator


Email Notification Requirements

Implementation of email notification using:
- Nodemailer
OR
- Transactional email APIs 

Email Notification Should Include:
- full name
- email
- phone number
- message
- timestamp

It should:
- Secure SMTP credentials using environment variables
- Gracefully handle failures
- Have retry logic
- Provide structured JSON response 

Error Handling Requirements

Frontend Error Handling:
- Manage invalid form submissions elegantly
- Validate input errors dynamically
- Provide animated error messages
- Avoid duplicate form submissions
- Handle loading states and retries
- Manage failed API calls appropriately
- Show fallback error messages to users
- Prevent frontend crashes caused by broken animations

Backend Error Handling:
- Validate all received requests
- Send formatted JSON error response
- Handle database connection errors
- Gracefully handle email failures
- Log server errors securely
- Ensure sensitive errors do not leak out
- Use HTTP status codes properly
- Create a central error handling middleware

Format of an API Error Response:
- success property
- error message
- validation info
- timestamp
- HTTP status code

Reliability of System:
- Do not allow application crashes
- Ensure frontend remains responsive in the event of errors
- Implement retry functionality in case email fails
- Enable graceful fallback in case an optional service fails
- Guard against malformed data and unforeseen exceptions

Performance Requirements

Ensure good performance by optimizing the application with respect to:
- high Lighthouse score
- 60fps animations
- lazy loading
- dynamic imports
- optimized images
- minimized CLS/LCP 
- minimizing unnecessary re-renders
- scalability of front-end rendering 
- minimized bundle size
Animations should never impact scroll smoothness.


Requirements for Accessibility

Implement:
- semantic HTML
- ARIA labels
- keyboard navigation
- screen reader compatibility
- focus management
- reduced-motion accessibility
- color contrast requirements


Requirements for SEO Optimization

Implement:
- metadata optimizations
- Open Graph tags
- Twitter card markup
- structured data
- sitemap integration
- semantic HTML for SEO optimization


Requirements for Code Quality

The code should be:
- modular
- reusable
- scalable
- production-ready
- type-safe
- maintainable
- structured well

Adhere to:
- component-driven architecture
- separation of concerns
- reusable hooks
- reusable animation systems
- good frontend engineering practices


Requirements for Output

Create:
- folder structure
- frontend architecture
- backend architecture
- reusable components
- Framer Motion animations
- responsive layout designs
- API development
- database schema
- environment variables setup
- deployment process
- accessibility guidelines
- performance optimizations
- security measures
- SEO implementation


Final Product Expectations

The final product should deliver:
- an experience like a cinematic futuristic development environment
- an immersive cyberspace narrative creation platform
- a high-end production portfolio
- an award-winning interactive experience

