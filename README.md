# scout2csv - Turn ScoutSuite Output(s) into a usable CSV file
Now this is a story all about how<br/>
My life got flipped turned upside down<br/>
And I'd like to take a minute, just sit right there<br/>
I'll tell you how I ended up writing this script...<br/>

No I won't as it's client confidential (and I can't rap). None the less here's a script that may be useful for dealing with multiple ScoutSuite reports at once, or QAing an AWS report. The output is more detailed than the default CSV export and allows for items to be checked off as they are checked for validity or reported on.

## Requirements
```
pip3 install -r requirements.txt
```

## Usage
```
python3 scout2csv.py [-h] [-i INPUT_DIR] [-o OUTPUT] [--level {danger,warning,good}]
```

### Arguments

| Flag | Default | Description |
|---|---|---|
| `-h`, `--help` | | Show help message and exit |
| `-i`, `--input-dir` | `.` (current directory) | Root directory to search recursively for `scoutsuite_results_aws*.js` files |
| `-o`, `--output` | `tool_output.csv` | Path for the output CSV file |
| `--level` | *(all severities)* | Filter findings to only this severity level: `danger`, `warning`, or `good` |

### Examples

Run from the directory containing your ScoutSuite report folders:
```
python3 scout2csv.py
```

Point at a specific reports directory and write to a custom output file:
```
python3 scout2csv.py -i ./scoutsuite-reports -o results.csv
```

Export only high-severity findings:
```
python3 scout2csv.py --level danger -o high-risk.csv
```

### Directory layout
The script recurses from `--input-dir`, so the folder structure doesn't matter as long as `scoutsuite_results_aws*.js` files are somewhere beneath it:
```
scout2csv.py
scoutsuitefolder1/
scoutsuitefolder2/
...
```

## Why isn't this better documented?
I've just finished QAing a configuration report with double digit aws accounts. Would you want to even look at a computer at that point? I am more than a few ciders into my Sunday evening.
