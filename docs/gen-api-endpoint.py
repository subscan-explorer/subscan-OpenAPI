import json

def parse_network_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    ignoreDomains = ['origintrail','origintrail-testnet','hydradx','creditcoin-classic','creditcoin-testnet','cc-enterprise-testnet']
    replaceNetwork = {
        "statemine": "assethub-kusama",
        "statemint": "assethub-polkadot",
        "darwinia2": "darwinia",
    }
    table = []

    # clean up data, replace network name
    for network in list(data.keys()):
        if network in replaceNetwork:
            data[replaceNetwork[network]] = data.pop(network)

    # sort by network name
    data = dict(sorted(data.items()))

    for network, details in data.items():
        status = 'live' if details['type'] == 'mainnet' else 'test'
        for domain in details['ui_domains']:
            if domain in ignoreDomains:
                continue
            table.append(f"| {network.capitalize():<18} | `{domain}.api.subscan.io` | {status:<6} |")

    return table

def print_table(table):
    header = "| Network             | API Host                                       | Status |"
    separator = "|---------------------|------------------------------------------------|--------|"
    print(header)
    print(separator)
    for row in table:
        print(row)

if __name__ == "__main__":
    json_file_path = 'network.json'
    table = parse_network_json(json_file_path)
    print_table(table)