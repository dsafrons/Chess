# Chess (PyGame)

A two-player chess game written in Python with PyGame.  
`main.py` handles the window, board state, input, and rendering.  
`pieces.py` defines the piece classes and their legal moves.

## Features
- Standard 8×8 board with PNG piece sprites
- Piece classes: Pawn, Knight, Bishop, Rook, Queen, King
- Mouse-based drag-and-drop movement
- Special moves:
  - **Castling**
  - **En passant**
  - **Pawn promotion**
- Detection of check and checkmate

## Requirements
- Python 3.8+
- [pygame](https://pypi.org/project/pygame/)

Install with:
```pip install pygame```

## Project Structure
```
Chess/
├── main.py          # Game loop, input handling, rendering
├── pieces.py        # Piece classes + legal move logic
├── background.png   # Board background image
├── piece_images/    # Piece sprites (PNG format)
│   ├── bishop-b.png
│   ├── bishop-w.png
│   ├── king-b.png
│   ├── king-w.png
│   ├── knight-b.png
│   ├── knight-w.png
│   ├── pawn-b.png
│   ├── pawn-w.png
│   ├── queen-b.png
│   ├── queen-w.png
│   ├── rook-b.png
│   └── rook-w.png
├── README.md
└── .gitignore
```

## How to Play
- Run main.py to start the game.
- Use the mouse to click and drag pieces.
- The game enforces legal moves only.
- Checkmate ends the game (shown in console output).

## Possible Improvements
- Add stalemate detection
- Visual indicators for legal moves and last move
- Undo/redo with move history (PGN)
- Basic AI opponent
- GUI enhancements (menus, restart button, timers)
