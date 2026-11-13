# API documentation maintenance

`network.json` is the supported direct API inventory. Keep `api_domains` and
`ui_domains` distinct: their subdomains can refer to different chain generations.
For example, the Creditcoin 3 explorer uses `creditcoin.subscan.io`, while its
API uses `creditcoin3.api.subscan.io`. `network_docs.py` supplies the same API host list
to the endpoint table and Apidog environment generators, excluding legacy aliases.

When updating supported networks:

1. Compare the inventory with the [public network list](https://polkadot.subscan.io/api/networks)
   and deployment configuration. The current UI list omits some independently
   served APIs, so absence alone does not establish retirement.
2. Check uncertain hosts with an authenticated `POST /api/scan/metadata` request.
   Follow `.codex/skills/read-subscan-live-data/SKILL.md`; do not store keys or
   credential-bearing responses in documentation. Do not infer retirement from a
   timeout, a rate limit, or one failed request alone.
3. Remove retired network entries from `network.json`. Keep supported historical
   APIs and set `is_archive: true` when indexing has stopped, including testnets.
4. Regenerate from the repository root (the scripts also work from other directories):

   ```bash
   python3 docs/api/gen-api-endpoint.py --write
   python3 docs/api/doc-env-tools.py
   python3 docs/api/gen-doc.py
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/api -p 'test_network_docs.py' -v
   git diff --check
   ```

`gen-api-endpoint.py` without `--write` only prints the table. Regeneration is
repeatable and replaces only the marked table in `Introduction.md`.
`gen-doc.py` updates the Markdown embedded in `subscan.apidog.json`; review its
diff for unrelated changes. No Swagger regeneration is needed for an inventory
change that leaves API operations and schemas unchanged.

## Generate and validate the complete documentation bundle

Use `make doc` after changing existing API annotations or supported networks.
It regenerates Swagger, the endpoint table, environments, embedded Markdown,
`apidog.openapi.json`, and `search-index.json`. The first run installs the pinned
documentation-only Node dependencies with `npm ci --ignore-scripts`.

```bash
source ~/.gvm/scripts/gvm
gvm use go1.25.3
make doc
npm --prefix docs/api test
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/api -p 'test_network_docs.py' -v
git diff --check
```

`swagger.json` remains generated from Go annotations. The derived OpenAPI 3.0.3
artifact uses the established `swagger2openapi` converter and validates internal
references offline. It adds named request/response examples and imports the
supported API hosts as servers, with Polkadot first. Credentials have no default
value; the reader supplies their own direct Subscan API key.

`public-routes.json` maps the existing public site URLs to method/path identities.
Only these operations enter the derived import and search index. Adding a Go
annotation does not authorize publishing a new endpoint: review public scope and
record its verified documentation URL separately before adding it to this map.
`examples.json` contains bounded public API captures and their request bodies;
refresh an example only after checking the real response and preserving secrets.

## Publish without an additional paid service

The existing `.github/workflows/docs-pro.yaml` mirrors `docs/api` from `master`
to the public `subscan-explorer/subscan-OpenAPI` repository. Reuse this workflow;
do not create a second independent copy of documentation sources.

In the existing Apidog project:

1. API definitions are imported by `.github/workflows/docs-pro.yaml` after a
   `master` documentation update, following the existing public repository mirror.
   The workflow sends the checked-out `apidog.openapi.json` directly to Apidog
   project `384478`, using the repository Actions secret `APIDOG_ACCESS_TOKEN`.
   The token's account must have import/edit access; renew the secret before its
   configured expiry. The request uses API version `2024-03-28`, the default module
   and main branch, automatic merge for endpoints/schemas, preserves endpoint
   folders, and keeps resources absent from the artifact. Confirm curated fields
   survive the first import; automatic merge is not a guarantee for every field.
   Keep the Markdown source bound to `docs/subscan.apidog.json`: this OpenAPI API
   integration does not replace Markdown import or site settings.
2. Publish only supported environments, with Polkadot first. The derived import
   includes all hosts; `environments.json` is also available for a native import.
   Native environment import appends entries, including duplicate names. For an
   existing project, import only missing environments and keep one published
   entry per supported host; do not repeatedly import the entire inventory.
   Unpublishing retired entries does not require deleting internal environments.
3. Keep Copy Page and llms.txt enabled, and enable the public documentation MCP.
4. Use `landing.html` as the custom homepage. Paste `site-search.css` and
   `site-search.js` into the site's Custom CSS and JavaScript settings, preserving
   other existing customization. The script fetches the mirrored public index
   only when a reader searches; matching stays in the browser and sends no
   query text, API credentials, or analytics to a third party.

The search shortcut is Ctrl/Cmd + Shift + K. Native name/path search remains
available if full-text search cannot load. The static index needs no Algolia
account, AI provider, or subscription. Ask AI and other usage-billed services
are intentionally left disabled.

After merging the workflow, check the first Actions run and Apidog import history,
then verify the public site before disabling only the old **API** scheduled source.
Keep the Markdown source enabled until its replacement is implemented. Local Client
scheduled imports require the Apidog project to remain open; unattended Markdown
sync is still unverified. No old Apidog schedule is disabled by this workflow.

The import fails on HTTP errors, invalid responses, or nonzero failure counters,
including partial failures returned with HTTP 200. A 120-second request timeout
bounds the call. It does not automatically retry writes after ambiguous failures;
inspect Apidog history first, then manually run the `docs` workflow on `master`.
Manual runs on other branches validate only by default. To explicitly test a
branch against the live project, dispatch with `test_import=true`; this writes
real Apidog data but does not mirror the branch into the public repository.
Production and test imports share a project-level concurrency lock. PRs run
validation without the token. Workflow runs are serialized per branch without cancelling an
in-flight import. The existing Slack failure notification remains in place.

Validate the integration without credentials or external writes:

```bash
node --test .github/scripts/apidog/import.test.cjs
npm --prefix docs/api ci --ignore-scripts
npm --prefix docs/api test
```

API reference: https://openapi.apidog.io/api-7312738

Repository updates, source import, and publication are separate checks. Verify
the public MCP button, credential input, named examples, default network,
homepage links, and an `X-API-Key` full-text search after saving site settings.
