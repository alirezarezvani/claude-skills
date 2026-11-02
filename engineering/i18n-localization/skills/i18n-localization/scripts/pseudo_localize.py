#!/usr/bin/env python3
"""pseudo_localize.py - generate a pseudo-locale from the source strings.

Load the output as an extra locale (en-XA by convention, ar-XB for --bidi) and
click through the UI before any translator is paid:

  * every translatable character is accented   -> text that stays plain ASCII
    on screen was never routed through the translation layer
  * strings are padded by the length-based expansion rates that translation
    typically needs (short labels grow most)    -> clipping, overflow, fixed widths
  * each string is wrapped in [[ ]]            -> a cut-off bracket shows truncation;
    two bracket pairs in one label show runtime concatenation
  * --bidi wraps text in RIGHT-TO-LEFT OVERRIDE -> mirrored layout and bidi bugs

Placeholders ({{name}}, {name}, %s, %1$s, %(name)s, %{name}), HTML/JSX tags and
ICU plural/select syntax are left untouched; only literal text inside them is
transformed. Reads and writes JSON or ARB (nested or flat) and Java .properties.

Exit codes: 0 written · 3 bad input. Stdlib only.
"""
import argparse
import json
import os
import re
import signal
import sys

ACCENTS = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                   'ȧƀƈḓḗƒɠħīĵķŀḿƞǿƥɋřşŧŭṽẇẋẏẑȦƁƇḒḖƑƓĦĪĴĶĿḾȠǾƤɊŘŞŦŬṼẆẊẎẐ'))
PROTECT = re.compile(r'\{\{[^{}]*\}\}|%(?:\d+\$)?[-+ 0#]*\d*(?:\.\d+)?[sdifuxXeEgGc@]|%\([\w.]+\)[sdif]|%\{[\w.]+\}'
                     r'|</?[A-Za-z0-9][^<>]*>|&[#\w]+;|\$t\([^)]*\)|@:[\w.]+|\\[nt]|https?://\S+')
PAD = '~·'
RLO, PDF = '‮', '‬'


def expansion(n):
    """Extra characters for a source string of n characters (length-based rates, short strings grow most)."""
    if n <= 10:
        rate = 1.0
    elif n <= 20:
        rate = 0.8
    elif n <= 30:
        rate = 0.6
    elif n <= 50:
        rate = 0.4
    elif n <= 70:
        rate = 0.35
    else:
        rate = 0.3
    return int(round(n * rate))


def _text(seg, bidi):
    parts, last = [], 0
    for m in PROTECT.finditer(seg):
        parts.append(_accent(seg[last:m.start()], bidi))
        parts.append(m.group(0))
        last = m.end()
    parts.append(_accent(seg[last:], bidi))
    return ''.join(parts)


def _accent(s, bidi):
    if not s:
        return s
    out = ''.join(ACCENTS.get(c, c) for c in s)
    return f'{RLO}{out}{PDF}' if bidi and out.strip() else out


def transform(msg, bidi=False):
    """Accent literal text, keep ICU structure and placeholders. Returns (text, literal_length)."""
    out, i, n = [], 0, len(msg)
    lit = [0]

    def text_until(i, in_branch):
        start = i
        buf = []
        while i < n:
            c = msg[i]
            if c == "'" and i + 1 < n and msg[i + 1] in "{}'#|":  # ICU quoting: copy verbatim
                j = msg.find("'", i + 1) if msg[i + 1] != "'" else i + 1
                j = n - 1 if j < 0 else j
                buf.append(msg[i:j + 1])
                i = j + 1
                continue
            if c == '{' and not msg.startswith('{{', i):
                break
            if c == '{' and msg.startswith('{{', i):
                j = msg.find('}}', i)
                j = n - 2 if j < 0 else j
                buf.append(msg[i:j + 2])
                i = j + 2
                continue
            if c == '}' and in_branch:
                break
            if c == '#' and in_branch:
                buf.append('\x00')
                i += 1
                continue
            buf.append(c)
            i += 1
        raw = ''.join(buf)
        lit[0] += len(PROTECT.sub('', raw.replace('\x00', '')))
        segs = raw.split('\x00')
        return '#'.join(_text(s, bidi) for s in segs), i

    def message(i, in_branch):
        res = []
        while i < n:
            t, i = text_until(i, in_branch)
            res.append(t)
            if i >= n or msg[i] == '}':
                break
            frag, i = argument(i)
            res.append(frag)
        return ''.join(res), i

    def argument(i):
        m = re.compile(r'\{\s*[^\s,{}]+\s*').match(msg, i)
        if not m:
            return msg[i], i + 1
        j = m.end()
        if j < n and msg[j] == '}':
            return msg[i:j + 1], j + 1
        mt = re.compile(r',\s*(plural|selectordinal|select)\s*,\s*(?:offset:\s*\d+\s*)?').match(msg, j)
        if not mt:  # number/date/time: copy to matching brace
            depth, k = 0, i
            while k < n:
                if msg[k] == '{':
                    depth += 1
                elif msg[k] == '}':
                    depth -= 1
                    if depth == 0:
                        return msg[i:k + 1], k + 1
                k += 1
            return msg[i:], n
        res = [msg[i:mt.end()]]
        k = mt.end()
        while k < n and msg[k] != '}':
            ms = re.compile(r'([^\s{}]+)(\s*)\{').match(msg, k)
            if not ms:
                res.append(msg[k])
                k += 1
                continue
            res.append(ms.group(0))
            body, k = message(ms.end(), True)
            res.append(body)
            if k < n:
                res.append('}')
                k += 1
            sp = re.compile(r'\s*').match(msg, k)
            res.append(sp.group(0))
            k = sp.end()
        res.append('}')
        return ''.join(res), k + 1

    body, _ = message(0, False)
    out.append(body)
    return ''.join(out), lit[0]


def pseudo(value, bidi=False, expand=True, brackets=True):
    if not isinstance(value, str) or not value.strip():
        return value
    body, n = transform(value, bidi)
    if expand and n:
        extra = expansion(n)
        body = body + ' ' + (PAD * extra)[:extra] if extra else body
    return f'[[{body}]]' if brackets else body


def walk(obj, fn, arb=False):
    if isinstance(obj, dict):
        return {k: (v if arb and k.startswith('@') else walk(v, fn, arb)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn, arb) for v in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj


def run_properties(text, fn):
    out = []
    for line in text.splitlines():
        m = re.match(r'(\s*(?:\\.|[^=:\s#!])+\s*[=:]\s*)(.*)$', line)
        if m and not line.lstrip().startswith(('#', '!')):
            val = fn(m.group(2))
            val = ''.join(c if ord(c) < 128 else f'\\u{ord(c):04x}' for c in val)
            out.append(m.group(1) + val)
        else:
            out.append(line)
    return '\n'.join(out) + '\n'


SAMPLE = {'cart': {'title': 'Your cart', 'items_one': '{{count}} item', 'items_other': '{{count}} items',
                   'welcome': 'Welcome back, <b>{{name}}</b>!'},
          'inbox': '{n, plural, =0 {No messages} one {# message} other {# messages}}',
          'save': 'Save'}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Generate a pseudo-locale (accented, expanded, bracketed) from source strings.')
    ap.add_argument('source', nargs='?', help='source locale file (.json, .arb, .properties)')
    ap.add_argument('-o', '--out', help='output file (default: stdout)')
    ap.add_argument('--bidi', action='store_true', help='wrap text in RIGHT-TO-LEFT OVERRIDE (ar-XB style)')
    ap.add_argument('--no-expand', action='store_true', help='do not pad strings')
    ap.add_argument('--no-brackets', action='store_true', help='do not wrap strings in [[ ]]')
    ap.add_argument('--output', choices=('text', 'json'), default='text', help='json prints a summary object')
    ap.add_argument('--sample', action='store_true', help='pseudo-localize a built-in example')
    a = ap.parse_args(argv)

    def fn(v):
        return pseudo(v, a.bidi, not a.no_expand, not a.no_brackets)

    if a.sample:
        result = walk(SAMPLE, fn)
        if a.output == 'json':
            print(json.dumps({'source': 'sample', 'strings': 6, 'result': result}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if not a.source or not os.path.isfile(a.source):
        print('error: give a source locale file (or --sample)', file=sys.stderr)
        return 3
    ext = os.path.splitext(a.source)[1].lower()
    try:
        if ext in ('.json', '.arb'):
            data = json.load(open(a.source, encoding='utf-8-sig'))
            result = walk(data, fn, arb=ext == '.arb')
            if ext == '.arb' and isinstance(result, dict) and '@@locale' in result:
                result['@@locale'] = 'ar_XB' if a.bidi else 'en_XA'
            text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        elif ext == '.properties':
            text = run_properties(open(a.source, encoding='utf-8').read(), fn)
        else:
            print(f'error: unsupported format {ext} (json, arb, properties)', file=sys.stderr)
            return 3
    except ValueError as e:
        print(f'error: {a.source}: {e}', file=sys.stderr)
        return 3
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, 'w', encoding='utf-8').write(text)
        if a.output == 'json':
            print(json.dumps({'source': a.source, 'out': a.out, 'bytes': len(text.encode())}))
        else:
            print(f'wrote {a.out} ({"ar-XB bidi" if a.bidi else "en-XA"} pseudo-locale)')
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
