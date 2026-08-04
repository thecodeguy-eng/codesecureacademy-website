# Code Secure Academy — Platform

Django site for CSA: student accounts, per-track cohort payments with
automatic WhatsApp group placement, a moderated review system, and a full
marketplace (sellers, listings, Paystack split payments).

## Stack

Django · Supabase (Postgres) · Render (hosting) · Cloudinary (media) ·
Paystack (payments) · Namecheap (domain) · django-allauth (auth)

## Local setup

```bash
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data       # placeholder tracks/cohorts/FAQs so the site isn't empty
python manage.py createsuperuser
python manage.py runserver
```

Without a `.env` file, the app runs locally against SQLite with a console
email backend (verification emails print to the terminal) and placeholder
Paystack test keys — good enough to click through every page, but checkout
will fail at the Paystack API call until real test keys are set (see below).

## Environment variables

Copy `.env.example` to `.env` and fill in real values. Full list is
documented inline there. Nothing in `.env` should ever be committed.

## Getting real credentials

- **Paystack**: sign up at paystack.com, grab the **test** secret/public
  keys first (Settings → API Keys & Webhooks) and use those until you're
  ready to go live. Also set the webhook URL there to
  `https://codesecureacademy.com/pay/webhook/paystack/` once deployed.
- **Cloudinary**: free account at cloudinary.com, Dashboard shows cloud
  name/API key/secret.
- **Supabase**: create a project, Database → Connection string → "Session
  pooler" URI is what goes in `DATABASE_URL`. Note: Supabase's free tier
  auto-pauses a project after 7 days with no API activity — the same
  external pinger set up for Render keep-alive (below) also keeps this
  project from pausing since it hits the app, which hits the DB.
- **Google OAuth**: Google Cloud Console → Credentials → OAuth client ID
  (Web application). Authorized redirect URI:
  `https://codesecureacademy.com/accounts/google/login/callback/`.
- **WhatsApp group links**: CSA creates the actual WhatsApp group per
  track manually, then the invite link is pasted into Django admin under
  **WhatsApp → Track WhatsApp groups**. The site never creates or manages
  the groups themselves — see "Worth flagging" in the original brief.

## Keeping the free tier alive (Render + Supabase)

Render's free web service spins down after ~15 min idle; Supabase's free
project pauses after 7 days with no activity. Set up a free external
pinger (cron-job.org or UptimeRobot) with **two** jobs once deployed:

1. `GET https://codesecureacademy.com/pay/healthz/` every ~10 min — keeps
   Render (and therefore Supabase) awake.
2. `GET https://codesecureacademy.com/pay/internal/release-expired-holds/`
   with header `X-Internal-Token: <INTERNAL_TASK_TOKEN from .env>` every
   ~2 min — this is the seat-hold cleanup job (releases expired holds,
   grace-checks slow bank transfers before releasing). Render's free tier
   has no built-in cron worker, so this piggybacks on the external pinger
   instead.

Render's free tier caps at 750 instance-hours/month — pinging one service
24/7 uses ~720 of those, which is fine as the only free service but leaves
almost no headroom if a second free Render service is added later.

## Pre-launch checklist

Things intentionally left as placeholders or flagged during the build —
confirm/replace all of these before real money moves through the site:

- [ ] Replace the placeholder cohort prices/dates/seat counts (`seed_data`
      command) with real numbers in Django admin.
- [ ] Add real WhatsApp group invite links per track in admin.
- [ ] Switch `PAYSTACK_*` keys from test to live once ready.
- [ ] **Verify `percentage_charge` semantics** on Paystack's Subaccount API
      (`apps/marketplace/models.py`, `Seller.approve()`) against a real
      test transaction before enabling marketplace payouts with real
      money — some Paystack API versions treat this as the platform's cut,
      others as the subaccount's. Getting it backwards sends CSA's 10% to
      the seller and vice versa.
- [ ] Decide official email: Zoho Mail (free) vs Google Workspace (paid),
      set up `info@codesecureacademy.com`, and fill in `EMAIL_*` vars.
- [ ] Point Namecheap DNS at Render once the custom domain is added there.
- [ ] **Have a Nigerian lawyer review the Privacy Policy and Terms of
      Service** (`apps/core/views.py` → `privacy_policy`/`terms_of_service`)
      before launch — they're a solid starting draft matched to what the
      site actually does, not legal advice. The refund window and
      marketplace liability clauses in the Terms are explicitly flagged as
      placeholders in the page itself.
- [ ] Set real numbers in **Site settings** (Django admin) once you have
      them — the homepage stats bar stays hidden until `students_trained`/
      `cohorts_run`/`hiring_partners` are non-zero, so it never shows made-up
      numbers, but it also won't show real ones until you enter them.
- [ ] Set `DEBUG=False` and a real `SECRET_KEY` / `INTERNAL_TASK_TOKEN` in
      production env vars — the defaults in `settings.py` are dev-only.

## Verifying the golden path

```bash
python manage.py runserver
```

- Sign up → check console/email for the verification link → verify →
  log in.
- Visit a track page → Enroll now → Paystack test checkout → land back on
  the enrollment success page → WhatsApp link shown (once a
  `TrackWhatsAppGroup` is configured in admin) → leave a review (sits
  pending until approved in admin).
- Marketplace: apply as a seller in admin → approve (creates the Paystack
  subaccount) → create + approve a listing → buy it as a different test
  user → order confirmation email → rate it.
- Seat-hold expiry: age an `Enrollment.seat_held_at` in the Django shell,
  hit `/pay/internal/release-expired-holds/` with the internal token, and
  confirm a "pending" Paystack transaction gets a grace window while a
  genuinely failed one gets released.

## Scope notes

The "tutors upload an intro-only preview, buyers get the full course link
after payment" flow is **not** built here — it was raised mid-scoping as
outside the agreed ₦75,000 and needs its own quote. The marketplace
`Listing` model is generic enough to support it later without a rework.
