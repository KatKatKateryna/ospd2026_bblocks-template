# Offline validation

Validates JSON records against a building block, with no network, using the same checks as the build: JSON Schema, JSON-LD uplift, SHACL rules. Requires Docker. `./build.sh` is unchanged.

## Steps

1. `./build.sh` (online): builds this repo's blocks into `build-local/`.
2. `local-build/fetch-imports.sh [-p]` (online; once, and again when imports change): prepares the cache.
3. `local-build/validate.sh [-p] [-b block] record.json...` (offline, any number of times).
   - Prints PASS/FAIL per record, with the reason; exit 0 all pass, 1 any fail, 2 error.
   - `-b`: block id or path, e.g. `processing-activity`, `ontology/activities`; default `workflow/model-of-models`.

After changing a block, rerun step 1 only; validation reads `build-local/` directly.

## Where files come from

| Files | Default | `-p` |
|---|---|---|
| This repo's blocks (schemas, contexts, `rules.shacl`, `ontology.ttl`) | read from `build-local/` and `_sources/`, never cached | downloaded from the published register, cached |
| Imported public blocks | downloaded once, cached | downloaded once, cached |

`-p` uses the published register (`PUBLISHED` in `validate.py`); prepare and validate with the same mode.

## What `fetch-imports.sh` downloads

Starting from the register (`build-local/register.json`, or the published one with `-p`), only what this repo's blocks need:

- the pinned Docker image;
- imported register indexes (transitively);
- every schema reached through `$ref`;
- SHACL shapes and ontologies inherited from dependencies (e.g. OGC PROV shapes, W3C PROV-O).

Files are saved as `.imports-cache/<host>/<path>` (git-ignored). The cache is replaced only after a complete download.

## Notes

- Validation runs with Docker networking off; a file missing from the cache is an error (exit 2), never a download.
- The Docker image is pinned by digest; override with `BBP_IMAGE`.
