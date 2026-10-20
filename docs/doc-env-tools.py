import json

from network_docs import DOC_DIR, load_endpoints


def generate_json(subdomains):
    """Build supported environments with an actively indexed default network."""
    domain = "api.subscan.io"
    environments = []
    ordered = sorted(subdomains, key=lambda name: (name != "polkadot", name))
    for i, subdomain in enumerate(ordered):
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


if __name__ == "__main__":
    data = generate_json([endpoint["domain"] for endpoint in load_endpoints()])
    with (DOC_DIR / "environments.json").open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")
