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
    
    for service in json_object['services'].values():
        for finding in service['findings'].values():
            if finding['flagged_items'] > 0:
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
                    'items': finding['items']
                })
    data.extend(findings)

df = pd.DataFrame(data)
print(df)
df.to_csv("tool_output.csv", index=False, encoding='utf-8-sig')

