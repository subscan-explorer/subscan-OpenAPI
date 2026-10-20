"""Print or refresh the API endpoint table from network.json."""

import argparse

from network_docs import DOC_DIR, load_endpoints


BEGIN_MARKER = "<!-- BEGIN SUPPORTED NETWORKS -->"
END_MARKER = "<!-- END SUPPORTED NETWORKS -->"


def generate_table(endpoints):
    """Render the supported hosts and service modes from the API inventory."""
    rows = [("Network", "API Host", "Status")]
    rows.extend(
        (endpoint["name"], f'`{endpoint["domain"]}.api.subscan.io`', endpoint["status"])
        for endpoint in endpoints
    )
    widths = [max(len(row[column]) for row in rows) for column in range(3)]
    lines = [
        "| " + " | ".join(value.ljust(width) for value, width in zip(row, widths)) + " |"
        for row in rows
    ]
    lines.insert(1, "|" + "|".join("-" * (width + 2) for width in widths) + "|")
    return "\n".join(lines) + "\n"


def update_table(file_path, table):
    """Replace only the marked table, failing if its boundaries are ambiguous."""
    content = file_path.read_text(encoding="utf-8")
    if content.count(BEGIN_MARKER) != 1 or content.count(END_MARKER) != 1:
        raise ValueError("Introduction must contain exactly one supported-network marker pair")
    before, rest = content.split(BEGIN_MARKER)
    _, after = rest.split(END_MARKER)
    file_path.write_text(before + BEGIN_MARKER + "\n\n" + table + "\n" + END_MARKER + after,
                         encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="update Introduction.md in place")
    args = parser.parse_args()
    table = generate_table(load_endpoints())
    if args.write:
        update_table(DOC_DIR / "Introduction.md", table)
    else:
        print(table, end="")
