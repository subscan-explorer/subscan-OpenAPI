## Authentication

There are two separate access paths:

- **Direct Subscan API:** Existing direct plans use the `X-API-Key` or `x-api-key` request header. Subscan no longer
  issues new free keys through the direct API platform.
- **PubFi Gateway:** New free access uses a PubFi API key with the `Authorization: Bearer <PubFi API key>` header.
  The gateway base URL is `https://api.pubfi.ai` in Production or `https://api-stg.pubfi.ai` in Staging.

Do not send a direct Subscan `X-API-Key` as a replacement for a PubFi Bearer key. See the
[Tutorial](https://support.subscan.io/doc-360177) for the PubFi onboarding and gateway path mapping.

## Direct Subscan Rate Limiting

Direct Subscan quotas depend on the current direct plan. Do not copy a historical quota into a new integration, and do
not rely on anonymous fallback access as a free onboarding path.

For a direct key with a quota of *10* requests per second, the quota is shared across the APIs and networks covered by
that key. For example:

- Client *A* requests `https://polkadot.api.subscan.io/api/now` with an API key;
- Simultaneously, client *B* requests `https://kusama.api.subscan.io/api/scan/metadata` with the same API key.
- After these *2* requests, only *8* requests with the same API key are allowed in that second.

Subscan API may return the Internet-Draft [RateLimit Header Fields for HTTP](https://tools.ietf.org/html/draft-polli-ratelimit-headers-01).
Through the response headers, clients can read the limit (`ratelimit-limit`), remaining quota
(`ratelimit-remaining`), and seconds until reset (`ratelimit-reset`) for a direct key. For example:

<div class="center-column"></div>

```shell
curl -isS -X POST -H "x-api-key: YOUR_KEY" https://kusama.api.subscan.io/api/now
```

An example of partial response headers:

<div class="center-column"></div>

```
ratelimit-remaining: 7
ratelimit-limit: 10
ratelimit-reset: 22
```

If a direct client reaches its rate limit, requests in the time slot may be throttled with an HTTP `429 Too Many
Requests` response that contains a [`retry-after` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After).

An example of partial response headers:

<div class="center-column"></div>

```
retry-after: 4
ratelimit-remaining: 0
ratelimit-limit: 10
ratelimit-reset: 4
```

An example of response body:

<div class="center-column"></div>

```json
{
  "message":"API rate limit exceeded"
}
```

<aside class="notice">
It is highly recommended to build your client with a backoff strategy to wait for <code>"retry-after"</code> seconds when hitting rate limits.
</aside>

## PubFi Free-Route Rate Limiting

PubFi free routes are separate from direct Subscan quotas. The live Registry advertises an eligible free route through
`free_rate_limit`; Runtime OpenAPI represents the same contract with `x-pubfi-free-variant`. Only append `:free` to
the exact gateway path when that contract is present. A free route still requires a PubFi Bearer key, is not anonymous,
and does not consume Credits. Limits and quota are runtime data, so clients should honor `Retry-After` on `429` and
avoid hard-coding the old Subscan free-plan values.

## HTTP Status Codes

The table below lists common status codes returned by the direct Subscan API or the PubFi Gateway. The exact response
body and error code depend on the selected access path.

| Code                      | Meaning                                                                                                                                         |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 OK                    | The request was handled without any error.                                                                                                      |
| 401 Unauthorized          | The credentials is either not found or invalid. Please refer to the `message` field in the JSON response for more detail.                       |
| 402 Payment Required      | The selected route requires a billing or admission action.                                                                                     |
| 404 Not Found             | The HTTP method or request URI was most likely wrong.                                                                                           |
| 429 Too Many Requests     | The direct or PubFi route limit was reached. Honor `retry-after` when present and recheck the applicable runtime policy.                         |
| 500 Internal Server Error | The servers could not respond your request due to an internal error. Find more information on our [status page](https://subscan.statuspage.io). |
| 502 Bad Gateway           | The servers could not respond your request due to an internal error. Find more information on our [status page](https://subscan.statuspage.io). |
| 503 Service Unavailable   | The Registry, credentials, health authority, or upstream service is unavailable.                                                                |
| 504 Gateway Timeout       | The servers could not respond your request due to an internal error. Find more information on our [status page](https://subscan.statuspage.io). |
