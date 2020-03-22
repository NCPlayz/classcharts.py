import aiohttp
import json
from urllib.parse import unquote
from datetime import datetime, timedelta
from .objects import *


class StudentClient:
    def __init__(self, code, date_of_birth):
        self.code = code
        self.date_of_birth = date_of_birth

        self.session = None

        self._session_id = ''
        self._registration_details = {}

        self.id = 0
        self.name = ''
        self.features = []
        self.account_disabled = False
        self.announcements = 0

    async def _request(self, verb, endpoint, *, params={}, data={}, headers={}):
        root = 'https://www.classcharts.com/'

        async with self.session.request(verb, root + endpoint, params=params, data=data, headers=headers) as response:
            print(await response.text())
            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                data = {}

        return data

    async def login(self):
        if not self.session:
            self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())

        form = aiohttp.FormData({
            '_method': 'POST',
            'code': self.code, 
            'dob': self.date_of_birth.strftime('%d/%m/%Y'),
            'remember_me': '1',
            'recaptcha-token': 'no-token-available'
        })
    
        await self._request('POST', 'student/login', data=form)

        for cookie in self.session.cookie_jar:
            if cookie.key == 'student_session_credentials':
                self._registration_details = json.loads(unquote(cookie.value))
                self._session_id = self._registration_details['session_id']

        await self.ping()

    async def ping(self):
        form = {
            'include_data': "true"
        }
        headers = {
            'Authorization': 'Basic {}'.format(self._session_id)
        }
        data = await self._request('POST', 'apiv2student/ping', data=form, headers=headers)

        self._session_id = data['meta']['session_id']
        user = data['data']['user']

        user.pop('first_name')
        user.pop('last_name')

        self.id = user.pop('id')
        self.name = user.pop('name')
        self.account_disabled = user.pop('is_disabled')
        self.announcements_count = user.pop('announcements_count')
        self.features = user


    async def activity(self, *, after: datetime = None, before: datetime = None):
        if after is None:
            after = datetime.now() - timedelta(days=31)
        if before is None:
            before = datetime.now()

        params = {
            'from': after.strftime("%Y-%m-%d"),
            'to': before.strftime("%Y-%m-%d")
        }
        headers = {
            'Authorization': 'Basic {}'.format(self._session_id)
        }

        data = await self._request('POST', 'apiv2student/activity/{}'.format(self.id), params=params, headers=headers)

        activity = data['data']

        points = []

        for point in activity:
            if point['type'] == 'detention':
                points.append(DetentionPoint(point))
            elif point['polarity'] == 'positive':
                points.append(Positive(point))
            elif point['polarity'] == 'negative':
                points.append(Negative(point))

        return points

    async def homeworks(self, *, display_date: DisplayDate = DisplayDate.due, after: datetime = None, before: datetime = None):
        if after is None:
            after = datetime.now() - timedelta(days=31)
        if before is None:
            before = datetime.now()

        params = {
            'display_date': display_date.value,
            'from': after.strftime("%Y-%m-%d"),
            'to': before.strftime("%Y-%m-%d")
        }
        headers = {
            'Authorization': 'Basic {}'.format(self._session_id)
        }

        data = await self._request('POST', 'apiv2student/homeworks/{}'.format(self.id), params=params, headers=headers)

        homeworks = data['data']

        ret = []

        for homework in homeworks:
            ret.append(Homework(homework))

        return ret

    async def detentions(self, *, after: datetime = None, before: datetime = None):
        if after is None:
            after = datetime.now() - timedelta(days=31)
        if before is None:
            before = datetime.now()

        params = {
            'from': after.strftime("%Y-%m-%d"),
            'to': before.strftime("%Y-%m-%d")
        }
        headers = {
            'Authorization': 'Basic {}'.format(self._session_id)
        }

        data = await self._request('POST', 'apiv2student/detentions/{}'.format(self.id), params=params, headers=headers)

        detentions = data['data']

        ret = []

        for detention in detentions:
            ret.append(Detention(detention))

        return ret
