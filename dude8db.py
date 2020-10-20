import peewee as pw
import datetime
import pytz

db = pw.SqliteDatabase('dude8.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Server(BaseModel):
    serverID = pw.IntegerField(primary_key=True)
    timezone = pw.TextField(null=True)
    weekly_notification = pw.IntegerField(null=True)
    notification_time = pw.TimeField()
    text_channel = pw.TextField(default="general")


class Course(BaseModel):
    serverID = pw.ForeignKeyField(Server, backref='course')
    course_name = pw.TextField()


class DueDates(BaseModel):
    course = pw.ForeignKeyField(Course, backref='duedates')
    description = pw.TextField()
    due_date = pw.DateTimeField()


def add_duedate(server_id, course, description, due_date):
    try:
        date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
    except ValueError:
        return "``ERROR: Invalid Date. Use format YYYY-MM-DD``"

    course_id = Course.get_or_create(serverID=server_id, course_name=course)
    DueDates.create(course=course_id[0],
                    description=description,
                    due_date=date)

    return f"Added: {description} on {due_date}."


def remove_duedate(server_id, course, description):
    course_id = Course.get_or_create(serverID=server_id, course_name=course)
    quantity_removed = DueDates.delete().where(DueDates.course == course_id[0],
                                               DueDates.description == description).execute()

    if quantity_removed:
        return f"Success! {description} removed."
    else:
        return f"No records matched."


def add_server(server_id):
    return Server.get_or_create(serverID=server_id,
                                notification_time=datetime.time(hour=8))


def change_timezone(server_id, timezone):
    if timezone in pytz.all_timezones:
        (Server.update({Server.timezone: timezone})
               .where(Server.serverID == server_id)).execute()
        return f"Successfully updated server timezone to {timezone}."
    else:
        return f"{timezone} is not a valid timezone."


def get_valid_servers(days_delta=7):
    now = datetime.datetime.now()
    valid_servers = (Server.select(Server.serverID)
                           .distinct(True)
                           .join(Course)
                           .join(DueDates)
                           .where(now < DueDates.due_date,
                                  DueDates.due_date <= now+datetime.timedelta(days=days_delta))
                     )

    return valid_servers


if __name__ == "__main__":
    db.connect()
    if input("Do you want to drop tables? Y/N: ").lower() in "yes":
        db.drop_tables([Server, DueDates, Course])
    db.create_tables([Server, DueDates, Course])
    add_server(767399931304476702)