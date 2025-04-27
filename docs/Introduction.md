With Subscan API, we provide a simple way to access the chain data of more than 90 substrate-based networks.

If you have any question or suggestion, please do not hesitate to contact our API support via [api@subscan.io](mailto:api@subscan.io).

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

5. All APIs documented here are specifically designed for Subscan UI. While they may undergo frequent updates,
   we strictly avoid introducing breaking changes. In the rare event of a mandatory breaking change, we will issue
    advance email notifications to all subscribers.

| Network              | API Host                                       | Status |
|----------------------|------------------------------------------------|--------|
| Acala                | `acala.api.subscan.io`                         | live   |
| Acala-test           | `acala-testnet.api.subscan.io`                 | test   |
| Ajuna                | `ajuna.api.subscan.io`                         | live   |
| Alephzero            | `alephzero.api.subscan.io`                     | live   |
| Altair               | `altair.api.subscan.io`                        | live   |
| Assethub-kusama      | `assethub-kusama.api.subscan.io`               | live   |
| Assethub-paseo       | `assethub-paseo.api.subscan.io`                | test   |
| Assethub-polkadot    | `assethub-polkadot.api.subscan.io`             | live   |
| Assethub-westend     | `assethub-westend.api.subscan.io`              | test   |
| Astar                | `astar.api.subscan.io`                         | live   |
| Autonomys            | `autonomys.api.subscan.io`                     | live   |
| Avail                | `avail.api.subscan.io`                         | live   |
| Avail-turing         | `avail-turing.api.subscan.io`                  | test   |
| Bajun                | `bajun.api.subscan.io`                         | live   |
| Basilisk             | `basilisk.api.subscan.io`                      | live   |
| Bifrost              | `bifrost-kusama.api.subscan.io`                | live   |
| Bifrost-p            | `bifrost.api.subscan.io`                       | live   |
| Bridgehub-kusama     | `bridgehub-kusama.api.subscan.io`              | live   |
| Bridgehub-paseo      | `bridgehub-paseo.api.subscan.io`               | test   |
| Bridgehub-polkadot   | `bridgehub-polkadot.api.subscan.io`            | live   |
| Bridgehub-westend    | `bridgehub-westend.api.subscan.io`             | test   |
| Calamari             | `calamari.api.subscan.io`                      | live   |
| Centrifuge           | `centrifuge-standalone-history.api.subscan.io` | live   |
| Centrifuge-parachain | `centrifuge.api.subscan.io`                    | live   |
| Clover               | `clover.api.subscan.io`                        | live   |
| Collectives          | `collectives-polkadot.api.subscan.io`          | live   |
| Continuum            | `continuum.api.subscan.io`                     | live   |
| Coretime-kusama      | `coretime-kusama.api.subscan.io`               | live   |
| Coretime-polkadot    | `coretime-polkadot.api.subscan.io`             | live   |
| Coretime-westend     | `coretime-westend.api.subscan.io`              | test   |
| Coretime-paseo       | `coretime-paseo.api.subscan.io`                | test   |
| Creditcoin           | `cc-enterprise.api.subscan.io`                 | live   |
| Creditcoin-cc3       | `creditcoin.api.subscan.io`                    | live   |
| Creditcoin-cc3-test  | `creditcoin3-testnet.api.subscan.io`           | test   |
| Creditcoin-dev       | `creditcoin3-dev.api.subscan.io`               | test   |
| Crust-main           | `crust.api.subscan.io`                         | live   |
| Crust-parachain      | `crust-parachain.api.subscan.io`               | live   |
| Darwinia             | `darwinia.api.subscan.io`                      | live   |
| Dbc                  | `dbc.api.subscan.io`                           | live   |
| Dock-pos             | `dock.api.subscan.io`                          | live   |
| Energywebx           | `energywebx.api.subscan.io`                    | live   |
| Energywebx-testnet   | `energywebx-testnet.api.subscan.io`            | test   |
| Enjin-canary-matrix  | `canary-matrix.api.subscan.io`                 | test   |
| Enjin-canary-relay   | `canary.api.subscan.io`                        | test   |
| Enjin-matrix         | `matrix.api.subscan.io`                        | live   |
| Enjin-relay          | `enjin.api.subscan.io`                         | live   |
| Gasp                 | `gasp.api.subscan.io`                          | live   |
| Heima                | `heima.api.subscan.io`                         | live   |
| Humanode             | `humanode.api.subscan.io`                      | live   |
| Hydradx              | `hydration.api.subscan.io`                     | live   |
| Integritee-para      | `integritee.api.subscan.io`                    | live   |
| Interlay             | `interlay.api.subscan.io`                      | live   |
| Karura               | `karura.api.subscan.io`                        | live   |
| Khala                | `khala.api.subscan.io`                         | live   |
| Kintsugi             | `kintsugi.api.subscan.io`                      | live   |
| Krest                | `krest.api.subscan.io`                         | live   |
| Kusama               | `kusama.api.subscan.io`                        | live   |
| Mangata              | `mangatax.api.subscan.io`                      | live   |
| Manta                | `manta.api.subscan.io`                         | live   |
| Moonbase             | `moonbase.api.subscan.io`                      | test   |
| Moonbeam             | `moonbeam.api.subscan.io`                      | live   |
| Moonriver            | `moonriver.api.subscan.io`                     | live   |
| Mythos               | `mythos.api.subscan.io`                        | live   |
| Nodle                | `nodle.api.subscan.io`                         | live   |
| Opal                 | `opal.api.subscan.io`                          | test   |
| Origintrail          | `neuroweb.api.subscan.io`                      | live   |
| Origintrail-rococo   | `neuroweb-testnet.api.subscan.io`              | test   |
| Paseo                | `paseo.api.subscan.io`                         | test   |
| Peaq                 | `agung-testnet.api.subscan.io`                 | test   |
| Peaq-main            | `peaq.api.subscan.io`                          | live   |
| Pendulum             | `pendulum.api.subscan.io`                      | live   |
| People-kusama        | `people-kusama.api.subscan.io`                 | live   |
| People-polkadot      | `people-polkadot.api.subscan.io`               | live   |
| People-paseo         | `people-paseo.api.subscan.io`                  | test   |
| Phala                | `phala.api.subscan.io`                         | live   |
| Pioneer              | `pioneer.api.subscan.io`                       | live   |
| Polkadex             | `polkadex.api.subscan.io`                      | live   |
| Polkadex-parachain   | `polkadex-parachain.api.subscan.io`            | live   |
| Polkadot             | `polkadot.api.subscan.io`                      | live   |
| Polymesh             | `polymesh.api.subscan.io`                      | live   |
| Polymesh-test        | `polymesh-testnet.api.subscan.io`              | test   |
| Robonomics           | `robonomics-freemium.api.subscan.io`           | live   |
| Robonomics-polkadot  | `robonomics.api.subscan.io`                    | live   |
| Shadow               | `shadow.api.subscan.io`                        | live   |
| Shibuya              | `shibuya.api.subscan.io`                       | test   |
| Shiden               | `shiden.api.subscan.io`                        | live   |
| Sora                 | `sora.api.subscan.io`                          | live   |
| Spiritnet            | `spiritnet.api.subscan.io`                     | live   |
| Stafi                | `stafi.api.subscan.io`                         | live   |
| Subspace             | `subspace.api.subscan.io`                      | test   |
| Tanssi-test          | `dancebox.api.subscan.io`                      | test   |
| Turing               | `turing.api.subscan.io`                        | live   |
| Unique               | `unique.api.subscan.io`                        | live   |
| Vara                 | `vara.api.subscan.io`                          | live   |
| Westend              | `westend.api.subscan.io`                       | test   |
| Zeitgeist            | `zeitgeist.api.subscan.io`                     | live   |
| Zkverify-testnet     | `zkverify-testnet.api.subscan.io`              | test   |
