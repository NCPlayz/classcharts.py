from datetime import datetime


class Homework:
    def __init__(self, data, description):
        self.title = data["title"] if data["title"] else "No Title Given."
        self.description = description if description else "No Description Given."
        self.issue_date = datetime.fromisoformat(data["issue_date"])
        self.due_date = datetime.fromisoformat(data["due_date"])
        self.teacher = Teacher(data["teacher"])
        self.lesson = Lesson(data["lesson"])

        self.attachments = []

        for i in data["homework_attachments"]:
            self.attachments.append(Attachment(i))

    def __repr__(self):
        return '<Homework title={!r} issue_date={!r} due_date={!r} teacher={!r} lesson={!r} attachments={!r}>'.format(self.title, self.issue_date, self.due_date, self.teacher, self.lesson, self.attachments)


class Teacher:
    def __init__(self, data):
        self.title = data["title"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        self.name = "{} {} {}".format(self.title, self.first_name[0], self.last_name)

    def __repr__(self):
        return '<Teacher name={!r}>'.format(self.name)

class Lesson:
    def __init__(self, data):
        self.name = data["name"]
        try:
            self.subject = data["subject"]["name"]
        except TypeError:
            self.subject = None

    def __repr__(self):
        return '<Lesson name={!r} subject={!r}>'.format(self.name, self.subject)


class Attachment:
    def __init__(self, data):
        self.file = data["file"]
        self.file_name = data["file_name"]

    def __repr__(self):
        return '<Attachment file_name={!r}>'.format(self.file_name)