import argparse
import json
import pandas as pd
from pathlib import Path


def extract_arns(json_object):
    """Build a scoutid -> ARN mapping by recursively searching the entire JSON tree."""
    scoutid_to_arn = {}

    def _walk(node, key=None):
        if isinstance(node, dict):
            if key is not None and 'arn' in node and node['arn']:
                scoutid_to_arn[key] = node['arn']
            for k, v in node.items():
                _walk(v, key=k)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(json_object)
    return scoutid_to_arn


def parse_result_file(result_path):
    """Parse a ScoutSuite result .js file and return (account_id, findings list)."""
    with open(result_path, "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        raise ValueError(f"Unexpected file format (fewer than 2 lines): {result_path}")

    json_object = json.loads(lines[1])
    account_id = json_object.get('account_id', 'N/A')
    foldername = str(result_path.parent)
    scoutid_to_arn = extract_arns(json_object)

    findings = []
    for service in json_object.get('services', {}).values():
        for finding in service.get('findings', {}).values():
            if finding.get('flagged_items', 0) == 0:
                continue
            for item in finding.get('items', []):
                parts = item.split('.')
                scoutid = parts[-1] if parts else item
                arn = scoutid_to_arn.get(scoutid, 'N/A')
                findings.append({
                    'folder name': foldername,
                    'account id': account_id,
                    'service': finding.get('service', 'N/A'),
                    'title': finding.get('description', 'N/A'),
                    'rationale': finding.get('rationale', 'N/A'),
                    'level': finding.get('level', 'N/A'),
                    'remediation': finding.get('remediation', 'N/A'),
                    'checked #': finding.get('checked_items', 0),
                    'flagged #': finding.get('flagged_items', 0),
                    'scoutid': scoutid,
                    'arn': arn,
                    'item': item,
                })
    return findings


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert ScoutSuite AWS result files into a single CSV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input-dir",
        type=Path,
        default=Path("."),
        help="Root directory to search recursively for scoutsuite_results_aws*.js files.",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("tool_output.csv"),
        help="Path for the output CSV file.",
    )
    parser.add_argument(
        "--level",
        choices=["danger", "warning", "good"],
        default=None,
        help="Filter findings to only this severity level.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    results = list(args.input_dir.rglob("scoutsuite_results_aws*.js"))
    if not results:
        print(f"No ScoutSuite result files found under '{args.input_dir}'.")
        exit(1)

    data = []
    for result in results:
        try:
            findings = parse_result_file(result)
            if args.level:
                findings = [f for f in findings if f.get('level') == args.level]
            data.extend(findings)
            print(f"Processed {result} ({len(findings)} findings)")
        except (ValueError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: skipping {result} — {e}")

    df = pd.DataFrame(data)
    df.to_csv(args.output, index=False, encoding='utf-8-sig')
    print(f"\nWrote {len(data)} rows to {args.output}")
