#!/usr/bin/env python3
"""locale_sync.py - check translation files against the source locale before a release.

Reads JSON / ARB (nested or flat, i18next or ICU), Java .properties, Apple
.strings, Android strings.xml and gettext .po files. For every target locale it
reports, against the source locale file of the same namespace:

  MISSING_KEY           key in source, absent in target                     (error)
  EMPTY_VALUE           key present, value empty                            (error)
  PLACEHOLDER_MISMATCH  {{name}} / {name} / %s / %1$s / %{name} differ      (error)
  ICU_SYNTAX            unbalanced braces, bad plural/select                (error)
  ICU_NO_OTHER          plural/select without the mandatory `other` branch  (error)
  PLURAL_MISSING        a CLDR plural category this locale needs for whole
                        numbers is missing (ru `few`/`many`, ar `zero`..)  (error;
                        warning when it only applies from 1,000,000 up)
  ZERO_NEVER_MATCHES    ICU `zero {...}` in a locale with no `zero` category;
                        it never fires, use `=0`                            (error)
  FUZZY                 gettext entry flagged fuzzy                         (warning)
  PLURAL_DEAD           category this locale never selects (`few` in de)    (warning)
  EXTRA_KEY             key only in target (orphan, or a renamed source key)(warning)
  UNTRANSLATED          target value identical to source                    (warning)
  TAG_MISMATCH          <b>, <0>, <link> markup differs                     (warning)
  JAVA_APOSTROPHE       lone ' in a Java MessageFormat string with {0} args
                        is swallowed (`Don't` renders `Dont`)               (warning)

Plural categories come from Unicode CLDR 49 (embedded; no network).

Exit codes: 0 clean · 2 warnings only · 3 bad input · 4 errors (block the release).
Stdlib only.
"""
import argparse
import json
import os
import re
import signal
import sys
import tempfile
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- CLDR
# Cardinal plural categories per locale, CLDR 49 (cldr-json plurals.json).
# "cat:N" = smallest whole number that selects it, "!" = it selects only N,
# bare "cat" = decimals only (never chosen for an integer count).
_CLDR = {
    'one:1! other:0': 'af an asa ast az bal bem bez bg brx ce cgg chr ckb da de dv ee el en eo et eu fi fo fur fy gsw ha haw hu ia ie io jgo jmc ka kaj kcg kk kkj kl ks ksb ku ky lb lg lij mas mgo ml mn mr nah nb nd ne nl nn nnh no nr ny nyn om or os pap ps rm rof rwk saq sc sd sdh seh sn so sq ss ssy st sv sw syr ta te teo tig tk tn tr ts ug ur uz ve vo vun wae xh xog yi',
    'other:0': 'bm bo dz hnj id ig ii ja jbo jv jw kde kea km ko lkt lo ms my nqo osa sah ses sg su th to tpi und wo yo yue zh',
    'one:0 other:2': 'ak am as bho bn csw doi fa ff gu guw hi hy kab kn kok kok-Latn ln mg nso pa pcm si tg ti tzm vi wa zu',
    'one:1! two:2! other:0': 'he iu naq sat se sma smi smj smn sms',
    'one:1! many:1000000 other:0': 'ca es gl it lld pt-PT scn vec',
    'zero:0! one:1! other:2': 'blo cv ksh lag',
    'one:1 few:2 other:0': 'bs hr sh sr',
    'one:1 two:2 few:3 other:0': 'dsb gd hsb sl',
    'one:1 few:2 many:0 other': 'be ru uk',
    'one:0 other:4': 'ceb fil tl',
    'zero:0! one:1! two:2! few:3 many:11 other:100': 'ar ars',
    'one:1! few:2 many other:0': 'cs sk',
    'one:0 many:1000000 other:2': 'fr pt',
    'one:1 other:0': 'is mk',
    'zero:0 one:1 other:2': 'lv prg',
    'one:1! few:0 other:20': 'mo ro',
    'one:1 two:2 few:3 many:1000000 other:0': 'br',
    'zero:0! one:1! two:2! few:3! many:6! other:4': 'cy',
    'one:1! two:2! few:3 many:7 other:0': 'ga',
    'one:1 two:2 few:0 many other:3': 'gv',
    'zero:0! one:1! two:2 few:3 many:21 other:4': 'kw',
    'one:1 few:2 many other:0': 'lt',
    'one:1! two:2! few:0 many:11 other:20': 'mt',
    'one:1! few:2 many:0 other': 'pl',
    'one:1 two:2! few:3 many other:0': 'sgs',
    'one:0 few:2 other:11': 'shi',
}
CATEGORIES = ('zero', 'one', 'two', 'few', 'many', 'other')
PLURAL_RULES = {}
for _sig, _locs in _CLDR.items():
    _rule = {}
    for _part in _sig.split():
        _cat, _, _n = _part.partition(':')
        _rule[_cat] = None if not _n else (int(_n.rstrip('!')), _n.endswith('!'))
    for _loc in _locs.split():
        PLURAL_RULES[_loc] = _rule


def plural_rule(locale):
    """Return {category: (min_int, single) | None} for a BCP 47-ish tag, or None if unknown."""
    if not locale:
        return None
    tag = locale.replace('_', '-')
    parts = tag.split('-')
    for cand in (tag, '-'.join(parts[:2]), parts[0]):
        for key in (cand, cand.lower(), parts[0].lower() + ('-' + parts[1] if len(parts) > 1 and cand != parts[0] else '')):
            if key in PLURAL_RULES:
                return PLURAL_RULES[key]
    return None


# ---------------------------------------------------------------- locale from path
_LOC_RE = re.compile(r'^([a-z]{2,3})(?:[-_]([A-Za-z]{4}))?(?:[-_]r?([A-Z]{2}|\d{3}))?$')


def _as_locale(token):
    m = _LOC_RE.match(token)
    if not m:
        return None
    lang, script, region = m.groups()
    if lang not in {k.split('-')[0] for k in PLURAL_RULES} and lang not in ('en', 'pt'):
        return None
    return '-'.join(x for x in (lang, script, region) if x)


def locale_of(path):
    """Infer (locale, namespace) from a path: en.json, de/common.json, values-ru/strings.xml,
    fr.lproj/Localizable.strings, messages_de.properties, app_pt_BR.arb, locale/de/LC_MESSAGES/x.po."""
    parts = os.path.normpath(path).split(os.sep)
    name = parts[-1]
    stem, ext = os.path.splitext(name)
    loc = _as_locale(stem)
    if loc:
        return loc, ext
    for sep in ('_', '-', '.'):  # messages_de, app_pt_BR, strings.de
        bits = stem.split(sep)
        for i in range(1, len(bits)):
            cand = _as_locale(sep.join(bits[i:])) if sep != '.' else _as_locale(bits[i])
            if cand:
                return cand, sep.join(bits[:i]) + ext
    for d in reversed(parts[:-1]):
        tok = d
        if tok.startswith('values-'):
            tok = tok[7:]
        if tok.endswith('.lproj'):
            tok = tok[:-6]
        if tok == 'values':
            return None, name  # Android default resources: no locale in the path
        cand = _as_locale(tok)
        if cand:
            return cand, name
        if tok == 'LC_MESSAGES':
            continue
    return None, name


# ----------------------------------------------------------------------- readers
class Entry:
    __slots__ = ('value', 'fuzzy', 'msgid', 'line')

    def __init__(self, value, fuzzy=False, msgid=None, line=None):
        self.value, self.fuzzy, self.msgid, self.line = value, fuzzy, msgid, line


def _flatten(obj, prefix, out, arb):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if arb and k.startswith('@'):
                continue
            _flatten(v, f'{prefix}.{k}' if prefix else k, out, arb)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _flatten(v, f'{prefix}[{i}]', out, arb)
    elif isinstance(obj, str):
        out[prefix] = Entry(obj)
    elif obj is not None:
        out[prefix] = Entry(str(obj))


def read_json(path, arb=False):
    with open(path, encoding='utf-8-sig') as f:
        data = json.load(f)
    out = {}
    _flatten(data, '', out, arb)
    return out


def read_properties(path):
    out, buf, start = {}, '', None
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().splitlines()
    for no, raw in enumerate(lines, 1):
        line = raw.lstrip() if not buf else raw.lstrip()
        if not buf and (not line or line[0] in '#!'):
            continue
        if not buf:
            start = no
        if re.search(r'(?<!\\)(\\\\)*\\$', line):
            buf += line[:-1]
            continue
        buf += line
        m = re.match(r'((?:\\.|[^=:\s])+)\s*[=:\s]\s*(.*)$', buf)
        if m:
            key = m.group(1).replace('\\', '')
            val = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), m.group(2))
            val = val.replace('\\n', '\n').replace('\\t', '\t').replace('\\:', ':').replace('\\=', '=')
            out[key] = Entry(val, line=start)
        buf = ''
    return out


def read_strings(path):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-16') if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else raw.decode('utf-8-sig')
    text = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    out = {}
    for m in re.finditer(r'"((?:\\.|[^"\\])*)"\s*=\s*"((?:\\.|[^"\\])*)"\s*;', text):
        line = text.count('\n', 0, m.start()) + 1
        val = m.group(2).replace('\\"', '"').replace('\\n', '\n')
        out[m.group(1).replace('\\"', '"')] = Entry(val, line=line)
    return out


def read_android(path):
    out = {}
    root = ET.parse(path).getroot()
    for el in root:
        name = el.get('name')
        if not name or el.get('translatable') == 'false':
            continue
        if el.tag == 'string':
            out[name] = Entry(''.join(el.itertext()).strip().strip('"'))
        elif el.tag == 'plurals':
            for item in el.findall('item'):
                out[f"{name}_{item.get('quantity')}"] = Entry(''.join(item.itertext()).strip().strip('"'))
        elif el.tag == 'string-array':
            for i, item in enumerate(el.findall('item')):
                out[f'{name}[{i}]'] = Entry(''.join(item.itertext()).strip().strip('"'))
    return out


def _po_unquote(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')


def read_po(path):
    """Key = msgctxt\\x04msgid; plural forms become key[0], key[1] ... ."""
    out, cur, field, fuzzy, start = {}, {}, None, False, None

    def flush():
        if 'msgid' in cur and cur['msgid'] != '':
            key = (cur.get('msgctxt', '') + '\x04' if 'msgctxt' in cur else '') + cur['msgid']
            if 'msgid_plural' in cur:
                for k in sorted(x for x in cur if x.startswith('msgstr[')):
                    out[f'{key}{k[6:]}'] = Entry(cur[k], fuzzy, cur['msgid'] if k == 'msgstr[0]' else cur['msgid_plural'], start)
            else:
                out[key] = Entry(cur.get('msgstr', ''), fuzzy, cur['msgid'], start)

    with open(path, encoding='utf-8', errors='replace') as f:
        for no, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            if line.startswith('#,') and 'fuzzy' in line:
                if 'msgstr' in ''.join(cur) or 'msgid' in cur:
                    flush()
                    cur = {}
                fuzzy = True
                continue
            if line.startswith('#'):
                continue
            m = re.match(r'(msgctxt|msgid_plural|msgid|msgstr\[\d+\]|msgstr)\s+(".*")\s*$', line)
            if m:
                kw = m.group(1)
                if kw in ('msgctxt', 'msgid') and any(k.startswith('msgstr') for k in cur):
                    flush()
                    cur, fuzzy = {}, fuzzy if kw == 'msgid' and False else False
                if kw in ('msgctxt', 'msgid') and not cur:
                    start = no
                field = kw
                cur[kw] = _po_unquote(m.group(2))
            elif line.startswith('"') and field:
                cur[field] += _po_unquote(line)
    flush()
    return out


READERS = {'.pot': read_po, '.json': read_json, '.arb': lambda p: read_json(p, arb=True), '.properties': read_properties,
           '.strings': read_strings, '.xml': read_android, '.po': read_po}


# ------------------------------------------------------------------ ICU parsing
class ICUError(Exception):
    pass


class Plural:
    __slots__ = ('arg', 'kind', 'selectors', 'pos')

    def __init__(self, arg, kind, selectors, pos):
        self.arg, self.kind, self.selectors, self.pos = arg, kind, selectors, pos


def parse_icu(msg):
    """Parse an ICU MessageFormat string (apostrophe mode DOUBLE_OPTIONAL).
    Returns (arg_names:set, plural_nodes:list). Raises ICUError."""
    args, plurals = set(), []
    n = len(msg)

    def ws(i):
        while i < n and msg[i].isspace():
            i += 1
        return i

    def message(i, in_plural):
        while i < n:
            c = msg[i]
            if c == "'":
                nxt = msg[i + 1] if i + 1 < n else ''
                if nxt == "'":
                    i += 2
                elif nxt in '{}|' or (in_plural and nxt == '#'):
                    j = i + 1
                    while True:
                        j = msg.find("'", j)
                        if j < 0:
                            return n  # quoted to the end: literal, ICU tolerates it
                        if j + 1 < n and msg[j + 1] == "'":
                            j += 2
                            continue
                        break
                    i = j + 1
                else:
                    i += 1
            elif c == '{':
                i = argument(i)
            elif c == '}':
                return i
            else:
                i += 1
        return i

    def argument(i):
        start = i
        i = ws(i + 1)
        m = re.compile(r'[^\s,{}]+').match(msg, i)
        if not m:
            raise ICUError(f'empty argument at {start}')
        name = m.group(0)
        args.add(name)
        i = ws(m.end())
        if i >= n:
            raise ICUError(f'unclosed {{ at {start}')
        if msg[i] == '}':
            return i + 1
        if msg[i] != ',':
            raise ICUError(f'expected , or }} after "{name}" at {i}')
        i = ws(i + 1)
        m = re.compile(r'[A-Za-z]+').match(msg, i)
        if not m:
            raise ICUError(f'missing argument type for "{name}" at {i}')
        kind = m.group(0)
        i = ws(m.end())
        if kind in ('plural', 'select', 'selectordinal'):
            if i >= n or msg[i] != ',':
                raise ICUError(f'{kind} "{name}" needs options at {i}')
            i = ws(i + 1)
            if kind == 'plural':
                mo = re.compile(r'offset:\s*\d+').match(msg, i)
                if mo:
                    i = ws(mo.end())
            selectors = []
            while i < n and msg[i] != '}':
                ms = re.compile(r'[^\s{}]+').match(msg, i)
                if not ms:
                    raise ICUError(f'bad selector in "{name}" at {i}')
                sel = ms.group(0)
                if sel in selectors:
                    raise ICUError(f'duplicate selector "{sel}" in "{name}"')
                selectors.append(sel)
                i = ws(ms.end())
                if i >= n or msg[i] != '{':
                    raise ICUError(f'selector "{sel}" in "{name}" has no {{message}} at {i}')
                i = message(i + 1, kind != 'select')
                if i >= n or msg[i] != '}':
                    raise ICUError(f'unclosed branch "{sel}" in "{name}"')
                i = ws(i + 1)
            if i >= n:
                raise ICUError(f'unclosed {kind} "{name}" at {start}')
            plurals.append(Plural(name, kind, selectors, start))
            return i + 1
        depth = 0  # number/date/time with a style or skeleton
        while i < n:
            if msg[i] == '{':
                depth += 1
            elif msg[i] == '}':
                if depth == 0:
                    return i + 1
                depth -= 1
            i += 1
        raise ICUError(f'unclosed {{ at {start}')

    end = message(0, False)
    if end < n:
        raise ICUError(f'unmatched }} at {end}')
    return args, plurals


# --------------------------------------------------------------- placeholders
_I18NEXT = re.compile(r'\{\{\s*-?\s*([\w.\-$]+)\s*(?:,[^}]*)?\}\}')
_PRINTF = re.compile(r'%(?:(\d+)\$)?[-+ 0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|q|z|t|j|L)?([sdifuxXeEgGcpo@])')
_PYNAMED = re.compile(r'%\(([\w.]+)\)[-+ 0#]*\d*(?:\.\d+)?[sdifr]')
_RUBY = re.compile(r'%\{([\w.]+)\}')
_WORDS = re.compile(r'[^\W\d_]{2,}')
_TAG = re.compile(r'</?([A-Za-z][\w-]*|\d+)\s*/?>')


_ICU_COMPLEX = re.compile(r'\{\s*[\w.]+\s*,\s*(?:plural|select|selectordinal)\s*,')


def placeholders(value):
    """Return (named:set, printf_seq:tuple, icu_args:set|None, plurals, icu_error)."""
    icu_mode = bool(_ICU_COMPLEX.search(value))
    named = set() if icu_mode else {('{{}}', m.group(1)) for m in _I18NEXT.finditer(value)}
    named |= {('%()', m.group(1)) for m in _PYNAMED.finditer(value)}
    named |= {('%{}', m.group(1)) for m in _RUBY.finditer(value)}
    stripped = _PYNAMED.sub('', _RUBY.sub('', value.replace('%%', '')))
    seq = []
    for m in _PRINTF.finditer(stripped):
        t = m.group(2)
        t = 'd' if t in 'diu' else t
        seq.append(f'%{m.group(1)}${t}' if m.group(1) else f'%{t}')
    icu, plurals, err = None, [], None
    body = _RUBY.sub('', value) if icu_mode else _I18NEXT.sub('', _RUBY.sub('', value))
    if '{' in body or '}' in body:
        try:
            icu, plurals = parse_icu(body)
        except ICUError as e:
            err = str(e)
    return named, tuple(seq), icu, plurals, err


def _printf_equal(a, b):
    if all('$' in x for x in a + b):  # positional: order free
        return sorted(a) == sorted(b)
    return a == b


# ------------------------------------------------------------------- checking
SEVERITY = {'MISSING_KEY': 'error', 'EMPTY_VALUE': 'error', 'PLACEHOLDER_MISMATCH': 'error', 'ICU_SYNTAX': 'error',
            'ICU_NO_OTHER': 'error', 'PLURAL_MISSING': 'error', 'ZERO_NEVER_MATCHES': 'error', 'FUZZY': 'warning',
            'PLURAL_DEAD': 'warning', 'EXTRA_KEY': 'warning', 'UNTRANSLATED': 'warning', 'TAG_MISMATCH': 'warning',
            'JAVA_APOSTROPHE': 'warning', 'UNKNOWN_LOCALE': 'warning', 'PLURAL_MILLIONS': 'warning'}


def collapse_millions(findings):
    """One warning per file for categories that only apply from 1,000,000 (fr/es/it/pt `many`)."""
    out, groups = [], {}
    for f in findings:
        if f['code'] == 'PLURAL_MILLIONS':
            groups.setdefault((f['file'], f['locale'], f['detail']), []).append(f['key'])
        else:
            out.append(f)
    for (file, loc, cat), keys in groups.items():
        out.append({'code': 'PLURAL_MISSING', 'severity': 'warning', 'locale': loc, 'file': file, 'key': f'{len(keys)} plural message(s)',
                    'line': None, 'detail': f'no `{cat}` branch; {loc} selects it only from 1,000,000 ("1 000 000 de ..."), '
                    f'otherwise `other` is used. Add it if such counts occur. First: {", ".join(sorted(keys)[:3])}'})
    return out
_PSUFFIX = re.compile(r'^(.*?)(_ordinal)?_(zero|one|two|few|many|other)$')


def _needed(rule):
    """Categories a whole-number count can select: {cat: min_int}."""
    return {c: v[0] for c, v in rule.items() if v is not None}


def check_icu_plurals(plurals, rule, locale, finding, key):
    for p in plurals:
        sels = p.selectors
        if 'other' not in sels:
            finding('ICU_NO_OTHER', key, f'{p.kind} "{p.arg}" has no `other` branch (required by ICU)')
        if p.kind != 'plural' or rule is None:
            continue
        exact = {int(s[1:]) for s in sels if re.fullmatch(r'=\d+', s)}
        for s in sels:
            if s in CATEGORIES and s not in rule:
                if s == 'zero':
                    finding('ZERO_NEVER_MATCHES', key, f'`zero` never matches in {locale}; use `=0 {{...}}` for an empty-count message')
                else:
                    finding('PLURAL_DEAD', key, f'`{s}` is never selected in {locale} (CLDR categories: {", ".join(rule)})')
        for cat, (low, single) in sorted(((c, v) for c, v in rule.items() if v), key=lambda x: x[1][0]):
            if cat == 'other' or cat in sels or (single and low in exact):
                continue
            if low >= 1000000:
                finding('PLURAL_MILLIONS', key, cat)
                continue
            finding('PLURAL_MISSING', key, f'{p.kind} "{p.arg}" lacks `{cat}` (e.g. {low}) needed in {locale}')


def compare(src, tgt, src_loc, tgt_loc, fmt, tgt_path):
    findings = []

    def finding(code, key, detail, severity=None):
        e = tgt.get(key) or src.get(key)
        findings.append({'code': code, 'severity': severity or SEVERITY[code], 'locale': tgt_loc, 'file': tgt_path,
                         'key': key.replace('\x04', ' | '), 'line': e.line if e else None, 'detail': detail})

    rule = plural_rule(tgt_loc)
    if rule is None:
        finding('UNKNOWN_LOCALE', '', f'no CLDR plural data for "{tgt_loc}"; plural checks skipped')

    # plural groups (i18next _one/_other, Android quantity items)
    def groups(d):
        g = {}
        for k in d:
            m = _PSUFFIX.match(k)
            if m:
                g.setdefault((m.group(1), bool(m.group(2))), set()).add(m.group(3))
        return {b: c for b, c in g.items() if 'other' in c or len(c) > 1}

    sg, tg = groups(src), groups(tgt)
    plural_keys = {f'{b}{"_ordinal" if o else ""}_{c}' for (b, o), cs in list(sg.items()) + list(tg.items()) for c in cs}

    for (base, ordinal), scats in sg.items():
        if ordinal:
            continue  # ordinal plural rules differ; not checked
        tcats = tg.get((base, ordinal))
        label = f'{base}_*'
        if not tcats:
            finding('MISSING_KEY', base, f'plural group {label} missing entirely')
            continue
        if rule:
            for cat, low in sorted(_needed(rule).items(), key=lambda x: x[1]):
                if cat not in tcats:
                    if low >= 1000000:
                        finding('PLURAL_MILLIONS', f'{base}_{cat}', cat)
                        continue
                    finding('PLURAL_MISSING', f'{base}_{cat}', f'{label} needs `_{cat}` in {tgt_loc} (e.g. count={low})')
            for cat in tcats:
                if cat not in rule and not (cat == 'zero' and fmt in ('.json', '.arb')):
                    finding('PLURAL_DEAD', f'{base}_{cat}', f'`_{cat}` is never selected in {tgt_loc}')

    po = fmt == '.po'
    for key, se in src.items():
        if key in plural_keys and not po:
            continue
        sval = se.value if not (po and not se.value) else (se.msgid or '')
        te = tgt.get(key)
        if te is None:
            finding('MISSING_KEY', key, f'source: "{_short(sval)}"')
            continue
        if te.value.strip() == '':
            finding('MISSING_KEY' if po else 'EMPTY_VALUE', key, f'source: "{_short(sval)}"' + (' (msgstr empty)' if po else ''))
            continue
        if te.fuzzy:
            finding('FUZZY', key, 'gettext marks this translation fuzzy; it is not used at runtime')
    for key, te in tgt.items():
        if key not in src and key not in plural_keys:
            finding('EXTRA_KEY', key, 'not in the source locale (orphan, or the source key was renamed)')

    # per-value checks: placeholders, ICU, tags, untranslated
    same_lang = (src_loc or '').split('-')[0] == (tgt_loc or '').split('-')[0]
    for key, te in tgt.items():
        if not te.value.strip():
            continue
        m = _PSUFFIX.match(key)
        if key in src:
            se = src[key]
        elif m and key in plural_keys:  # compare a plural variant with the source's `other`
            se = src.get(f'{m.group(1)}{m.group(2) or ""}_other') or src.get(f'{m.group(1)}{m.group(2) or ""}_one')
        else:
            se = None
        tn, tp, ticu, tplur, terr = placeholders(te.value)
        if terr:
            finding('ICU_SYNTAX', key, terr)
            continue
        else:
            check_icu_plurals(tplur, rule, tgt_loc, finding, key)
        if fmt == '.properties' and ticu and re.search(r"(?<!')'(?![{}'])", te.value):
            finding('JAVA_APOSTROPHE', key, "lone ' before text in a {0}-style message; java.text.MessageFormat drops it. Write ''")
        if se is None:
            continue
        sval = se.value if se.value or not po else (se.msgid or '')
        sn, sp, sicu, _, serr = placeholders(sval)
        if serr:
            continue
        problems = []
        if sn != tn:
            miss = sorted(f'{{{{{x[1]}}}}}' if x[0] == '{{}}' else x[1] for x in sn - tn)
            extra = sorted(f'{{{{{x[1]}}}}}' if x[0] == '{{}}' else x[1] for x in tn - sn)
            problems.append(f'missing {", ".join(miss)}' if miss else '')
            problems.append(f'unknown {", ".join(extra)}' if extra else '')
        if not _printf_equal(sp, tp):
            problems.append(f'printf {list(sp)} vs {list(tp)}')
        if (sicu or set()) != (ticu or set()) and (sicu or ticu):
            miss = sorted((sicu or set()) - (ticu or set()))
            extra = sorted((ticu or set()) - (sicu or set()))
            if m and key in plural_keys and not extra:
                miss = []  # a plural variant may drop {count}, e.g. ru "one" written as a word
            if miss:
                problems.append('missing {' + '}, {'.join(miss) + '}')
            if extra:
                problems.append('unknown {' + '}, {'.join(extra) + '}')
        problems = [p for p in problems if p]
        if problems:
            finding('PLACEHOLDER_MISMATCH', key, '; '.join(problems) + f' (source: "{_short(sval)}")')
        stags = sorted(t.lower() for t in _TAG.findall(sval))
        ttags = sorted(t.lower() for t in _TAG.findall(te.value))
        if stags != ttags:
            finding('TAG_MISMATCH', key, f'markup {stags} vs {ttags}')
        if (not same_lang and te.value == sval and len(re.findall(r'[^\W\d_]', sval)) >= 4
                and len(_WORDS.findall(sval)) >= 2 and not re.match(r'^(https?://|[\w.+-]+@)', sval)):
            finding('UNTRANSLATED', key, f'identical to source: "{_short(sval)}"')
    return findings


def lint_source(src, src_loc, fmt, path):
    """ICU syntax and plural coverage of the source locale itself."""
    findings = []
    rule = plural_rule(src_loc)

    def finding(code, key, detail, severity=None):
        e = src.get(key)
        findings.append({'code': code, 'severity': severity or SEVERITY[code], 'locale': src_loc, 'file': path,
                         'key': key.replace('\x04', ' | '), 'line': e.line if e else None, 'detail': detail})

    for key, e in src.items():
        val = e.value or (e.msgid or '')
        _, _, _, plur, err = placeholders(val)
        if err:
            finding('ICU_SYNTAX', key, err)
        else:
            check_icu_plurals(plur, rule, src_loc, finding, key)
    return findings


def _po_nplurals(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        m = re.search(r'nplurals\s*=\s*(\d+)', f.read(4000))
    return int(m.group(1)) if m else None


def check_po(path, loc, pot, source_locale):
    """gettext: msgid is the source text; msgstr is checked against it."""
    tgt = read_po(path)
    src = {k: Entry(e.msgid or '', line=e.line) for k, e in tgt.items()}
    if pot:
        for k, e in read_po(pot).items():
            src.setdefault(k, Entry(e.msgid or '', line=e.line))
    findings = compare(src, tgt, source_locale, loc, '.po', path)
    rule = plural_rule(loc)
    want = sum(1 for v in (rule or {}).values() if v and v[0] < 1000000) if rule else None
    have = _po_nplurals(path)
    if want and have and have != want:
        findings.append({'code': 'PLURAL_MISSING', 'severity': 'warning', 'locale': loc, 'file': path, 'key': 'Plural-Forms',
                         'line': None, 'detail': f'header nplurals={have}, but {loc} has {want} whole-number plural forms in CLDR'})
    if have:
        bases = {}
        for k in tgt:
            m = re.match(r'(.*)\[(\d+)\]$', k, re.S)
            if m:
                bases.setdefault(m.group(1), set()).add(int(m.group(2)))
        for b, idx in bases.items():
            if len(idx) < have or any(not tgt[f'{b}[{i}]'].value.strip() for i in idx):
                findings.append({'code': 'PLURAL_MISSING', 'severity': 'error', 'locale': loc, 'file': path,
                                 'key': b.replace('\x04', ' | '), 'line': tgt[f'{b}[{min(idx)}]'].line,
                                 'detail': f'{len(idx)} msgstr forms (some may be empty), header needs {have}'})
    return findings, len(tgt)


def _short(s, n=60):
    s = s.replace('\n', '\\n')
    return s if len(s) <= n else s[:n - 1] + '…'


# ------------------------------------------------------------------------- CLI
def discover(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'build', 'dist', '.next')]
                for nm in names:
                    ext = os.path.splitext(nm)[1]
                    if ext in READERS and nm not in ('package.json', 'tsconfig.json', 'package-lock.json', 'AndroidManifest.xml'):
                        if ext == '.xml' and not os.path.basename(root).startswith('values'):
                            continue
                        files.append(os.path.join(root, nm))
        elif os.path.isfile(p):
            files.append(p)
        else:
            raise SystemExit(f'error: {p} not found')
    return sorted(set(files))


def run(paths, source_locale, source_file=None):
    files = discover(paths)
    if source_file and source_file not in files:
        files.append(source_file)
    if not files:
        raise ValueError('no translation files found (json, arb, properties, strings, strings.xml, po)')
    by_ns = {}
    for f in files:
        loc, ns = locale_of(f)
        ext = os.path.splitext(f)[1]
        if f == source_file:
            loc = source_locale
        if loc is None and ext == '.xml':
            loc = source_locale  # Android values/ holds the default (source) strings
        if loc is None and ext == '.po' and f.endswith('.pot'):
            loc = source_locale
        if loc is None:
            continue
        by_ns.setdefault((ns, ext), {})[f] = loc
    findings, compared, skipped = [], [], []
    po_files = [f for f in files if f.endswith('.po')]
    for f in po_files:
        loc = locale_of(f)[0]
        if loc is None:
            skipped.append(f)
            continue
        pots = [p for p in files if p.endswith('.pot') and locale_of(p)[1].replace('.pot', '') == locale_of(f)[1].replace('.po', '')]
        findings_f, n = check_po(f, loc, pots[0] if pots else None, source_locale)
        findings += findings_f
        compared.append({'file': f, 'locale': loc, 'source': pots[0] if pots else '(msgids)', 'keys': n, 'source_keys': n})
    for (ns, ext), members in sorted(by_ns.items()):
        if ext in ('.po', '.pot'):
            continue
        srcs = [f for f, l in members.items() if l == source_locale or f == source_file]
        if not srcs:
            srcs = [f for f, l in members.items() if l.split('-')[0] == source_locale.split('-')[0]]
        if not srcs:
            skipped.extend(members)
            continue
        sfile = srcs[0]
        try:
            src = READERS[ext](sfile)
        except (ValueError, ET.ParseError, UnicodeDecodeError) as e:
            raise ValueError(f'{sfile}: {e}')
        findings += lint_source(src, source_locale, ext, sfile)
        for f, loc in sorted(members.items()):
            if f == sfile:
                continue
            try:
                tgt = READERS[ext](f)
            except (ValueError, ET.ParseError, UnicodeDecodeError) as e:
                findings.append({'code': 'ICU_SYNTAX', 'severity': 'error', 'locale': loc, 'file': f, 'key': '',
                                 'line': None, 'detail': f'cannot parse file: {e}'})
                continue
            findings += compare(src, tgt, source_locale, loc, ext, f)
            compared.append({'file': f, 'locale': loc, 'source': sfile, 'keys': len(tgt), 'source_keys': len(src)})
    findings = collapse_millions(findings)
    return {'source_locale': source_locale, 'compared': compared, 'unmatched_files': skipped, 'findings': findings}


SAMPLE = {
    'locales/en/common.json': {'cart': {'title': 'Your cart', 'items_one': '{{count}} item', 'items_other': '{{count}} items',
                                        'checkout': 'Check out', 'welcome': 'Welcome back, {{name}}!'},
                               'inbox': '{n, plural, zero {No messages} one {# message} other {# messages}}'},
    'locales/de/common.json': {'cart': {'title': 'Dein Warenkorb', 'items_one': '{{count}} Artikel', 'items_other': '{{count}} Artikel',
                                        'welcome': 'Willkommen zurück, {{vorname}}!'},
                               'inbox': '{n, plural, one {# Nachricht} other {# Nachrichten}}'},
    'locales/ru/common.json': {'cart': {'title': 'Ваша корзина', 'items_one': '{{count}} товар', 'items_other': '{{count}} товара',
                                        'checkout': 'Check out', 'welcome': 'С возвращением, {{name}}!'},
                               'inbox': '{n, plural, one {# сообщение} other {# сообщений}}'},
}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Check translation files against the source locale: missing keys, '
                                 'placeholders, ICU syntax and CLDR plural categories.')
    ap.add_argument('paths', nargs='*', help='locale files or directories (default: ./locales if present)')
    ap.add_argument('--source-locale', default='en', help='source language tag (default: en)')
    ap.add_argument('--source-file', help='explicit source file when the locale is not in its path')
    ap.add_argument('--output', choices=('text', 'json'), default='text')
    ap.add_argument('--sample', action='store_true', help='run on a built-in example with planted defects')
    ap.add_argument('--max', type=int, default=200, help='max findings printed in text mode')
    a = ap.parse_args(argv)
    tmp = None
    if a.sample:
        tmp = tempfile.mkdtemp(prefix='locale_sync_')
        for rel, data in SAMPLE.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        a.paths = [os.path.join(tmp, 'locales')]
    if not a.paths:
        guess = [d for d in ('locales', 'public/locales', 'src/locales', 'src/i18n', 'i18n', 'translations', 'lang', 'l10n') if os.path.isdir(d)]
        if not guess:
            print('error: no paths given and no locales/ directory found', file=sys.stderr)
            return 3
        a.paths = guess[:1]
    try:
        res = run(a.paths, a.source_locale, a.source_file)
    except (ValueError, OSError) as e:
        print(f'error: {e}', file=sys.stderr)
        return 3
    errs = [f for f in res['findings'] if f['severity'] == 'error']
    warns = [f for f in res['findings'] if f['severity'] == 'warning']
    verdict = 'BLOCKED' if errs else ('WARN' if warns else 'PASS')
    res['verdict'] = verdict
    res['errors'], res['warnings'] = len(errs), len(warns)
    if not res['compared'] and not res['findings']:
        print(f'error: no target locale matched source locale "{a.source_locale}" (use --source-locale / --source-file)', file=sys.stderr)
        return 3
    if a.output == 'json':
        if tmp:
            for f in res['findings']:
                f['file'] = os.path.relpath(f['file'], tmp)
            for c in res['compared']:
                c['file'], c['source'] = os.path.relpath(c['file'], tmp), os.path.relpath(c['source'], tmp)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        locs = sorted({c['locale'] for c in res['compared']})
        print(f'{verdict}: {len(errs)} errors, {len(warns)} warnings across {len(locs)} target locale(s) '
              f'[{", ".join(locs)}] vs source "{a.source_locale}"')
        order = {'error': 0, 'warning': 1}
        shown = sorted(res['findings'], key=lambda f: (order[f['severity']], f['file'], f['key']))[:a.max]
        for f in shown:
            where = os.path.relpath(f['file'], tmp) if tmp else f['file']
            line = f':{f["line"]}' if f['line'] else ''
            print(f"  {f['severity'][:4].upper()} {f['code']:<20} {where}{line}  {f['key']}  - {f['detail']}")
        if len(res['findings']) > a.max:
            print(f'  ... {len(res["findings"]) - a.max} more (use --output json)')
        if res['unmatched_files']:
            print(f'  note: {len(res["unmatched_files"])} file(s) had no source-locale counterpart: '
                  + ', '.join(res['unmatched_files'][:5]))
    return 4 if errs else (2 if warns else 0)


if __name__ == '__main__':
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
