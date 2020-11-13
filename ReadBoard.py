import chess.pgn
import chess

pgn = open("Carlsen.pgn")


class ReadBoard:
    def generate_moves(self):
        list_of_game_moves = []

        for num in range(10):
            game = chess.pgn.read_game(pgn)
            list_of_moves = []
            moves = game.mainline_moves()
            board = chess.Board()

            for move in moves:
                list_of_moves.append(move)
                board.push(move)

            list_of_game_moves.append(list_of_moves)

        return list_of_game_moves
