###############################
# WARNING                     #
###############################
# If you edit this file you will need to 
#  - reinitalize the database file (database.sqlite3)
#    deleting and restarting should do it



from . import db

class room_members(db.Model):
    room = db.Column(db.String(255), primary_key=True)
    member_id = db.Column(db.String(255), primary_key=True)
    member_name = db.Column(db.String(255))
    spectator = db.Column(db.Boolean())

