import json


def parse_network_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    ignoreDomains = ['origintrail','origintrail-testnet','hydradx','creditcoin-classic','creditcoin-testnet','cc-enterprise-testnet']
    replaceNetwork = {
        "statemine": "assethub-kusama",
        "statemint": "assethub-polkadot",
    }
    networks = []
    data = dict(sorted(data.items()))

    for network, details in data.items():
        for domain in details['ui_domains']:
            if domain in ignoreDomains:
                continue
            networks.append(domain)

    return networks

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


data = generate_json(parse_network_json('network.json'))
with open('environments.json', 'w') as f:
    json.dump(data, f, indent=2)
