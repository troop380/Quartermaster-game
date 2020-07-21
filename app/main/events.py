import functools
from flask import session, request
from flask_login import current_user
import flask_login
from flask_socketio import emit, join_room, leave_room
from .. import socketio, login_manager
from ..models import db, room_members

# expire a room key after X seconds of being idle
room_idle_max = 1200


class User(flask_login.UserMixin):
    pass


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            print(("User {} is not authenticated, "
                   "disconnecting").format(current_user))
#            disconnect()
            room = session.get('room')
            leave_room(room)
        else:
            return f(*args, **kwargs)
    return wrapped


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    update_room_idle(room)
    name = session.get('name')
#    sid = request.cookies.get(app.session_cookie_name)
    print("Room {} - Name {}".format(room, name))
    sid = session.sid
    print("Sessionid {}".format(sid))
    join_room(room)

    emit('status', {'msg': name + ' has entered the room.'}, room=room)
    # Sample message sent to just to the user who logged in
    emit('message',
         {'msg': "Hello " + name + " thanks for joining %s" % (request.sid)},
         room=request.sid)

    # add the user to the user list in sqlite
    query = room_members(room=room,
                         member_id=sid,
                         member_name=name,
                         spectator=True,
                         dm_room=request.sid)
    db.session.add(query)
    db.session.commit()
    # update_observer_status(room,sid)
    send_userlist(room)


@socketio.on('text', namespace='/chat')
@authenticated_only
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    update_room_idle(room)
    emit('message',
         {'msg': session.get('name') + ':' + message['msg']},
         room=room)


# @socketio.on('disconnect', namespace='/chat')
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
    db.session.query(room_members).filter_by(room=room, member_id=sid).delete()
    db.session.commit()
    send_userlist(room)


@socketio.on("observer", namespace="/chat")
@authenticated_only
def checkObserver(message):
    room = session.get('room')
    name = session.get('name')
    sid = session.sid
    listtmp = (db.session.query(room_members.spectator)
               .filter_by(room=room, member_id=sid).all())
    spec = [value for value, in listtmp]
    new_spec = None
    if spec[0] is True:
        new_spec = False
    else:
        new_spec = True
    print(("User {} wants to toggle "
          "their observer status "
           "from {} to {}").format(name, spec[0], new_spec))
    (
        db.session.query(room_members)
        .filter_by(room=room, member_id=sid)
        .update({room_members.spectator: new_spec})
    )
    db.session.commit()

    update_observer_status(room, sid)


def update_observer_status(room, sid):
    """
        Send the observer status to the client
        this is used on inital login
        and when the user toggles the status
    """
    listtmp = (
        db.session.query(room_members)
        .filter_by(room=room, member_id=sid)
        .all()
        )
    print(listtmp)
    for record in listtmp:
        Spec = None
        if record.spectator is True:
            Spec = "Spectator"
        else:
            Spec = "Player"
        emit('observer_status', Spec, room=record.dm_room)


@socketio.on("voted", namespace="/chat")
@authenticated_only
def checkVote(message):
    room = session.get('room')
    update_room_idle(room)
    emit("status", {"msg": message["voteChoice"]}, room=room)


def update_room_idle(room):
    # we may need to do something different here
    # expiring the key removes the data
    # but people could still be in the room
    pass


def send_userlist(room):
    # Get the mamber name from the room_members table filterd by the room
    userlisttmp = (
        db.session.query(room_members.member_name)
        .filter_by(room=room)
        .all())
    # cleanup the results to display
    userlist = [value for value, in userlisttmp]
    print("Userlist - {}".format(userlist))
    emit('userlist', userlist, room=room)

    # need to compare the sid's in the rooms table
    # with the sids in the session table
    # and remove any folks from rooms who's sessions have expired
