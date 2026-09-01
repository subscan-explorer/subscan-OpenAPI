# Getting Started

Subscan supports two separate onboarding paths:

- **Free access through PubFi:** create a PubFi API key and call an eligible Subscan route through the PubFi Gateway.
- **Direct paid access through Subscan:** purchase or upgrade a plan on the Subscan API Platform, create a new direct
  Subscan API key under that plan, and call the network-specific Subscan API host.

Subscan no longer issues new free API keys from the Subscan API Platform, but the direct platform remains the supported
place to purchase, upgrade, renew, and manage paid Subscan plans and to create new direct API keys under those plans.
PubFi credentials and direct Subscan credentials are not interchangeable.

## Choose an access path

| Requirement | Access path |
|-------------|-------------|
| New free access | Create a PubFi account and use a PubFi API key with an eligible `:free` Subscan route. |
| Direct Subscan paid access | Purchase a plan on the [Subscan Pricing page](https://pro.subscan.io/pricing), then create a new direct API key and manage it on the [API Service page](https://pro.subscan.io/api_service). |
| Upgrade or renew an existing direct plan | Use the plan, subscription, and renewal controls on the Subscan API Platform. |
| PubFi metered access | Follow the selected PubFi route's current billing policy. |

## Free access through PubFi

This section uses the PubFi production Dashboard and API base URL:

- Dashboard: [pubfi.ai/dashboard](https://pubfi.ai/dashboard)
- API base URL: `https://api.pubfi.ai`

The live Registry and Runtime OpenAPI are the authority for the routes and limits that are available at any given time.

### 1. Sign in to PubFi

Open the [PubFi sign-in page](https://pubfi.ai/login). Use the email or Google sign-in flow to create or access your
PubFi account. After authentication, open the [PubFi Dashboard](https://pubfi.ai/dashboard).

![PubFi sign-in page](https://raw.githubusercontent.com/subscan-explorer/subscan-OpenAPI/main/docs/images/pubfi-login.jpg)

### 2. Create a PubFi API key

1. In the Dashboard, find the **API keys** section.
2. Select **Create key**.
3. Enter a descriptive name, such as `subscan-local-dev`, and submit the form.
4. Copy the complete secret immediately and store it in a secret manager.

The complete secret is displayed only once. Later, the Dashboard shows a shortened preview rather than the full key.
API-key management requires an authenticated Dashboard session with Owner or Admin membership.

![PubFi Dashboard API keys section](https://raw.githubusercontent.com/subscan-explorer/subscan-OpenAPI/main/docs/images/pubfi-dashboard-api-keys.jpg)

If the key is lost, revoke it from the Dashboard and create a replacement. Never put a real key in source code,
documentation, screenshots, shell history, logs, or a public issue.

### 3. Load the PubFi key securely

For a short local test, load the key into an environment variable. Replace the placeholder locally; never commit the
resulting value:

```shell
export PUBFI_API_KEY='<copy the PubFi API key here>'
export PUBFI_API_BASE='https://api.pubfi.ai'
```

### 4. Verify the key and account binding

The following private, read-only request confirms that the key is valid and shows the billing account bound to it. It
does not create billing state:

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

PubFi uses the `Authorization: Bearer ...` header for API-key access. The direct Subscan `X-API-Key` header is not a
substitute for a PubFi API key.

### 5. Find a current Subscan route

Before calling an endpoint, inspect the current public contracts:

```shell
curl --fail --silent --show-error \
  "${PUBFI_API_BASE}/v1/capabilities" > pubfi-capabilities.json

curl --fail --silent --show-error \
  "${PUBFI_API_BASE}/openapi.json" > pubfi-openapi.json
```

Use the response to find a capability whose `provider_key` is `subscan` and whose readiness status is `ready`. Check
the exact HTTP method, path, request policy, and billing mode before making the request.

Do not infer execution from the Subscan Discovery page, an old example, or a saved route. Discovery is useful for
source evaluation; the live Registry and Runtime OpenAPI decide whether a route can run. See
[PubFi API Key and Runtime](https://docs.pubfi.ai/getting-started/api-key-runtime) for the current runtime contract
instead of relying on a screenshot that can become outdated.

### 6. Call Subscan through the PubFi Gateway

PubFi preserves the Subscan API path after adding the gateway prefix. For a network-specific route, the pattern is:

```text
https://api.pubfi.ai/v1/gateway/subscan/<network>/api/<subscan-path>
```

For example, the current Runtime OpenAPI exposes a ready metadata route with a free variant. Verify that it is still
present before using it:

```shell
export PUBFI_GATEWAY_PATH='/v1/gateway/subscan/polkadot/api/scan/metadata:free'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "Authorization: Bearer ${PUBFI_API_KEY}" \
  "${PUBFI_API_BASE}${PUBFI_GATEWAY_PATH}"
```

The `:free` suffix is not a general switch. Append it only when the matching capability advertises `free_rate_limit`
or the matching OpenAPI operation contains `x-pubfi-free-variant`. A free route still requires the normal PubFi Bearer
key; it is not anonymous and it is not an x402 request.

For a route that does not advertise a free variant, use the exact path and method from the current contract and follow
its billing policy. Remove `:free` only when the normal route is ready and the account has the required allocation or
Credits.

#### Mapping a direct Subscan URL

The gateway mapping keeps the original Subscan network and API path, but changes the host and authentication header:

```text
Direct Subscan:
https://polkadot.api.subscan.io/api/scan/metadata

PubFi Gateway:
https://api.pubfi.ai/v1/gateway/subscan/polkadot/api/scan/metadata[:free]
```

The example illustrates the mapping only. The live Registry remains authoritative for whether this route, method,
network, body, and free variant are currently available.

#### Free-route limits

Free-route limits are controlled by PubFi and may be scoped to a provider or route. Read the current
`free_rate_limit` object instead of carrying forward the old Subscan free-plan limit. A free request does not consume
Credits, but it can still be rejected by the account-level request window, concurrency limit, or quota. On `429`,
honor `Retry-After` when it is present and inspect the response code before retrying.

### 7. Manage and rotate PubFi keys

Use the **Edit** and **Revoke** actions in the Dashboard to manage a key. Revocation is irreversible for that key. If a
key may have been exposed, revoke it immediately, create a replacement, update the secret store, and restart clients
that use the old value.

### PubFi troubleshooting

| Status | Meaning in the PubFi flow | Next step |
|--------|---------------------------|-----------|
| `401` | The PubFi key is missing or invalid. | Check the Bearer header and secret. |
| `402` | The selected route requires a billing or admission action. | Inspect the current billing mode and account allocation. |
| `403` | The account is not authorized for the selected route. | Recheck route readiness and account membership. |
| `404` | No active Registry route matches the method and path. | Fetch the current Registry and use an exact ready path. |
| `429` | A free-route, concurrency, or other rate limit was reached. | Honor `Retry-After` and the current limit/quota policy. |
| `503`/`504` | Registry, credential, health, or upstream availability/timeout issue. | Retry with backoff after checking the current runtime status. |

## Direct paid access through Subscan

Use this path when you need to purchase a direct Subscan plan, increase the quota of an existing direct plan, or keep
calling network-specific `*.api.subscan.io` hosts with a direct Subscan API key.

### 1. Sign in to the Subscan API Platform

Open the [Subscan API Platform](https://pro.subscan.io/login), sign in, or create an account and complete email
verification when required.

![Subscan API Platform sign-in](https://api.apidog.com/api/v1/projects/384478/resources/338719/image-preview)

### 2. Purchase or upgrade a paid plan

Review the current plans on the [Subscan Pricing page](https://pro.subscan.io/pricing). Select the plan that matches
your request quota, API-key count, page-size, history, support, and SLA requirements. The direct Developer, Advanced,
Professional, and Enterprise plan paths remain available independently of PubFi.

The Pricing page currently lists Fiat (USD) and Crypto (DOT) payment options and an annual-payment discount. Treat the
live Pricing and checkout pages as authoritative because plan names, quotas, prices, payment options, and discounts may
change.

![Subscan plan payment options](https://api.apidog.com/api/v1/projects/384478/resources/338524/image-preview)

Existing customers can use the platform's upgrade controls to move to an eligible higher plan.

![Upgrade a direct Subscan plan](https://api.apidog.com/api/v1/projects/384478/resources/338525/image-preview)

Enterprise customers should use the contact option shown on the Pricing page for custom requirements.

### 3. Create and manage a direct Subscan API key

After the paid plan is active, open the [API Service page](https://pro.subscan.io/api_service) to create a new direct
API key under that plan and review its plan and status.

![Create a direct Subscan API key](https://api.apidog.com/api/v1/projects/384478/resources/338522/image-preview)

Store the complete secret in a secret manager. If a key is no longer needed or may have been exposed, revoke it from
the API Service page. Revocation is irreversible for that key.

![Revoke a direct Subscan API key](https://api.apidog.com/api/v1/projects/384478/resources/338523/image-preview)

### 4. Call the direct Subscan API

Direct Subscan API requests use the network-specific host and the `X-API-Key` or `x-api-key` header:

```shell
export SUBSCAN_API_KEY='<copy the direct Subscan API key here>'

curl --fail-with-body --silent --show-error \
  --request POST \
  --header "X-API-Key: ${SUBSCAN_API_KEY}" \
  'https://polkadot.api.subscan.io/api/scan/metadata'
```

The direct key's quota and endpoint access follow its active Subscan plan. Do not use a PubFi Bearer key on a direct
Subscan API host.

### 5. Manage subscription and renewal

Use the Subscan API Platform to manage the paid plan's subscription and renewal. The controls available to an account
depend on its current plan and payment method; use the live platform and checkout terms as the authority.

![Manage a direct Subscan subscription](https://api.apidog.com/api/v1/projects/384478/resources/338526/image-preview)

![Renew a direct Subscan plan](https://api.apidog.com/api/v1/projects/384478/resources/338527/image-preview)

## Further reading

- [Subscan API Pricing](https://pro.subscan.io/pricing)
- [Subscan API Service](https://pro.subscan.io/api_service)
- [Subscan API PRO](https://support.subscan.io/doc-735188)
- [PubFi Quickstart](https://docs.pubfi.ai/getting-started/quickstart)
- [PubFi API Key and Runtime](https://docs.pubfi.ai/getting-started/api-key-runtime)
- [PubFi live Registry](https://api.pubfi.ai/v1/capabilities)
- [PubFi Runtime OpenAPI](https://api.pubfi.ai/openapi.json)
- [Subscan API on PubFi Discovery](https://pubfi.ai/discovery/api/subscan)
- [Subscan API Introduction](https://support.subscan.io/doc-361776)
