import peewee as pw

db = pw.SqliteDatabase('dude8.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Server(BaseModel):
    serverID = pw.IntegerField(primary_key=True)
    timezone = pw.TextField()
    weekly_notification = pw.IntegerField(null=True)
    notification_time = pw.TimeField()


class DueDates(BaseModel):
    serverID = pw.ForeignKeyField(Server, backref='duedates')
    description = pw.TextField()
    due_date = pw.DateTimeField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([Server, DueDates])