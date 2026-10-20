"""Read the public API endpoint inventory shared by documentation generators."""

import json
from pathlib import Path


DOC_DIR = Path(__file__).resolve().parent

# These historical aliases are excluded from public API documentation.
LEGACY_DOMAINS = {
    "origintrail", "origintrail-testnet", "hydradx", "creditcoin-classic",
    "creditcoin-testnet", "cc-enterprise-testnet",
}

# Deployment identifiers differ from the names already used in the API guide.
NETWORK_NAMES = {
    "statemine": "assethub-kusama",
    "statemint": "assethub-polkadot",
    "darwinia2": "darwinia",
    "bifrost-p": "bifrost-polkadot",
    "crust-main": "crust",
    "collectives": "collectives-polkadot",
    "peaq": "peaq-testnet",
}


def load_endpoints(file_path=DOC_DIR / "network.json"):
    """Load supported API hosts, preserving explicit archive status.

    API and UI subdomains can identify different backend generations. Use the
    explicit API mapping rather than deriving hosts from the explorer URL.
    """
    with open(file_path, encoding="utf-8") as file:
        networks = json.load(file)

    endpoints = []
    seen_domains = set()
    for network, details in networks.items():
        network_type = details["type"]
        if network_type not in ("mainnet", "testnet"):
            raise ValueError(f"unsupported network type for {network}: {network_type}")
        status = "archive" if details.get("is_archive") else (
            "live" if network_type == "mainnet" else "test"
        )
        name = NETWORK_NAMES.get(network, network).capitalize()
        for domain in details["api_domains"]:
            if domain in LEGACY_DOMAINS:
                continue
            if domain in seen_domains:
                raise ValueError(f"duplicate public API domain: {domain}")
            seen_domains.add(domain)
            endpoints.append({"name": name, "domain": domain, "status": status})

    return sorted(endpoints, key=lambda endpoint: (endpoint["name"], endpoint["domain"]))
