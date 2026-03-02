# SaaS Scaffolder

**Tier:** POWERFUL  
**Category:** Product Team  
**Domain:** Full-Stack Development / Project Bootstrapping

---

## Overview

Generate complete, production-ready SaaS projects from a product brief. Outputs a fully wired Next.js App Router project with authentication, database, payments, and a working dashboard — not a toy starter kit.

**Stack:** Next.js 14+ App Router · TypeScript · Tailwind CSS · shadcn/ui  
**Auth:** NextAuth.js / Clerk / Supabase Auth  
**Database:** NeonDB / Supabase / PlanetScale (Drizzle ORM)  
**Payments:** Stripe / Lemon Squeezy  

---

## Core Capabilities

- Generate full project file tree with all boilerplate written
- Wire auth, DB, and payments together from day one
- Output landing page, auth flow, dashboard layout, API routes, DB schema
- Produce environment variable templates and deployment configs
- Generate a scaffold checklist to track completion

---

## When to Use

- Starting a new SaaS from a product idea or brief
- Standardizing project structure across a team
- Rapidly prototyping to validate before committing to architecture
- Onboarding engineers to a consistent codebase pattern

---

## Triggering This Skill

Provide a product brief in this format:

```
Product: [name]
Description: [1-3 sentences]
Auth: nextauth | clerk | supabase
Database: neondb | supabase | planetscale
Payments: stripe | lemonsqueezy | none
Features: [comma-separated list]
```

---

## File Tree Output

```
my-saas/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── settings/page.tsx
│   │   ├── billing/page.tsx
│   │   └── layout.tsx
│   ├── (marketing)/
│   │   ├── page.tsx
│   │   ├── pricing/page.tsx
│   │   └── layout.tsx
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── webhooks/stripe/route.ts
│   │   ├── billing/checkout/route.ts
│   │   └── billing/portal/route.ts
│   └── layout.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   │   ├── login-form.tsx
│   │   └── register-form.tsx
│   ├── dashboard/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── stats-card.tsx
│   ├── marketing/
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── pricing.tsx
│   │   └── footer.tsx
│   └── billing/
│       ├── plan-card.tsx
│       └── usage-meter.tsx
├── lib/
│   ├── auth.ts
│   ├── db.ts
│   ├── stripe.ts
│   ├── validations.ts
│   └── utils.ts
├── db/
│   ├── schema.ts
│   └── migrations/
├── hooks/
│   ├── use-subscription.ts
│   └── use-user.ts
├── types/index.ts
├── middleware.ts
├── .env.example
├── drizzle.config.ts
└── next.config.ts
```

---

## Key Component Patterns

### Auth Config (NextAuth)

```typescript
// lib/auth.ts
import { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "./db"

export const authOptions: NextAuthOptions = {
  adapter: DrizzleAdapter(db),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    session: async ({ session, user }) => ({
      ...session,
      user: {
        ...session.user,
        id: user.id,
        subscriptionStatus: user.subscriptionStatus,
      },
    }),
  },
  pages: { signIn: "/login" },
}
```

### Database Schema (Drizzle + NeonDB)

```typescript
// db/schema.ts
import { pgTable, text, timestamp, integer } from "drizzle-orm/pg-core"

export const users = pgTable("users", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified"),
  image: text("image"),
  stripeCustomerId: text("stripe_customer_id").unique(),
  stripeSubscriptionId: text("stripe_subscription_id"),
  stripePriceId: text("stripe_price_id"),
  stripeCurrentPeriodEnd: timestamp("stripe_current_period_end"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
})

export const accounts = pgTable("accounts", {
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  type: text("type").notNull(),
  provider: text("provider").notNull(),
  providerAccountId: text("provider_account_id").notNull(),
  refresh_token: text("refresh_token"),
  access_token: text("access_token"),
  expires_at: integer("expires_at"),
})
```

### Stripe Checkout Route

```typescript
// app/api/billing/checkout/route.ts
import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { stripe } from "@/lib/stripe"
import { db } from "@/lib/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"

export async function POST(req: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  const { priceId } = await req.json()
  const [user] = await db.select().from(users).where(eq(users.id, session.user.id))

  let customerId = user.stripeCustomerId
  if (!customerId) {
    const customer = await stripe.customers.create({ email: session.user.email! })
    customerId = customer.id
    await db.update(users).set({ stripeCustomerId: customerId }).where(eq(users.id, user.id))
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?upgraded=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    subscription_data: { trial_period_days: 14 },
  })

  return NextResponse.json({ url: checkoutSession.url })
}
```

### Protected Dashboard Layout

```typescript
// app/(dashboard)/layout.tsx
import { redirect } from "next/navigation"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { Sidebar } from "@/components/dashboard/sidebar"

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions)
  if (!session) redirect("/login")

  return (
    <div className="flex h-screen">
      <Sidebar user={session.user} />
      <main className="flex-1 overflow-y-auto bg-gray-50 p-6">{children}</main>
    </div>
  )
}
```

### Middleware

```typescript
// middleware.ts
import { withAuth } from "next-auth/middleware"
import { NextResponse } from "next/server"

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token
    if (req.nextUrl.pathname.startsWith("/dashboard") && !token) {
      return NextResponse.redirect(new URL("/login", req.url))
    }
  },
  { callbacks: { authorized: ({ token }) => !!token } }
)

export const config = {
  matcher: ["/dashboard/:path*", "/settings/:path*", "/billing/:path*"],
}
```

### Environment Variables Template

```bash
# .env.example
NEXT_PUBLIC_APP_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_PRO_PRICE_ID=price_...
```

---

## Scaffold Checklist (25 Items)

### Foundation
- [ ] 1. Next.js initialized with TypeScript and App Router
- [ ] 2. Tailwind CSS configured with custom theme tokens
- [ ] 3. shadcn/ui installed and configured
- [ ] 4. ESLint + Prettier configured
- [ ] 5. `.env.example` created with all required variables

### Database
- [ ] 6. Drizzle ORM installed and configured
- [ ] 7. Schema written (users, accounts, sessions, verification_tokens)
- [ ] 8. Initial migration generated and applied
- [ ] 9. DB client singleton exported from `lib/db.ts`
- [ ] 10. DB connection tested in local environment

### Authentication
- [ ] 11. Auth provider installed (NextAuth / Clerk / Supabase)
- [ ] 12. OAuth provider configured (Google / GitHub)
- [ ] 13. Auth API route created
- [ ] 14. Session callback adds user ID and subscription status
- [ ] 15. Middleware protects dashboard routes
- [ ] 16. Login and register pages built with error states

### Payments
- [ ] 17. Stripe client initialized with TypeScript types
- [ ] 18. Checkout session route created
- [ ] 19. Customer portal route created
- [ ] 20. Stripe webhook handler with signature verification
- [ ] 21. Webhook updates user subscription status in DB idempotently

### UI
- [ ] 22. Landing page with hero, features, pricing sections
- [ ] 23. Dashboard layout with sidebar and responsive header
- [ ] 24. Billing page showing current plan and upgrade options
- [ ] 25. Settings page with profile update form and success states

---

## Customization Points

| Point | Options |
|---|---|
| Auth provider | nextauth, clerk, supabase-auth |
| Database | neondb, supabase-pg, planetscale |
| ORM | drizzle (default), prisma |
| Payment provider | stripe, lemonsqueezy |
| UI theme | default, zinc, slate, rose |
| Billing model | per-seat, flat-rate, usage-based |

---

## Common Pitfalls

- **Missing NEXTAUTH_SECRET** — causes random sign-out loops in production
- **Webhook secret mismatch** — use `stripe listen --forward-to` locally, never hardcode raw secret
- **Edge runtime conflicts** — Drizzle needs Node.js runtime; set `export const runtime = "nodejs"` on API routes
- **Session type not extended** — add `declare module "next-auth"` to include custom fields
- **Drizzle migrations in CI** — use `drizzle-kit push` for dev, `drizzle-kit migrate` for prod

---

## Best Practices

- Always create a `lib/stripe.ts` singleton — never instantiate Stripe inline in route handlers
- Use server actions for form mutations, not client-side fetch where avoidable
- Keep webhook handlers idempotent — check DB state before writing
- Add `Suspense` boundaries around dashboard async data fetches
- Store `stripeCurrentPeriodEnd` in DB and check it server-side for all feature gating
- Ship with rate limiting on auth routes from day one (use Upstash Redis + `@upstash/ratelimit`)
