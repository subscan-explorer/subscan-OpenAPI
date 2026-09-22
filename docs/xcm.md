## Description

XCM API provide multiple APIS to query XCM historical data, including: XCM message(UMP,DMP,HRMP,SnowBridge,S2S Bridge), HRMP channels and statistics.

> **Note**: 
> 1. XCM API is only available for the relaychain(Polkadot, Kusama, Westend, Pasco, Enjin relaychain).
> 2. XCM API is currently only available for paid plans.

## Endpoints

- /api/scan/xcm/list
- /api/scan/xcm/info
- /api/scan/xcm/meta
- /api/scan/xcm/channels
- /api/scan/xcm/channel
- /api/scan/xcm/stat
- /api/scan/xcm/check_hash
- /api/scan/xcm/bridge_stat

## XCM V2 journey API

The V2 shadow API is independent from the legacy XCM renderer. Existing
`/api/scan/xcm/*` routes continue to return the legacy contract and are not
changed by the V2 rollout. V2 reads only the `xcm_v2_*` PostgreSQL read model
and never performs archive RPC during an HTTP request.

- `POST /api/v2/scan/xcm/journey/list` returns bounded journey summaries; it does not
  embed hops.
- `POST /api/v2/scan/xcm/journey/info` accepts `journey_id`, `legacy_unique_id`, or the
  migration alias `unique_id`, and returns one journey with ordered `hops`.
- `POST /api/v2/scan/xcm/journey/check_hash` accepts `hash`/`message_hash` and/or
  `topic_id`, returning the matching V2 journey identities.

V2 responses use explicit `{relay_chain, para_id}` locations for the journey
and every hop. They do not return recursive `child_message`,
`message_relay_chain`, or route-wide inferred para-id fields. Missing source or
destination facts are represented as `null`; `completeness` separately reports
`partial`, `complete`, or `repair_required`.

Journey details expose `cross_chain_status`, bridge metadata backed by actual
lane/nonce or transaction evidence, and `hops[].parent_sequence`. The parent
sequence expresses child/onward relationships without restoring the recursive
legacy `child_message` field. Westend-to-Rococo source-only S2S records only
the Westend execution and bridge handoff. It does not request or fabricate
Rococo facts and therefore remains `relayed`, `partial`, and
`cross_chain_status=2`.

The V2 list supports bounded `row`/`page` pagination and the high-frequency
owner relay, origin/destination para, address, status, protocol, hash, topic,
bridge-type, and `after_id` filters. Unsupported legacy-only filters are not
silently applied. V1 deep links can continue using `legacy_unique_id` while UI
details migrate behind a feature flag.

The V2 routes are a dark-launch contract: they read only the persisted
`xcm_v2_*` model and never call archive RPC in the request path. Enable them
per UI feature flag only after fixture, PostgreSQL, parity, and live-archive
checks pass; a disabled or unavailable V2 path may fall back to the existing
`/api/scan/xcm/*` routes. V2 backfill and comparison are asynchronous bounded
jobs, not request-time double reads. Production V2 fact stages do not read V1
message/result tables; only the asynchronous read-only comparison stage may
load V1 rows, and it cannot write them into V2. Polkadot↔Kusama S2S journeys
are written by the Polkadot owner only.
