# JSON specifications


## From Client

### {command:"restart", side: side}
Initialize board and set player.  
Abandon now playing game.

### {command:"put", put:[x,y]}
Put on (x,y).

### {command:"ai", ai: ai}
Change AI behavior.  
ai = ["MTS", "RND", "NN"].

---

## From Server

### {command:"update", player: player, board: [[board]]}
Update board.

### {command: "judge", win: player}
Send which player is the winner.

###{command: "error", message: "msg"}
Error notification.