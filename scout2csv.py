import os
import glob
import pandas as pd
import json
from pathlib import Path

results = list(Path(".").rglob("scoutsuite_results_aws*.js"))
data = []

for result in results:
    with open(result, "r") as file:
        all_lines = file.readlines()
    json_string = all_lines[1]  # Get the second line (index 1)
    json_object = json.loads(json_string)
    foldername = str(result).split("/")[0]
    accountid = json_object['account_id']
    findings = []

    # Create a mapping of scoutid to arn
    scoutid_to_arn = {}
    for service_name, service_data in json_object['services'].items():
        for region_name, region_data in service_data.get('regions', {}).items():
            for resource_name, resource_data in region_data.get('trails', {}).items():
                if isinstance(resource_data, dict) and 'arn' in resource_data:
                    scoutid = resource_name
                    arn = resource_data['arn']
                    scoutid_to_arn[scoutid] = arn

    for service in json_object['services'].values():
        for finding in service['findings'].values():
            if finding['flagged_items'] > 0:
                for item in finding['items']:
                    scoutid = item.split('.')[-2]  # Extract scoutid (second to last element)

                    # Lookup for arn using scoutid
                    arn = scoutid_to_arn.get(scoutid, 'N/A')

                    findings.append({
                        'folder name': foldername,
                        'account id': accountid,
                        'service': finding['service'],
                        'title': finding['description'],
                        'rationale': finding['rationale'],
                        'level': finding['level'],
                        'remediation': finding['remediation'],
                        'checked #': finding['checked_items'],
                        'flagged #': finding['flagged_items'],
                        'scoutid': scoutid,
                        'arn': arn,
                        'item': item
                    })
    data.extend(findings)

df = pd.DataFrame(data)
print(df)
df.to_csv("tool_output.csv", index=False, encoding='utf-8-sig')
