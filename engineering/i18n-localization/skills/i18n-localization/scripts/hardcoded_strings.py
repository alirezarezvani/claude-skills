#!/usr/bin/env python3
"""hardcoded_strings.py - find user-facing text that bypasses the translation layer.

Scans React (.jsx/.tsx/.js/.ts), Vue (.vue), Svelte (.svelte) and HTML templates:

  TEXT              literal text between tags: <button>Save</button>          (error)
  ATTR              user-facing attribute literal: placeholder="Search..."   (error)
  EXPR_LITERAL      string literal rendered from a {...} child expression:
                    {busy ? 'Saving...' : 'Save'}                             (warning)
  CONCAT            translated string glued with + or a template literal;
                    word order differs by language, use interpolation         (warning)
  LOCALE_DEFAULT    toLocaleString()/Intl.*Format() with no locale: formats in
                    the runtime's locale, not the one the user picked         (warning)
  CURRENCY_LITERAL  '$' + amount or `$${x}` instead of Intl.NumberFormat      (warning)
  DATE_PATTERN      hardcoded 'MM/dd/yyyy'-style pattern                       (warning)

Text inside <Trans>, <FormattedMessage>, <code>, <pre>, <script>, <style>, <svg>
is skipped, as are test/story files and lines carrying `i18n-ignore`.
Single tokens listed in .i18n-allow (one per line: brand names, units) are skipped.

Exit codes: 0 clean · 2 warnings only · 3 bad input · 4 errors. Stdlib only. Heuristic:
it reads source text, not a parsed AST, so check each finding before acting on it.
"""
import argparse
import json
import os
import re
import signal
import sys
import tempfile

EXTS = {'.jsx', '.tsx', '.js', '.ts', '.vue', '.svelte', '.html', '.htm'}
SKIP_DIRS = {'public', 'static', 'node_modules', '.git', 'dist', 'build', '.next', 'coverage', 'out', '.nuxt', 'vendor', 'storybook-static'}
SKIP_FILE = re.compile(r'(\.test\.|\.spec\.|\.stories\.|\.story\.|\.d\.ts$|__tests__|__mocks__|/e2e/|/cypress/|/playwright/)')
SKIP_TAGS = {'trans', 'formattedmessage', 'formattedhtmlmessage', 'code', 'pre', 'script', 'style', 'svg', 'kbd', 'samp',
             'i18n-t', 'translate', 'formattednumber', 'formatteddate'}
USER_ATTRS = ('placeholder', 'title', 'alt', 'aria-label', 'aria-description', 'aria-placeholder', 'label', 'helperText',
              'helper-text', 'tooltip', 'description', 'heading', 'caption', 'emptyText', 'empty-text', 'confirmText',
              'cancelText', 'okText', 'submitText', 'subtitle', 'header', 'errorMessage', 'error-message', 'hint', 'text')
_ATTR_RE = re.compile(r'(?<![\w:@.-])(' + '|'.join(re.escape(a) for a in USER_ATTRS) +
                      r')\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{\s*"([^"]*)"\s*\}|\{\s*\'([^\']*)\'\s*\}|\{\s*`([^`$]*)`\s*\})')
_WORDY = re.compile(r'[^\W\d_]{2,}')
_JS_KEYWORDS_BEFORE_JSX = {'return', 'yield', 'default', 'case', 'await', 'in', 'of', 'else', 'do'}
_TFUNC = r'(?:\$?t|i18n\.t|t\$|translate|intl\.formatMessage|formatMessage|\$tc|\$te)\('
_CONCAT = [re.compile(_TFUNC + r'[^()]*(?:\([^()]*\)[^()]*)*\)\s*\+\s*[\w\'"`]'),
           re.compile(r'[\w\'"`)\]]\s*\+\s*' + _TFUNC),
           re.compile(r'`[^`]*\$\{\s*' + _TFUNC + r'[^`]*\$\{(?!\s*' + _TFUNC + r')[^`]*`'),
           re.compile(r'`[^`]*\$\{(?!\s*' + _TFUNC + r')[^}]*\}[^`]*\$\{\s*' + _TFUNC + r'[^`]*`')]
_LOCALE_DEFAULT = re.compile(r'\.toLocale(?:Date|Time)?String\(\s*\)|new\s+Intl\.(?:NumberFormat|DateTimeFormat|RelativeTimeFormat|PluralRules|ListFormat)\(\s*\)')
_CURRENCY = re.compile(r'([\'"][$€£¥₹]\s*[\'"]\s*\+)|(\+\s*[\'"]\s*[$€£¥₹][\'"])|(`[^`]*[$€£¥₹]\$\{)|(\.toFixed\(\d\)\s*\+\s*[\'"]\s*[$€£¥₹])')
_DATE_PAT = re.compile(r'[\'"`](?:MM[/.-]dd[/.-]yy(?:yy)?|MM[/.-]DD[/.-]YY(?:YY)?|dd[/.-]MM[/.-]yyyy|DD[/.-]MM[/.-]YYYY|M/d/yyyy|yyyy-MM-dd HH:mm|h:mm a|hh:mm A)[\'"`]')


def strip_comments(src, html=False):
    """Blank out comments, keeping offsets and newlines. Respects quotes and template literals."""
    out = list(src)
    i, n = 0, len(src)
    quote = None
    while i < n:
        c = src[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if html and src.startswith('<!--', i):
            j = src.find('-->', i + 4)
            j = n if j < 0 else j + 3
            for k in range(i, j):
                if out[k] != '\n':
                    out[k] = ' '
            i = j
            continue
        if not html and c in '\'"`':
            quote = c
        elif not html and src.startswith('//', i) and (i == 0 or src[i - 1] != ':'):
            j = src.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        elif not html and src.startswith('/*', i):
            j = src.find('*/', i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != '\n':
                    out[k] = ' '
            i = j
            continue
        elif not html and src.startswith('{/*', i):
            pass
        i += 1
    return ''.join(out)


def _prev_token(src, i):
    j = i - 1
    while j >= 0 and src[j] in ' \t\r\n':
        j -= 1
    if j < 0:
        return ''
    if src[j].isalnum() or src[j] in '_$':
        k = j
        while k >= 0 and (src[k].isalnum() or src[k] in '_$'):
            k -= 1
        return src[k + 1:j + 1]
    return src[j]


def _scan_tag(src, i):
    """src[i] == '<'. Return (end_index_after_>, name, closing, selfclosing, tagtext) or None."""
    n = len(src)
    m = re.compile(r'<(/?)\s*([A-Za-z][\w.:-]*)').match(src, i)
    if not m:
        if src.startswith('<>', i) or src.startswith('</>', i):
            return (i + (2 if src[i + 1] == '>' else 3), '', src[i + 1] == '/', False, '')
        return None
    j, depth, quote = m.end(), 0, None
    while j < n:
        c = src[j]
        if quote:
            if c == '\\':
                j += 2
                continue
            if c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif c == '>' and depth <= 0:
            text = src[i:j + 1]
            return (j + 1, m.group(2), m.group(1) == '/', text.rstrip('>').rstrip().endswith('/'), text)
        elif c == '<' and depth <= 0 and quote is None and j > m.end():
            return None  # not a tag (comparison/generic)
        j += 1
    return None


def _skip_braces(src, i):
    """src[i] == '{'. Return index after the matching '}'."""
    depth, quote, n = 0, None, len(src)
    j = i
    while j < n:
        c = src[j]
        if quote:
            if c == '\\':
                j += 2
                continue
            if c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return n


_STR_LIT = re.compile(r'(?<![\w$.])([\'"])((?:\\.|(?!\1).)*)\1')


def scan_markup(src, kind, allow):
    """Yield (offset, code, detail). kind: 'jsx' | 'vue' | 'svelte' | 'html'."""
    n = len(src)
    i = 0
    stack = []
    in_markup_depth = 0  # for jsx: only scan text after we have seen a tag
    while i < n:
        c = src[i]
        if c == '<':
            if kind == 'jsx':
                prev = _prev_token(src, i)
                if prev and (prev[-1].isalnum() or prev[-1] in '_$)]') and prev not in _JS_KEYWORDS_BEFORE_JSX:
                    i += 1
                    continue
            t = _scan_tag(src, i)
            if not t:
                i += 1
                continue
            end, name, closing, selfclosing, text = t
            lname = name.lower()
            if kind == 'jsx' and not closing and not selfclosing:
                k = end
                while k < n and src[k] in ' \t':
                    k += 1
                if k < n and src[k] in '>,)[];=|&(':  # TS generic such as Record<string, Array<Foo>>
                    i += 1
                    continue
            if closing:
                while stack:
                    if stack.pop() == lname:
                        break
                if kind == 'jsx' and not stack:
                    in_markup_depth = 0
            else:
                skip = any(s in SKIP_TAGS for s in stack) or lname in SKIP_TAGS
                if not skip:
                    for m in _ATTR_RE.finditer(text):
                        val = next(g for g in m.groups()[1:] if g is not None)
                        if _user_text(val, allow):
                            yield (i + m.start(), 'ATTR', f'{m.group(1)}="{val.strip()[:60]}"')
                if not selfclosing and name:
                    stack.append(lname)
                    in_markup_depth = 1
            i = end
            if kind in ('jsx', 'svelte', 'vue', 'html') and (stack or kind != 'jsx'):
                # text run until next '<' or '{'
                j = i
                while j < n and src[j] not in '<' and not (src[j] == '{' and kind in ('jsx', 'svelte')):
                    if kind == 'vue' and src.startswith('{{', j):
                        break
                    j += 1
                run = src[i:j]
                if not any(s in SKIP_TAGS for s in stack) and _user_text(_strip_entities(run), allow):
                    lead = len(run) - len(run.lstrip())
                    yield (i + lead, 'TEXT', run.strip()[:60])
                i = j
            continue
        if c == '{' and kind in ('jsx', 'svelte') and stack:
            end = _skip_braces(src, i)
            expr = src[i + 1:end - 1]
            if not any(s in SKIP_TAGS for s in stack) and not expr.lstrip().startswith(('/*', '#', ':', '/', '@')):
                if 'className' not in expr:
                    bare = _blank_calls(expr)
                    bare = re.sub(r'<[A-Za-z][^<>]*>', lambda m: ' ' * len(m.group(0)), bare)
                    for m in _STR_LIT.finditer(bare):
                        val = m.group(2)
                        if re.search(r'[\w$\]]\s*[:=]\s*$', bare[:m.start()]) or re.search(r'\.(?:includes|startsWith|endsWith|indexOf|get|has|match|test|replace|split|join|push|set|find|with|when|case|eq|is|equals)\(\s*$|(?:===|!==|==|!=)\s*$', bare[:m.start()]):
                            continue
                        if _user_text(val, allow) and (' ' in val.strip() or val[:1].isupper()) and not re.search(r'[/\\:#=]|^\w+-\w+|\w\.\w', val):
                            yield (i + 1 + m.start(), 'EXPR_LITERAL', val[:60])
            i = end
            # text continuing after the expression
            j = i
            while j < n and src[j] != '<' and src[j] != '{':
                j += 1
            run = src[i:j]
            if not any(s in SKIP_TAGS for s in stack) and _user_text(_strip_entities(run), allow):
                lead = len(run) - len(run.lstrip())
                yield (i + lead, 'TEXT', run.strip()[:60])
            i = j
            continue
        if kind == 'vue' and src.startswith('{{', i):
            j = src.find('}}', i)
            i = n if j < 0 else j + 2
            j = i
            while j < n and src[j] != '<' and not src.startswith('{{', j):
                j += 1
            run = src[i:j]
            if stack and not any(s in SKIP_TAGS for s in stack) and _user_text(_strip_entities(run), allow):
                yield (i + len(run) - len(run.lstrip()), 'TEXT', run.strip()[:60])
            i = j
            continue
        i += 1


def _blank_calls(expr):
    """Blank every t(...) / formatMessage(...) call, balancing nested parentheses."""
    out = list(expr)
    for m in re.finditer(_TFUNC, expr):
        depth, j, quote = 0, m.end() - 1, None
        while j < len(expr):
            c = expr[j]
            if quote:
                if c == '\\':
                    j += 2
                    continue
                if c == quote:
                    quote = None
            elif c in '"\'`':
                quote = c
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        for k in range(m.start(), min(j + 1, len(expr))):
            out[k] = ' '
    return ''.join(out)


def _strip_entities(s):
    return re.sub(r'&[#\w]+;', ' ', s)


def _user_text(s, allow):
    s = s.strip()
    if not s or not _WORDY.search(s):
        return False
    if re.fullmatch(r'[\w.-]+\.(?:png|svg|jpg|jpeg|gif|webp|css|js|ts|json)', s) or re.match(r'^(https?:|mailto:|/|#|\.)', s):
        return False
    if re.fullmatch(r'[a-z]+(?:[A-Z][a-z]+)+|[a-z]+(?:[-_][a-z0-9]+)+|[A-Z0-9_]{2,}', s):  # identifiers, kebab keys, CONSTANTS
        return False
    if re.search(r'[;=]|=>|\(\)|&&|\|\|', s):  # code leaked into a text run (generics, comparisons)
        return False
    if re.search(r'^[,:)\]}]|\b(?:export|const|let|var|function|private|public|protected|import|interface|readonly|async)\s+[\w{]|\w\(\s*$|\w\(\s*\n|\w\??\s*:\s*[\w{(\[]+\s*[,;)\n]|^\w+\.\w+\(', s):
        return False  # TypeScript or JS code, not UI text
    if re.fullmatch(r'[\w.+-]+@[\w-]+\.[\w.]+', s):
        return False
    words = _WORDY.findall(s)
    if all(w in allow for w in words):
        return False
    return True


def scan_code(src):
    for rx, code in ((_LOCALE_DEFAULT, 'LOCALE_DEFAULT'), (_CURRENCY, 'CURRENCY_LITERAL'), (_DATE_PAT, 'DATE_PATTERN')):
        for m in rx.finditer(src):
            yield (m.start(), code, m.group(0).strip()[:60])
    seen = set()
    for rx in _CONCAT:
        for m in rx.finditer(src):
            line_start = src.rfind('\n', 0, m.start())
            if line_start in seen:
                continue
            seen.add(line_start)
            yield (m.start(), 'CONCAT', m.group(0).strip()[:60])


SEVERITY = {'TEXT': 'error', 'ATTR': 'error', 'EXPR_LITERAL': 'warning', 'CONCAT': 'warning', 'LOCALE_DEFAULT': 'warning',
            'CURRENCY_LITERAL': 'warning', 'DATE_PATTERN': 'warning'}


def scan_file(path, allow):
    ext = os.path.splitext(path)[1].lower()
    with open(path, encoding='utf-8', errors='replace') as f:
        raw = f.read()
    findings = []
    if ext in ('.html', '.htm'):
        kinds = [('html', strip_comments(raw, html=True), 0)]
    elif ext == '.vue':
        src = strip_comments(raw, html=True)
        kinds = []
        m = re.search(r'<template[^>]*>(.*)</template>', src, re.S)
        if m:
            kinds.append(('vue', m.group(1), m.start(1)))
        for s in re.finditer(r'<script[^>]*>(.*?)</script>', raw, re.S):
            kinds.append(('code', strip_comments(s.group(1)), s.start(1)))
    elif ext == '.svelte':
        src = strip_comments(raw, html=True)
        body = re.sub(r'<(script|style)[^>]*>.*?</\1>', lambda m: ' ' * len(m.group(0)), src, flags=re.S)
        kinds = [('svelte', body, 0)]
        for s in re.finditer(r'<script[^>]*>(.*?)</script>', raw, re.S):
            kinds.append(('code', strip_comments(s.group(1)), s.start(1)))
    else:
        src = strip_comments(raw)
        kinds = [('jsx', src, 0)] if ext in ('.jsx', '.tsx') or re.search(r'return\s*\(?\s*<[A-Za-z]', src) else []
        kinds.append(('code', src, 0))
    lines = raw.splitlines()
    for kind, text, base in kinds:
        it = scan_code(text) if kind == 'code' else scan_markup(text, kind, allow)
        for off, code, detail in it:
            line = raw.count('\n', 0, base + off) + 1
            ltxt = lines[line - 1] if line - 1 < len(lines) else ''
            prev = lines[line - 2] if line >= 2 else ''
            if 'i18n-ignore' in ltxt or 'i18n-ignore-next-line' in prev:
                continue
            findings.append({'file': path, 'line': line, 'code': code, 'severity': SEVERITY[code], 'text': detail})
    return findings


def walk(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        if not os.path.isdir(p):
            raise FileNotFoundError(p)
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith('.'))
            for f in sorted(files):
                fp = os.path.join(root, f)
                if os.path.splitext(f)[1].lower() in EXTS and not SKIP_FILE.search(fp.replace(os.sep, '/')):
                    yield fp


def load_allow(path):
    words = set()
    if path and os.path.isfile(path):
        for line in open(path, encoding='utf-8'):
            line = line.split('#', 1)[0].strip()
            if line:
                words.update(_WORDY.findall(line))
    return words


SAMPLE = {
    'src/Cart.tsx': '''import { useTranslation } from 'react-i18next';
export function Cart({ items, total, busy }: Props) {
  const { t } = useTranslation();
  const label = t('cart.count') + ' ' + items.length;   // CONCAT
  const list = useState<string[]>([]);                  // generic, not JSX
  return (
    <section aria-label="Shopping cart">
      <h2>{t('cart.title')}</h2>
      <p>Your cart is empty</p>
      <input placeholder={t('cart.search')} />
      <button disabled={busy} onClick={() => checkout()}>{busy ? 'Saving...' : t('cart.checkout')}</button>
      <span>{'$' + total.toFixed(2)}</span>
      <time>{new Date().toLocaleDateString()}</time>
      <Trans i18nKey="cart.terms">By paying you accept the <a href="/terms">terms</a>.</Trans>
      <code>npm run build</code>
    </section>
  );
}
''',
}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Find user-facing strings that bypass the translation layer '
                                 '(React, Vue, Svelte, HTML).')
    ap.add_argument('paths', nargs='*', default=['src'], help='files or directories (default: src)')
    ap.add_argument('--allow-file', default='.i18n-allow', help='words to ignore, one per line (default: .i18n-allow)')
    ap.add_argument('--warn-only', action='store_true', help='report TEXT/ATTR as warnings (adoption mode)')
    ap.add_argument('--output', choices=('text', 'json'), default='text')
    ap.add_argument('--sample', action='store_true', help='scan a built-in component with planted defects')
    ap.add_argument('--max', type=int, default=200)
    a = ap.parse_args(argv)
    tmp = None
    if a.sample:
        tmp = tempfile.mkdtemp(prefix='hardcoded_')
        for rel, body in SAMPLE.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8').write(body)
        a.paths = [os.path.join(tmp, 'src')]
    allow = load_allow(a.allow_file)
    try:
        files = list(walk(a.paths))
    except FileNotFoundError as e:
        print(f'error: {e} not found', file=sys.stderr)
        return 3
    findings = []
    for f in files:
        findings += scan_file(f, allow)
    if a.warn_only:
        for f in findings:
            f['severity'] = 'warning'
    if tmp:
        for f in findings:
            f['file'] = os.path.relpath(f['file'], tmp)
    errs = sum(f['severity'] == 'error' for f in findings)
    warns = len(findings) - errs
    verdict = 'BLOCKED' if errs else ('WARN' if warns else 'PASS')
    counts = {}
    for f in findings:
        counts[f['code']] = counts.get(f['code'], 0) + 1
    if a.output == 'json':
        print(json.dumps({'verdict': verdict, 'files_scanned': len(files), 'errors': errs, 'warnings': warns,
                          'by_code': counts, 'findings': findings}, ensure_ascii=False, indent=2))
    else:
        print(f'{verdict}: {errs} errors, {warns} warnings in {len(files)} file(s) '
              + (' '.join(f'{k}={v}' for k, v in sorted(counts.items())) if counts else ''))
        for f in sorted(findings, key=lambda x: (x['severity'] != 'error', x['file'], x['line']))[:a.max]:
            print(f"  {f['severity'][:4].upper()} {f['code']:<16} {f['file']}:{f['line']}  {f['text']}")
        if len(findings) > a.max:
            print(f'  ... {len(findings) - a.max} more (use --output json)')
    return 4 if errs else (2 if warns else 0)


if __name__ == '__main__':
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
