# Módulo completo de Apylabrados
def startGame():
    """
    Inicializa todas las variables para comenzar una nueva partida
    """
    # Creamos las variables booleana end, show_help y show_help_plus
    global end
    end = False
    global show_help
    show_help = True
    global show_help_plus
    show_help_plus = True
    
    # Creamos la bolsa de fichas del juego
    global bag_of_pawns
    bag_of_pawns = Pawns()
    bag_of_pawns.createBag()

    # Creamos las fichas del jugador
    global player_pawns
    player_pawns = Pawns()

    # Creamos el tablero de juego
    global board
    board = Board()
    Board.score = 0

    # Mensaje de bienvenida e instrucciones
    welcome()
    instructions()


def welcome():
    """
    Muestra el mensaje de bienvenida para la primera vez que empezamos a jugar
    """
    filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/welcome_message.txt"
    with open(filepath, "r") as f:
        print(f.read())


def instructions():
    """
    Muestra las instrucciones de la partida de Apylabrados
    """
    filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/instructions_message.txt"
    with open(filepath, "r") as f:
        print(f.read())


def deal7Pawns():
    """
    Reparte fichas al jugador hasta completar las 7 de su mano actual
    """
    while(player_pawns.getTotalPawns() < 7):
        player_pawns.addPawn(bag_of_pawns.takeRandomPawn())
    print("Estas son tus fichas:")
    player_pawns.showPawns()
    
    
def showOptions():
    """
    Muestra las opciones en caso de que todavía no haya palabra introducida
    """
    global show_help
    filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/options_message.txt"
    print("\n¿Qué deseas hacer? {}".format("" if show_help else "(Introduce SHOWHELP para ver las diferentes opciones)"))
    if show_help:
        with open(filepath, "r") as f:
            print(f.read())
        show_help = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help = True
        showOptions()
    elif ans == "ENTERWORD":
        introduceNewWord()
    elif ans == "MYPAWNS":
        print("Estas son tus fichas:")
        player_pawns.showPawns()
        showOptions()
    elif ans == "MYSCORE":
        print("Puntos: {}".format(Board.score))
        showOptions()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOptions()
    elif ans == "HELPWORD":
        helpWithWords()
        showOptions()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOptions()
    
    
    
def showOptionsPlus():
    """
    Muestra las opciones en caso de que haya palabra introducida para colocar en el tablero
    """
    global show_help_plus
    filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/options_plus_message.txt"
    print("\n¿Qué deseas hacer? {}".format("" if show_help_plus else "(Introduce SHOWHELP para ver las diferentes opciones)"))
    if show_help_plus:
        with open(filepath, "r") as f:
            print(f.read())
        show_help_plus = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help_plus = True
        showOptionsPlus()
    elif ans == "ENTERPOSITION":
        introduceCoordinatesAndDirection()
    elif ans == "ENTERWORD":
        introduceNewWord()
    elif ans == "MYPAWNS":
        print("Estas son tus fichas:")
        player_pawns.showPawns()
        showOptionsPlus()
    elif ans == "MYSCORE":
        print("Puntos: {}".format(Board.score))
        showOptionsPlus()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOptionsPlus()
    elif ans == "HELPWORD":
        helpWithWords()
        showOptionsPlus()
    elif ans == "HELPPOS":
        helpWithPosition()
        showOptionsPlus()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOptionsPlus()



def helpWithWords():
    """
    Muestra las posibles palabras que se pueden formar con las fichas disponibles del jugador
    y las que ya hay colocadas en el tablero
    """
    print("Estas son las posibles palabras a formar:")
    if board.totalWords == 0:
        Dictionary.showWords(player_pawns)
    else:
        board_letters = []
        for i in range(15):
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    Dictionary.showWordsPlus(player_pawns, board.board[i][j])


def helpWithPosition():
    """
    Muestra las posibles colocaciones en el tablero de la palabra introducida
    """
    print("Estas son las posibles colocaciones")
    board.showWordPlacement(player_pawns, new_word)


def introduceNewWord():
    """
    Permite que el usuario introduzca una nueva palabra por consola
    y comprueba que existe en el diccionario, y que puede formarse con las 
    fichas de que dispone el jugador y las ubicadas sobre el tablero. 
    """
    print("Introduce tu palabra:")
    global new_word
    new_word = Word.readWord()
    new_word_ft = new_word.getFrequency()
    player_pawns_ft = player_pawns.getFrequency()
    isInDictionary = Dictionary.validateWord(new_word)
    
    if board.totalWords == 0:
        newWordIsSubset = FrequencyTable.isSubset(new_word_ft, player_pawns_ft)
    else:
        board_letters = []
        forcedBreak = False
    
        for i in range(15):
            if forcedBreak:
                break
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    player_pawns_plus = player_pawns_ft
                    player_pawns_plus.update(board.board[i][j])
                    newWordIsSubset = FrequencyTable.isSubset(new_word_ft, player_pawns_plus)
                    player_pawns_plus.delete(board.board[i][j])
                    
                    if newWordIsSubset:
                        forcedBreak = True
                        break
    
    if not isInDictionary or not newWordIsSubset:
        if not newWordIsSubset:
            print("No puedes formar esa palabra con tus fichas")
        showOptions()
    else:
        showOptionsPlus()


def introduceCoordinatesAndDirection():
    """
    Permite al jugador introducir por consola la posición y orientación de una palabra.
    Comprueba si la palabra se puede colocar en dicha ubicación.
    """
    print("Introduce coordenada de la fila: ", end = " ")
    x = int(input())
    print("Introduce coordenada de la columna: ", end = " ")
    y = int(input())
    print("Introduce dirección: ", end = " ")
    direction = input().upper()
    
    if direction != "V" and direction != "H":
        print("Recuerda: solamente hay dos posibles direcciones para colocar las palabras: V (vertical) y H (horizontal)")
        showOptionsPlus()

    possible, message = board.isPossible(new_word, x, y, direction)
    if not possible:
        print(message)
        showOptionsPlus()
    else:
        needed_pawns = board.getPawns(new_word, x, y, direction)
        if FrequencyTable.isSubset(needed_pawns.getFrequency(), player_pawns.getFrequency()):
            board.placeWord(player_pawns, new_word, x, y, direction)
            board.showBoard()
            print("\nPuntos: {}\n".format(Board.score))
        else:
            print("Las fichas de que dispones no son suficientes")
            showOptionsPlus()


def endGame():
    """
    Finaliza la partida actual
    """
    print("Fin del juego")
    global end
    end = True





class Pawns:
    
    points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
              "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
              "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
    }
    
    def __init__(self):
        self.letters = []

    
    def addPawn(self, c):
        """
        Añade una ficha c al array de caracteres letters
        """
        self.letters.append(c)
        
        
    def addPawns(self, c, n):
        """
        Añade n veces una ficha c al array de caracteres letters
        """
        for i in range(n):
            self.addPawn(c)
            
    
    def createBag(self):
        """
        Crea la bolsa con las 100 fichas del juego
        """
        import pandas as pd
        filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/bag_of_pawns.csv"
        bag = pd.read_csv(filepath)
        for item in bag.itertuples():
            self.addPawns(item[1], item[2])
        
    
    def showPawns(self):
        """
        Muestra las fichas que contiene la bolsa y el número de veces que está repetida cada ficha
        """
        ft_pawns = self.getFrequency()
        ft_pawns.showFrequency()
                                                            
    
    def takeRandomPawn(self):
        """
        Toma una ficha de la bolsa de forma aleatoria y la elimina de la bolsa
        """
        from numpy import random
        idx = random.randint(0, self.getTotalPawns() - 1)
        letter = self.letters[idx]
        self.letters.remove(letter)
        return letter
        
        
    def getFrequency(self):
        """
        Muestra la frecuencia de aparición de cada ficha
        """
        ft = FrequencyTable()
        for c in self.letters:
            ft.update(c)
        return ft

    
    def takePawn(self, c):
        """
        Toma la ficha c de la bolsa y la elimina de la bolsa
        """
        self.letters.remove(c)

        
        
    def getTotalPawns(self):
        """
        Obtenemos el total de fichas del objeto
        """
        return len(self.letters)
        
        
    @staticmethod    
    def getPoints(c):
        """
        Devuelve los puntos de la ficha c
        """
        return Pawns.points[c]
        
    
    @staticmethod
    def showPawnsPoints():
        """
        Muestra por pantalla la puntuación de cada ficha
        """
        print("Puntos de cada ficha:")
        count = 0
        end = "   "
        for key in Pawns.points:
            print("{}:{}{}".format(key, " " if Pawns.getPoints(key) < 9 else "", Pawns.getPoints(key)), end = end)
            count += 1
            end = "\n" if count % 3 == 2 else "   "
               




class Word:
    
    def __init__(self):
        self.word = []
        
        
    def __str__(self):
        """
        Imprimimos la palabra en formato string
        """
        string = ""
        for i in range(self.getLengthWord()):
            string += self.word[i]
        return string
    

    def areEqual(self, w):
        """
        Comprueba si dos palabras son iguales
        """
        return self.word == w.word
        

    def isEmpty(self):
        """ 
        Comprueba si una palabra es vacía
        """
        return self.getLengthWord() == 0
            
    
    @classmethod
    def readWord(cls):
        """
        Lee una palabra por teclado y la devuelve como un objeto de la clase Word
        """
        input_word = input().strip()
        w = Word()
        for c in input_word.upper():
            w.word.append(c)
        return w

    
    @staticmethod
    def readWordFromFile(f):
        """
        Lee una palabra del fichero f y la devuelve como un objeto de la clase Word
        """
        w = Word()
        file_word = f.readline()
        # Consideramos toda la línea salvo el salto de línea \n --> Solo consideramos la palabra
        for c in file_word[:-1]:
            w.word.append(c)
        return w
        
        
    def getFrequency(self):
        """
        Muestra la frecuencia de aparición de cada letra en una palabra
        """
        ft = FrequencyTable()
        for c in self.word:
            ft.update(c)
        return ft
        
        
    def getLengthWord(self):
        """
        Devuelve la longitud de la palabra
        """
        return len(self.word)
        
        
        
        
        
        
class Dictionary:
    
    filepath = "/content/drive/MyDrive/python-basico/proyecto final/scripts/dictionary.txt"
    
    @staticmethod
    def validateWord(word):
        """
        Comprueba si la palabra word se encuentra en el diccionario
        """
        with open(Dictionary.filepath, "r") as f:
            w = Word.readWordFromFile(f)
            while (not w.isEmpty() and not word.areEqual(w)):
                w = Word.readWordFromFile(f)
                
        if w.isEmpty() and not word.areEqual(w):
            print("La palabra no se encuentra en el diccionario")
            return False
            
        else:
            return True
     
            
    @staticmethod
    def showWords(pawns):
        """
        Muestra todas las posibles palabras que se pueden formar con las fichas de pawns
        """
        tf_pawns = pawns.getFrequency()
        count = 0
        end = " "
        with open(Dictionary.filepath, "r") as f:
            word = Word.readWordFromFile(f)
            while (not word.isEmpty()):
                n = word.getLengthWord()
                tf_word = word.getFrequency()
                if FrequencyTable.isSubset(tf_word, tf_pawns):
                    print(word, end = end * (10 - n) if end == " " else end)
                    count += 1
                    end = "\n" if count % 5 == 4 else " "
                word = Word.readWordFromFile(f)
            
    
    @staticmethod
    def showWordsPlus(pawns, c):
        """
        Muestra todas las posibles palabras que contienen el caracter c y que se pueden formar con las fichas de pawns
        """
        tf_pawns = pawns.getFrequency()
        tf_pawns.update(c)
        count = 0
        end = " "
        with open(Dictionary.filepath, "r") as f:
            word = Word.readWordFromFile(f)
            while (not word.isEmpty()):
                n = word.getLengthWord()
                if c in word.word:
                    tf_word = word.getFrequency()
                    if FrequencyTable.isSubset(tf_word, tf_pawns):
                        print(word, end = end * (10 - n) if end == " " else end)
                        count += 1
                        end = "\n" if count % 5 == 4 else " "
                word = Word.readWordFromFile(f)
        print("")
        





class FrequencyTable:
    
    def __init__(self):
        self.letters = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
        self.frequencies = [0 for x in range(0, len(self.letters))]
        
        
    def showFrequency(self):
        """
        Muestra la frecuencia de aquellas letras con frecuencia diferente de 0
        """
        for i in range(len(self.letters)):
            if self.frequencies[i] != 0:
                print("{}: {}".format(self.letters[i], self.frequencies[i]))
    
    @staticmethod
    def isSubset(ft1, ft2):
        """
        Comprueba si ft1 es subconjuto de ft2
        """
        for x in range(len(ft1.frequencies)):
            if ft1.frequencies[x] > ft2.frequencies[x]:
                return False
        return True
        
    
    def update(self, c):
        """
        Actualiza la frecuencia de la letra c que pasemos por parámetro (suma 1)
        """
        idx = self.letters.index(c)
        self.frequencies[idx] += 1
      
        
    def delete(self, c):
        """
        Actualiza la frecuencia de la letra c que pasemos por parámetro (resta 1)
        """
        idx = self.letters.index(c)
        self.frequencies[idx] -= 1
        
        
        
        
        
class Board:
    score = 0
    
    def __init__(self):
        self.board = [[" " for j in range(15)] for i in range(15)]
        self.totalWords = 0
        self.totalPawns = 0
        
        
    def showBoard(self):
        """
        Muestra el tablero
        """
        print("\n ", end = " ")
        for n in range(len(self.board)):
            print("{}{} ".format(0 if n <= 9 else "", n), end = " ")
        print("\n+" + "---+" * len(self.board))
        for i in range(len(self.board)):
            print("|", end = " ")
            for j in range(len(self.board)):
                print(self.board[i][j] + " |", end = " ")
            print("{}{}".format(0 if i <= 9 else "", i))
            print("+" + "---+" * len(self.board))
            
            
    def placeWord(self, player_pawns, word, x, y, direction):
        """
        Colocamos la palabra word sobre el tablero y eliminamos las fichas usadas de la bolsa del jugador
        """
        for letter in word.word:
            if letter != self.board[x][y]:
                player_pawns.takePawn(letter)
                self.totalPawns += 1
                self.board[x][y] = letter
                Board.score += Pawns.getPoints(letter)
            
            if direction == "V":
                x += 1
            if direction == "H":
                y += 1
            
        self.totalWords += 1
        
        
        
    def isPossible(self, word, x, y, direction):
        """
        Comprueba si es posible colocar la palabra word en la posición y dirección proporcionadas
        """
        message = ""
        x0 = x
        y0 = y
    
        # Si es el primer turno, comprobamos si alguna ficha se sitúa sobre la casilla central
        if self.totalWords == 0:
            message = "Ninguna ficha pasa por la casilla central"
            if direction == "V":
                if y0 != 7:
                    return (False, message)
                elif x0 + word.getLengthWord() - 1 < 7 or x0 > 7:
                    return (False, message)
                    
            if direction == "H":
                if x0 != 7:
                    return (False, message)
                elif y0 + word.getLengthWord() - 1 < 7 or y0 > 7:
                    return (False, message)

        else:
            # Comprobamos si la palabra se sale del tablero
            message = "La palabra se sale de los límites del tablero"
            if (x0 < 0 or x0 >= 15 or y0 < 0 or y0 >= 15):
                return (False, message)
            if direction == "V" and x0 + word.getLengthWord() - 1 >= 15:
                return (False, message)
            if direction == "H" and y0 + word.getLengthWord() - 1 >= 15:
                return (False, message)
                
            # Comprobamos si se utiliza alguna ficha del tablero para formar la palabra
            x = x0
            y = y0
            blanks = []
            for c in word.word:
                if self.board[x][y] == " ":
                   blanks.append(c)
                    
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
            
            if len(blanks) == word.getLengthWord():
                message = "No se está utilizando ninguna ficha del tablero"
                return (False, message)
        
            # Comprobamos si la casilla está libre u ocupada por la misma letra
            x = x0
            y = y0
            for c in word.word:
                if self.board[x][y] != " " and self.board[x][y] != c:
                    message = "Hay una ficha diferente ocupando una posición"
                    return (False, message)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
                    
            # Comprobamos si se coloca una nueva ficha en el tablero
            x = x0
            y = y0
            matching = []
            for c in word.word:
                if self.board[x][y] == c:
                    matching.append(c)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
            
            if len(matching) == word.getLengthWord():
                message = "No se está colocando ninguna ficha nueva en el tablero"
                return (False, message)
            
                
            # Comprobamos que no hay fichas adicionales a principio y final de palabra
            message = "Hay fichas adicionales a principio o final de palabra"
            x = x0
            y = y0
            if direction == "V" and ((x != 0 and self.board[x - 1][y] != " ") or 
                                     (x + word.getLengthWord() != 14 and self.board[x + word.getLengthWord()][y] != " ")):
                return (False, message)
            if direction == "H" and ((y != 0 and self.board[x][y - 1] != " ") or 
                                     (y + word.getLengthWord() != 14 and self.board[x][y + word.getLengthWord()] != " ")):
                return (False, message)
        
        message = "La palabra se puede situar en el tablero"
        return (True, message)
            
        
    def getPawns(self, word, x, y, direction):
        """
        Dada una palabra, posición y dirección, devuelve las letras necesarias para formar la palabra word
        """
        needed_letters = Word()
        possible, message = self.isPossible(word, x, y, direction)
        
        if not possible:
            print(message)
        else:
            for c in word.word:
                if self.board[x][y] != c:
                    needed_letters.word.append(c)
                if direction == "V":
                    x += 1
                if direction == "H":
                    y += 1
        return needed_letters
        
    
    def showWordPlacement(self, pawns, word):
        """
        Dadas las fichas del jugador y una palabra, muestra las posibles colocaciones de la palabra
        """
        for direction in ["V", "H"]:
            print("{}:".format("Vertical" if direction == "V" else "Horizontal"))
            for i in range(15):
                for j in range(15):
                    if self.isPossible(word, i, j, direction)[0] == True:
                        needed_pawns = self.getPawns(word, i, j, direction)
                        if FrequencyTable.isSubset(needed_pawns.getFrequency(), pawns.getFrequency()):
                            print("(x = {}, y = {})".format(i, j))
  

