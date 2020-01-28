from pony.orm import Database, Required, PrimaryKey
from datetime import datetime

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class VoiceMSG(db.Entity):
    voice_id = PrimaryKey(str)
    user_id = Required(int)
    oga_path = Required(str)
    wav_path = Required(str)
    date = Required(datetime)


class FacesPhoto(db.Entity):
    photo_id = PrimaryKey(str)
    user_id = Required(int)
    photo_path = Required(str)
    date = Required(datetime)


db.generate_mapping(create_tables=True)