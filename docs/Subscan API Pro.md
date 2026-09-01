
Subscan API PRO is a paid direct-Subscan service for customers who need plan-specific quotas or features. Customers can
still purchase, upgrade, renew, and manage paid plans on the [Subscan API Platform](https://pro.subscan.io/) and create
new direct API keys under those plans. Only new free-key creation has been discontinued on the direct platform; new
free integrations should use a PubFi API key and the PubFi Gateway instead.

PubFi free-route access is a separate product path. A PubFi key, a PubFi `:free` route, and any PubFi Credits are not a
Subscan PRO subscription and should not be described as one.

## Features

- **Higher Quotas**: PRO users can receive higher quotas according to the selected direct plan.
- **Plan-specific Support**: Support levels depend on the selected direct plan, from community support to escalated or
  dedicated support.
- **Additional endpoints**: Plan availability may include additional endpoints; confirm the current plan terms before
  relying on them.


## Upgrade to PRO

1. Review the direct Subscan plans on the [Pricing page](https://pro.subscan.io/pricing).
2. Sign in to the [Subscan API Platform](https://pro.subscan.io/login) and purchase or upgrade the appropriate plan.
3. Create a new direct API key under the paid plan, or manage an existing one, on the
   [API Service page](https://pro.subscan.io/api_service).
4. Send that key in the `X-API-Key` or `x-api-key` header to the network-specific `*.api.subscan.io` host.

The live Pricing and checkout pages are authoritative for quotas, prices, payment methods, discounts, and renewal
terms. The [Getting Started Tutorial](https://support.subscan.io/doc-360177) documents both this direct paid flow and
the separate PubFi free flow.
