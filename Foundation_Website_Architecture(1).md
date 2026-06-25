# SKIFCO — Web Application Architecture & Build Plan

**Stack:** Django 6.x (MVT, Python 3.12+) · PostgreSQL · Bootstrap 5 · jQuery/AJAX · Razorpay · Django Admin as staff control panel · Django built-in Tasks (async)
**Scope confirmed:** Public site + beneficiary/application management · Donations with 80G receipts · Events & camps · Photo/video gallery · Volunteer signup · English only

> **3 assumptions I'm making until you confirm** — please correct any:
> 1. Trust's registered name is **SKIFCO** (display name; final legal style e.g. "SKIFCO Foundation/Trust" to confirm). Project package: `sfoundation`.
> 2. The trust either holds, or is applying for, **12A + 80G** registration. Tax-deductible receipts are only legally valid once 80G is granted, so the donation module is built to switch on receipts the day registration is in hand.
> 3. Deployment target is a **single Linux VPS** (e.g. Hostinger/DigitalOcean/Contabo) to start, with a clean path to scale. Change this and the deployment section changes.

---

## 1. Requirement Analysis

### 1.1 Actors (who uses the system)
| Actor | What they do | Access |
|---|---|---|
| **Public visitor** | Browse programs, read stories, view gallery/events, donate | No login |
| **Donor** | Donate, get 80G receipt, see donation history | Optional account |
| **Applicant (beneficiary)** | Apply for aid (scholarship, medical, skill training, relief), upload documents, track status | Account required |
| **Volunteer/Member** | Register interest, see assigned events | Account required |
| **Staff / Program Officer** | Review applications, manage events, upload gallery, publish news | Django admin |
| **Trustee / Super-admin** | Everything + financial reports, user management | Django admin |

### 1.2 Functional requirements
- **Content (admin-managed):** Programs by 7 pillars, News/Blog, Impact stats, Team/Trustees, Partners, static pages (About, Objectives, Contact, Privacy, Terms, Refund).
- **CSR & Partnerships:** Dedicated page (why partner, CSR project categories, implementation & reporting approach) + a **partner/CSR inquiry form** captured to admin.
- **Reports & Transparency:** Admin-uploadable annual reports / audited statements (PDF), shown on a public Transparency page — a credibility multiplier for donors and CSR.
- **Donations:** One-time + recurring, preset + custom amounts, Razorpay checkout, server-side verification, auto 80G receipt PDF, donor dashboard.
- **Beneficiary applications:** Multi-type application form, document upload, status workflow (Submitted → Under Review → Approved/Rejected → Disbursed), applicant status tracking, staff review queue.
- **Events & camps:** Calendar + list, event detail, public registration, capacity limits.
- **Gallery:** Albums with photos and embedded videos (YouTube/self-hosted), lazy-loaded.
- **Volunteers:** Signup form with area-of-interest + skills + availability + consent, admin assignment.
- **Legal pages (required before donations go live):** Privacy Policy, Terms & Conditions, Refund/Cancellation Policy, Contact — Razorpay will not approve a live merchant account without these published.
- **Engagement & discovery:** Newsletter signup, contact form, WhatsApp click-to-chat, SDG alignment content, SEO metadata + sitemap.xml + robots.txt + schema markup.

### 1.3 Non-functional requirements
Mobile-first (most of your UP audience and donors are on phones), page loads under ~2.5s on 4G, WCAG-AA-leaning accessibility, secure handling of PII/financial data, English-only, SEO-friendly URLs and metadata.

### 1.4 The objectives → site structure mapping
Your 7 main pillars become **Program categories**, not hardcoded pages:
`Education · Healthcare · Skill Development · Environment · Research & Innovation · Partnerships · Community Development`
Every program is a database row tagged to a pillar. Add/edit/retire from admin forever — no developer needed.

---

## 2. System Architecture

```
                    ┌─────────────────────────────────────────┐
   Visitor /        │              NGINX (reverse proxy)        │
   Donor /          │   TLS termination · static/media · gzip   │
   Applicant ──────▶│              rate limiting                │
                    └───────────────┬───────────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │     Gunicorn (WSGI workers)    │
                    │         Django 6.x (3.12+)     │
                    │  ┌──────────────────────────┐  │
                    │  │  Public site (MVT views) │  │
                    │  │  AJAX views (JsonResponse)│  │
                    │  │  Django Admin (staff)     │  │
                    │  └──────────────────────────┘  │
                    └───┬───────────┬────────────┬───┘
                        │           │            │
              ┌─────────▼──┐  ┌─────▼─────┐  ┌───▼──────────┐
              │ PostgreSQL │  │   Redis    │  │ Media storage │
              │ (primary)  │  │ cache +    │  │ local FS now, │
              │            │  │ task backend │ │ S3-ready later│
              └────────────┘  └─────┬──────┘  └──────────────┘
                                    │
                            ┌───────▼────────┐
                            │ Django Tasks    │  async: receipt PDFs,
                            │ worker (or Celery)│ emails, image thumbs
                            └────────────────┘
                                    │
                External:  Razorpay API · SMTP/email · WhatsApp link
```

**Why this shape:** Django serves both the public MVT pages and a thin REST/AJAX layer for dynamic bits (donation, application submit, status check, gallery load-more). Django Admin *is* the staff backend — no separate dashboard to build. Django 6's built-in Tasks framework (backed by Redis or the DB) keeps slow work (PDF generation, email, thumbnails) off the request cycle so pages stay fast — no Celery needed at this scale; Celery remains a drop-in upgrade if volume/scheduling grows. Everything except Razorpay runs on one box at launch and splits onto separate hosts later without code changes.

---

## 3. Database Design

### 3.1 Apps (bounded contexts)
```
accounts      → custom User, roles, profiles
core          → SiteConfig, ImpactStat, ContactMessage, Newsletter, static Page
                (Page covers About, Objectives, Privacy, Terms, Refund)
programs      → Program, ProgramCategory, (optional) SDGGoal tags
events        → Event, EventRegistration
gallery       → Album, MediaItem
volunteers    → Volunteer, InterestArea
partnerships  → Partner, CSRCategory, CSRInquiry          ← from start guide
transparency  → Report (annual reports / audited PDFs)     ← from start guide
donations     → Donation, Receipt, RecurringPlan
beneficiaries → Application, ApplicationDocument, ApplicationStatusLog, AidType
news          → Post, Category, Tag
stories       → ImpactStory   (testimonials / social proof)
```

### 3.2 Core entities & relationships (text ERD)

```
User (accounts)
 ├─ id, email (login), full_name, phone, role[applicant|volunteer|donor|staff|admin]
 ├─ is_active, is_staff, date_joined
 └─ 1─1 ApplicantProfile / VolunteerProfile (optional, role-based)

ProgramCategory (the 7 pillars)
 └─ id, name, slug, icon, order

Program
 ├─ id, category_FK → ProgramCategory, title, slug, summary, body(rich)
 ├─ cover_image, is_featured, is_active, start_date, created/updated
 └─ indexes: (slug), (category, is_active)

Event
 ├─ id, title, slug, category_FK?, description, venue, address
 ├─ start_datetime, end_datetime, capacity, is_published, cover_image
 └─ 1─N EventRegistration (name, email, phone, attendees, created)

Album → 1─N MediaItem
 MediaItem: type[image|video], file/url, caption, thumbnail, order

Volunteer
 └─ user_FK?, name, email, phone, skills(M2M Skill), availability, message, status

Donation
 ├─ id, donor_FK? (User, nullable for guests), donor_name, donor_email, donor_phone
 ├─ donor_pan (for >₹ receipts), donor_address
 ├─ amount, currency, type[one_time|recurring], program_FK? (earmark)
 ├─ razorpay_order_id, razorpay_payment_id, razorpay_signature
 ├─ status[created|paid|failed|refunded], paid_at, created_at
 └─ 1─1 Receipt
 Receipt: receipt_no(unique seq), pdf_file, eighty_g_number, issued_at

AidType (lookup: Scholarship, Medical Aid, Skill Training, Relief, Other)

Application (the sensitive core)
 ├─ id, applicant_FK → User, aid_type_FK → AidType, reference_no(unique)
 ├─ details(JSON/structured), requested_amount?
 ├─ status[submitted|under_review|approved|rejected|disbursed]
 ├─ assigned_to_FK? (staff User), reviewer_notes(internal), created/updated
 ├─ 1─N ApplicationDocument (file, doc_type, uploaded_at)
 └─ 1─N ApplicationStatusLog (from_status, to_status, by_user, note, at)

SiteConfig (singleton): name, tagline, logo, contact, socials, whatsapp,
                        razorpay_keys(ref), eighty_g_number, twelve_a_number,
                        registered_address, donations_enabled(bool)
ImpactStat: label, value, suffix, order   (homepage counters)
Partner: name, logo, url, type[csr|institution|govt|ngo], order, is_active
CSRCategory (lookup): name, description   (e.g. Digital Classroom, Mobile Medical Unit)
CSRInquiry: org_name, contact_person, email, phone, csr_category_FK?,
            budget_range?, message, created, is_handled   ← partner lead capture
Report (transparency): title, type[annual|audit|impact], pdf_file, year,
                       published_at, is_public
Page (static/flat): title, slug, body(rich), is_published   ← About, Objectives,
                    Privacy, Terms, Refund
SDGGoal (optional tag): number, title, M2M → Program
Post (news): title, slug, excerpt, body, cover, author_FK, published_at, status
ImpactStory: name, photo, quote, program_FK?, is_featured
Newsletter: email(unique), subscribed_at
ContactMessage: name, email, phone, subject, message, created, is_read
```

**Key indexing/constraints:** unique on `slug` fields, `Donation.razorpay_order_id`, `Receipt.receipt_no`, `Application.reference_no`, `Newsletter.email`; composite index on `Application(status, aid_type)` and `Donation(status, created_at)` for admin filtering and reports; `on_delete=PROTECT` on financial FKs (never silently delete a paid donation), `SET_NULL` on optional links.

---

## 4. Folder Structure

```
foundation/
├── manage.py
├── requirements/
│   ├── base.txt        # Django>=6.0, psycopg[binary], Pillow, razorpay, redis, WeasyPrint, django-environ
│   ├── dev.txt         # + django-debug-toolbar
│   └── prod.txt        # + gunicorn, sentry-sdk
├── .env                # secrets (NOT in git)
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py · asgi.py
│   └── tasks.py        # Django Tasks config (swap to celery.py if Celery chosen)
├── apps/
│   ├── accounts/  ├── core/       ├── programs/
│   ├── events/    ├── gallery/    ├── volunteers/
│   ├── donations/ ├── beneficiaries/ ├── news/ └── stories/
│        each: models.py, views.py (CBVs), urls.py, forms.py,
│              admin.py, services.py, tests/
├── templates/
│   ├── base.html
│   ├── partials/   (navbar, footer, donation_modal, ...)
│   ├── pages/      (home, about, contact, ...)
│   └── <app>/      (per-app templates)
├── static/
│   ├── css/  (custom.css over Bootstrap)
│   ├── js/   (donation.js, application.js, gallery.js)
│   ├── img/
│   └── vendor/ (bootstrap, jquery)
├── media/          (uploads — served by NGINX, gitignored)
└── docs/
```

**Why split settings + `apps/` package:** environment-specific config without `if DEBUG` spaghetti, and a clean namespace so app names never collide with pip packages. `services.py` per app keeps business logic out of views (thin views, fat services) — this is the single biggest maintainability win.

---

## 5. Views & URL Design (generic CBVs — no REST/API layer)

Per your decision, **no DRF / API layer.** Everything is server-rendered with Django's generic class-based views; forms post normally and re-render with messages. Only the handful of genuinely dynamic actions (Razorpay handshake, gallery lazy-load) use small plain `JsonResponse` views called by jQuery — no framework needed. All writes are CSRF-protected and rate-limited.

**Page & form views (generic CBVs):**

| View | Base class | URL | Auth |
|---|---|---|---|
| Home | `TemplateView` | `/` | none |
| About | `DetailView` (Page) | `/about/` | none |
| Our Objectives | `DetailView` (Page) | `/objectives/` | none |
| Programs list / detail | `ListView` / `DetailView` | `/programs/`, `/programs/<slug>/` | none |
| CSR & Partnerships | `TemplateView` + form | `/csr-partnerships/` | none |
| CSR inquiry submit | `CreateView` | `/csr-partnerships/enquire/` | none |
| Reports & Transparency | `ListView` (Report) | `/reports/` | none |
| Events list / detail | `ListView` / `DetailView` | `/events/`, `/events/<slug>/` | none |
| Event register | `CreateView` | `/events/<slug>/register/` | none |
| Gallery albums / album | `ListView` / `DetailView` | `/gallery/`, `/gallery/<slug>/` | none |
| Volunteer signup | `CreateView` | `/volunteer/` | none |
| Contact | `FormView` | `/contact/` | none |
| News / Blog list / detail | `ListView` / `DetailView` | `/blog/`, `/blog/<slug>/` | none |
| Donate page | `TemplateView` | `/donate/` | none |
| Donation success | `TemplateView` | `/donate/success/` | none |
| Legal pages | `DetailView` (Page) | `/privacy-policy/`, `/terms/`, `/refund-policy/` | none |
| Donor history | `ListView` | `/account/donations/` | donor (own) |
| Apply for aid | `CreateView` | `/apply/` | applicant |
| My applications | `ListView` | `/account/applications/` | applicant (own) |
| Application status | `DetailView` | `/account/applications/<ref>/` | applicant (owner) |

**Small AJAX views (plain function/`View` returning `JsonResponse`):**

| Endpoint | Purpose |
|---|---|
| POST `/donate/create-order/` | Create Razorpay order, return order_id |
| POST `/donate/verify/` | Verify signature server-side, mark paid, queue receipt |
| GET `/gallery/<slug>/items/` | Lazy-load next batch of media |
| POST `/newsletter/subscribe/` | Newsletter signup |

**The ownership rule (unchanged and non-negotiable):** every applicant-facing `ListView`/`DetailView` overrides `get_queryset()` to filter to `request.user`, so a 404 — not someone else's data — is returned if a URL is tampered with. Enforced by `LoginRequiredMixin` + a custom `ApplicantRequiredMixin` for role.

---

## 6. UI/UX Layout Design

**Design language:** clean, trustworthy, lots of white space, your green-on-light palette (pulled from the logo concept — green = growth/environment fits your pillars). Mobile-first.

```
HOME
┌──────────────────────────────────────────┐
│ Navbar: Logo | Programs Events Gallery    │
│         About News | [ Donate ]  (sticky) │  ← Donate CTA in header
├──────────────────────────────────────────┤
│ HERO: mission line + photo/video           │
│   [ Donate Now ]   [ Apply for Aid ]        │  ← two primary actions
├──────────────────────────────────────────┤
│ IMPACT STATS:  1,200 students · 40 camps…  │  ← animated counters
├──────────────────────────────────────────┤
│ FOCUS AREAS: 7 pillar cards (icon+blurb)    │
├──────────────────────────────────────────┤
│ FEATURED PROGRAMS  (cards)                  │
├──────────────────────────────────────────┤
│ IMPACT STORIES  (beneficiary quotes/photos) │  ← social proof
├──────────────────────────────────────────┤
│ UPCOMING EVENTS  +  GALLERY teaser          │
├──────────────────────────────────────────┤
│ DONATE BAND (repeat CTA) + Newsletter        │
├──────────────────────────────────────────┤
│ FOOTER: contact, address, 80G/12A no.,       │
│   socials, WhatsApp, [ Donate ] (repeat)     │
└──────────────────────────────────────────┘
```

**Donation flow (modal, 3 steps):** amount (presets ₹500/₹1000/₹2500 + custom) → details (name, email, phone, PAN+address if claiming 80G) → Razorpay checkout → success page + emailed receipt. Research shows preset amounts, concrete impact framing ("₹1000 funds a month of a child's tuition"), and repeating the Donate button in header/hero/footer materially lifts conversions.

**Apply-for-aid flow:** register/login → choose aid type → fill form → upload documents → submit → tracking page with a clear status timeline.

> I can render clickable wireframes and an ERD diagram inline whenever you want to see them visually — just say the word.

---

## 7. Implementation Plan (phased)

| Phase | Deliverable | Why this order |
|---|---|---|
| **0. Foundation** | Project scaffold, split settings, custom User model, base template, deploy a "hello" to the VPS | Custom User MUST exist before first migration — non-negotiable |
| **1. Public core (your MVP)** | core app, SiteConfig, Programs, Home, About, Objectives, CSR & Partnerships (+inquiry), Contact, **legal pages (Privacy/Terms/Refund)** | Matches your guide's MVP page list; legal pages here so the donation gateway can be approved in Phase 3 |
| **2. Engagement & trust** | Events + registration, Gallery, Volunteers, Reports & Transparency, Blog, Newsletter | High-value, low-risk; Reports/Blog build donor & CSR credibility |
| **3. Donations** | Razorpay integration, donation modal, receipts (80G-ready) | Revenue; needs careful testing in Razorpay test mode; requires Phase 1 legal pages live |
| **4. Beneficiaries** | Applications, documents, status workflow, staff review | Most sensitive — built last, on a hardened auth base |
| **5. Hardening & launch** | Security pass, performance, SEO (sitemap/robots/schema), backups, monitoring, content review | Includes your guide's review/launch checklists |

Each phase ends deployable. We build, you review, we move on. This sequence folds your guide's 5-phase launch plan and MVP page list into our technical phasing — same destination, ordered for dependency safety (legal pages before live donations, hardened auth before beneficiary data).

---

## 8. Build Deliverables (per phase — no code in this plan)

This is a planning document, so no code is included here. Working, production-ready code is delivered phase by phase per the Section 7 plan, each phase ending in a deployable state. The concrete deliverables per phase:

- **Phase 0 — Foundation:** project scaffold, split settings (base/dev/prod), custom User model + migrations, base Bootstrap 5 template, `.env` template, deployed "it's alive" page on the VPS.
- **Phase 1 — Public core:** `core` (SiteConfig, ImpactStat, Partner, static pages), `programs` (categories + programs), Home, About, Contact, News — all wired to Django admin for staff editing.
- **Phase 2 — Engagement:** Events + registration, Gallery (albums/media + lazy-load), Volunteer signup, Newsletter.
- **Phase 3 — Donations:** Razorpay integration (test mode first), donation modal, server-side signature verification, 80G-ready receipt generation, donor history.
- **Phase 4 — Beneficiaries:** Applications, document upload, audited status workflow, owner-only tracking views, staff review queue in admin.
- **Phase 5 — Hardening:** security pass, performance/caching, SEO, backups, monitoring, launch.

Each delivery includes models, views (generic CBVs), forms, admin config, templates, and tests for that module.

## 9. Security Considerations

Beneficiary data (income, medical need, ID documents) is the highest-risk asset here, so security is first-class, not a checkbox.

- **Auth:** custom User, email login, Django's PBKDF2 hashing, strong password validators, lockout after repeated failures (django-axes), email verification before applications.
- **Authorization:** object-level checks — an applicant can only ever read/modify *their own* application; staff scoped by role; trustees only for financial reports. Never filter by client-supplied IDs without an ownership check.
- **Sensitive documents:** uploaded files stored **outside the web root**, served only through a permission-checked Django view (never a public media URL), validated for type/size, virus-scan hook ready.
- **Payments:** no card data ever touches your server (Razorpay-hosted), signature verified server-side, webhook endpoint also verified, idempotent payment handling to prevent double-credit.
- **Transport & headers:** HTTPS only, HSTS, secure+httponly cookies, CSRF on all writes, clickjacking protection, and a strict **Content Security Policy via Django 6's built-in `ContentSecurityPolicyMiddleware`** (no third-party `django-csp` needed).
- **Input:** Django ORM (no raw SQL) blocks injection; autoescaping + bleach on any rich text blocks XSS; rate-limit public POST endpoints.
- **PII discipline:** collect only what's needed, mask PAN in admin lists, restrict who can view documents, log access to sensitive records, document a retention policy.
- **Secrets:** all in `.env`/environment, never in git; rotate Razorpay/email keys on staff changes.

---

## 10. Performance Optimization

- **DB:** indexes as listed; `select_related`/`prefetch_related` on list views; paginate everything; avoid N+1 in admin (`list_select_related`).
- **Caching:** Redis for the homepage, program/category lists, and impact stats (low-churn, high-traffic); template fragment caching for navbar/footer; cache invalidation on save via signals.
- **Media:** Pillow-generated responsive thumbnails, WebP, lazy-loading, width/height set to avoid layout shift; gallery loads via AJAX in batches.
- **Static:** WhiteNoise or NGINX for compressed, far-future-cached, hashed static files; defer non-critical JS; ship only the Bootstrap/jQuery you use.
- **Async:** Django 6 built-in Tasks handle PDF receipts, emails, and thumbnailing so requests stay fast (Celery as an upgrade path if needed).
- **Front-end budget:** target <2.5s LCP on 4G; measure with Lighthouse before launch.

---

## 11. Deployment Strategy

**Launch (single VPS):**
- Ubuntu LTS · Python 3.12+ · NGINX (TLS via Let's Encrypt/Certbot) · Gunicorn (systemd) · PostgreSQL · Redis · Django Tasks worker (systemd; or Celery worker+beat if chosen).
- Code from git, `prod.txt` deps in a virtualenv, `collectstatic`, `migrate` on deploy.
- **Backups:** nightly `pg_dump` + media sync to off-site/object storage; test restores.
- **Monitoring:** Sentry for errors, UptimeRobot for uptime, basic log rotation.
- **Domain/email:** point DNS, configure SPF/DKIM on your transactional email (so receipts don't land in spam).
- **CI (optional but recommended):** GitHub Actions runs tests + lint on push; deploy on tag.

**Scale path when you outgrow one box:** move PostgreSQL and Redis to managed instances, move media to S3-compatible storage + CDN, run multiple Gunicorn hosts behind a load balancer — all without application code changes, because the architecture already separates these concerns.

---

---

# Part II — Content & Information Architecture

*Integrated from the project start guide. Part I above is the technical architecture; Part II governs the sitemap, page content, and — most importantly — how the copy gets written. Project package name: `sfoundation`.*

## 12. Content Strategy & Writing Principles  *(the governing rule)*

All website copy is **original** — written from the Trust deed objectives, local needs, planned activities, and real future goals. Reference NGO sites are studied **only** for structure, program categorisation, and content flow. Never for their text, photos, impact numbers, or project names.

Non-negotiable content rules:
- No copy-pasted paragraphs, and no other NGO's wording, impact figures, photos/graphics, or project names.
- **No claims of completed work or impact numbers until the Trust has real records.** Until then, use intent framing: *"we aim to," "we plan to," "our focus will be," "the Trust intends to support."*
- Simple, honest, human, warm-but-professional tone — it should read as if the founders and team wrote it, not a generic template.
- The Trust deed's legal language stays in official documents; the website presents simplified, public-friendly versions of the objectives.
- Every page must pass the human-content check: does it sound like a real organisation, stay clear and simple, avoid fake claims, match the objectives, explain who benefits and what's planned, invite people to connect, and feel trustworthy?

**How this affects the build:** when I draft per-page content in each phase, I write to these rules and hand you editable drafts to approve — never locked text. Real photos and impact numbers are added by your team only when they genuinely exist.

## 13. Information Architecture (sitemap)

**Target navigation (full):**
```text
Home · About Us · Our Objectives
Programs ▸ Education · Healthcare · Skill Development · Environment ·
           Innovation & STEM · Community Development · Disaster Relief · Elderly Care
CSR & Partnerships · Volunteer · Donate · Gallery · Reports & Transparency
Blog · Contact Us   (footer: Privacy · Terms · Refund Policy)
```

**First-launch MVP navigation (fewer pages, ship fast):**
```text
Home · About Us · Programs · CSR & Partnerships · Volunteer/Donate · Contact Us
(+ Privacy · Terms · Refund in footer — required before donations go live)
```

**Canonical routes:** `/ · /about · /objectives · /programs · /programs/<slug> · /csr-partnerships · /volunteer · /donate · /gallery · /reports · /blog · /contact · /privacy-policy · /terms · /refund-policy`

## 14. Page-by-Page Content Plan

**Home** — hero with one clear message + intro + focus areas + "why this work matters" + program cards + how to support + CSR CTA + contact CTA. Primary CTAs: *Explore Our Programs · Partner With Us · Support The Mission · Contact Us.*

**About Us** — who we are, why we started, vision, mission, core values (integrity, compassion, inclusivity, transparency, community participation, sustainability, dignity, collaboration, innovation, accountability), non-profit/non-political commitment, trustees/leadership, registration details once available.

**Our Objectives** — the 7 pillars + "Other Charitable Activities," each rewritten in plain public-friendly language. Full legal text is *not* pasted here.

**Program pages** (one per pillar; intent-framed, original):

| Pillar | Working page title | Core planned activities |
|---|---|---|
| Education | Education for Every Learner | learning centres, school support, digital classrooms, scholarships, remedial classes, career guidance, girls' education |
| Healthcare | Health Support for Underserved Communities | health camps, mobile medical units, maternal & child welfare, nutrition, sanitation, wellness |
| Skill Development | Skills for Sustainable Livelihoods | IT/digital skills, women entrepreneurship, vocational training, placement, incubation |
| Environment | A Greener, Sustainable Future | tree plantation, water conservation, waste management, recycling, clean-tech awareness |
| Innovation & STEM | Science & Innovation for All | community innovation labs, STEM & robotics, digital knowledge centres, AI learning |
| Community Development | Empowering Communities | self-help groups, micro-finance, women & child welfare, cultural preservation |
| Disaster Relief | Standing With Communities in Crisis | relief material, medical response, rehabilitation support |
| Elderly Care | Dignity & Care for Elders | elder support, rehabilitation, livelihood & dignity for seniors |

**CSR & Partnerships** — why partner, CSR project categories (digital classroom, skill centre, women entrepreneurship, health camp series, mobile medical unit, STEM/robotics lab, plantation & water, disaster relief, elderly care, community projects), implementation approach, monitoring & reporting, transparency commitment, inquiry form.

**Volunteer** — form fields: full name, email, phone, city, area of interest, skills, availability, message, **consent checkbox**. Interest areas include teaching/mentoring, health-camp support, digital-literacy training, environment drives, fundraising, content/design/photography, event coordination, social media, research & documentation, community outreach.

**Reports & Transparency** — public list of annual reports / audited statements / impact summaries (PDF), grouped by year and type.

**Contact** — form (to admin) + address + map + email + phone + WhatsApp button.

## 15. Reference Websites (structure study only — never copy)

Studied for structure, program categorisation, donation/transparency patterns, and content flow only; all copy written original.

| Focus | Reference | What to study |
|---|---|---|
| Education / child learning | pratham.org | program structure, learning outcomes, community approach |
| Broad multi-program NGO | smilefoundationindia.org | program pages, donation style, impact storytelling |
| School meals / nutrition | akshayapatra.org | food+education link, donor trust |
| Healthcare / medical relief | doctorsforyou.org | health camps, disaster medical response |
| Rural dev / disaster relief | goonj.org | dignity-based messaging, community participation |
| Elderly care | helpageindia.org | senior care, dignity, livelihood |
| Water / climate / rural | wotr.org | environment, climate resilience |
| Environmental education | ceeindia.org | education for sustainable development |
| Digital literacy | defindia.org | digital inclusion, rural tech access |
| Digital skilling | nasscomfoundation.org | employability, tech for good |
| STEM / hands-on science | agastya.org | mobile labs, creativity labs |
| Robotics / STEM | indiastemfoundation.org | STEM labs, CSR-based programs |
| Govt NGO reference | ngodarpan.gov.in | NGO profile structure |
| CSR collaboration | csrxchange.gov.in | CSR project listing, partnership orientation |
| SDG / national priority | niti.gov.in | SDG alignment framing |

## 16. SDG Alignment (content layer)

Programs can optionally carry SDG tags shown on program pages and the About page to frame work against national/global priorities.

| SDG | Mapped Trust work |
|---|---|
| 1 No Poverty | livelihood, relief, community development |
| 2 Zero Hunger | food support, nutrition, feeding programs |
| 3 Good Health | healthcare, medical relief, wellness |
| 4 Quality Education | schools, literacy, scholarships, STEM |
| 5 Gender Equality | women empowerment, skill training |
| 6 Clean Water & Sanitation | sanitation, hygiene, rainwater harvesting |
| 7 Clean Energy | renewable energy awareness |
| 8 Decent Work | skill development, entrepreneurship |
| 9 Innovation & Infrastructure | innovation labs, STEM, AI, incubation |
| 10 Reduced Inequalities | support for marginalized communities |
| 11 Sustainable Communities | community development, heritage, disaster resilience |
| 12 Responsible Consumption | recycling, waste management |
| 13 Climate Action | environment, climate awareness |
| 17 Partnerships | CSR, government, NGO partnerships |

## 17. Content Collection Checklist (gather before final copy)

Trust name · logo (clean vector) · tagline · registration details (12A/80G) · registered address · trustee names & roles · founder message · vision · mission · objectives summary · program priority list · target locations · target beneficiaries · contact number · email · bank details (for donations) · certificates (if any) · photos (if any) · partner details (if any) · initial project plan · any completed activities (if any).

A founder message, vision, and mission already exist as **starting drafts** in your guide — I'll tailor these to the real Trust details when we write the About page, rather than treat them as final.

## 18. Guide → Django mapping (no stack change)

Your guide's section 16 suggested a generic Next.js/React/Strapi option; we are **keeping Django MVT + Bootstrap 5**. The rest of that section maps directly onto our build:
- "CMS / simple admin panel" → **Django admin** (already our staff control panel).
- Suggested "components" (Header, Footer, HeroSection, ProgramCard, ImpactCard, CTASection, TrusteeCard, PartnerLogoSection, VolunteerForm, ContactForm, GalleryGrid, ReportList, BlogCard, FAQSection, SDGCard, TestimonialCard) → **Django template partials** (`{% partialdef %}` / `{% partial %}`, native in Django 6) for in-file reusable fragments, plus `templates/partials/` includes for larger shared blocks.
- PostgreSQL, SMTP/email, analytics, SEO (sitemap/robots/schema), and the security task list → already covered in Part I (Sections 3, 9, 10, 11).

## Immediate next step
Confirm the 3 assumptions at the top (name, 80G status, hosting), then I'll execute **Phase 0 + Phase 1** and hand you a running, deployable project scaffold: settings, custom user, base Bootstrap template, the Programs/Home/About/Contact modules, and admin configured for your staff.
