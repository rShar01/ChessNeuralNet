from os import close
from re import I
import re
import chess.pgn
import chess
from random import randrange

## A simple script to generate some data

def get_game_win(game, name_1, name_2):
    try:
        if(game == "Failed to get game, moving on!"):
            return -1
        
        color = game.headers["White"]
        is_white = True if color == name_1 or color == name_2 else False

        result = game.headers["Result"]

        if result == "1/2-1/2":
            return 0

        if is_white and result == "1-0":
            return 1

        if not is_white and result == "0-1":
            return 1
        
        return -1
    
    except AttributeError:
        return -500


def get_random_fen(game):
    try:
        count = 0
        for move in game.mainline_moves():
            count = count + 1
        
        rand_state = randrange(0,count)
        board = chess.Board()

        for move in game.mainline_moves():
            if rand_state <= 0:
                break

            rand_state = rand_state - 1
            board.push(move)

        return board.fen()
    
    except ValueError:
        return "Failed to get game, moving on!"
    except AttributeError:
        return "Failed to get game, moving on!"




carlsen_pgn = open("Carlsen.pgn")
ivan_pgn = open("Ivanchuk.pgn")
caruana_pgn = open("Caruana.pgn")
train_out = open("training.txt", 'w')
test_out = open("testing.txt", 'w')


## Generate training data
for game_num in range(2000):
    print("---game number " + str(game_num) + "---")
    carlsen_game = chess.pgn.read_game(carlsen_pgn)
    ivan_game = chess.pgn.read_game(ivan_pgn)
    caruana_game = chess.pgn.read_game(caruana_pgn)

    carlsen_win = get_game_win(carlsen_game,"Carlsen,Magnus", "Carlsen,M")
    carlsen_fen = get_random_fen(carlsen_game)

    ivan_win = get_game_win(ivan_game, "Ivanchuk, Vassily", "Ivanchuk,V")
    ivan_fen = get_random_fen(ivan_game)

    caruana_win = get_game_win(caruana_game, "Caruana,Fabiano", "Caruana,F")
    caruana_fen = get_random_fen(caruana_game)


    if caruana_fen != "Failed to get game, moving on!" and caruana_win != -500:
        train_out.write(caruana_fen + " " + str(caruana_win))
        train_out.write("\n")
    
    if carlsen_fen != "Failed to get game, moving on!" and carlsen_win != -500:
        train_out.write(carlsen_fen + " " + str(carlsen_win))
        train_out.write("\n")

    if ivan_fen != "Failed to get game, moving on!" and ivan_win != -500:
        train_out.write(ivan_fen + " " + str(ivan_win))
        train_out.write("\n")
   



## Generate testing data
for game_num in range(500):
    print("---game number " + str(game_num) + "---")
    carlsen_game = chess.pgn.read_game(carlsen_pgn)
    ivan_game = chess.pgn.read_game(ivan_pgn)
    caruana_game = chess.pgn.read_game(caruana_pgn)

    
    carlsen_win = get_game_win(carlsen_game,"Carlsen,Magnus", "Carlsen,M")
    carlsen_fen = get_random_fen(carlsen_game)

    ivan_win = get_game_win(ivan_game, "Ivanchuk, Vassily", "Ivanchuk,V")
    ivan_fen = get_random_fen(ivan_game)

    caruana_win = get_game_win(caruana_game, "Caruana,Fabiano", "Caruana,F")
    caruana_fen = get_random_fen(caruana_game)

    if caruana_fen != "Failed to get game, moving on!" and caruana_win != -500:
        test_out.write(caruana_fen + " " + str(caruana_win))
        test_out.write("\n")
        game_num = game_num - 1
    
    if carlsen_fen != "Failed to get game, moving on!" and carlsen_win != -500:
        test_out.write(carlsen_fen + " " + str(carlsen_win))
        test_out.write("\n")
        game_num = game_num - 1

    if ivan_fen != "Failed to get game, moving on!" and ivan_win != -500:
        test_out.write(ivan_fen + " " + str(ivan_win))
        test_out.write("\n")
        game_num = game_num - 1



train_out.close()
test_out.close()
