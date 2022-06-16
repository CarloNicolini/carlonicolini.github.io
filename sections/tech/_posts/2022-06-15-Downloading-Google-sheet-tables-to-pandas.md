---
layout: post
date: 2022-06-15
title: How to download google sheet data to Pandas
---

All you need is a Google Sheets file with one or more sheets and of course some data. The file needs to be set to the sharing option which allows everyone with the link to view the data.


## Option One — if you have multiple sheets
This option allows you to read in a specific sheet from a file containing multiple sheets. You can use the url-structure of google sheets in combination with the unique id of your file and a given sheet name to read in the data.
All you need to do is create a f-string for the url which takes the sheet id and sheet name and formats them into a url pandas can read.

```python
import pandas as pd
sheet_id = “1XqOtPkiE_Q0dfGSoyxrH730RkwrTczcRbDeJJpqRByQ”
sheet_name = “sample_1”
url = f”https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url)
```

You can find the sheet id in the url of your file behind “d/”, copy it from your browser and paste it into your code. The sheet name is the name you gave your sheet.
After you’ve specified the id and name you can simply use the appropriately formatted url string to read the data into a pandas DataFrame (see below).


## Option Two — if your file only has one sheet
If your file is simply one sheet with data you can directly copy and paste the url into your code and just replace one part by a set expression. This expression changes the url, so that it ouputs a csv file when called.
It’s as simple as this:

```python
sheet_url = “https://docs.google.com/spreadsheets/d/1XqOtPkiE_Q0dfGSoyxrH730RkwrTczcRbDeJJpqRByQ/edit#gid=0"
url_1 = sheet_url.replace(‘/edit#gid=’, ‘/export?format=csv&gid=’)
```

The only thing you have to replace in this code snippet is the sheet_url. After part of the string has been replaced you can use `.read_csv()` as usual.

Please note that the composition of the GoogleSheets urls might change in the future, which might break the code.


