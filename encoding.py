import numpy as np
import chess

def get_reach_and_attack(board, position_dict, turn):
  # gets reachability and attacking squares for 'turn' colored pieces
  reach = ''
  attack = ''

  board.turn = turn
  legal_moves = [str(x) for x in list(board.legal_moves)]
  for mv in legal_moves:
    if mv[2:] in position_dict:
      # attacking
      attack += position_dict[mv[:2]] + '>' + position_dict[mv[2:]] + mv[2:] + ' '
    else:
      # reachable
      weight = 1 - ((7./64.) * chess.square_distance(chess.SQUARE_NAMES.index(mv[:2]), chess.SQUARE_NAMES.index(mv[2:])))
      reach += position_dict[mv[:2]] + mv[2:] + '|' + str(weight) + ' '
  
  return reach, attack

def get_defend_and_rayAttack(board, pos_dict):

  defend = ''
  ray = ''

  board_copy = board.copy()

  sub_piece = ''
  
  # for each piece on the board, 
  # flip color and use legal moves to check what pieces are defending it
  # and clear board except for the one piece to determine ray attacks
  for occupied_square in pos_dict:
    
    if pos_dict[occupied_square].isupper():
      sub_piece = 'p'
      board.turn = chess.WHITE
      board_copy.turn = chess.WHITE
    else:
      sub_piece = 'P'
      board.turn = chess.BLACK
      board_copy.turn = chess.BLACK
    
    ####### defending #######
    # flip color of piece
    board.set_piece_at(chess.SQUARE_NAMES.index(occupied_square), chess.Piece.from_symbol(sub_piece))

    legal_moves = [str(x) for x in list(board.legal_moves)]

    for mv in legal_moves:
      if mv[2:] == occupied_square:
        defend += pos_dict[mv[:2]] + '<' + pos_dict[mv[2:]] + mv[2:] + ' '
    
    # flip color of that piece back
    board.set_piece_at(chess.SQUARE_NAMES.index(occupied_square), chess.Piece.from_symbol(pos_dict[occupied_square]))
    ##########################
    
    ####### ray attacks #######
    board_copy.clear_board()
    board_copy.set_piece_at(chess.SQUARE_NAMES.index(occupied_square), chess.Piece.from_symbol(pos_dict[occupied_square]))

    legal_moves = [str(x) for x in list(board_copy.legal_moves)]

    for mv in legal_moves:
      if mv[2:] in pos_dict:
        if (pos_dict[mv[:2]].islower() and pos_dict[mv[2:]].isupper()) or (pos_dict[mv[:2]].isupper() and pos_dict[mv[2:]].islower()):
          ray += pos_dict[mv[:2]] + '=' + pos_dict[mv[2:]] + mv[2:] + ' '
    ##########################
  
  return defend, ray

def get_encoding(fen):
    
    board = chess.Board(fen)

    # naive encoding (i.e. what piece is on what square)
    base = ''
    pieces = board.piece_map()
    for p in pieces:
      base = base + str(pieces[p]) + chess.square_name(p) + " "

    # dictionary to keep track of what piece is on what square
    pos = base.split()
    pos_dict = {}
    for item in pos:
      pos_dict[item[1:]] = item[0]
    
    ########## reachability / attacking ##########
    reachable = ''
    attacking = ''

    reachable_t, attacking_t = get_reach_and_attack(board, pos_dict, chess.WHITE)
    reachable += reachable_t
    attacking += attacking_t

    reachable_t, attacking_t = get_reach_and_attack(board, pos_dict, chess.BLACK)
    reachable += reachable_t
    attacking += attacking_t
    ##############################################

    ########## defending / ray attacks ##########
    defending, ray_attacks = get_defend_and_rayAttack(board, pos_dict)
    ##############################################
    
    encoding = base + " " + reachable + " " + attacking + " " + defending + " " + ray_attacks
    return encoding