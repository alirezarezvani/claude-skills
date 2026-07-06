---
name: strict-api
description: >
  Reality-check layer that prevents the agent from inventing APIs, methods,
  imports, or variables that do not exist. Ensures minimal code means correct minimal code,
  not hallucinated minimal code. A fake one-liner that calls a non-existent
  function is a bug with extra confidence. Use whenever the user says 
  "no hallucinations", "verify APIs", "reality check", or "don't invent functions".
---

# Strict API Verification

Inventing a function that doesn't exist is the opposite of efficiency.
You wrote a line that looks minimal. You shipped a bug that takes an hour to debug.
The true lazy path is: use only what is provably there.

## The Only Rule

Before you write any function call, import, or method access, you must be
able to answer: **"Does this exist in the version the user is running?"**

If the answer is "probably" or "I think so" — stop. You don't know.

## What this blocks

**Made-up methods.** `fs.readFileLines()` does not exist. `path.combine()` is
.NET, not Node.js. `csv.read_csv()` is pandas, not Python's `csv` module.
Writing these is not minimal code — it is confident garbage.

**Framework confusion.** Every framework has a twin that sounds like it:
- `render_template` (Flask) vs `render()` (Django)
- `useForm()` (react-hook-form) vs nothing built into React

**Deprecated APIs.** Using a deprecated API is writing code that will break on the next upgrade.

## How to handle uncertainty

You are not sure if a method exists in the user's version? Say so:

`// verify fs.openAsBlob exists in your Node.js version (>= 20.0)`

One comment costs nothing. A silent wrong call costs an hour of the user's time.

If the uncertainty is high enough that you cannot write correct code, say:
> "I'd need to check whether X exists in version Y before using it. What version are you on?"
