import numpy as np
import chess
from numpy.lib.function_base import piecewise
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential(
    [
      keras.Input(shape=(12,64)),
      layers.Flatten(),
      layers.Dense(384, activation="relu", name="layer1"),
      layers.Dense(192, activation="relu", name="layer2"),
      layers.Dense(96, activation="relu", name="layer3"),
      layers.Dense(64, activation="relu", name="layer4"),
      layers.Dense(16, activation="relu", name="layer5"),
      layers.Dense(3, activation="softmax",  name="layer6"),
    ]
)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

## set up board containers for data
train_board = np.ndarray(shape=(5500, 12, 64))
train_res = np.ndarray(shape=(5500, 1))
test_board = np.ndarray(shape=(1200, 12, 64))
test_res = np.ndarray(shape=(1200, 1))





training_data = open("training.txt", 'r')
testing_data = open("testing.txt", 'r')

for i in range(5500):
  collection = np.ndarray(shape=(12,64))

  self_pawn = np.zeros(64)
  self_rook = np.zeros(64)
  self_knight = np.zeros(64)
  self_bishop = np.zeros(64)
  self_queen = np.zeros(64)
  self_king = np.zeros(64)

  enemy_pawn = np.zeros(64)
  enemy_rook = np.zeros(64)
  enemy_knight = np.zeros(64)
  enemy_bishop = np.zeros(64)
  enemy_queen = np.zeros(64)
  enemy_king = np.zeros(64)

  line = training_data.readline()
  words = line.split()
  board = chess.Board(words[0] + " " + words[1] + " " + words[2] + " " + words[3] + " " + words[4] + " " + words [5])

  lop = board.piece_map()

  for piece in lop:
      p = lop[piece]
      type = p.piece_type
      color = p.color
      if type == chess.PAWN:
          if(color == chess.WHITE):
              self_pawn[piece] = 1
          else:
              enemy_pawn[piece] = 1

      elif type == chess.ROOK:
          if(color == chess.WHITE):
              self_rook[piece] = 1
          else:
              enemy_rook[piece] = 1

      elif type == chess.KNIGHT:
          if(color == chess.WHITE):
              self_knight[piece] = 1
          else:
              enemy_knight[piece] = 1

      elif type == chess.BISHOP:
          if(color == chess.WHITE):
              self_bishop[piece] = 1
          else:
              enemy_bishop[piece] = 1

      elif type == chess.QUEEN:
          if(color == chess.WHITE):
              self_queen[piece] = 1
          else:
              enemy_queen[piece] = 1

      elif type == chess.KING:
          if(color == chess.WHITE):
              self_king[piece] = 1
          else:
              enemy_king[piece] = 1

  collection[0] = self_pawn
  collection[1] = self_bishop
  collection[2] = self_king
  collection[3] = self_knight
  collection[4] = self_queen
  collection[5] = self_rook

  collection[6] = enemy_pawn
  collection[7] = enemy_bishop
  collection[8] = enemy_king
  collection[9] = enemy_knight
  collection[10] = enemy_queen
  collection[11] = enemy_rook
  
  train_board[i] = collection
  train_res[i] = words[-1]


for i in range(1200):
  collection = np.ndarray(shape=(12,64))

  self_pawn = np.zeros(64)
  self_rook = np.zeros(64)
  self_knight = np.zeros(64)
  self_bishop = np.zeros(64)
  self_queen = np.zeros(64)
  self_king = np.zeros(64)

  enemy_pawn = np.zeros(64)
  enemy_rook = np.zeros(64)
  enemy_knight = np.zeros(64)
  enemy_bishop = np.zeros(64)
  enemy_queen = np.zeros(64)
  enemy_king = np.zeros(64)

  line = testing_data.readline()
  words = line.split()
  board = chess.Board(words[0] + " " + words[1] + " " + words[2] + " " + words[3] + " " + words[4] + " " + words [5])

  lop = board.piece_map()

  for piece in lop:
      p = lop[piece]
      type = p.piece_type
      color = p.color
      if type == chess.PAWN:
          if(color == chess.WHITE):
              self_pawn[piece] = 1
          else:
              enemy_pawn[piece] = 1

      elif type == chess.ROOK:
          if(color == chess.WHITE):
              self_rook[piece] = 1
          else:
              enemy_rook[piece] = 1

      elif type == chess.KNIGHT:
          if(color == chess.WHITE):
              self_knight[piece] = 1
          else:
              enemy_knight[piece] = 1

      elif type == chess.BISHOP:
          if(color == chess.WHITE):
              self_bishop[piece] = 1
          else:
              enemy_bishop[piece] = 1

      elif type == chess.QUEEN:
          if(color == chess.WHITE):
              self_queen[piece] = 1
          else:
              enemy_queen[piece] = 1

      elif type == chess.KING:
          if(color == chess.WHITE):
              self_king[piece] = 1
          else:
              enemy_king[piece] = 1

  collection[0] = self_pawn
  collection[1] = self_bishop
  collection[2] = self_king
  collection[3] = self_knight
  collection[4] = self_queen
  collection[5] = self_rook

  collection[6] = enemy_pawn
  collection[7] = enemy_bishop
  collection[8] = enemy_king
  collection[9] = enemy_knight
  collection[10] = enemy_queen
  collection[11] = enemy_rook
  
  test_board[i] = collection
  test_res[i] = words[-1]


training_data.close()
testing_data.close()
   
## reshape data to fit keras
train_res = tf.keras.utils.to_categorical(train_res, 3)
test_res = tf.keras.utils.to_categorical(test_res, 3)

## train
model.fit(train_board, train_res, epochs=40)


## evaluate
score = model.evaluate(test_board, test_res, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])
