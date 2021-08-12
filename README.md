# Python Chess Project

A chess game with graphic user interface

## Requirements:

* Python 3.*  
* $ pip install -r requirements.txt

## To get Started:

* Run main.py  
  (Please make sure the working directory is this chess folder!  
  Otherwise, chess_font.ttf might not get found by the Python interpreter.)  
* Left click to make chess moves  
* Right click to highlight squares  
  (Any left-clicks can cancel all highlights)  
* Press the U key to undo chess moves  
* Press left-arrow key and right-arrow key to rewind for previous positions  
  (Any mouse-clicks can return to the current position)

## Features:

* Builtin main menu and result page  
* A sidebar displaying game logs  
* Determine legal moves and dangerous squares  
  (Allow castling, en passant, and pawn promotion)  
  (Allow blocking or capturing dangerous source to escape checks)  
  (Ensure pieces pinned to their king move without surrendering the king)  
* Determine in-check, checkmate, and stalemate  
* Determine more draw conditions  
  (repetition, fifty-move, and impossibility of checkmate)  
* Highlight chess moves and checks  
* Highlight right-clicks  
* Allow undoing chess moves  
* Allow rewinding for previous positions

## Features to Implement in the Future:

* Add a chess engine  
* Allow scrolling in the sidebar  
* Read from and save as PGN