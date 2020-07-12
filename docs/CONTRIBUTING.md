## Rebase your fork after your pull request
```
~/Projects
$ cd Quartermaster-game/

 ~/Projects/Quartermaster-game (master)
$ git remote add upstream https://github.com/troop380/Quartermaster-game.git

 ~/Projects/Quartermaster-game (master)
$ git fetch upstream
From https://github.com/troop380/Quartermaster-game
 * [new branch]      master     -> upstream/master

 ~/Projects/Quartermaster-game (master)
$ git rebase upstream/master
Current branch master is up to date.

 ~/Projects/Quartermaster-game (master)
$
```

## Data Storage
### Client session data
You can store data in session for the user, this information is user specific and will not contribute to the game. We will use the session id from here to identify the user on the server side data. This session is configured to expire. This is managed by the flask-session library and the data is stored int he sessions table.
#### Getting Session Data
```
    room = session.get('room')
```
#### Setting Session Data
```
    session['room'] = form.room.data
```

### Server side game data
Game data should be stored using sqlalchemy. Sqlalchemy has lots of way to get and store data, some examples below.
#### Tables
Look at the table definitions in app/models.pl

#### Getting DB data
```
    # Get the mamber name from the room_members table filterd by the room
    userlisttmp = db.session.query(room_members.member_name).filter_by(room=room).all()
    # cleanup the results to display
    userlist = [value for value, in userlisttmp]
    print("Userlist - {}".format(userlist))
```
#### Saving DB data
```
    query = room_members(room = room, member_id = sid, member_name = name)
    db.session.add(query)
    db.session.commit()
```
