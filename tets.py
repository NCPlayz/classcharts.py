import asyncio
import datetime
import classcharts
from pprint import pprint

client = classcharts.StudentClient("TVWZNW7R", datetime.datetime(year=2005, month=2, day=23))

async def main():
    await client.login()
    attendance = await client.attendance()
    pprint(attendance)
    print(attendance.percentage)
    for day in attendance.days.values():
        print(day[0])
    await client.logout()

asyncio.run(main())