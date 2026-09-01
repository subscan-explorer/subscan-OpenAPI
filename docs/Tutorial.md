# Getting Started

> **Access model update:** Subscan no longer issues new free API keys from the Subscan API Platform. New integrations that need free access should create a PubFi API key and call Subscan through the PubFi Gateway. Do not use the old `pro.subscan.io` free-plan flow described in earlier versions of this page.

This tutorial covers the current PubFi onboarding path for Subscan data. PubFi provides the account-bound API key, the gateway endpoint, and the runtime route policy. The live Registry and Runtime OpenAPI are the authority for the routes and limits that are available at any given time.

## Access paths

| Requirement | Current path |
|-------------|--------------|
| New free access | Create a PubFi account and use a PubFi API key with an eligible `:free` Subscan route. |
| Paid or metered access | Use the PubFi route's current billing policy, which may require account Credits or another supported execution mode. |
| Existing direct Subscan plan | Continue to follow the current Subscan plan and authentication instructions. This page does not create or manage direct Subscan keys. |

PubFi has separate Production and Staging environments. Keep the dashboard, API base URL, API key, and any payment or test network in the same environment.

| Environment | Dashboard | API base URL |
|-------------|-----------|---------------|
| Production | [pubfi.ai/dashboard](https://pubfi.ai/dashboard) | `https://api.pubfi.ai` |
| Staging | [stg.pubfi.ai](https://stg.pubfi.ai) | `https://api-stg.pubfi.ai` |

## 1. Sign in to PubFi

Open the [PubFi sign-in page](https://pubfi.ai/login). Use the email or Google sign-in flow to create or access your PubFi account. After authentication, open the [PubFi Dashboard](https://pubfi.ai/dashboard).

![PubFi sign-in page](https://raw.githubusercontent.com/subscan-explorer/subscan-OpenAPI/main/docs/images/pubfi-login.jpg)

## 2. Create a PubFi API key

1. In the Dashboard, find the **API keys** section.
2. Select **Create key**.
3. Enter a descriptive name, such as `subscan-local-dev`, and submit the form.
4. Copy the complete secret immediately and store it in a secret manager.

The complete secret is displayed only once. Later, the Dashboard shows a shortened preview rather than the full key. API-key management requires an authenticated Dashboard session with Owner or Admin membership.

![PubFi Dashboard API keys section](https://raw.githubusercontent.com/subscan-explorer/subscan-OpenAPI/main/docs/images/pubfi-dashboard-api-keys.jpg)

If the key is lost, revoke it from the Dashboard and create a replacement. Never put a real key in source code, documentation, screenshots, shell history, logs, or a public issue.

## 3. Load the key securely

For a short local test, load the key into an environment variable. Replace the placeholder locally; never commit the resulting value:

```shell
export PUBFI_API_KEY='<copy the PubFi API key here>'
export PUBFI_API_BASE='https://api.pubfi.ai'
```

For Staging, use a Staging key with `https://api-stg.pubfi.ai` and keep it in a separate variable such as `STG_PUBFI_API_KEY`. A key created in one environment is not accepted by the other environment.

## 4. Verify the key and account binding

The following private, read-only request confirms that the key is valid and shows the billing account bound to it. It does not create billing state:

```shell
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${PUBFI_API_KEY}" \
  "${PUBFI_API_BASE}/v1/auth/context"
```

The response has this shape; values are account-specific:

```json
{
  "principal_id": "<stable execution principal>",
  "billing_account_id": "<billing account for this key>",
  "actor_subject_id": null
}
```

PubFi uses the `Authorization: Bearer ...` header for API-key access. The legacy `X-API-Key` header is not a substitute for a PubFi API key.

## 5. Find a current Subscan route

Before calling an endpoint, inspect the current public contracts for the selected environment:

```shell
curl --fail --silent --show-error \
  "${PUBFI_API_BASE}/v1/capabilities" > pubfi-capabilities.json

curl --fail --silent --show-error \
  "${PUBFI_API_BASE}/openapi.json" > pubfi-openapi.json
```

Use the response to find a capability whose `provider_key` is `subscan` and whose readiness status is `ready`. Check the exact HTTP method, path, request policy, and billing mode before making the request.

Do not infer execution from the Subscan Discovery page, an old example, or a saved route. Discovery is useful for source evaluation; the live Registry and Runtime OpenAPI decide whether a route can run. See [PubFi API Key and Runtime](https://docs.pubfi.ai/getting-started/api-key-runtime) for the current runtime contract instead of relying on a screenshot that can become outdated.

## 6. Call Subscan through the PubFi Gateway

PubFi preserves the Subscan API path after adding the gateway prefix. For a network-specific route, the pattern is:

```text
https://api.pubfi.ai/v1/gateway/subscan/<network>/api/<subscan-path>
```

For example, the current Runtime OpenAPI exposes a ready metadata route with a free variant. Verify that it is still present before using it:

```shell
export PUBFI_GATEWAY_PATH='/v1/gateway/subscan/polkadot/api/scan/metadata:free'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Authorization: Bearer ${PUBFI_API_KEY}" \
  "${PUBFI_API_BASE}${PUBFI_GATEWAY_PATH}"
```

The `:free` suffix is not a general switch. Append it only when the matching capability advertises `free_rate_limit` or the matching OpenAPI operation contains `x-pubfi-free-variant`. A free route still requires the normal PubFi Bearer key; it is not anonymous and it is not an x402 request.

For a route that does not advertise a free variant, use the exact path and method from the current contract and follow its billing policy. Remove `:free` only when the normal route is ready and the account has the required allocation or Credits.

### Mapping a direct Subscan URL

The gateway mapping keeps the original Subscan network and API path, but changes the host and authentication header:

```text
Direct Subscan:
https://polkadot.api.subscan.io/api/scan/metadata

PubFi Gateway:
https://api.pubfi.ai/v1/gateway/subscan/polkadot/api/scan/metadata[:free]
```

The example illustrates the mapping only. The live Registry remains authoritative for whether this route, method, network, body, and free variant are currently available.

### Free-route limits

Free-route limits are controlled by PubFi and may be scoped to a provider or route. Read the current `free_rate_limit` object instead of carrying forward the old Subscan “5 req/s” statement. A free request does not consume Credits, but it can still be rejected by the account-level request window, concurrency limit, or quota. On `429`, honor `Retry-After` when it is present and inspect the response code before retrying.

## 7. Manage and rotate keys

Use the **Edit** and **Revoke** actions in the Dashboard to manage a key. Revocation is irreversible for that key. If a key may have been exposed, revoke it immediately, create a replacement, update the secret store, and restart clients that use the old value.

## Troubleshooting

| Status | Meaning in the PubFi flow | Next step |
|--------|---------------------------|-----------|
| `401` | The PubFi key is missing, invalid, or belongs to another environment. | Check the Bearer header, secret, and API base URL. |
| `402` | The selected route requires a billing or admission action. | Inspect the current billing mode and account allocation. |
| `403` | The account is not authorized for the selected route. | Recheck route readiness and account membership. |
| `404` | No active Registry route matches the method and path. | Fetch the current Registry and use an exact ready path. |
| `429` | A free-route, concurrency, or other rate limit was reached. | Honor `Retry-After` and the current limit/quota policy. |
| `503`/`504` | Registry, credential, health, or upstream availability/timeout issue. | Retry with backoff after checking the current runtime status. |

## Further reading

- [PubFi Quickstart](https://docs.pubfi.ai/getting-started/quickstart)
- [PubFi API Key and Runtime](https://docs.pubfi.ai/getting-started/api-key-runtime)
- [PubFi live Registry](https://api.pubfi.ai/v1/capabilities)
- [PubFi Runtime OpenAPI](https://api.pubfi.ai/openapi.json)
- [Subscan API on PubFi Discovery](https://pubfi.ai/discovery/api/subscan)
- [Subscan API Introduction](https://support.subscan.io/doc-361776)
