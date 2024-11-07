With Subscan API, we provide a simple way to access the chain data of more than 70 substrate-based networks.

If you have any question or suggestion, please do not hesitate to contact our API support
via [api@subscan.io](mailto:api@subscan.io).

The documentation was created with [apidog](apidog.com).

## API Keys

**Get a free API key that includes higher quotas or start your trial with other available plans
at <https://pro.subscan.io/>.**

## Service Status

The service status of Subscan API can be found on our [status page](https://subscan.statuspage.io).

## Service Level Agreement

Subscan provides our customers the Service Level Agreement (SLA), which includes **Monthly Uptime Percentage**
commitment for multiple networks. Please contact us ([api@subscan.io](mailto:api@subscan.io)) for more information.

## API Endpoints

Please notice before you get started:

1. The following endpoints list is maintained mannually and it might be outdated. In fact, every individual network
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

| Network             | API Host                                       | Status |
|---------------------|------------------------------------------------|--------|
| Polkadot            | `polkadot.api.subscan.io`                      | live   |
| Kusama              | `kusama.api.subscan.io`                        | live   |
| Assethub Polkadot   | `assethub-polkadot.api.subscan.io`             | live   |
| Assethub Kusama     | `assethub-kusama.api.subscan.io`               | live   |
| Assethub Westend    | `assethub-westend.api.subscan.io`              | test   |
| Assethub Paseo      | `assethub-paseo.api.subscan.io/`               | test   |
| Acala               | `acala.api.subscan.io`                         | live   |
| Acala Mandala       | `acala-testnet.api.subscan.io`                 | test   |
| Ajuna               | `ajuna.api.subscan.io`                         | live   |
| Alephzero           | `alephzero.api.subscan.io`                     | live   |
| Alephzero testnet   | `alephzero-testnet.api.subscan.io`             | test   |
| Altair              | `altair.api.subscan.io`                        | live   |
| Astar               | `astar.api.subscan.io`                         | live   |
| Avail testnet       | `avail-testnet.api.subscan.io`                 | test   |
| Bajun               | `bajun.api.subscan.io`                         | live   |
| Basilisk            | `basilisk.api.subscan.io`                      | live   |
| Bifrost             | `bifrost.api.subscan.io`                       | live   |
| Bifrost Kusama      | `bifrost-kusama.api.subscan.io`                | live   |
| BridgeHub Polkadot  | `bridgehub-polkadot.api.subscan.io`            | live   |
| BridgeHub Kusama    | `bridgehub-kusama.api.subscan.io`              | live   |
| BridgeHub Westend   | `bridgehub-westend.api.subscan.io`             | test   |
| BridgeHub paseo     | `bridgehub-paseo.api.subscan.io`               | test   |
| Calamari            | `calamari.api.subscan.io`                      | live   |
| Centrifuge          | `centrifuge.api.subscan.io`                    | live   |
| Centrifuge Solo     | `centrifuge-standalone-history.api.subscan.io` | live   |
| Clover              | `clover.api.subscan.io`                        | live   |
| Composable          | `composable.api.subscan.io`                    | live   |
| Continuum           | `continuum.api.subscan.io`                     | live   |
| creditcoin          | `creditcoin.api.subscan.io`                    | live   |
| creditcoin-testnet  | `creditcoin-testnet.api.subscan.io`            | test   |
| Crust               | `crust.api.subscan.io`                         | live   |
| Crust Shadow        | `shadow.api.subscan.io`                        | live   |
| DeepBrain Chain     | `dbc.api.subscan.io`                           | live   |
| Dock                | `dock.api.subscan.io`                          | live   |
| Darwinia            | `darwinia.api.subscan.io`                      | live   |
| Enjin               | `enjin.api.subscan.io`                         | live   |
| Enjin-matrix        | `matrix.api.subscan.io`                        | live   |
| Enjin-canary-matrix | `canary-matrix.api.subscan.io`                 | test   |
| Enjin-canary        | `canary.api.subscan.io`                        | test   |
| Energywebx          | `energywebx.api.subscan.io`                    | live   |
| Energywebx-testnet  | `energywebx-testnet.api.subscan.io`            | test   |
| Humanode            | `humanode.api.subscan.io`                      | live   |
| HydraDX             | `hydradx.api.subscan.io`                       | live   |
| IntegriTEE          | `integritee.api.subscan.io`                    | live   |
| Interlay            | `interlay.api.subscan.io`                      | live   |
| joystream           | `joystream.api.subscan.io`                     | live   |
| Karura              | `karura.api.subscan.io`                        | live   |
| Kintsugi            | `kintsugi.api.subscan.io`                      | live   |
| Khala               | `khala.api.subscan.io`                         | live   |
| krest               | `krest.api.subscan.io`                         | live   |
| KILT Spiritnet      | `spiritnet.api.subscan.io`                     | live   |
| Mangata             | `mangatax.api.subscan.io`                      | live   |
| Moonbase            | `moonbase.api.subscan.io`                      | test   |
| Moonbeam            | `moonbeam.api.subscan.io`                      | live   |
| Moonriver           | `moonriver.api.subscan.io`                     | live   |
| Manta               | `manta.api.subscan.io`                         | live   |
| Nodle               | `nodle.api.subscan.io`                         | live   |
| NeuroWeb            | `neuroweb.api.subscan.io`                      | live   |
| NeuroWeb Testnet    | `neuroweb-testnet.api.subscan.io`              | test   |
| paseo               | `paseo.api.subscan.io`                         | test   |
| Peaq                | `peaq.api.subscan.io`                          | live   |
| Peaq  Testnet       | `peaq-testnet.api.subscan.io`                  | test   |
| Phala               | `phala.api.subscan.io`                         | live   |
| Picasso             | `picasso.api.subscan.io`                       | live   |
| Pioneer             | `pioneer.api.subscan.io`                       | live   |
| Polkadex            | `polkadex.api.subscan.io`                      | live   |
| Polkadex Parachain  | `polkadex-parachain.api.subscan.io`            | live   |
| Polymesh            | `polymesh.api.subscan.io`                      | live   |
| Polymesh Testnet    | `polymesh-testnet.api.subscan.io`              | test   |
| Quartz              | `quartz.api.subscan.io`                        | live   |
| Robonomics          | `robonomics.api.subscan.io`                    | live   |
| Shibuya             | `shibuya.api.subscan.io`                       | test   |
| Shiden              | `shiden.api.subscan.io`                        | live   |
| SORA                | `sora.api.subscan.io`                          | live   |
| Subspace            | `subspace.api.subscan.io`                      | live   |
| Stafi               | `stafi.api.subscan.io`                         | live   |
| Turing              | `turing.api.subscan.io`                        | live   |
| Unique              | `unique.api.subscan.io`                        | live   |
| Vara                | `vara.api.subscan.io`                          | live   |
| Westend             | `westend.api.subscan.io`                       | test   |
| Zeitgeist           | `zeitgeist.api.subscan.io`                     | live   |
