import json
import pandas as pd
from pathlib import Path


def extract_arns(json_object):
    """Build a scoutid -> ARN mapping across all services and resource types."""
    scoutid_to_arn = {}
    for service_data in json_object.get('services', {}).values():
        for region_data in service_data.get('regions', {}).values():
            for resources in region_data.values():
                if not isinstance(resources, dict):
                    continue
                for resource_name, resource_data in resources.items():
                    if isinstance(resource_data, dict) and 'arn' in resource_data:
                        scoutid_to_arn[resource_name] = resource_data['arn']
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
                scoutid = parts[-2] if len(parts) >= 2 else item
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


if __name__ == "__main__":
    output_file = "tool_output.csv"
    results = list(Path(".").rglob("scoutsuite_results_aws*.js"))

    if not results:
        print("No ScoutSuite result files found.")
        exit(1)

    data = []
    for result in results:
        try:
            findings = parse_result_file(result)
            data.extend(findings)
            print(f"Processed {result} ({len(findings)} findings)")
        except (ValueError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: skipping {result} — {e}")

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nWrote {len(data)} rows to {output_file}")
