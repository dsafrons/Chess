import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self, piece, color, position):
        super().__init__()

        self.piece = piece
        self.color = color
        self.pos = position
        self.has_moved = False
        self.possible_moves = []

        self.image = pygame.image.load(f'piece_images/{self.piece}-{self.color[0]}.png').convert_alpha()

    def update_position(self, board):
        for row_index, row in enumerate(board):
            for col_index, piece in enumerate(row):
                if piece == self:
                    self.pos = (row_index, col_index)


class Pawn(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)
        self.en_passant_index = None

    def update_possible_moves(self, board, last_move):
        self.possible_moves = []
        self.en_passant_index = None
        if self.color == 'white':
            # up one
            if self.pos[0] - 1 >= 0 and board[self.pos[0]-1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]))
            # up two
            if not self.has_moved and self.pos[0] - 2 >= 0 and board[self.pos[0]-2][self.pos[1]] == '' and board[self.pos[0]-1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0]-2, self.pos[1]))
            # take top right
            if self.pos[0] - 1 >= 0 and self.pos[1] + 1 <= 7 and board[self.pos[0] - 1][self.pos[1] + 1] != '' and board[self.pos[0] - 1][self.pos[1] + 1].color == 'black':
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] + 1))
            # take top left
            if self.pos[0] - 1 >= 0 and self.pos[1] - 1 >= 0 and board[self.pos[0] - 1][self.pos[1] - 1] != '' and board[self.pos[0] - 1][self.pos[1] - 1].color == 'black':
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] - 1))
            # en passant
            if last_move and self.pos[0] == last_move[2][0] and last_move[0] == 'pawn' and abs(last_move[1][0] - last_move[2][0]) == 2 and (self.pos[1] + 1 == last_move[2][1] or self.pos[1] - 1 == last_move[2][1]) and board[last_move[2][0]][last_move[2][1]].color == 'black':
                if self.pos[1] + 1 == last_move[2][1]:
                    self.possible_moves.append((self.pos[0]-1, self.pos[1] + 1))
                    self.en_passant_index = self.possible_moves.index((self.pos[0] - 1, self.pos[1] + 1))
                else:
                    self.possible_moves.append((self.pos[0]-1, self.pos[1] - 1))
                    self.en_passant_index = self.possible_moves.index((self.pos[0]-1, self.pos[1] - 1))
        else:
            # up one
            if self.pos[0] + 1 <= 7 and board[self.pos[0] + 1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1]))
            # up two
            if not self.has_moved and self.pos[0] + 2 <= 7 and board[self.pos[0] + 2][self.pos[1]] == '' and board[self.pos[0] + 1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0] + 2, self.pos[1]))
            # take bottom left
            if self.pos[0] + 1 <= 7 and self.pos[1] - 1 >= 0 and board[self.pos[0] + 1][self.pos[1] - 1] != '' and board[self.pos[0] + 1][self.pos[1] - 1].color == 'white':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] - 1))
            # take bottom right
            if self.pos[0] + 1 <= 7 and self.pos[1] + 1 <= 7 and board[self.pos[0] + 1][self.pos[1] + 1] != '' and board[self.pos[0] + 1][self.pos[1] + 1].color == 'white':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] + 1))
            # en passant
            if last_move and self.pos[0] == last_move[2][0] and last_move[0] == 'pawn' and abs(last_move[1][0] - last_move[2][0]) == 2 and (self.pos[1] + 1 == last_move[2][1] or self.pos[1] - 1 == last_move[2][1]) and board[last_move[2][0]][last_move[2][1]].color == 'white':
                if self.pos[1] + 1 == last_move[2][1]:
                    self.possible_moves.append((self.pos[0]+1, self.pos[1] + 1))
                    self.en_passant_index = self.possible_moves.index((self.pos[0]+1, self.pos[1] + 1))
                else:
                    self.possible_moves.append((self.pos[0]+1, self.pos[1] - 1))
                    self.en_passant_index = self.possible_moves.index((self.pos[0]+1, self.pos[1] - 1))


class Knight(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)

    def update_possible_moves(self, board):
        self.possible_moves = []
        # left 2 up 1
        if self.pos[1] - 2 >= 0 and self.pos[0] - 1 >= 0:
            if board[self.pos[0]-1][self.pos[1]-2] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]-2))
            elif board[self.pos[0]-1][self.pos[1]-2].color != self.color:
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] - 2))
        # left 1 up 2
        if self.pos[1] - 1 >= 0 and self.pos[0] - 2 >= 0:
            if board[self.pos[0]-2][self.pos[1]-1] == '':
                self.possible_moves.append((self.pos[0]-2, self.pos[1]-1))
            elif board[self.pos[0]-2][self.pos[1]-1].color != self.color:
                self.possible_moves.append((self.pos[0] - 2, self.pos[1] - 1))
        # right 2 up 1
        if self.pos[1] + 2 <= 7 and self.pos[0] - 1 >= 0:
            if board[self.pos[0]-1][self.pos[1]+2] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]+2))
            elif board[self.pos[0]-1][self.pos[1]+2].color != self.color:
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] + 2))
        # right 1 up 2
        if self.pos[1] + 1 <= 7 and self.pos[0] - 2 >= 0:
            if board[self.pos[0]-2][self.pos[1]+1] == '':
                self.possible_moves.append((self.pos[0]-2, self.pos[1]+1))
            elif board[self.pos[0]-2][self.pos[1]+1].color != self.color:
                self.possible_moves.append((self.pos[0] - 2, self.pos[1] + 1))
        # left 2 down 1
        if self.pos[1] - 2 >= 0 and self.pos[0] + 1 <= 7:
            if board[self.pos[0]+1][self.pos[1]-2] == '':
                self.possible_moves.append((self.pos[0]+1, self.pos[1]-2))
            elif board[self.pos[0]+1][self.pos[1]-2].color != self.color:
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] - 2))
        # left 1 down 2
        if self.pos[1] - 1 >= 0 and self.pos[0] + 2 <= 7:
            if board[self.pos[0]+2][self.pos[1]-1] == '':
                self.possible_moves.append((self.pos[0]+2, self.pos[1]-1))
            elif board[self.pos[0]+2][self.pos[1]-1].color != self.color:
                self.possible_moves.append((self.pos[0] + 2, self.pos[1] - 1))
        # right 2 down 1
        if self.pos[1] + 2 <= 7 and self.pos[0] + 1 <= 7:
            if board[self.pos[0]+1][self.pos[1]+2] == '':
                self.possible_moves.append((self.pos[0]+1, self.pos[1]+2))
            elif board[self.pos[0]+1][self.pos[1]+2].color != self.color:
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] + 2))
        # right 1 down 2
        if self.pos[1] + 1 <= 7 and self.pos[0] + 2 <= 7:
            if board[self.pos[0]+2][self.pos[1]+1] == '':
                self.possible_moves.append((self.pos[0]+2, self.pos[1]+1))
            elif board[self.pos[0]+2][self.pos[1]+1].color != self.color:
                self.possible_moves.append((self.pos[0] + 2, self.pos[1] + 1))


class Bishop(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)

    def update_possible_moves(self, board):
        self.possible_moves = []
        for i in range(1, 8):
            if self.pos[1] - i >= 0 and self.pos[0] - i >= 0:
                if board[self.pos[0]-i][self.pos[1]-i] == '':
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]-i))
                elif board[self.pos[0]-i][self.pos[1]-i].color == self.color:
                    break
                elif board[self.pos[0]-i][self.pos[1]-i].color != self.color:
                    self.possible_moves.append((self.pos[0] - i, self.pos[1] - i))
                    break
        for i in range(1, 8):
            if self.pos[1] - i >= 0 and self.pos[0] + i <= 7:
                if board[self.pos[0]+i][self.pos[1]-i] == '':
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]-i))
                elif board[self.pos[0]+i][self.pos[1]-i].color == self.color:
                    break
                elif board[self.pos[0]+i][self.pos[1]-i].color != self.color:
                    self.possible_moves.append((self.pos[0] + i, self.pos[1] - i))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7 and self.pos[0] - i >= 0:
                if board[self.pos[0]-i][self.pos[1]+i] == '':
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]+i))
                elif board[self.pos[0]-i][self.pos[1]+i].color == self.color:
                    break
                elif board[self.pos[0]-i][self.pos[1]+i].color != self.color:
                    self.possible_moves.append((self.pos[0] - i, self.pos[1] + i))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7 and self.pos[0] + i <= 7:
                if board[self.pos[0]+i][self.pos[1]+i] == '':
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]+i))
                elif board[self.pos[0]+i][self.pos[1]+i].color == self.color:
                    break
                elif board[self.pos[0]+i][self.pos[1]+i].color != self.color:
                    self.possible_moves.append((self.pos[0] + i, self.pos[1] + i))
                    break


class Rook(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)

    def update_possible_moves(self, board):
        self.possible_moves = []
        for i in range(1, 8):
            if self.pos[1] - i >= 0:
                if board[self.pos[0]][self.pos[1]-i] == '':
                    self.possible_moves.append((self.pos[0], self.pos[1]-i))
                elif board[self.pos[0]][self.pos[1]-i].color == self.color:
                    break
                elif board[self.pos[0]][self.pos[1]-i].color != self.color:
                    self.possible_moves.append((self.pos[0], self.pos[1]-i))
                    break
        for i in range(1, 8):
            if self.pos[0] - i >= 0:
                if board[self.pos[0]-i][self.pos[1]] == '':
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]))
                elif board[self.pos[0]-i][self.pos[1]].color == self.color:
                    break
                elif board[self.pos[0]-i][self.pos[1]].color != self.color:
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7:
                if board[self.pos[0]][self.pos[1]+i] == '':
                    self.possible_moves.append((self.pos[0], self.pos[1]+i))
                elif board[self.pos[0]][self.pos[1]+i].color == self.color:
                    break
                elif board[self.pos[0]][self.pos[1]+i].color != self.color:
                    self.possible_moves.append((self.pos[0], self.pos[1]+i))
                    break
        for i in range(1, 8):
            if self.pos[0] + i <= 7:
                if board[self.pos[0]+i][self.pos[1]] == '':
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]))
                elif board[self.pos[0]+i][self.pos[1]].color == self.color:
                    break
                elif board[self.pos[0]+i][self.pos[1]].color != self.color:
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]))
                    break


class Queen(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)

    def update_possible_moves(self, board):
        self.possible_moves = []
        for i in range(1, 8):
            if self.pos[1] - i >= 0:
                if board[self.pos[0]][self.pos[1] - i] == '':
                    self.possible_moves.append((self.pos[0], self.pos[1] - i))
                elif board[self.pos[0]][self.pos[1] - i].color == self.color:
                    break
                elif board[self.pos[0]][self.pos[1] - i].color != self.color:
                    self.possible_moves.append((self.pos[0], self.pos[1] - i))
                    break
        for i in range(1, 8):
            if self.pos[0] - i >= 0:
                if board[self.pos[0] - i][self.pos[1]] == '':
                    self.possible_moves.append((self.pos[0] - i, self.pos[1]))
                elif board[self.pos[0] - i][self.pos[1]].color == self.color:
                    break
                elif board[self.pos[0] - i][self.pos[1]].color != self.color:
                    self.possible_moves.append((self.pos[0] - i, self.pos[1]))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7:
                if board[self.pos[0]][self.pos[1] + i] == '':
                    self.possible_moves.append((self.pos[0], self.pos[1] + i))
                elif board[self.pos[0]][self.pos[1] + i].color == self.color:
                    break
                elif board[self.pos[0]][self.pos[1] + i].color != self.color:
                    self.possible_moves.append((self.pos[0], self.pos[1] + i))
                    break
        for i in range(1, 8):
            if self.pos[0] + i <= 7:
                if board[self.pos[0] + i][self.pos[1]] == '':
                    self.possible_moves.append((self.pos[0] + i, self.pos[1]))
                elif board[self.pos[0] + i][self.pos[1]].color == self.color:
                    break
                elif board[self.pos[0] + i][self.pos[1]].color != self.color:
                    self.possible_moves.append((self.pos[0] + i, self.pos[1]))
                    break
        for i in range(1, 8):
            if self.pos[1] - i >= 0 and self.pos[0] - i >= 0:
                if board[self.pos[0]-i][self.pos[1]-i] == '':
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]-i))
                elif board[self.pos[0]-i][self.pos[1]-i].color == self.color:
                    break
                elif board[self.pos[0]-i][self.pos[1]-i].color != self.color:
                    self.possible_moves.append((self.pos[0] - i, self.pos[1] - i))
                    break
        for i in range(1, 8):
            if self.pos[1] - i >= 0 and self.pos[0] + i <= 7:
                if board[self.pos[0]+i][self.pos[1]-i] == '':
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]-i))
                elif board[self.pos[0]+i][self.pos[1]-i].color == self.color:
                    break
                elif board[self.pos[0]+i][self.pos[1]-i].color != self.color:
                    self.possible_moves.append((self.pos[0] + i, self.pos[1] - i))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7 and self.pos[0] - i >= 0:
                if board[self.pos[0]-i][self.pos[1]+i] == '':
                    self.possible_moves.append((self.pos[0]-i, self.pos[1]+i))
                elif board[self.pos[0]-i][self.pos[1]+i].color == self.color:
                    break
                elif board[self.pos[0]-i][self.pos[1]+i].color != self.color:
                    self.possible_moves.append((self.pos[0] - i, self.pos[1] + i))
                    break
        for i in range(1, 8):
            if self.pos[1] + i <= 7 and self.pos[0] + i <= 7:
                if board[self.pos[0]+i][self.pos[1]+i] == '':
                    self.possible_moves.append((self.pos[0]+i, self.pos[1]+i))
                elif board[self.pos[0]+i][self.pos[1]+i].color == self.color:
                    break
                elif board[self.pos[0]+i][self.pos[1]+i].color != self.color:
                    self.possible_moves.append((self.pos[0] + i, self.pos[1] + i))
                    break


class King(Piece):
    def __init__(self, piece, color, position):
        super().__init__(piece, color, position)

    def update_possible_moves(self, *args):
        board = args[0]
        self.possible_moves = []
        # top left
        if self.pos[1] - 1 >= 0 and self.pos[0] - 1 >= 0:
            if board[self.pos[0] - 1][self.pos[1] - 1] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]-1))
            elif board[self.pos[0] - 1][self.pos[1] - 1].color != self.color:
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] - 1))
        # top
        if self.pos[0] - 1 >= 0:
            if board[self.pos[0] - 1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]))
            elif board[self.pos[0] - 1][self.pos[1]].color != self.color:
                self.possible_moves.append((self.pos[0] - 1, self.pos[1]))
        # top right
        if self.pos[1] + 1 <= 7 and self.pos[0] - 1 >= 0:
            if board[self.pos[0] - 1][self.pos[1] + 1] == '':
                self.possible_moves.append((self.pos[0]-1, self.pos[1]+1))
            elif board[self.pos[0] - 1][self.pos[1] + 1].color != self.color:
                self.possible_moves.append((self.pos[0] - 1, self.pos[1] + 1))
        # right
        if self.pos[1] + 1 <= 7:
            if board[self.pos[0]][self.pos[1]+1] == '':
                self.possible_moves.append((self.pos[0], self.pos[1]+1))
            elif board[self.pos[0]][self.pos[1]+1].color != self.color:
                self.possible_moves.append((self.pos[0], self.pos[1]+1))
        # left
        if self.pos[1] - 1 >= 0:
            if board[self.pos[0]][self.pos[1] - 1] == '':
                self.possible_moves.append((self.pos[0], self.pos[1] - 1))
            elif board[self.pos[0]][self.pos[1] - 1].color != self.color:
                self.possible_moves.append((self.pos[0], self.pos[1] - 1))
        # bottom left
        if self.pos[1] - 1 >= 0 and self.pos[0] + 1 <= 7:
            if board[self.pos[0] + 1][self.pos[1] - 1] == '':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] - 1))
            elif board[self.pos[0] + 1][self.pos[1] - 1].color != self.color:
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] - 1))
        # bottom
        if self.pos[0] + 1 <= 7:
            if board[self.pos[0] + 1][self.pos[1]] == '':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1]))
            elif board[self.pos[0] + 1][self.pos[1]].color != self.color:
                self.possible_moves.append((self.pos[0] + 1, self.pos[1]))
        # bottom right
        if self.pos[1] + 1 <= 7 and self.pos[0] + 1 <= 7:
            if board[self.pos[0] + 1][self.pos[1] + 1] == '':
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] + 1))
            elif board[self.pos[0] + 1][self.pos[1] + 1].color != self.color:
                self.possible_moves.append((self.pos[0] + 1, self.pos[1] + 1))

        if len(args) == 4:
            possible_moves = args[1]
            white_in_check = args[2]
            black_in_check = args[3]
            if (self.color == 'black' and not black_in_check) or (self.color == 'white' and not white_in_check):
                if not self.has_moved and board[self.pos[0]][7] != '' and board[self.pos[0]][7].piece == 'rook' and board[self.pos[0]][7].color == self.color and not board[self.pos[0]][7].has_moved and board[self.pos[0]][5] == '' and board[self.pos[0]][6] == '' and (self.pos[0], 5) not in possible_moves:
                    self.possible_moves.append((self.pos[0], self.pos[1] + 2))
                if not self.has_moved and board[self.pos[0]][0] != '' and board[self.pos[0]][0].piece == 'rook' and board[self.pos[0]][0].color == self.color and not board[self.pos[0]][0].has_moved and board[self.pos[0]][3] == '' and board[self.pos[0]][2] == '' and board[self.pos[0]][1] == '' and (self.pos[0], 3) not in possible_moves and (self.pos[0], 2) not in possible_moves:
                    self.possible_moves.append((self.pos[0], self.pos[1] - 2))
