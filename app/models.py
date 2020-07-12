from . import db

class room_members(db.Model):
    room = db.Column(db.String(255), primary_key=True)
    member_id = db.Column(db.String(255), primary_key=True)
    member_name = db.Column(db.String(255))

