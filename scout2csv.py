import os
import glob
import pandas as pd
import json
from pathlib import Path

results = list(Path(".").rglob("scoutsuite_results_aws*.js"))
df = pd.DataFrame()

for result in results:
	file_variable = open(result, "r")
	all_lines_variable = file_variable.readlines()
	json_string = all_lines_variable[2 - 1]
	json_object = json.loads(json_string)
	foldername = str(result).split("/")[0]
	accountid = json_object['account_id']
	findings = []
	for service in json_object['services'].values():
		for finding in service['findings'].values():
			if finding['flagged_items'] > 0:
				findings.append({'folder name': foldername, 'account id': accountid, 'service': finding['service'], 'title': finding['description'], 'rationale': finding['rationale'], 'level': finding['level'], 'remediation': finding['remediation'], 
					'checked #': finding['checked_items'], 'flagged #': finding['flagged_items'], 'items': finding['items']})
	df = df.append(findings)
print(df)
df.to_csv( "tool_output.csv", index=False, encoding='utf-8-sig')
