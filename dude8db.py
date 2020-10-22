import peewee as pw
from playhouse.shortcuts import model_to_dict
from datetime import datetime, timedelta
import pytz

db = pw.SqliteDatabase('dude8.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Server(BaseModel):
    serverID = pw.IntegerField(primary_key=True)
    timezone = pw.TextField(null=True)
    weekly_notification = pw.IntegerField(null=True)
    notification_time = pw.IntegerField()
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
        date = datetime.strptime(due_date, '%Y-%m-%d').date()
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
                                notification_time=8)


def valid_servers():
    yesterday = datetime.now() - timedelta(days=1)
    query = (Server.select(Server)
                   .distinct()
                   .join(Course)
                   .join(DueDates)
                   .where(
        (Server.timezone.is_null(False)) &
        (DueDates.due_date >= yesterday)
    ))
    dict_form = [model_to_dict(server, backrefs=True) for server in query]

    return dict_form


def change_timezone(server_id, timezone):
    if timezone in pytz.all_timezones:
        (Server.update({Server.timezone: timezone})
               .where(Server.serverID == server_id)).execute()
        return f"Successfully updated server timezone to {timezone}."
    else:
        return f"{timezone} is not a valid timezone."


def change_notification(server_id, new_hour):
    if 0 <= int(new_hour) <= 23:
        (Server.update({Server.notification_time: new_hour})
               .where(Server.serverID == server_id)).execute()
        return f"Successfully updated server notification time to {new_hour}:00"
    else:
        return f"{new_hour} is not a valid hour. Enter an hour between 0-23."


def change_weekly_notification(server_id, new_day):
    if 0 <= int(new_day) <= 6:
        (Server.update({Server.weekly_notification: new_day})
               .where(Server.serverID == server_id)).execute()
        return f"Successfully updated server notification day to {new_day}."
    else:
        return f"{new_day} is not a valid day. Please enter a number 0-6 for Sunday-Saturday."


if __name__ == "__main__":
    db.connect()
    if input("Do you want to drop tables? Y/N: ").lower() in "yes":
        db.drop_tables([Server, DueDates, Course])
    db.create_tables([Server, DueDates, Course])
    add_server(767399931304476702)