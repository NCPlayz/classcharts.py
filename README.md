# classcharts.py

An unofficial API wrapper for the ClassCharts homework and student API.
It is work-in-progress.

## Examples

Examples are using the asyncio REPL.

```py
>>> import asyncio
>>> import datetime   
>>> import classcharts
>>> hc = classcharts.HomeworkClient("Your_School_Here")
>>> await hc.request(datetime.datetime.now(), 7)
[<Homework ...>, <Homework ...>]
```

```py
>>> import asyncio
>>> import datetime
>>> import classcharts
>>> sc = classcharts.StudentClient("MYC0D3", datetime.datetime(year=1970, month=1, day=1))
>>> await sc.detentions()
[<Detention ...>, <Detention ...>]
```
