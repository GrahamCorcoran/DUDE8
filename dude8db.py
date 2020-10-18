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
    try:
        date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
    except ValueError:
        return "``ERROR: Invalid Date. Use format YYYY-MM-DD``"

    DueDates.create(serverID=server_id,
                    description=description,
                    due_date=due_date)

    return f"Added: {description} on {due_date}."


def remove_duedate(server_id, description):
    query = DueDates.delete().where(serverID=server_id,
                                    description=description)
    return query.execute()


def bulk_add(server_id, input_csv):
    split_input = [_.strip() for _ in input_csv.split(',')]
    descriptions = []
    due_dates = []
    for index, item in enumerate(split_input):
        if index % 2 == 0:
            descriptions.append(item)
        else:
            due_dates.append(item)

    data_list = [{'serverID': server_id,
                  'description': description,
                  'due_date': due_date}
                 for description, due_date in zip(descriptions, due_dates)]

    print(data_list)
    DueDates.insert_many(data_list).execute()

    return "Success"



def add_server(server_id):
    return Server.get_or_create(serverID=server_id,
                                notification_time=datetime.time(hour=8))


if __name__ == "__main__":
    db.connect()
    if input("Do you want to drop tables? Y/N: ").lower() in "yes":
        db.drop_tables([Server, DueDates])
    db.create_tables([Server, DueDates])