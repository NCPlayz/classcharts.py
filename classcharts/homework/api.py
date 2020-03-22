from datetime import datetime, timedelta
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from .objects import Homework


class HomeworkClient:
    def __init__(self, school: str):
        self.school = school
        self.session = None
        self.url = "https://www.classcharts.com/apipublic/homework"

    async def request(self, date: datetime, year: int):
        if not self.session:
            self.session = aiohttp.ClientSession()

        start = date.date() - timedelta(days=date.weekday())
        end = start + timedelta(days=6)

        body = "lesson_name=&year={}&subject=&teacher=&from={}&to={}&hash={}".format(year, start, end, self.school)
        body += "&homework_display_date=issue_date&csrf=a893725f23c7eb94f8a0e3a82e2a5ceb"

        headers = {
            'Host': 'www.classcharts.com',
            'User-Agent': 'ClassCharts Python (3.x, aiohttp)',
            'Accept': '*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '166',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0, no-cache',
            'TE': 'Trailers',
            'Pragma': 'no-cache'
        }

        async with self.session.post(self.url, data=body, headers=headers) as response:
            res = await response.json()

        return self.homeworkify(res['data'])

    def homeworkify(self, data: dict):
        homeworks = []

        for i in data:
            description = re.sub("\n\n+", "\n", BeautifulSoup(i['description'], "lxml").text)

            homeworks.append(Homework(i, description))

        return homeworks
