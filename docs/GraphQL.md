Subscan exposes a public GraphQL endpoint at `POST https://$NETWORK_NAME.api.subscan.io/graphql`.

The GraphQL API is a **read-only beta** surface that complements the existing REST API. It is intended for
composition queries where clients need to fetch related block, extrinsic, event, transfer, and account data in a
single request. REST remains the recommended default for standard fixed-shape integrations and high-frequency polling.

## Authentication

All GraphQL requests must be authenticated with the same API key model as the REST API.

- Send your key in the `X-API-Key` header.
- During beta, GraphQL access is available only to GraphQL-enabled API keys.
- Requests made with a key that is not allowed to use GraphQL return a GraphQL error with code `GRAPHQL_DISABLED_FOR_KEY`.

## Endpoint and Request Format

- Method: `POST`
- Path: `/graphql`
- Content-Type: `application/json`
- Body fields:
  - `query`: required GraphQL document string
  - `variables`: optional JSON object
  - `operationName`: optional operation name when the document contains multiple operations

Example:

```shell
curl -X POST "https://polkadot.api.subscan.io/graphql" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "query": "query Ping { ping }"
  }'
```

Example response:

```json
{
  "data": {
    "ping": "pong"
  },
  "extensions": {
    "requestId": "9a4d1c8e-8b8b-4db0-9b1e-7a4a6b37db50"
  }
}
```

## Using with Apidog

Subscan supports two complementary workflows in Apidog:

- Import the OpenAPI spec to get a runnable `POST /graphql` request with the correct header and JSON payload shape.
- Create a dedicated GraphQL request in Apidog, point it at the same `/graphql` endpoint, and click `Fetch Schema` to enable autocomplete and schema browsing.

For GraphQL-enabled API keys, schema introspection is enabled by default. The standard schema-fetch query used by Apidog is also allowed even though normal application queries remain subject to the public depth and complexity limits below.

## Supported Root Queries

| Query                                                             | Description                                                                               |
|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `ping`                                                            | Liveness check that returns `"pong"`.                                                     |
| `block(number: Int, hash: String)`                                | Returns one block by height or hash. Exactly one of `number` or `hash` must be provided.  |
| `account(address: String!)`                                       | Returns account balance and display data for the given address, or `null` when not found. |
| `event(index: String!)`                                           | Returns one event by canonical `blockNum-eventIdx` index.                                 |
| `extrinsic(hash: String!)`                                        | Returns one extrinsic by hash, or `null` when not found.                                  |
| `transfer(hash: String!, eventIndex: Int!)`                       | Returns one transfer event under an extrinsic hash, or `null` when not found.             |
| `transfers(account: String!, first: Int = 20, after: String)`     | Returns a paginated transfer connection for an account.                                   |
| `tokenHoldings(account: String!, first: Int = 20, after: String)` | Returns a paginated token-holdings connection for an account.                             |

## Pagination

`transfers` and `tokenHoldings` use cursor pagination and return a connection object with:

- `nodes`: the current page of results
- `pageInfo.hasNextPage`: whether another page is available
- `pageInfo.nextCursor`: the opaque cursor to pass back as `after`

Pagination rules:

- `first` defaults to `20`
- `first` must be between `1` and `100`
- `after` must be the opaque cursor returned by the previous page
- cursors are opaque and must not be parsed or constructed by clients

Example:

```json
{
  "query": "query Transfers($account: String!, $first: Int!, $after: String) { transfers(account: $account, first: $first, after: $after) { nodes { hash eventIndex amount symbol from { address } to { address } } pageInfo { hasNextPage nextCursor } } }",
  "variables": {
    "account": "14Qqoo5Qm3m4NQj2aL9e8JmA6wTz2F9qk4jv8D4hQwFZk9yP",
    "first": 20,
    "after": null
  }
}
```

## Query Limits and Beta Notes

The GraphQL API is intentionally constrained during beta:

- read-only queries only; mutations are not supported
- schema introspection is enabled by default for GraphQL-enabled API keys so API tooling can fetch the schema
- maximum query depth: `10`
- maximum alias count: `20`
- maximum query complexity: `500`

When a query exceeds platform limits, Subscan returns GraphQL errors with stable codes such as:

- `INVALID_ARGUMENT`
- `INVALID_CURSOR`
- `PAGINATION_LIMIT_EXCEEDED`
- `QUERY_ALIAS_EXCEEDED`
- `QUERY_DEPTH_EXCEEDED`
- `QUERY_COMPLEXITY_EXCEEDED`
- `GRAPHQL_DISABLED_FOR_KEY`

## Error Format and Request Tracing

GraphQL responses follow standard GraphQL response conventions:

- successful requests return a `data` object
- input and execution problems return an `errors` array
- every response includes `extensions.requestId`
- every HTTP response also includes the `X-Request-Id` header

Example error response:

```json
{
  "errors": [
    {
      "message": "`first` value 500 must be between 1 and 100",
      "extensions": {
        "code": "PAGINATION_LIMIT_EXCEEDED"
      }
    }
  ],
  "extensions": {
    "requestId": "d650a0a4-f0e0-4ccb-8a24-8cc9bfe9c8a0"
  }
}
```

## Quick Example

```shell
curl -X POST "https://polkadot.api.subscan.io/graphql" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "query": "query Account($address: String!) { account(address: $address) { address display nativeBalance nativeSymbol } }",
    "variables": {
      "address": "14Qqoo5Qm3m4NQj2aL9e8JmA6wTz2F9qk4jv8D4hQwFZk9yP"
    }
  }'
```
