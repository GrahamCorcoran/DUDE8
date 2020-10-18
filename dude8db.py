import peewee as pw
import datetime

db = pw.SqliteDatabase('dude8.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Server(BaseModel):
    serverID = pw.IntegerField(primary_key=True)
    timezone = pw.TextField(null=True)
    weekly_notification = pw.IntegerField(null=True)
    notification_time = pw.TimeField()


class DueDates(BaseModel):
    serverID = pw.ForeignKeyField(Server, backref='duedates')
    description = pw.TextField()
    due_date = pw.DateTimeField()


def add_duedate(server_id, description, due_date):
    return DueDates.create(serverID=server_id,
                           description=description,
                           due_date=due_date)


def remove_duedate(server_id, description):
    query = DueDates.delete().where(serverID=server_id,
                                    description=description)
    return query.execute()


def add_server(server_id):
    return Server.get_or_create(serverID=server_id,
                                notification_time=datetime.time(hour=8))


if __name__ == "__main__":
    db.connect()
    if input("Do you want to drop tables? Y/N: ").lower() in "yes":
        db.drop_tables([Server, DueDates])
    db.create_tables([Server, DueDates])