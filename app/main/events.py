from flask import session, current_app
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from ..models import db, room_members

# expire a room key after X seconds of being idle
room_idle_max = 1200


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    update_room_idle(room)
    name = session.get('name')
    join_room(room)
    emit('status', {'msg': name + ' has entered the room.'}, room=room)
    
    # add the user to the user list in sqlite
    query = room_members(room = room, member = name)
    db.session.add(query)
    db.session.commit()
    send_userlist(room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    update_room_idle(room)
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    emit('status', {'msg': name + ' has left the room.'}, room=room)

    # remove the user to the user list in sqlite
    #query = room_members(room = room, member = name)
    db.session.query(room_members).filter_by(room = room, member = name).delete()
    db.session.commit()
    send_userlist(room)


@socketio.on("voted", namespace="/chat")
def checkVote(message):
    room = session.get('room')
    update_room_idle(room)
    emit("status", {"msg": message["voteChoice"]}, room=room)
    

def update_room_idle(room):
    # create key to access room member list
    room_member_key = "room:{}:members".format(room)
    # use the redis expire call to set the expire time for the room key
#    rdata.expire(room_member_key,room_idle_max)
    # we may need to do something different here, expiring the key removes the data
    # but people could still be in the room

def send_userlist(room):
    # create key to access room member list
    #room_member_key = "select member_name from room_members where room = \"{}\";".format(room)
    userlisttmp = db.session.query(room_members.member).filter_by(room=room).all()
    # cleanup the results to display
    userlist = [value for value, in userlisttmp]
    print("Userlist - {}".format(userlist))
    emit('userlist', userlist, room=room)
