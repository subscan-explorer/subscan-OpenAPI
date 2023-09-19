import json

subdomains = ["polkadot","kusama","darwinia","assethub-polkadot","assethub-kusama","assethub-rococo","acala","acala-testnet","alephzero","altair","astar","bajun","basilisk","bifrost","bifrost-kusama","bifrost-testnet","calamari","centrifuge","centrifuge-standalone-history","clover","clv","clover-testnet","composable","crab","crust","maxwell","shadow","dbc","dock","dolphin","efinity","encointer","equilibrium","genshiro","humanode","hydradx","integritee","interlay","karura","kintsugi","khala","krest","kilt-testnet","spiritnet","litmus","mangatax","moonbase","moonbeam","moonriver","nodle","origintrail","origintrail-testnet","pangolin","pangolin-parachain","pangoro","parallel","parallel-heiko","peaq-testnet","phala","picasso","picasso-rococo","pioneer","polkadex","polymesh","polymesh-testnet","quartz","reef","robonomics","rococo","sakura","shibuya","shiden","sora","subspace","stafi","datahighway","turing","unique","vara","westend","zeitgeist"]

def generate_json(subdomains):
    domain = "api.subscan.io"
    environments = []
    for i, subdomain in enumerate(subdomains):
        baseUrl = "https://{}.{}".format(subdomain, domain)
        environment = {
            "baseUrl": baseUrl,
            "baseUrls": {
                "default": baseUrl
            },
            "name": subdomain.capitalize(),
            "ordering": i,
            "projectType": "HTTP"
        }
        environments.append(environment)

    servers = [
        {
            "name": "host",
            "id": "default"
        }
    ]

    data = {
        "environments": environments,
        "servers": servers
    }

    return data


data = generate_json(subdomains)
with open('environments.json', 'w') as f:
    json.dump(data, f, indent=2)
