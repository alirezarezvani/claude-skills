# Outreach Prep Sheet — one per person

If you cannot fill section 2 without opening a template, do not send the message. The
person-specific line is the entire difference between outreach and spam, and
`outreach_message_builder.py` refuses without it.

---

## 1. Who

- Name (spelled the way they spell it): ______
- What they actually do (not their title): ______
- How you found them: ______
- Have you commented on their work in the last two weeks? ______

If the last answer is no, consider doing that first. Comment for two weeks, then invite.
That order converts better than any wording optimisation.

## 2. The specific line — the one that could not be sent to anyone else

Name the artifact and the part of it that mattered:

> ______________________________________________________________

Checks:
- Does it name something they made, said, or decided? ______
- Could this sentence be sent to anyone else on your list? If yes, rewrite it. ______
- Is it a disagreement or a use, rather than a compliment? (Better if so.) ______

## 3. The reason

One clause: what you want to follow, learn, or compare notes on.

> ______________________________________________________________

## 4. The ask — **not in a first-touch connection note**

Leave blank for a connection request. The note's job is the conversation, not the meeting:
in large third-party samples a note barely moves acceptance (~26.4% either way) but roughly
doubles the reply rate after acceptance.

For a later message, keep it bounded and small:

> ______________________________________________________________

## 5. Volume check before sending

- Invitations already pending: ______
- New invitations planned this week: ______
- Recent acceptance rate: ______ (below 20% → stop and fix targeting)

```bash
python3 ../scripts/outreach_volume_guard.py --invites <n> --pending <n> \
  --minutes <n> --acceptance <0.xx> --output human
```

## 6. Assemble and check

```bash
python3 ../scripts/outreach_message_builder.py --type connection \
  --recipient "..." --specific-line "..." --reason "..." --output human
```

Cap: 200 characters free, 300 with `--premium`.

## 7. Follow-up rule

One follow-up, at least a week later, **only with something new to say**. "Just bumping this
up" is not new information. A second follow-up with nothing new is the point at which you
become the thing you were avoiding.

- Date sent: ______
- Accepted? ______
- Follow-up sent (date, and what was new): ______
