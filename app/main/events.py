from flask import session, current_app, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio, login_manager
from ..models import db, room_members

# expire a room key after X seconds of being idle
room_idle_max = 1200


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    update_room_idle(room)
    name = session.get('name')
#    sid = request.cookies.get(app.session_cookie_name)
    print("Room {} - Name {}".format(room,name))
    sid = session.sid
    print("Sessionid {}".format(sid))
    join_room(room)
    emit('status', {'msg': name + ' has entered the room.'}, room=room)
    
    # add the user to the user list in sqlite
    query = room_members(room = room, member_id = sid, member_name = name)
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
    sid = session.sid
    leave_room(room)
    emit('status', {'msg': name + ' has left the room.'}, room=room)

    # remove the user to the user list in sqlite
    db.session.query(room_members).filter_by(room = room, member_id = sid).delete()
    db.session.commit()
    send_userlist(room)


@socketio.on("voted", namespace="/chat")
def checkVote(message):
    room = session.get('room')
    update_room_idle(room)
    emit("status", {"msg": message["voteChoice"]}, room=room)
    

def update_room_idle(room):
    # we may need to do something different here, expiring the key removes the data
    # but people could still be in the room
    pass

def send_userlist(room):
    # Get the mamber name from the room_members table filterd by the room
    userlisttmp = db.session.query(room_members.member_name).filter_by(room=room).all()
    # cleanup the results to display
    userlist = [value for value, in userlisttmp]
    print("Userlist - {}".format(userlist))
    emit('userlist', userlist, room=room)

    # need to compare the sid's in the rooms table with the sids in the session table
    # and remove any folks from rooms who's sessions have expired
