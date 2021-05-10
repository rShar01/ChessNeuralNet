import numpy as np
import chess
import chess.engine
import operator

def activation(x):
    return 1 / (1 + np.exp(-x))

def reLu(x):
    return max(0, x)


class NeuralNet:
    def __init__(self, current_board: chess.Board, color: bool):
        # TODO: read and save as a JSON object?
        self.weights = {}
        self.weights[chess.PAWN] = np.random.rand()
        self.weights[chess.KNIGHT] = np.random.rand()
        self.weights[chess.BISHOP] = np.random.rand()
        self.weights[chess.ROOK] = np.random.rand()
        self.weights[chess.QUEEN] = np.random.rand()
        self.weights[chess.KING] = np.random.rand()

        self.bias = {}
        self.bias[chess.PAWN] = np.random.rand()
        self.bias[chess.KNIGHT] = np.random.rand()
        self.bias[chess.BISHOP] = np.random.rand()
        self.bias[chess.ROOK] = np.random.rand()
        self.bias[chess.QUEEN] = np.random.rand()
        self.bias[chess.KING] = np.random.rand()

        self.input_board = current_board
        self.color = color
        self.layer = []
        self.results = {}
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\projects\RealChessBot\stockfish_20090216_x64_bmi2.exe")
        self.possible_moves = current_board.generate_legal_moves()

    def evaluate_current_pos(self, color, fen, move):
        board = chess.Board(fen)
        board.push(move)
        result = self.engine.analyse(board, chess.engine.Limit(depth=2))
        score = result["score"].pov(self.color).score()
        return score

    def feed_forward(self):
        for move in self.possible_moves:
            square = move.from_square
            piece_type = self.input_board.piece_at(square).piece_type
            self.results[move] = ((self.evaluate_current_pos(self.color, self.input_board.fen(), move) * self.weights[piece_type]) + self.bias[piece_type])

        return max(self.results.items(), key=operator.itemgetter(1))[0]



    def backpropagation(self, diff: int):
        loss = 0.5 * np.power(diff, 2)
        for piece in self.weights:
            self.weights[piece] = self.weights[piece] * loss
        for piece in self.bias:
            self.bias[piece] = self.bias[piece] - diff

