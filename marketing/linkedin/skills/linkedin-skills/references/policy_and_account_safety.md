# Policy and Account Safety — the rules that end the project if you break them

Organic LinkedIn growth is a compounding asset with a single point of failure:
the account. A restriction resets it to zero and there is no appeals process you
can schedule around. This is why this plugin gates every lane through
`linkedin_policy_gate.py` before drafting anything, and why it has no LinkedIn
credentials at all.

None of this is legal advice. It is a summary of published rules, written so an
agent can refuse the right things for the right reasons.

---

## 1. What the User Agreement actually prohibits (§8.2 "Don'ts")

LinkedIn's User Agreement prohibits members from, among other things:

- **Developing, supporting, or using software, devices, scripts, robots, or any
  other means or processes** — including crawlers, browser plugins and add-ons —
  **to scrape the Services or otherwise copy profiles and other data.**
- **Using bots or other automated methods** to access the Services, add or
  download contacts, send or redirect messages, or **create, comment on, like,
  share, or re-share posts, or otherwise drive inauthentic engagement.**
- Creating a false identity, misrepresenting your identity, or using someone
  else's account.
- Posting inaccurate information, or content that violates the Professional
  Community Policies.

Read the second bullet carefully: **it names commenting, liking, and sharing.**
The prohibition is not limited to sending messages. An engagement pod that
coordinates real humans to reciprocally comment on schedule is squarely inside
"otherwise drive inauthentic engagement", and the fact that a human pressed the
key does not take it outside the rule.

## 2. Third-party tools

LinkedIn maintains a Help article on **Prohibited Software and Extensions**
stating that it does not permit third-party software — crawlers, bots, browser
plug-ins, or extensions — that scrapes, modifies the appearance of, or automates
activity on LinkedIn. It notes two consequences: accounts may be restricted or
closed, and the tools themselves may stop working without notice.

The named-tool list in `linkedin_policy_gate.py` (Dux-Soup, PhantomBuster,
Expandi, Linked Helper, Meet Alfred, Waalaxy, Octopus CRM, Lempod, and others) is
not an official LinkedIn blacklist — it is a list of tools whose advertised
function is exactly what the policy prohibits. The gate refuses on the function,
and names the tool only because that is how people describe what they want.

**The supported path exists:** LinkedIn's own scheduler for posts, and LinkedIn's
Marketing Developer Platform for partners with API access. If a workflow can be
done through those, it is fine.

## 3. What actually triggers a restriction

LinkedIn does not publish its enforcement thresholds. Observable patterns from
LinkedIn's own Help documentation on account restrictions and from widespread
reporting:

| Trigger | Why it fires |
|---|---|
| High invitation volume with low acceptance | The signature of untargeted bulk invites. Acceptance rate is the discriminator, not volume alone. |
| Many "I don't know this person" / spam reports | Recipient-side signal, and the most damaging one. |
| Machine-regular activity patterns | Constant per-hour rates, activity at 03:00 local, identical intervals. |
| Identical message or comment text at volume | Directly matches the "inauthentic engagement" language. |
| Detected automation extension | Automated detection of the prohibited-software class. |
| Profile data inconsistent with a real person | Stock photo, no history, sudden high-volume activity. |

The practical read: **restrictions correlate with looking automated more than
with volume itself.** A person sending 20 genuinely personal invitations a week
for a year is invisible. A person sending 200 identical ones in a day is not.

## 4. Rate limits worth knowing (🟡 observed, not published)

- **Connection invitations:** a weekly limit widely observed around 100, adjusted
  per account. **Pending invitations count against it**, so a backlog of
  un-actioned invites silently shrinks the allowance.
- **Withdrawn invitations** cannot be re-sent to the same person for roughly
  three weeks.
- **Messaging:** no published cap for first-degree connections; InMail credits
  are metered by subscription.

`outreach_volume_guard.py` uses conservative working numbers and says explicitly
that they are observations.

## 5. Content rules that cost reach rather than the account

The Professional Community Policies commit LinkedIn to reducing distribution of
several content classes. Relevant to organic creators:

- **Engagement bait** — "comment X for the guide", "like if you agree", "tag
  three people". Explicitly named.
- **Spam and unsolicited commercial content**, including repetitive posting.
- **Misleading or false content**, which for a professional audience includes
  fabricated metrics and invented case studies.

These do not usually restrict an account. They make the work not work, which for
a compounding organic strategy is nearly as bad.

## 6. Things this plugin refuses even where LinkedIn permits them

Three refusals are editorial rather than legal, and they are held anyway:

1. **Fabricated proof.** Inventing a metric, a client, or a testimonial. Legal
   exposure aside (FTC endorsement rules apply to testimonials in many
   jurisdictions), a professional audience contains people who can check.
2. **Ghostwriting an executive's account without their knowledge.** Ghostwriting
   with the account holder's review is normal and fine; the account holder is the
   author of record either way, which means they have to have read it.
3. **Posting confidential or identifying detail about employers, clients, or
   individuals without consent.** Employment agreements, NDAs, and sector rules
   (financial promotion, medical claims, securities disclosure) sit outside
   LinkedIn's policies entirely and bind you anyway.

## 7. Regional obligations the plugin surfaces but cannot resolve

- **GDPR / UK GDPR** — sending unsolicited B2B messages, and any processing of
  contact data outside LinkedIn, has a legal basis question attached. Scraping
  member data to build a list has a much harder one.
- **EU Digital Services Act** and comparable regimes — platform transparency and
  reporting obligations that affect what recourse you have, not what you may do.
- **FTC Endorsement Guides** (US) and equivalents — disclosure obligations for
  paid or incentivised endorsements, including on personal profiles.

Where any of these are in play, the answer is a named human — legal, compliance,
or the client — not a tool.

---

## Sources

1. LinkedIn. **User Agreement**, §8.2 "Don'ts."
   linkedin.com/legal/user-agreement
2. LinkedIn Help. **"Prohibited software and extensions."**
   linkedin.com/help/linkedin/answer/a1341387
3. LinkedIn Help. **"Automated activity on LinkedIn."**
   linkedin.com/help/linkedin/answer/a1340567
4. LinkedIn Help. **"Account restrictions."**
   linkedin.com/help/linkedin/answer/a1340522
5. LinkedIn. **Professional Community Policies.**
   linkedin.com/legal/professional-community-policies — authenticity, spam,
   engagement bait, misinformation.
6. LinkedIn. **Marketing Developer Platform** documentation — the supported
   programmatic path, and the scope it is actually granted for.
7. US Federal Trade Commission. **Guides Concerning the Use of Endorsements and
   Testimonials in Advertising** (16 CFR Part 255) — why an invented testimonial
   is a legal problem and not only an editorial one.

---

**The one-line version:** you can build a serious LinkedIn presence entirely
inside the rules, it takes longer than the shortcuts promise, and the shortcuts
put the compounding asset at risk to save a few months. That trade is bad
arithmetic, and it is the reason this plugin refuses rather than warns.
