from datetime import datetime
from enum import Enum
from .utils import sanitise


class ActivityPoint:
    def __repr__(self):
        return '<{} id={!r} point_type={!r} score={!r} reason={!r}>'.format(self.__class__.__name__, self.id, self.point_type, self.score, self.reason)


class Positive(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.point_type = data['type']
        self.score = data['score']
        self.reason = data['reason']
        self.timestamp = datetime.fromisoformat(data['timestamp'])
        self.lesson = data['lesson_name']
        self.teacher = data['teacher_name']
        self.note = data['note']


class Negative(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.point_type = data['type']
        self.score = data['score']
        self.reason = data['reason']
        self.timestamp = datetime.fromisoformat(data['timestamp'])
        self.lesson = data['lesson_name']
        self.teacher = data['teacher_name']
        self.note = data['note']


class DetentionPoint(ActivityPoint):
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.point_type = data['type']
        self.score = data['score']
        self.reason = data['reason']
        self.date_set = datetime.fromisoformat(data['timestamp'])
        self.lesson = data['lesson_name']
        self.teacher = data['teacher_name']
        self.note = data['note']
        self.date = datetime.fromisoformat(data['detention_date'])
        self.time = datetime.strptime(data['detention_time'], '%H:%M')
        self.location = data['detention_location']
        self.type = data['detention_type']


class Announcement:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = sanitise(data['description'])
        self.viewed = True if data['state'] == 'viewed' else False
        self.timestamp = datetime.fromisoformat(data['timestamp'])
        self.school_name = data['school_name']

    def __repr__(self):
        return '<Announcement id={!r} title={!r} timestamp={!r} school_name={!r}>'.format(self.id, self.title, self.timestamp, self.school_name)


class DisplayDate(Enum):
    due = 'due_date'
    issue = 'issue_date'

class Homework:  # different from homework.Homework
    def __init__(self, data):
        self.lesson = data['lesson']
        self.subject = data['subject']
        self.teacher = data['teacher']
        self.id = data['id']
        self.title = sanitise(data['title'])
        self.description = sanitise(data['description'])
        self.issue_date = datetime.strptime(data['issue_date'], "%Y-%m-%d")
        self.due_date = datetime.strptime(data['due_date'], "%Y-%m-%d")
        self.validated_attachments = [Attachment(d) for d in data['validated_attachments']]
        self.completion_time = (int(data['completion_time_value'] or '0'), data['completion_time_unit'])
        self.status = HomeworkStatus(data['status'])

    def __repr__(self):
        return '<Homework id={!r} lesson={!r} teacher={!r} title={!r} issue_date={!r} due_date={!r} status={!r}>'.format(self.id, self.lesson, self.teacher, self.title, self.issue_date, self.due_date, self.status)


class Attachment:
    def __init__(self, data):
        self.id = data['id']
        self.filename = data['file_name']
        self.file = data['file']
        self.validated_file = data.get('validated_attachment')

    def __repr__(self):
        return '<Attachment id={!r} filename={!r}>'.format(self.id, self.filename)


class HomeworkStatus:
    def __init__(self, data):
        self.id = data['id']
        self.ticked = True if data['ticked'] == 'yes' else False
        self.submitted_attachments = [Attachment(d) for d in data['attachments']]

    def __repr__(self):
        return '<HomeworkStatus id={!r} ticked={!r} submitted_attachments={!r}>'.format(self.id, self.ticked, self.submitted_attachments)


class Teacher:
    def __init__(self, data):
        self.title = data["title"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        self.name = "{} {} {}".format(self.title, self.first_name[0], self.last_name)

    def __repr__(self):
        return '<Teacher name={!r}>'.format(self.name)


class BasicLesson:
    def __init__(self, data):
        self.name = data["name"]
        try:
            self.subject = data["subject"]["name"]
        except TypeError:
            self.subject = None

    def __repr__(self):
        return '<BasicLesson name={!r} subject={!r}>'.format(self.name, self.subject)


class Detention:
    def __init__(self, data):
        self.id = data['id']
        self.attended = True if data['attended'] == "yes" else False
        time = datetime.strptime(data['time'], "%H:%M")
        self.date = datetime.fromisoformat(data['date']).replace(minute=time.minute, hour=time.hour)
        self.length = int(data['length'])
        self.location = data['location']
        self.lesson = BasicLesson(data['lesson'])
        self.teacher = Teacher(data['teacher'])
        self.lesson_pupil_behaviour = data['lesson_pupil_behaviour']['reason']
        self.detention_type = data['detention_type']['name']

    def __repr__(self):
        return '<Detention id={!r} attended={!r} date={!r} length={!r} lesson={!r} teacher={!r} detention_type={!r}>'.format(self.id, self.attended, self.date, self.length, self.lesson, self.teacher, self.detention_type)


class Lesson(BasicLesson):
    def __init__(self, data):
        super().__init__({"name": data["lesson_name"], "subject": {"name": data["subject_name"]}})
        title, first_name, last_name = data["teacher_name"].split(" ")
        self.teacher = Teacher({"title": title, "first_name": first_name, "last_name": last_name})
        self.room = data["room_name"]
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.period = {"name": data["period_name"], "number": data["period_number"]}
        self.start = datetime.fromisoformat(data["start_time"])
        self.end = datetime.fromisoformat(data["end_time"])
        self.note = data["note"] or None
        self._key = data["key"]
    
    def __repr__(self):
        return '<Lesson name={!r} subject={!r} room={!r}>'.format(self.name, self.subject, self.room)


class Timetable:
    def __init__(self, data):
        self.lessons = [Lesson(data) for data in data["data"]]
        self.date = datetime.fromisoformat(data["meta"]["dates"][0])
        self.start = datetime.fromisoformat(data["meta"]["start_time"])
        self.end = datetime.fromisoformat(data["meta"]["end_time"])

    def __repr__(self):
        return "<Timetable date={!r}>".format(self.date)


class AttendanceLesson(BasicLesson):
    def __init__(self, name, data):
        super().__init__({"name": name, "subject": {"name": None}})
        self.code = data["code"] or None
        self.late_minutes = int(data["late_minutes"] or "0")
        self.status = data["status"]

    def __repr__(self):
        return '<AttendanceLesson name={!r} code={!r}>'.format(self.name, self.code)


class Attendance:
    def __init__(self, data):
        self.percentage = int(data["meta"]["percentage"])
        self.percentage_singe_august = int(data["meta"]["percentage_singe_august"])
        self.dates = [datetime.fromisoformat(date) for date in data["meta"]["dates"]]
        self.days = {}

        for date, day in data["data"].items():
            self.days[datetime.fromisoformat(date)] = [AttendanceLesson(name, lesson) for name, lesson in day.items()]

        self.sessions = data["meta"]["sessions"]
        self.start = datetime.fromisoformat(data["meta"]["start_date"])
        self.end = datetime.fromisoformat(data["meta"]["end_date"])

    def __repr__(self):
        return "<Attendance percentage={!r}>".format(self.percentage)
