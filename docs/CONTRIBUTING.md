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
