import pygame
from pygame import gfxdraw
from sys import exit
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from math import floor


class Game:
    def __init__(self, display_surface, clock):
        # game setup from main
        self.display_surface = display_surface
        self.clock = clock

        # background
        self.background = pygame.image.load('background.png').convert_alpha()

        # game logic
        self.piece_dragged = None
        self.turn = 'white'
        self.latest_move = None
        self.black_in_check = 0
        self.white_in_check = 0
        self.blacks_possible_moves_cause_check = set()
        self.whites_possible_moves_cause_check = set()

        # board
        self.board = [['', ] * 8 for _ in range(8)]
        self.setup_board()
        self.update_piece_possible_moves()

    def setup_board(self):
        self.board[0][0] = Rook('rook', 'black', (0, 0))
        self.board[0][7] = Rook('rook', 'black', (0, 7))
        self.board[7][0] = Rook('rook', 'white', (7, 0))
        self.board[7][7] = Rook('rook', 'white', (7, 7))
        self.board[0][1] = Knight('knight', 'black', (0, 1))
        self.board[0][6] = Knight('knight', 'black', (0, 6))
        self.board[7][1] = Knight('knight', 'white', (7, 1))
        self.board[7][6] = Knight('knight', 'white', (7, 6))
        self.board[0][2] = Bishop('bishop', 'black', (0, 2))
        self.board[0][5] = Bishop('bishop', 'black', (0, 5))
        self.board[7][2] = Bishop('bishop', 'white', (7, 2))
        self.board[7][5] = Bishop('bishop', 'white', (7, 5))
        self.board[0][3] = Queen('queen', 'black', (0, 3))
        self.board[7][3] = Queen('queen', 'white', (7, 3))
        self.board[0][4] = King('king', 'black', (0, 4))
        self.board[7][4] = King('king', 'white', (7, 4))
        for i in range(8):
            self.board[1][i] = Pawn('pawn', 'black', (1, i))
        for i in range(8):
            self.board[6][i] = Pawn('pawn', 'white', (6, i))

    def draw_pieces(self):
        for row_index, row in enumerate(self.board):
            for col_index, piece in enumerate(row):
                if piece != '' and piece != self.piece_dragged:
                    pos = (col_index*100, row_index*100)
                    self.display_surface.blit(piece.image, pos)

                if piece != '' and (self.white_in_check or self.black_in_check) and self.piece_dragged == piece:
                    if self.white_in_check and piece.color == 'white':
                        for move in piece.possible_moves:
                            if (piece.piece, move) in self.whites_possible_moves_cause_check:
                                if self.board[move[0]][move[1]] != '':
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 - 1, move[0] * 100 + 1), (move[1] * 100 - 1, move[0] * 100 + 20 + 1), (move[1] * 100 + 20 - 1, move[0] * 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 + 99 - 1, move[0] * 100 + 1), (move[1] * 100 + 99 - 1, move[0] * 100 + 20 + 1), (move[1] * 100 + 99 - 20 - 1, move[0] * 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 - 1, move[0] * 100 + 100 + 1), (move[1] * 100 - 1, move[0] * 100 + 100 - 20 + 1), (move[1] * 100 + 20 - 1, move[0] * 100 + 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 + 99 - 1, move[0] * 100 + 100 + 1), (move[1] * 100 + 99 - 1, move[0] * 100 + 100 - 20 + 1), (move[1] * 100 + 99 - 20 - 1, move[0] * 100 + 100 + 1)])
                                else:
                                    pygame.gfxdraw.filled_circle(self.display_surface, move[1] * 100 + 50, move[0] * 100 + 50, 16, (131, 139, 139, 200))
                    elif self.black_in_check and piece.color == 'black':
                        for move in piece.possible_moves:
                            if (piece.piece, move) in self.blacks_possible_moves_cause_check:
                                if self.board[move[0]][move[1]] != '':
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 - 1, move[0] * 100 + 1), (move[1] * 100 - 1, move[0] * 100 + 20 + 1), (move[1] * 100 + 20 - 1, move[0] * 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 + 99 - 1, move[0] * 100 + 1), (move[1] * 100 + 99 - 1, move[0] * 100 + 20 + 1), (move[1] * 100 + 99 - 20 - 1, move[0] * 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 - 1, move[0] * 100 + 100 + 1), (move[1] * 100 - 1, move[0] * 100 + 100 - 20 + 1), (move[1] * 100 + 20 - 1, move[0] * 100 + 100 + 1)])
                                    pygame.draw.polygon(self.display_surface, 'grey', [(move[1] * 100 + 99 - 1, move[0] * 100 + 100 + 1), (move[1] * 100 + 99 - 1, move[0] * 100 + 100 - 20 + 1), (move[1] * 100 + 99 - 20 - 1, move[0] * 100 + 100 + 1)])
                                else:
                                    pygame.gfxdraw.filled_circle(self.display_surface, move[1] * 100 + 50, move[0] * 100 + 50, 16, (131, 139, 139, 200))

                elif piece != '' and self.piece_dragged == piece:
                    for pos in piece.possible_moves:
                        if self.move_legal((piece.pos[0], piece.pos[1]), (pos[0], pos[1])):
                            if self.board[pos[0]][pos[1]] != '':
                                pygame.draw.polygon(self.display_surface, 'grey', [(pos[1]*100-1, pos[0]*100+1), (pos[1]*100-1, pos[0]*100+20+1), (pos[1]*100+20-1, pos[0]*100+1)])
                                pygame.draw.polygon(self.display_surface, 'grey', [(pos[1] * 100 + 99 - 1, pos[0] * 100 + 1), (pos[1] * 100 + 99 - 1, pos[0] * 100 + 20 + 1), (pos[1] * 100 + 99 - 20 - 1, pos[0] * 100 + 1)])
                                pygame.draw.polygon(self.display_surface, 'grey', [(pos[1] * 100 - 1, pos[0] * 100 + 100 + 1), (pos[1] * 100 - 1, pos[0] * 100 + 100 - 20 + 1), (pos[1] * 100 + 20 - 1, pos[0] * 100 + 100 + 1)])
                                pygame.draw.polygon(self.display_surface, 'grey', [(pos[1] * 100 + 99 - 1, pos[0] * 100 + 100 + 1), (pos[1] * 100 + 99 - 1, pos[0] * 100 + 100 - 20 + 1), (pos[1] * 100 + 99 - 20 - 1, pos[0] * 100 + 100 + 1)])
                            else:
                                pygame.gfxdraw.filled_circle(self.display_surface, pos[1] * 100 + 50, pos[0] * 100 + 50, 16, (131, 139, 139, 200))

    def draw_board_background(self):
        self.display_surface.blit(self.background, (-2, 0))

    def during_drag_piece_img(self):
        if self.piece_dragged:
            dragged_piece_img = self.piece_dragged.image
            mouse_pos = pygame.mouse.get_pos()
            self.display_surface.blit(dragged_piece_img, (mouse_pos[0]-50, mouse_pos[1]-50))

    def swap_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    def update_piece_possible_moves(self):
        king_list = []
        for row_index, row in enumerate(self.board):
            for col_index, piece in enumerate(row):
                if piece != '':
                    if piece.piece == 'pawn':
                        piece.update_possible_moves(self.board, self.latest_move)
                    elif piece.piece == 'king':
                        king_list.append((piece, self.board))
                    else:
                        piece.update_possible_moves(self.board)

        for king in king_list:
            self.detect_check()
            king[0].update_possible_moves(king[1], self.possible_moves('black' if king[0].color == 'white' else 'white'), self.white_in_check, self.black_in_check)

    def do_move(self):
        ended_mouse_pos = pygame.mouse.get_pos()
        self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)] = self.board[self.piece_dragged.pos[0]][self.piece_dragged.pos[1]]
        self.latest_move = [self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)].piece,
                            (self.piece_dragged.pos[0], self.piece_dragged.pos[1]),
                            (floor(ended_mouse_pos[1] / 100), floor(ended_mouse_pos[0] / 100))]
        self.board[self.piece_dragged.pos[0]][self.piece_dragged.pos[1]] = ''
        # en passant
        if self.piece_dragged.piece == 'pawn' and self.piece_dragged.possible_moves.index((floor(
                ended_mouse_pos[1] / 100), floor(ended_mouse_pos[0] / 100))) == self.piece_dragged.en_passant_index:
            if self.piece_dragged.color == 'white':
                self.board[floor(ended_mouse_pos[1] / 100) + 1][floor(ended_mouse_pos[0] / 100)] = ''
            else:
                self.board[floor(ended_mouse_pos[1] / 100) - 1][floor(ended_mouse_pos[0] / 100)] = ''
        # castling
        if self.piece_dragged.piece == 'king' and abs(self.piece_dragged.pos[1] - floor(ended_mouse_pos[0] / 100)) == 2:
            # long
            if floor(ended_mouse_pos[0] / 100) == 2:
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) + 1] = self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)-2]
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) - 2] = ''
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) + 1].has_moved = True
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100 + 1)].update_position(self.board)
            # short
            elif floor(ended_mouse_pos[0] / 100) == 6:
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) - 1] = self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) + 1]
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) + 1] = ''
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100) - 1].has_moved = True
                self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100 - 1)].update_position(self.board)
        self.swap_turn()
        self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)].has_moved = True
        if self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)] != '':
            self.board[floor(ended_mouse_pos[1] / 100)][floor(ended_mouse_pos[0] / 100)].update_position(self.board)
        self.update_piece_possible_moves()

    def move_legal(self, starting, ending):
        if self.turn == 'white':
            new_piece = self.board[ending[0]][ending[1]]
            self.board[ending[0]][ending[1]] = self.board[starting[0]][starting[1]]
            old_piece = self.board[starting[0]][starting[1]]
            self.board[starting[0]][starting[1]] = ''

            for row_index, row in enumerate(self.board):
                for col_index, piece in enumerate(row):
                    if piece != '' and piece.color == 'black':
                        if piece.piece != 'pawn':
                            piece.update_possible_moves(self.board)
                        else:
                            piece.update_possible_moves(self.board, (self.board[ending[0]][ending[1]].piece, (starting[0], starting[1]), (ending[0], ending[1])))
            self.detect_check()

            # reverts board
            self.board[ending[0]][ending[1]] = new_piece
            self.board[starting[0]][starting[1]] = old_piece
            if self.board[ending[0]][ending[1]] != '':
                self.board[ending[0]][ending[1]].update_position(self.board)

            for row_index, row in enumerate(self.board):
                for col_index, piece in enumerate(row):
                    if piece != '' and piece.color == 'black':
                        if piece.piece != 'pawn':
                            piece.update_possible_moves(self.board)
                        else:
                            piece.update_possible_moves(self.board, self.latest_move)

            return not (self.white_in_check == 1 or self.white_in_check == 2)

        if self.turn == 'black':
            new_piece = self.board[ending[0]][ending[1]]
            self.board[ending[0]][ending[1]] = self.board[starting[0]][starting[1]]
            old_piece = self.board[starting[0]][starting[1]]
            self.board[starting[0]][starting[1]] = ''

            for row_index, row in enumerate(self.board):
                for col_index, piece in enumerate(row):
                    if piece != '' and piece.color == 'white':
                        if piece.piece != 'pawn':
                            piece.update_possible_moves(self.board)
                        else:
                            piece.update_possible_moves(self.board, (self.board[ending[0]][ending[1]].piece, (starting[0], starting[1]), (ending[0], ending[1])))
            self.detect_check()

            # reverts board
            self.board[ending[0]][ending[1]] = new_piece
            self.board[starting[0]][starting[1]] = old_piece
            if self.board[ending[0]][ending[1]] != '':
                self.board[ending[0]][ending[1]].update_position(self.board)

            for row_index, row in enumerate(self.board):
                for col_index, piece in enumerate(row):
                    if piece != '' and piece.color == 'white':
                        if piece.piece != 'pawn':
                            piece.update_possible_moves(self.board)
                        else:
                            piece.update_possible_moves(self.board, self.latest_move)

            return not (self.black_in_check == 1 or self.black_in_check == 2)

    def drag_pieces(self, event):
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                # drag started
                started_mouse_pos = pygame.mouse.get_pos()
                if self.board[floor(started_mouse_pos[1]/100)][floor(started_mouse_pos[0]/100)] != '' and self.board[floor(started_mouse_pos[1]/100)][floor(started_mouse_pos[0]/100)].color == self.turn:
                    self.piece_dragged = self.board[floor(started_mouse_pos[1]/100)][floor(started_mouse_pos[0]/100)]
            if ev.type == pygame.MOUSEBUTTONUP:
                # drag ended
                ended_mouse_pos = pygame.mouse.get_pos()
                if self.piece_dragged and self.piece_dragged.pos != (floor(ended_mouse_pos[1]/100), floor(ended_mouse_pos[0]/100)) and (floor(ended_mouse_pos[1]/100), floor(ended_mouse_pos[0]/100)) in self.piece_dragged.possible_moves:
                    if self.white_in_check:
                        if (self.piece_dragged.piece, (floor(ended_mouse_pos[1]/100), floor(ended_mouse_pos[0]/100))) in self.whites_possible_moves_cause_check:
                            self.do_move()
                            self.whites_possible_moves_cause_check = set()
                    elif self.black_in_check:
                        if (self.piece_dragged.piece, (floor(ended_mouse_pos[1] / 100), floor(ended_mouse_pos[0] / 100))) in self.blacks_possible_moves_cause_check:
                            self.do_move()
                            self.blacks_possible_moves_cause_check = set()
                    else:
                        if self.move_legal((self.piece_dragged.pos[0], self.piece_dragged.pos[1]), (floor(ended_mouse_pos[1] / 100), floor(ended_mouse_pos[0] / 100))):
                            self.do_move()
                            self.detect_check()


                    self.detect_check()
                    if self.white_in_check == 1 or self.white_in_check == 2:
                        if self.white_in_check == 2:
                            king_can_only_avoid = True
                        else:
                            king_can_only_avoid = False
                        color_checked = 'white'
                        color_checking = 'black'
                        for move in self.possible_moves(color_checked):
                            piece_poses_can_make_move = []
                            for row_index, row in enumerate(self.board):
                                for col_index, piece in enumerate(row):
                                    if piece != '' and move in piece.possible_moves and piece.color == color_checked:
                                        piece_poses_can_make_move.append((row_index, col_index))

                            for piece_pos in piece_poses_can_make_move:
                                did_en_passant = False
                                en_passanted_piece = None
                                if self.board[piece_pos[0]][piece_pos[1]].piece == 'pawn' and self.board[piece_pos[0]][piece_pos[1]].possible_moves.index((move[0], move[1])) == self.board[piece_pos[0]][piece_pos[1]].en_passant_index:
                                    if self.board[piece_pos[0]][piece_pos[1]].color == 'white':
                                        en_passanted_piece = self.board[move[0] + 1][move[1]]
                                        self.board[move[0] + 1][move[1]] = ''
                                    else:
                                        en_passanted_piece = self.board[move[0] - 1][move[1]]
                                        self.board[move[0] - 1][move[1]] = ''
                                    did_en_passant = True

                                new_piece = self.board[move[0]][move[1]]
                                self.board[move[0]][move[1]] = self.board[piece_pos[0]][piece_pos[1]]
                                old_piece = self.board[piece_pos[0]][piece_pos[1]]
                                self.board[piece_pos[0]][piece_pos[1]] = ''


                                for row_index, row in enumerate(self.board):
                                    for col_index, piece in enumerate(row):
                                        if piece != '' and piece.color == color_checking:
                                            if piece.piece != 'pawn':
                                                piece.update_possible_moves(self.board)
                                            else:
                                                piece.update_possible_moves(self.board, (self.board[move[0]][move[1]].piece, (piece_pos[0], piece_pos[1]), (move[0], move[1])))
                                self.detect_check()

                                # reverts board
                                if did_en_passant:
                                    if self.board[move[0]][move[1]].color == 'white':
                                        self.board[move[0] + 1][move[1]] = en_passanted_piece
                                    else:
                                        self.board[move[0] - 1][move[1]] = en_passanted_piece
                                self.board[move[0]][move[1]] = new_piece
                                self.board[piece_pos[0]][piece_pos[1]] = old_piece
                                if self.board[move[0]][move[1]] != '':
                                    self.board[move[0]][move[1]].update_position(self.board)


                                for row_index, row in enumerate(self.board):
                                    for col_index, piece in enumerate(row):
                                        if piece != '' and piece.color == color_checking:
                                            if piece.piece != 'pawn':
                                                piece.update_possible_moves(self.board)
                                            else:
                                                piece.update_possible_moves(self.board, self.latest_move)

                                if self.white_in_check == 0:
                                    if king_can_only_avoid:
                                        if self.board[piece_pos[0]][piece_pos[1]].piece == 'king':
                                            self.whites_possible_moves_cause_check.add((self.board[piece_pos[0]][piece_pos[1]].piece, (move[0], move[1])))
                                    else:
                                        self.whites_possible_moves_cause_check.add((self.board[piece_pos[0]][piece_pos[1]].piece, (move[0], move[1])))
                        self.detect_check()

                    if self.black_in_check == 1 or self.black_in_check == 2:
                        if self.black_in_check == 2:
                            king_can_only_avoid = True
                        else:
                            king_can_only_avoid = False
                        color_checked = 'black'
                        color_checking = 'white'
                        for move in self.possible_moves(color_checked):
                            piece_poses_can_make_move = []
                            for row_index, row in enumerate(self.board):
                                for col_index, piece in enumerate(row):
                                    if piece != '' and move in piece.possible_moves and piece.color == color_checked:
                                        piece_poses_can_make_move.append((row_index, col_index))

                            for piece_pos in piece_poses_can_make_move:
                                did_en_passant = False
                                en_passanted_piece = None
                                if self.board[piece_pos[0]][piece_pos[1]].piece == 'pawn' and self.board[piece_pos[0]][piece_pos[1]].possible_moves.index((move[0], move[1])) == self.board[piece_pos[0]][piece_pos[1]].en_passant_index:
                                    if self.board[piece_pos[0]][piece_pos[1]].color == 'white':
                                        en_passanted_piece = self.board[move[0] + 1][move[1]]
                                        self.board[move[0] + 1][move[1]] = ''
                                    else:
                                        en_passanted_piece = self.board[move[0] - 1][move[1]]
                                        self.board[move[0] - 1][move[1]] = ''
                                    did_en_passant = True

                                new_piece = self.board[move[0]][move[1]]
                                self.board[move[0]][move[1]] = self.board[piece_pos[0]][piece_pos[1]]
                                old_piece = self.board[piece_pos[0]][piece_pos[1]]
                                self.board[piece_pos[0]][piece_pos[1]] = ''

                                for row_index, row in enumerate(self.board):
                                    for col_index, piece in enumerate(row):
                                        if piece != '' and piece.color == color_checking:
                                            if piece.piece != 'pawn':
                                                piece.update_possible_moves(self.board)
                                            else:
                                                piece.update_possible_moves(self.board, (self.board[move[0]][move[1]].piece, (piece_pos[0], piece_pos[1]), (move[0], move[1])))
                                self.detect_check()

                                # reverts board
                                if did_en_passant:
                                    if self.board[move[0]][move[1]].color == 'white':
                                        self.board[move[0] + 1][move[1]] = en_passanted_piece
                                    else:
                                        self.board[move[0] - 1][move[1]] = en_passanted_piece
                                self.board[move[0]][move[1]] = new_piece
                                self.board[piece_pos[0]][piece_pos[1]] = old_piece
                                if self.board[move[0]][move[1]] != '':
                                    self.board[move[0]][move[1]].update_position(self.board)

                                for row_index, row in enumerate(self.board):
                                    for col_index, piece in enumerate(row):
                                        if piece != '' and piece.color == color_checking:
                                            if piece.piece != 'pawn':
                                                piece.update_possible_moves(self.board)
                                            else:
                                                piece.update_possible_moves(self.board, self.latest_move)

                                if self.black_in_check == 0:
                                    if king_can_only_avoid:
                                        if self.board[piece_pos[0]][piece_pos[1]].piece == 'king':
                                            self.blacks_possible_moves_cause_check.add((self.board[piece_pos[0]][piece_pos[1]].piece, (move[0], move[1])))
                                    else:
                                        self.blacks_possible_moves_cause_check.add((self.board[piece_pos[0]][piece_pos[1]].piece, (move[0], move[1])))
                        self.detect_check()

                self.piece_dragged = None

    def check_pawn_promotion(self):
        for row_index, row in enumerate(self.board):
            for col_index, piece in enumerate(row):
                if row_index == 0 or row_index == 7:
                    if piece != '' and piece.piece == 'pawn' and row_index == 0:
                        self.board[row_index][col_index] = Piece('queen', 'white', (row_index, col_index))
                    if piece != '' and piece.piece == 'pawn' and row_index == 7:
                        self.board[row_index][col_index] = Piece('queen', 'black', (row_index, col_index))
                else:
                    continue

    def detect_checkmate(self):
        if self.white_in_check and len(self.whites_possible_moves_cause_check) == 0:
            print('white got checkmated')
        elif self.black_in_check and len(self.blacks_possible_moves_cause_check) == 0:
            print('black got checkmated')

    def possible_moves(self, color):
        possible_moves_for_color = []
        for row_index, row in enumerate(self.board):
            for col_index, piece in enumerate(row):
                if piece != '' and piece.color == color:
                    for move in piece.possible_moves:
                        possible_moves_for_color.append(move)

        return possible_moves_for_color

    def piece_pos(self, piece_to_find, color):
        for row_index, row in enumerate(self.board):
            for col_index, piece in enumerate(row):
                if piece != '' and piece.piece == piece_to_find and piece.color == color:
                    return row_index, col_index

    def detect_check(self):
        if self.piece_pos('king', 'white') in self.possible_moves('black'):
            self.white_in_check = self.possible_moves('black').count(self.piece_pos('king', 'white'))
        else:
            self.white_in_check = 0

        if self.piece_pos('king', 'black') in self.possible_moves('white'):
            self.black_in_check = self.possible_moves('white').count(self.piece_pos('king', 'black'))
        else:
            self.black_in_check = 0

    def update(self, event):
        self.drag_pieces(event)

        self.draw_board_background()
        self.draw_pieces()
        self.during_drag_piece_img()
        self.check_pawn_promotion()
        self.detect_check()
        self.detect_checkmate()


class Main:
    def __init__(self):
        # pygame inits`
        pygame.init()
        self.display_surface = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        # game initialization
        self.game = Game(self.display_surface, self.clock)

    def run(self):
        while True:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.game.update(ev)

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
