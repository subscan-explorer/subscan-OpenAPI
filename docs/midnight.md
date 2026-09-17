# Midnight Compact Contract Verification

This guide explains how to verify a deployed Midnight Compact contract on Subscan.

Subscan recompiles the submitted Compact source with the selected compiler version and compares the generated verifier keys with the keys recorded for the deployed contract. The source, compiler version, and generated circuits must match the deployment artifact.

## Before you start

Prepare the following:

- The deployed contract address and the Midnight network where it was deployed.
- The exact Compact source used for deployment.
- The exact Compact compiler version used to compile the contract.
- Every source file required by the contract if it is a multi-file project.

## Prepare the source file

Choose the source type that matches your build artifact.

### Single file

Use **Single file** when the complete contract is contained in one `.compact` file. Upload the exact source used for deployment. If the contract depends on additional project files, use the multi-file format instead.

### Multi-file Standard Input JSON

Use **Standard-Input-JSON** for a project with imports or multiple Compact files. The uploaded file must be valid JSON with a `contracts` map and an `entry-file` pointing to the contract entry file:

```json
{
  "contracts": {
    "src/main.compact": "<complete source of main.compact>",
    "src/library.compact": "<complete source of library.compact>"
  },
  "entry-file": "src/main.compact"
}
```

Include every imported file, preserve the paths used by the source, and do not add trailing commas. The `entry-file` value must match one of the keys in `contracts`.

## Verify in the Subscan UI

1. Open the contract page on the same Midnight network where the contract was deployed.
2. Open the **Contract** tab and click **Verify Now** for an unverified contract.
3. Select the matching compiler type: **Single file** or **Standard-Input-JSON**.
4. Select the exact **Compact Version** used during deployment. The available versions are provided by the network's supported compiler list.
5. Upload the matching `.compact` file or Standard Input JSON file.
6. Click **Contract Verification** and wait for the result.

Production verification may run asynchronously. If the status is **Verifying**, refresh the contract page later and do not submit another request until the current verification finishes. A successful result shows the contract as **Verified** and exposes the verified source and contract metadata.

## Troubleshooting

| Result or message | What to check |
| --- | --- |
| `contract not found` | Confirm the address and selected network, and wait for the contract to be indexed. |
| `unsupported compiler version` | Select a Compact version offered by the network's supported version list. |
| Compilation error | Check the source type, JSON syntax, `entry-file`, file paths, imports, and compiler version. |
| Verifier key mismatch | Confirm that the source and compiler version are exactly the deployment artifacts and that all project files are included. |
| `contract is being verified` | Wait for the current verification job to finish before submitting again. |
| `contract already verified` | Use the existing verified source and metadata; a second verification is not required. |

The submitted source becomes public after successful verification. Do not include private keys, wallet seeds, or other secrets in the source artifact.

For Compact language and toolchain details, see the [Midnight Compact documentation](https://docs.midnight.network/compact).
