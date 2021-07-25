# ScoutSuiteToCSV
Now this is a story all about how
My life got flipped turned upside down
And I'd like to take a minute, just sit right there
I'll tell you how I ended up writing this script...

No I won't as it's client confidential (and I can't rap). None the less here's a script that may be useful for dealing with multiple ScoutSuite reports at once, or QAing an AWS report. The output is more detailed than the default CSV export and allows for items to be checked off as they are checked for validity or reported on.

## Steps
Place script in root directory so it looks something like this
```
scout2csv.py
scoutsuitefolder1
scoutsuitefolder2
etc...
```
The script will look in all subfolders for the `scoutsuite_results_aws*.js` so it doesn't matter what the folders are called. Running it is as simple as `python3 scout2csv.py`.

##Requirements
It has them just use `pip3 install` until it works. I imagine pandas is maybe the only none default library.

##Why isn't this better documented?
I've just finished QAing a configuration report with double digit aws accounts. Would you want to even look at a computer at that point?
