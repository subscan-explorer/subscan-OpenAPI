With Subscan API, we provide a simple way to access the chain data of more than 90 substrate-based networks.

If you have any question or suggestion, please do not hesitate to contact our API support
via [api@subscan.io](mailto:api@subscan.io).

The documentation was created with [apidog](https://apidog.com).

## Access and API Keys

Subscan no longer issues new free API keys from the Subscan API Platform. New integrations that need free access should
create a [PubFi](https://pubfi.ai/) account, create a PubFi API key in the [PubFi Dashboard](https://pubfi.ai/dashboard),
and call Subscan through the PubFi Gateway. See the [Tutorial](https://support.subscan.io/doc-360177) for the complete
onboarding and request flow.

PubFi API-key requests use `Authorization: Bearer <PubFi API key>` and the PubFi gateway base URL. The old direct
Subscan `X-API-Key` flow is not the free onboarding path described here. Existing direct Subscan customers should use
the authentication and plan instructions that apply to their current direct plan.

### Data for AI Agents

Subscan data is also available through [PubFi](https://pubfi.ai/), a preferred data infrastructure
layer for AI agents. PubFi aggregates data discovery, intelligent refinement, and machine-native settlement to build a
new agent data supply chain for Web3 applications.

With PubFi, users can access Subscan-powered on-chain data through an account-bound API key, eligible free route
variants, usage-based pricing, and x402 payments. The live PubFi Registry and Runtime OpenAPI determine which Subscan
routes, methods, networks, and free variants are available at request time.

- To learn more about [PubFi](https://pubfi.ai/), visit [here](https://pubfi.ai/).
- To start using Subscan data through PubFi, see the [Subscan API on PubFi](https://pubfi.ai/discovery/api/subscan).


## Service Status

The service status of Subscan API can be found on our [status page](https://subscan.statuspage.io).

## Service Level Agreement

Subscan provides our customers the Service Level Agreement (SLA), which includes **Monthly Uptime Percentage**
commitment for multiple networks. Please contact us ([api@subscan.io](mailto:api@subscan.io)) for more information.

## API Endpoints

Please notice before you get started:

1. The following endpoints list is maintained manually and it might be outdated. In fact, every individual network
   supported on Subscan.io will have available API endpoint as well. The endpoint naming convention
   is `https://$NETWORK_NAME.api.subscan.io` where the `$NETWORK_NAME` is the same as the subdomain of the corresponding
   network on Subscan.io.

2. All the endpoints are forced to HTTPS only. Please make sure you use `https://` with the API hosts.

3. SLA covered endpoints are shown on our [service status page](https://subscan.statuspage.io/). Several networks are
   excluded from our SLA for now. It might because: 1) the network is a testnet, not as stable as a mainnet, or could be
   reset in a relatively higher chance; 2) the chain RPC that Subscan relied on is maintained by others (e.g. the chain
   developers). We may update the covered list in the future. Please let us know if you want to have other networks
   included in the SLA.

4. The **Status** marked as **live** is production network, and it will be maintained continuously. The **Status**
   marked as **test** is test network, which may be unstable. Some new features of Subscan will be updated on testnet
   first.

5. All APIs documented here are specifically designed for Subscan UI. While they may undergo frequent updates,
   we strictly avoid introducing breaking changes. In the rare event of a mandatory breaking change, we will issue
   advance email notifications to all subscribers.

| Network              | API Host                                       | Status  |
|----------------------|------------------------------------------------|---------|
| Altair               | `altair.api.subscan.io`                        | archive |
| Assethub-kusama      | `assethub-kusama.api.subscan.io`               | live    |
| Assethub-paseo       | `assethub-paseo.api.subscan.io`                | test    |
| Assethub-polkadot    | `assethub-polkadot.api.subscan.io`             | live    |
| Assethub-westend     | `assethub-westend.api.subscan.io`              | test    |
| Astar                | `astar.api.subscan.io`                         | live    |
| Autonomys            | `autonomys.api.subscan.io`                     | live    |
| Autonomys-chronos    | `autonomys-chronos.api.subscan.io`             | test    |
| Avail                | `avail.api.subscan.io`                         | live    |
| Avail-turing         | `avail-turing.api.subscan.io`                  | test    |
| Bifrost-polkadot     | `bifrost.api.subscan.io`                       | live    |
| Bridgehub-kusama     | `bridgehub-kusama.api.subscan.io`              | live    |
| Bridgehub-polkadot   | `bridgehub-polkadot.api.subscan.io`            | live    |
| Bridgehub-westend    | `bridgehub-westend.api.subscan.io`             | test    |
| Centrifuge           | `centrifuge-standalone-history.api.subscan.io` | archive |
| Centrifuge-parachain | `centrifuge.api.subscan.io`                    | archive |
| Collectives-polkadot | `collectives-polkadot.api.subscan.io`          | live    |
| Coretime-kusama      | `coretime-kusama.api.subscan.io`               | live    |
| Coretime-polkadot    | `coretime-polkadot.api.subscan.io`             | live    |
| Coretime-westend     | `coretime-westend.api.subscan.io`              | test    |
| Creditcoin           | `cc-enterprise.api.subscan.io`                 | live    |
| Creditcoin-cc3       | `creditcoin.api.subscan.io`                    | live    |
| Creditcoin-cc3-test  | `creditcoin3-testnet.api.subscan.io`           | test    |
| Creditcoin-dev       | `creditcoin3-dev.api.subscan.io`               | test    |
| Crust                | `crust.api.subscan.io`                         | live    |
| Crust-parachain      | `crust-parachain.api.subscan.io`               | archive |
| Darwinia             | `darwinia.api.subscan.io`                      | live    |
| Energywebx           | `energywebx.api.subscan.io`                    | live    |
| Energywebx-testnet   | `energywebx-testnet.api.subscan.io`            | test    |
| Enjin-canary-matrix  | `canary-matrix.api.subscan.io`                 | test    |
| Enjin-canary-relay   | `canary.api.subscan.io`                        | test    |
| Enjin-matrix         | `matrix.api.subscan.io`                        | live    |
| Enjin-relay          | `enjin.api.subscan.io`                         | live    |
| Humanode             | `humanode.api.subscan.io`                      | live    |
| Kusama               | `kusama.api.subscan.io`                        | live    |
| Manta                | `manta.api.subscan.io`                         | archive |
| Midnight             | `midnight.api.subscan.io`                      | live    |
| Midnight-preview     | `midnight-preview.api.subscan.io`              | test    |
| Midnight-preprod     | `midnight-preprod.api.subscan.io`              | test    |
| Moonbase             | `moonbase.api.subscan.io`                      | archive |
| Moonbeam             | `moonbeam.api.subscan.io`                      | archive |
| Moonriver            | `moonriver.api.subscan.io`                     | archive |
| Mythos               | `mythos.api.subscan.io`                        | live    |
| Neuroweb             | `neuroweb.api.subscan.io`                      | live    |
| Neuroweb-testnet     | `neuroweb-testnet.api.subscan.io`              | archive |
| Paseo                | `paseo.api.subscan.io`                         | test    |
| Peaq-testnet         | `agung-testnet.api.subscan.io`                 | test    |
| Peaq-main            | `peaq.api.subscan.io`                          | live    |
| Pendulum             | `pendulum.api.subscan.io`                      | live    |
| People-kusama        | `people-kusama.api.subscan.io`                 | live    |
| People-polkadot      | `people-polkadot.api.subscan.io`               | live    |
| People-westend       | `people-westend.api.subscan.io`                | test    |
| Polkadot             | `polkadot.api.subscan.io`                      | live    |
| Polymesh             | `polymesh.api.subscan.io`                      | live    |
| Polymesh-test        | `polymesh-testnet.api.subscan.io`              | test    |
| Robonomics-polkadot  | `robonomics.api.subscan.io`                    | live    |
| Shibuya              | `shibuya.api.subscan.io`                       | test    |
| Shiden               | `shiden.api.subscan.io`                        | live    |
| Space-time           | `sxt.api.subscan.io`                           | live    |
| Vara                 | `vara.api.subscan.io`                          | live    |
| Vflow                | `vflow.api.subscan.io`                         | live    |
| Westend              | `westend.api.subscan.io`                       | test    |
| Zkverify             | `zkverify.api.subscan.io`                      | live    |
| Zkverify-testnet     | `zkverify-testnet.api.subscan.io`              | test    |
| Zkverify-vflow       | `vflow-testnet.api.subscan.io`                 | test    |
