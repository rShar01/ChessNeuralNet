import NeuralNet
import chess
import ReadBoard
import chess.engine

# TODO: add engine?

scanner = ReadBoard.ReadBoard()
magnus_moves = scanner.generate_moves()

"""
ai_move = ai.feed_forward()
magnus_move = magnus_moves[0][0]

print("Magnus evaluation: " + str(ai.evaluate_current_pos(chess.WHITE, magnus_board.fen(), magnus_move)))
print("AI evaluation: " + str(ai.evaluate_current_pos(chess.WHITE, ai_board.fen(), ai_move)))
print(ai.results)

magnus_board.push(magnus_move)
ai_board.push(ai_move)

print()
print("===== MAGNUS BOARD =====")
print(magnus_board)
print()
print("===== AI BOARD ======")
print(ai_board)

"""

board = chess.Board()
color = True

# training loop
for move in magnus_moves[0]:
    ai = NeuralNet.NeuralNet(board, color)
    ai_move = ai.feed_forward()
    ai_value = ai.evaluate_current_pos(color, board.fen(), ai_move)
    mag_value = ai.evaluate_current_pos(color, board.fen(), move)
    ai.backpropagation(mag_value - ai_value)
    print(mag_value - ai_value)
    print(move)
    board.push(move)
    color = not color
    print(board.fen())
    print()

print(ai.weights)
print(ai.bias)



