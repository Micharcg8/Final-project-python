#MEJORAS DEL PRYECTO

# Cambiar el método de la clase Board

def showBoard(self):
  # Cargamos las librerías que nos harán falta
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd

  # Función que pasa del intervalo [-1, 16] al intervalo [0, 1]
  def transformation(x):
      return (x + 1)/17

  # Creamos la figura de plt que guardará el tablero
  fig = plt.figure(figsize = [10, 10])
  ax = fig.add_subplot(111)

  # Dibujamos las rectas verticales y horizontales
  for x in range(16):
      ax.plot([x, x], [0, 15], 'k')
  for y in range(16):
      ax.plot([0, 15], [y, y], 'k')

  # Redefinimos los límites de los ejes
  ax.set_xlim(-1, 16)
  ax.set_ylim(-1, 16)

  # Escalamos para que la parrilla ocupe toda la figura
  ax.set_position([0, 0, 1, 1])

  # Nos deshacemos de los ejes
  ax.set_axis_off()

  for i in range(len(self.board)):
      # números de arriba
      ax.text(transformation(i + 0.5), transformation(15.5), str(i),
              verticalalignment = "center", horizontalalignment = "center",
              fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
              transform = ax.transAxes)
      # números de la derecha
      ax.text(transformation(15.5), transformation(i + 0.5), str(14 - i),
              verticalalignment = "center", horizontalalignment = "center",
              fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
              transform = ax.transAxes)
      # letras
      for j in range(len(self.board)):
          ax.text(transformation(j + 0.5), transformation(14 - i + 0.5), self.board[i][j],
                  verticalalignment = "center", horizontalalignment = "center",
                  transform = ax.transAxes, fontsize = 15)

  plt.show()


  #CASILLAS DE COLORES
  # Modificación del método del tablero que habíamos programado en el extra 1

def showBoard(self):
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd
      
  def generate_vertex(center_x, center_y):
    vertex = np.array([[center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
                       [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]])
    return vertex

  def transformation(x):
    return (x + 1)/17

  filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/xycolor_board.csv"
  xycolors = pd.read_csv(filepath)

  fig = plt.figure(figsize = [10, 10])
  ax = fig.add_subplot(111)

  for x in range(16):
    ax.plot([x, x], [0, 15], 'k')   
  for y in range(16):
    ax.plot([0, 15], [y, y], 'k')

  ax.set_xlim(-1, 16)
  ax.set_ylim(-1, 16)

  # Escalamos para que la parrilla ocupe toda la figura
  ax.set_position([0, 0, 1, 1])

  # Nos deshacemos de los ejes
  ax.set_axis_off()

  for row in xycolors.itertuples():
    polygon = plt.Polygon(generate_vertex(row[1], row[2]), color = row[3])
    ax.add_artist(polygon)

  for i in range(len(self.board)):
    # top
    ax.text(transformation(i + 0.5), transformation(15.5), str(i),
            verticalalignment = "center", horizontalalignment = "center",
            fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
            transform = ax.transAxes)
    # right
    ax.text(transformation(15.5), transformation(i + 0.5), str(14 - i),
            verticalalignment = "center", horizontalalignment = "center",
            fontsize = 20, fontfamily = "fantasy", fontweight = "bold",
            transform = ax.transAxes)
    for j in range(len(self.board)):
        ax.text(transformation(j + 0.5), transformation(14 - i + 0.5), self.board[i][j],
                verticalalignment = "center", horizontalalignment = "center",
                transform = ax.transAxes, fontsize = 15)

  plt.show()

#CONFIGURACION DE LOS MULTIPLICADORES
def __init__(self):
  self.board = [[" " for j in range(15)] for i in range(15)]
  self.totalWords = 0
  self.totalPawns = 0
  self.multiplier = [[(1, "") for j in range(15)] for i in range(15)]


def setUpMultiplier(self):
  """
  Configura el multiplicador de cada casilla
  """
  import pandas as pd
  filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/multiplier_board.csv"
  multipliers = pd.read_csv(filepath)
  for row in multipliers.itertuples():
    self.multiplier[row[1]][row[2]] = (row[3], row[4])


#MULTIPLICAR EL VALOR DE LAS FICHAS Y DE LAS PALABRAS

def placeWord(self, player_pawns, word, x, y, direction):
    """
    Colocamos la palabra word sobre el tablero y eliminamos las fichas usadas de la bolsa del jugador
    """

    word_points = 0
    word_multiplier = 1
    for letter in word.word:
        if letter != self.board[x][y]:
            player_pawns.takePawn(letter)
            self.totalPawns += 1
            self.board[x][y] = letter
            
            if self.multiplier[x][y][1] != "w":# multiplicador de pawn o nada
                word_points += Pawns.getPoints(letter) * self.multiplier[x][y][0]
            else:# multiplicador de word
                word_points += Pawns.getPoints(letter)
                word_multiplier *= self.multiplier[x][y][0]
        
        if direction == "V":
            x += 1
        if direction == "H":
            y += 1
        
    Board.score += word_points * word_multiplier
    self.totalWords += 1

#MOSTRAR LA PUNTUACION DE LA PARTIDA

    ax.text(transformation(0), transformation(-0.5), "Score: {}".format(Board.score),
          verticalalignment = "center", horizontalalignment = "left",
          fontsize = 25, fontfamily = "fantasy", fontweight = "bold",
          transform = ax.transAxes)

#LAS FICHAS DE LA MANO DEL JUGADOR
 deal7Pawns()
          
  pawn_pos = 4
  for pawn in player_pawns.letters:
    polygon = plt.Polygon(generate_vertex(pawn_pos, -0.6), color = "#FFF68F")
    ax.add_artist(polygon)
    ax.text(transformation(pawn_pos), transformation(-0.6), pawn,
            verticalalignment = "center", horizontalalignment = "center",
            transform = ax.transAxes, fontsize = 15)
    pawn_pos += 1.5

    #LEYENDA DE LAS CASILLAS DEL TABLERO

    def legend():
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd
      
  def generate_vertex(center_x, center_y):
    vertex = np.array([[center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
                        [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]])
    return vertex

  def transformationX(x):
    return x / 16

  def transformationY(x):
    return (x + 1) / 3

  fig = plt.figure(figsize = [10, 2])
  ax = fig.add_subplot(111)

  ax.set_xlim(0, 16)
  ax.set_ylim(-1, 2)

  # Escalamos para que la parrilla ocupe toda la figura
  ax.set_position([0, 0, 1, 1])

  # Nos deshacemos de los ejes
  ax.set_axis_off()

  colors = ["#FFCCCC", "#B2FFCD", "#CCCEFF", "#CCF9FF"]
  texts = ["x3\nPalabra", "x2\nPalabra", "x3\nLetra", "x2\nLetra"]
  for i in range(4):
    polygon = plt.Polygon(generate_vertex(1.5 + 4 * i, 0.5), color = colors[i])
    ax.add_artist(polygon)
    ax.text(transformationX(3.5 + 4 * i), transformationY(.5), texts[i],
            verticalalignment = "center", horizontalalignment = "center",
            fontsize = 25, fontfamily = "fantasy", fontweight = "bold",
            transform = ax.transAxes)

  plt.show() 