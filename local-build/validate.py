"""Validate JSON records against a published building block (JSON Schema, JSON-LD uplift, SHACL).

Validation reads remote files only from the cache (IMPORTS_CACHE, default .imports-cache/); --fetch fills it.
This repo's blocks come from the local build (build-local/, from ./build.sh); --published uses the published register instead.

Usage:
  validate.py --fetch [--published]           download everything to the cache (online)
  validate.py [--published] [-b block] record.json...   validate (offline); block = id or path, e.g. processing-activity
"""
import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit

import jsonschema
import pyshacl
import requests
import yaml
from jsonschema.validators import RefResolver, validator_for
from rdflib import BNode, Graph, Namespace

PUBLISHED = 'https://katkatkateryna.github.io/ospd2026_bblocks-template/build/register.json'
LOCAL_BASE = 'http://localhost:9090/register/'  # --base-url used by build.sh
REGISTER = LOCAL_BASE + 'build-local/register.json'
DEFAULT_BBLOCK = 'lu.rss-hydro.mom.workflow.model-of-models'
SH = Namespace('http://www.w3.org/ns/shacl#')
REPO = Path(__file__).resolve().parent.parent
CACHE = Path(os.environ.get('IMPORTS_CACHE', REPO / '.imports-cache'))
online = False


def fetch(url: str) -> bytes:
    url = urldefrag(url)[0]
    if url.startswith(LOCAL_BASE):
        return (REPO / url[len(LOCAL_BASE):]).read_bytes()
    u = urlsplit(url)
    f = CACHE / u.netloc / (u.path.lstrip('/') or 'index')
    if f.is_dir():
        f = f / 'index'
    if f.is_file():
        return f.read_bytes()
    if not online:
        raise IOError(f'Not cached: {url} (run local-build/fetch-imports.sh)')
    r = requests.get(url, headers={'Accept': 'text/turtle, application/json;q=0.9, */*;q=0.5'}, timeout=60)
    r.raise_for_status()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(r.content)
    return r.content


def load_doc(url: str):
    return yaml.safe_load(fetch(url))


def load_registers() -> dict:
    """All building blocks from the register and its (transitive) imports, by identifier."""
    bblocks, pending, seen = {}, [REGISTER], set()
    while pending:
        url = pending.pop()
        if url in seen:
            continue
        seen.add(url)
        reg = load_doc(url)
        for b in reg.get('bblocks', []):
            bblocks.setdefault(b['itemIdentifier'], b)
        pending.extend(reg.get('imports', []))
    return bblocks


def dependencies(bblocks: dict, bid: str) -> list:
    result, pending = [], [bid]
    while pending:
        i = pending.pop()
        if i in result or i not in bblocks:
            continue
        result.append(i)
        pending.extend(d.removeprefix('bblocks://') for d in bblocks[i].get('dependsOn', []))
    return result


def schema_url(b: dict):
    s = b.get('schema') or {}
    return s.get('application/json') or s.get('application/yaml')


def parse_rdf(url: str) -> Graph:
    data = fetch(url)
    for fmt in ('turtle', 'xml', 'json-ld'):
        try:
            return Graph().parse(data=data, format=fmt, publicID=url)
        except Exception:
            continue
    raise ValueError(f'Cannot parse RDF from {url}')


def inline_context(ctx, base: str):
    """Replace remote context references with their content."""
    if isinstance(ctx, list):
        return [inline_context(c, base) for c in ctx]
    if isinstance(ctx, str):
        url = urljoin(base, ctx)
        return inline_context(load_doc(url).get('@context', {}), url)
    return ctx


def walk_refs(url: str, seen: set):
    """Fetch a schema and every schema it references."""
    url = urldefrag(url)[0]
    if url in seen:
        return
    seen.add(url)
    stack = [load_doc(url)]
    while stack:
        n = stack.pop()
        if isinstance(n, dict):
            if isinstance(n.get('$ref'), str) and not n['$ref'].startswith('#'):
                walk_refs(urljoin(url, n['$ref']), seen)
            stack.extend(n.values())
        elif isinstance(n, list):
            stack.extend(n)


def prefetch():
    bblocks = load_registers()
    local = [i for i, b in bblocks.items() if schema_url(b) and schema_url(b).startswith(REGISTER.rsplit('/build', 1)[0])]
    seen = set()
    for bid in local:
        b = bblocks[bid]
        walk_refs(schema_url(b), seen)
        if b.get('ldContext'):
            inline_context(b['ldContext'], b['ldContext'])
        for files in (b.get('shaclShapes') or {}).values():
            for f in files:
                fetch(f)
        for dep in dependencies(bblocks, bid):
            for src in [bblocks[dep].get('ontology')] + (bblocks[dep].get('shaclClosures') or []):
                if src:
                    fetch(src)
    print(f'Cached files for {len(local)} building blocks in {CACHE}')


def validate(bid: str, files: list) -> bool:
    bblocks = load_registers()
    if bid not in bblocks:
        match = [i for i in bblocks if i.endswith('.' + bid.replace('/', '.'))]
        if len(match) != 1:
            sys.exit(f'Unknown building block {bid}')
        bid = match[0]
    b = bblocks[bid]
    s_url = schema_url(b)
    schema = load_doc(s_url)
    resolver = RefResolver(s_url, schema, handlers={'http': load_doc, 'https': load_doc})
    validator = validator_for(schema)(schema, resolver=resolver)
    context = inline_context(b['ldContext'], b['ldContext']) if b.get('ldContext') else {}
    shapes = {f: parse_rdf(f) for fs in (b.get('shaclShapes') or {}).values() for f in fs}
    closure = Graph()
    for dep in dependencies(bblocks, bid):
        for src in [bblocks[dep].get('ontology')] + (bblocks[dep].get('shaclClosures') or []):
            if src:
                closure += parse_rdf(src)

    all_ok = True
    for fn in files:
        errors = []
        doc = json.loads(Path(fn).read_text())
        err = jsonschema.exceptions.best_match(validator.iter_errors(doc))
        if err:
            errors.append(f'JSON Schema: {err.message} (at /{"/".join(map(str, err.absolute_path))})')
        else:
            if isinstance(doc, list):
                doc = {'@context': context, '@graph': doc}
            else:
                doc = {**doc, '@context': [context] + ([doc['@context']] if '@context' in doc else [])}
            g = Graph().parse(data=json.dumps(doc), format='json-ld')
            for shapes_url, sg in shapes.items():
                conforms, results, _ = pyshacl.Validator(g, shacl_graph=sg, ont_graph=closure,
                                                         options={'advanced': True}).run()
                if not conforms:
                    q = ('PREFIX sh: <http://www.w3.org/ns/shacl#> SELECT ?f ?s ?m WHERE { ?r a sh:ValidationResult ; '
                         'sh:focusNode ?f ; sh:sourceShape ?s . OPTIONAL { ?r sh:resultMessage ?m } }')
                    for f, shape, m in results.query(q):
                        # Report a blank property shape under its named parent shape.
                        parent = sg.value(predicate=SH.property, object=shape) if isinstance(shape, BNode) else None
                        if parent is not None:
                            shape, m = parent, m or sg.value(parent, SH.message)
                        errors.append(f'SHACL {shape}: {f} - {m or "constraint violated"}')
        all_ok &= not errors
        print(('FAIL ' if errors else 'PASS ') + fn)
        for e in errors:
            print('  ' + e)
    return all_ok


def main():
    global online, REGISTER
    p = argparse.ArgumentParser()
    p.add_argument('--fetch', action='store_true')
    p.add_argument('--published', action='store_true')
    p.add_argument('-b', '--bblock', default=DEFAULT_BBLOCK)
    p.add_argument('files', nargs='*')
    a = p.parse_args()
    online = a.fetch
    if a.published:
        REGISTER = PUBLISHED
    if a.fetch:
        prefetch()
        return
    if not a.files:
        p.error('no records given')
    try:
        ok = validate(a.bblock, a.files)
    except (IOError, requests.RequestException) as e:
        print(f'ERROR {e}', file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
