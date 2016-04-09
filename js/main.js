"use strict"

const url = "ws://127.0.0.1:8888/ws";

const cells = [];
let playerCell = null;
let webSocket = null;

const initView = ()=>{
  const board = document.getElementById("board");
  const cell = document.getElementById("cell");
  const indicator = document.getElementById("indicator");
  const row = document.getElementById("row");
  
  for(let y in [0,1,2,3,4,5,6,7,8]){
    let r = row.cloneNode(true);
    for(let x in [0,1,2,3,4,5,6,7,8]){
      var c = null;
      if(x==0 && y == 0){
        c = cell.cloneNode(true);
        playerCell = c;
      }else if(x==0 || y==0){
        c = indicator.cloneNode(true);
        if(x==0){
          c.textContent = "ABCDEFGH".charAt(y-1);
        }else{
          c.textContent = "12345678".charAt(x-1);
        }
      }else{
        c = cell.cloneNode(true);
        const _x = x-1;
        const _y = y-1;
        c.onclick = ()=>{
          handleClick(_x,_y);
        }
        cells.push(c);
      }
      r.appendChild(c);
    }
    board.appendChild(r);
  }
};

const updateView = (player, board)=>{
  updateCell(playerCell, player);
  board.forEach((v, i)=>{
    updateCell(cells[i], v);
  });
};

const updateCell = (cell, player)=>{
  if(player == 0){
    cell.className = "cell";
  }else if(player == -1){
    cell.className = "cell white";
  }else{
    cell.className = "cell black";
  }
};

const handle = (event)=>{
  if(event && event.data){
    const json = JSON.parse(event.data);
    const command = json.command;
    
    console.log(json)
    
    switch(command){
      case "update":
        updateView(json.player, json.board);
        break;
      case "judge":
        if(json.winner == -1){
          alert("White won.");
        }else if(json.winner == 1){
          alert("Black won.");
        }else{
          alert("Draw.");
        }
        break;
      case "error":
        console.log("error:", json["message"]);
        break;
      default:
        console.log("invalid command:", command);
        break;
    }
  }
};

const handleClick = (x, y)=>{
  const json = {command: "put", position:[x,y]};
  
  webSocket.send(JSON.stringify(json));
};



onload = ()=>{
  
  initView();
  
  webSocket = new WebSocket(url);
  webSocket.onopen = ()=>{
    console.log("WebSocket Opened.");
  };
  webSocket.onmessage = handle;
  webSocket.onclose = ()=>{
    alert("WebSocket Closed.")
    console.log("WebSocket Closed.");
  };
  webSocket.onerror = (event)=>{
    console.log("error:"+event);
  };
  
  document.getElementById("ai").onchange = ()=>{
    const ai = document.getElementById("ai").value;
    const json = {command: "ai", "ai":ai};
    webSocket.send(JSON.stringify(json));
  };
  
  const restart = (side)=>{
    return ()=>{
      const json = {command: "restart", "side":side};
      webSocket.send(JSON.stringify(json));
    };
  };
  document.getElementById("restart_black").onclick = restart(1);
  document.getElementById("restart_white").onclick = restart(-1);
};