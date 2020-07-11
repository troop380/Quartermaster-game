from . import db

class room_members(db.Model):
    room = db.Column(db.String(255), primary_key=True)
    member = db.Column(db.String(255), primary_key=True)

