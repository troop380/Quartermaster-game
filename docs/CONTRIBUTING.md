## Setting up you development environment
It you are familiar with how to work with python code, you can skip this section

### Tools to download
There are various options for a numbe of these, feel free to use a replacement that works for you
#### Git
Download the git client for your platform from https://git-scm.com/
You can accept the prompts during the install, there are a lot of prompts
#### Pyhton
Download the latest version of python https://www.python.org/downloads/
During the install there should be an option to add python to the prompt. This is not required, but will give you more options later.
#### Editor
There are a lot of options here
##### VScode
##### Atom

### Setting up development environment
I like to check out all the project I have into a project folder somewhere in my home directory. If this is the only project you are working on, any directory will do. You will need to clone the github repo. Launch the git-bash program and execute the following, if you will be putting the code in a different directory, make sure to 'cd' to the directory of you choosing before running the git clone.
```
git clone https://github.com/troop380/Quartermaster-game.git
```

You can make edits on you local machine, you will need to install Python as well as the required libraries through pip
```
pip install -r requirements.txt
```
Or, if you did not add python to the path when you installed it, you should be able to run it with the following
```
py -3 -m pip install -r requirements.txt
```

To run the server
```
python chat.py
```
Or, if you did not add python to the path when you installed it, you should be able to run it with the following
```
py -3 chat.py
```

At this point you should be able to connect to http://localhost:5000 in your local browser. You could connect from other conputers on your local network or from the internet if you setup port redirection on you internet firewall.

## Rebase your fork after your pull request
```
$ cd Quartermaster-game/

 ~/Quartermaster-game (master)
$ git remote add upstream https://github.com/troop380/Quartermaster-game.git

 ~/Quartermaster-game (master)
$ git fetch upstream
From https://github.com/troop380/Quartermaster-game
 * [new branch]      master     -> upstream/master

 ~/Quartermaster-game (master)
$ git rebase upstream/master
Current branch master is up to date.

 ~/Quartermaster-game (master)
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
