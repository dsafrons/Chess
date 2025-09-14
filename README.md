Chess (Python)

A simple chess game implemented in Python. Clean code, minimal dependencies, and clear separation between board/pieces logic and the UI layer.

Features

- Standard chess rules (pieces, legal moves, turn order)
- Board and piece sprites loaded from local assets
- Single-player hot-seat (two people on one keyboard/mouse)
- Simple, readable code split into main.py and pieces.py for easy extension

How to play

- Click a piece to see/select a move.
- Click a target square to move.
- Turn alternates between White and Black.

Code overview
pieces.py

- Defines classes for each piece (e.g., Pawn, Rook, Knight, Bishop, Queen, King)
- Encapsulates move generation and legality checks
- Keeps piece symbols, colors, and movement vectors together for clarity

main.py

- Initializes the window, board state, and assets (background.png, piece_images/*)
- Handles input events (mouse and keys)
- Renders board and pieces
- Calls piece/board logic to validate moves and update game state

Assets

- background.png for the board background
- piece_images/ for piece sprites
