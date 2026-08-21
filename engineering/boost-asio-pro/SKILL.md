---
name: "boost-asio-pro"
description: "Use when writing or reviewing asynchronous C++ networking code with Boost.Asio or standalone Asio — TCP/UDP servers and clients, SSL/TLS, timers, strands, io_context, co_spawn, awaitable, async_read/async_write, asio::spawn, yield_context, or pre-C++20 completion-handler callbacks."
---

# Boost.Asio / standalone Asio

## Overview

Write async C++ networking code that compiles on the *user's* Boost, not the newest one. Asio's API changed shape three times (classic `io_service` → `io_context` → C++20 coroutines) and most Asio code on the internet is from the first era, so **pick the style from the toolchain first**, then follow that style's reference file.

**References:** [Boost.Asio](https://www.boost.org/doc/libs/latest/doc/html/boost_asio.html) · [standalone Asio](https://think-async.com/Asio/)

Use this skill whenever async C++ networking code is being written or reviewed — and especially when the target toolchain is old, where coroutine examples simply will not compile. The three worked implementations it references are CI-verified from Boost 1.62 (2016) through 1.90.

## Step 1: pick the style (do this before writing code)

Determine the Boost (or Asio) version and the C++ standard actually in use — `find_package(Boost)` output, `dpkg -l libboost-dev`, `brew info boost`, `CMAKE_CXX_STANDARD`, or ask. Do not assume the newest.

| Boost | C++ std | Style | Read |
|-------|---------|-------|------|
| ≥ 1.77 | C++20 | Coroutines (`co_await` + `awaitable<T>`) — preferred | [references/coroutines.md](references/coroutines.md) |
| ≥ 1.74 | C++11–17 | Completion handlers (callbacks) — the portable baseline | [references/pre-cpp20.md](references/pre-cpp20.md) |
| ≥ 1.80 | C++11–17 | Stackful `asio::spawn` + `yield_context` (links Boost.Coroutine — not header-only) | [references/pre-cpp20.md](references/pre-cpp20.md) |
| 1.62–1.65 | C++11 | Classic `io_service` / `strand.wrap` / `expires_from_now` | [references/classic-boost.md](references/classic-boost.md) |

SSL/TLS in any style: [references/ssl.md](references/ssl.md). CMake for any style: [references/build.md](references/build.md).

`io_context`, `make_strand`, `bind_executor`, `steady_timer`, `signal_set`, `async_read`/`async_write`/`async_read_until`, buffers and `resolver` are **library** features — identical in the coroutine and callback styles. Only the suspension mechanism differs.

## Step 2: version floors (verified by compiling, not from docs)

Reach for one of these and the build breaks on older distros:

| Feature | Floor |
|---------|-------|
| `experimental/awaitable_operators.hpp` (the `\|\|` / `&&` operators) | **Boost ≥ 1.77** / Asio ≥ 1.20 |
| `as_tuple` completion token | **Boost ≥ 1.79** / Asio ≥ 1.21 |
| `co_composed` (custom composed ops) | **Boost ≥ 1.85** / Asio ≥ 1.30 |
| 3-arg `asio::spawn(ex, fn, token)` | **Boost ≥ 1.80** (older Boost has only `spawn(ex, fn)`) |
| `any_io_executor` (`strand<any_io_executor>`, `tcp::socket`'s default executor) | **Boost ≥ 1.74** — the floor for the callback style; below it, use legacy `io_context::strand` |
| `io_context`, `make_strand`, `expires_after` | **Boost ≥ 1.66** — below it, classic `io_service` |

Distro floors that bite: **Debian bookworm ships Boost 1.74** (no `awaitable_operators.hpp` — `#include` fails outright), Ubuntu 20.04 ships 1.71 (no `any_io_executor`), Debian 9 ships 1.62.

Language, not library: the chrono literals `250ms` / `30s` are **C++14**. For a true C++11 build write `std::chrono::milliseconds(250)`.

## Step 3: the rules that are actually easy to get wrong

**A strand does not serialize writes.** A strand serializes handler *execution*, not whole composed operations. Two `async_write`s in flight on the same strand still **interleave bytes on the wire**. Full-duplex (a read loop plus concurrent pushes/replies) needs a per-connection strand **and** an outbound queue with an in-flight flag, so at most one `async_write` exists at a time. This is the single most common wrong answer about Asio.

**Buffers do not own memory.** `asio::buffer()` is a view. Storage must outlive the operation: coroutine locals are fine across `co_await` in the same frame; in callback style the same data must become a **member**, not a local.

**Connections must outlive their handlers.** `enable_shared_from_this`, and capture `self` in *every* `co_spawn` / handler — read loop, write loop, and each timer.

**Frame with composed reads.** `async_read` (fills the buffer exactly) for a length prefix and then the body; never `async_read_some`, which returns short.

**Wrap `as_tuple`.** Always `as_tuple(use_awaitable)`. Bare `as_tuple` resolves against the operation's default token and compiles in some contexts, fails in others.

**`async_accept(make_strand(...))` changes two things**: it forces an explicit completion token back on the call, and the accepted socket is `basic_stream_socket<tcp, strand<...>>`, not `tcp::socket`. Take it **by value** or with `auto` — binding it to `tcp::socket&` will not compile.

**Re-arming a timer resolves the pending wait with `operation_aborted`.** In an idle-timeout loop that is the signal to keep waiting, not an error.

**GCC needs `-fcoroutines`** for the C++20 style, and header-only Boost needs `BOOST_ERROR_CODE_HEADER_ONLY` defined in exactly one place (CMake).

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Buffer dangling (local goes out of scope during async op) | Ensure buffer lifetime ≥ operation lifetime; coroutine locals or members, not callback locals |
| Forgetting `io.run()` | No handlers dispatch without `run()` / `run_one()` |
| Concurrent socket access without strand | Wrap in `strand<>` or serialize via one coroutine chain |
| Assuming a strand prevents interleaved writes | Add a write queue — see Step 3 |
| Using `use_awaitable` where `deferred` suffices | Omit the token (default is `deferred`) unless using `\|\|` / `&&` |
| Ignoring short reads/writes | Use composed `async_read` / `async_write` / `async_read_until`, not `async_read_some` |
| Not setting `reuse_address` on the acceptor | Set before `bind`/`listen` or restarts hit "address in use" |
| SSL operations without a strand | *All* `ssl::stream` ops need strand synchronization |
| Blocking inside a handler | Never block in a completion handler |
| Accepting a socket with the wrong executor type | See `async_accept(make_strand(...))` in Step 3 |
| Requiring the `Boost::system` component | Header-only since 1.74: `Boost::headers` + `BOOST_ERROR_CODE_HEADER_ONLY`. Only classic (pre-1.66) needs the link |
| Missing `-fcoroutines` on GCC | Build fails — add `$<$<CXX_COMPILER_ID:GNU>:-fcoroutines>` |
| Writing coroutine code for a Boost that predates it | Do Step 1 first |

## Boost.Asio vs standalone Asio

Same author, same API — namespace and includes differ.

| Aspect | Boost.Asio | Standalone Asio |
|--------|-----------|-----------------|
| Namespace / include | `boost::asio` / `<boost/asio.hpp>` | `asio` / `<asio.hpp>` |
| Error code | `boost::system::error_code` | `asio::error_code` (or `std::error_code`) |
| Install (brew) | `brew install boost` | `brew install asio` |
| CMake | `Boost::headers` | manual include path |
| Version (2025) | 1.87–1.90 (with Boost) | 1.30–1.36 (independent) |
| Macro prefix | `BOOST_ASIO_` | `ASIO_` |

Support both with a shim, then use `net::` throughout:
```cpp
#ifdef USE_STANDALONE_ASIO
  #include <asio.hpp>
  namespace net = asio;
  using error_code = asio::error_code;
#else
  #include <boost/asio.hpp>
  namespace net = boost::asio;
  using error_code = boost::system::error_code;
#endif
namespace ssl = net::ssl;
using tcp = net::ip::tcp;
```

## Before you call it done

Check the code you just wrote against this list:

- [ ] Style matches the target Boost version and C++ standard (Step 1), and every API used clears its floor (Step 2).
- [ ] Every buffer passed to an async op outlives that op — no callback locals, no dangling `string_view`.
- [ ] At most one `async_write` per socket in flight, enforced by a queue + flag, if anything writes concurrently with reading.
- [ ] Every async chain on a shared object runs on the same strand; `self` captured in every handler and `co_spawn`.
- [ ] Framing / delimited reads use composed `async_read` / `async_read_until`.
- [ ] Errors are handled, not swallowed: `as_tuple(use_awaitable)` destructured, or the callback's `ec` checked, on every op.
- [ ] `operation_aborted` distinguished from real errors wherever a timer is re-armed or an op is cancelled.
- [ ] Acceptor sets `reuse_address`; shutdown path closes the acceptor and drains sessions.
- [ ] CMake has the standard, `-fcoroutines` for GCC (C++20 only), `BOOST_ERROR_CODE_HEADER_ONLY` in one place, and `Boost::coroutine` only if using stackful `spawn`.
- [ ] It compiles. Build it — most of the mistakes above are compile-time, and the version floors are only real once tested.

## Worked examples

Three CI-verified implementations of the same full-duplex framed-protocol server, one per style — copy from the one matching Step 1. All three live in the upstream repository and are built by CI on every push.

- [market-data-feed](https://github.com/alexprivalov/boost-asio-skill/tree/main/examples/market-data-feed) — C++20 coroutines (Boost 1.77+; verified 1.83–1.90)
- [market-data-feed-precpp20](https://github.com/alexprivalov/boost-asio-skill/tree/main/examples/market-data-feed-precpp20) — callbacks, C++11-clean (verified Boost 1.74+, incl. Windows/MSVC)
- [market-data-feed-classic](https://github.com/alexprivalov/boost-asio-skill/tree/main/examples/market-data-feed-classic) — classic `io_service` (verified back to Boost 1.62 / Debian 9)

## Official documentation

- Overview: https://www.boost.org/doc/libs/latest/doc/html/boost_asio/overview.html
- Reference: https://www.boost.org/doc/libs/latest/doc/html/boost_asio/reference.html
- Examples: https://www.boost.org/doc/libs/latest/doc/html/boost_asio/examples.html

## Cross-References

- `engineering/docker-development` — the old-Boost verification lanes this skill's floors come from are containerised builds (Debian 9 / bookworm, Fedora).
- `engineering/chaos-engineering` — for exercising the failure paths this skill tells you to handle: half-open sockets, idle timeouts, partial frames.
- `engineering-team/playwright-pro` — the client-side counterpart when the server built here is driven from browser-based integration tests.
