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

## Existing ES-backed list

`POST /api/v2/scan/xcm/list` continues to serve the existing XCM message and
statistics contract from the legacy index. The `/api/v2` URL version does not
refer to the retired independent Journey indexer.

The independent Journey API and its feature flags have been removed. The
`/api/scan/xcm/*` endpoints listed above remain available.
