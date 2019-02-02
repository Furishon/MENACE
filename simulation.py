'''
MENACE: Machine Educable Noughts And Crosses Engine
NOW IN CHOPSTICKS-O-VISION!

TODO:
ADD ACCTUAL GAME FUNCTIONALTY
'''


import pandas as pd
import numpy as np

'''
HtL: high to low
LtH: low to high
HtH: high to high
LtL: low to low
splt: split
'''
standardMoves = ['HtL', 'HtL', 'LtH', 'LtH', 'HtH', 'HtH', 'LtL', 'LtL', 'splt', 'splt']
#HOW MANY MOVES TO ADD AFTER A WIN
moveIncrement = 3

#IMPORTS ALL POSSIBLE GAME POSITIONS AS A PANDAS.SERIES
#ALL BOARD POSITIONS GIVEN IN THE FOLLOWING FORMAT: ((X,Y),(A,B))
#WHERE: (X, Y) IS THE HAND OF PLAYER 1 & (A, B) IS THE HAND OF PLAYER 2
possibleBoardPositions = pd.read_csv('handCombinations.csv')


def appendMany(array, value, times):
	'''APPENDS A VALUE TO AN ARRAY MULTIPLE TIMES
	ARGS:
		array: array, the target array
		value: string, the value to be appended
		times: int, the number of times to append value to array'''
	for ___	in range(0, times):
		array.append(value)

class Box:
	def __init__(self, boardPosition, standardMoves):
		self.boardPosition = boardPosition
		self.moves = standardMoves
	
	def chooseMove(self):
		'''RETURNS ONE MOVE IN THE BOX
		RETURNS:
			string, a move'''
		if len(self.moves) == 0:
			self.moves.extend(standardMoves)
			print(len(self.moves))
		return self.moves[np.random.randint(0, max(1, len(self.moves)))]		

	def addMove(self, chosenMove):
		'''ADDS A MOVE TO THE BOX A (moveIncrement) NUMBER OF TIMES
		ARGS:
			chosenMove: string, the move to be added'''
		appendMany(self.moves, chosenMove, moveIncrement)

	def delMove(self, chosenMove):
		'''REMOVES MOVE FROM THE BOX, REMOVING THE FIRST MOVE MATCHING chosenMove
		ARGS:
			chosenMove: string, the move to be removed'''
		for n in range(0, len(self.moves)):
			if self.moves[n] == chosenMove:
				del self.moves[n]
				return
	
	def reduceMoves(self):
		noLtL = self.moves.count('LtL')
		noLtH = self.moves.count('LtH')
		noHtH = self.moves.count('HtH')
		noHtL = self.moves.count('HtL')
		noSplt = self.moves.count('splt')
		#+ 1 REMOVES PROBLEMS WITH DIVISION BY 0
		totalNo = noLtL + noLtH + noHtL + noHtH + noSplt + 1
		
		#THE PERCENTAGE OF EACH MOVE IN THE BOX, THE SUM OF ALL SHOULD BE APPROX. 1
		percentageLtL = noLtL / totalNo
		percentageLtH = noLtH / totalNo
		percentageHtL = noHtL / totalNo
		percentageHtH = noHtH / totalNo
		percentageSplt = noSplt / totalNo
		
		#NORMALIZES ALL VALUES TO SUM UP TO APPROX. 100
		reducedLtL = int(np.ceil(percentageLtL * 100)) + 1
		reducedLtH = int(np.ceil(percentageLtH * 100)) + 1
		reducedHtL = int(np.ceil(percentageHtL * 100)) + 1
		reducedHtH = int(np.ceil(percentageHtH * 100)) + 1
		reducedSplt = int(np.ceil(percentageSplt * 100)) + 1

		self.moves = []
		appendMany(self.moves, 'LtL', reducedLtL)
		appendMany(self.moves, 'LtH', reducedLtH)
		appendMany(self.moves, 'HtL', reducedHtL)
		appendMany(self.moves, 'HtH', reducedHtH)
		appendMany(self.moves, 'splt', reducedSplt)
		
#CREATES A BOX OBJECT FOR EACH POSSIBLE BOARD POSITION 
boxes = []
for n in range(0, len(possibleBoardPositions)):
	boxes.append(Box(boardPosition = possibleBoardPositions['handCombinations'][n],
					 standardMoves = standardMoves))

class MENACE:
	'''CLASS CONTAINING THE FUNCTIONALITY FOR A CHOPSTICKS-PLAYING BOT
	METHODS:
		__init__: creates a set of boxes containing moves, one for each possible board position
		chooseMove: chooses a move at random from a given box
		train: if win, then adds used move to all used boxes; if loss, then removes used move from all used boxes'''
	
	def __init__(self, playerID):	
		#KEEPS TRACK OF WHICH MOVES WERE PLAYED IN WHICH POSITION 
		#self.moveHistory[n][0] = the board position
		#self.moveHistory[n][1] = the move played
		self.moveHistory = []
		#The player ID (1 or 2)
		self.playerID = playerID
		#The other players playerID
		if self.playerID == 1:
			self.otherPlayerID = 2
		elif self.playerID == 2:
			self.otherPlayerID = 1

	def chooseMove(self, currentPosition):
		'''CHOOSES A MOVE FOR A GIVEN BOARD POSITION
		ARGS:
			currentPosition: list of lists, the current position of the board
		RETURNS:
			string, a move'''
		for box in boxes:
			if str(box.boardPosition) == str(currentPosition):
				while True:
					choosenMove = box.chooseMove()
					print('P{}: {}'.format(self.playerID, choosenMove))
					if choosenMove == 'LtL':
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					elif choosenMove == 'LtH' and currentPosition[self.otherPlayerID -1][1] < 5:
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					elif choosenMove == 'splt' and currentPosition[self.playerID - 1][0] == 2 and currentPosition[self.playerID - 1][1] >= 5:
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					elif choosenMove == 'splt' and currentPosition[self.playerID - 1][0] == 4 and currentPosition[self.playerID - 1][1] >= 5:
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					elif choosenMove == 'HtL' and currentPosition[self.playerID - 1][1] < 5:
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					elif choosenMove == 'HtH' and currentPosition[self.playerID - 1][1] < 5 and currentPosition[self.otherPlayerID - 1][1] < 5:
						self.moveHistory.append([box.boardPosition, choosenMove])
						return choosenMove
					else:
						#IF THE MOVE IS ILLEGAL, REMOVE IT FROM THE BOX
						box.delMove(choosenMove)
						#ILLEGAL MOVE, TRY AGAIN
						print('ILLEGAL MOVE, RETRY')

	def train(self, victory):
		'''TRAINS THE MODEL BY ADDING MOVES IF IT WON AND REMOVING THEM IF IT LOST
		ARGS:
			victory: bool, The end result of a match; True = win; False = loss'''
		for item in self.moveHistory:
			thenBoardPosition = item[0] 		
			thenMove = item[1]

			#FOR EACH ITEM IN MOVE HISTORY: DELETES PLAYED MOVE IF LOSS, ADDS MOVE IF WIN
			for box in boxes:
				if str(box.boardPosition) == str(thenBoardPosition):
					if victory:
						box.addMove(thenMove)
					else:
						box.delMove(thenMove)
		self.moveHistory = []

	def save(self, timesTrained):
	#SAVES THE CURRENT CONFIG TO A CSV FILE
		trainedBoardPosition = [] 
		trainedConfig = []

		for box in boxes:
			trainedBoardPosition.append(box.boardPosition)
			trainedConfig.append(box.moves)
		trainedConfig_DataFrame = pd.DataFrame({'handCombinations':trainedBoardPosition, 'trainedConfig':trainedConfig})
		trainedConfig_DataFrame.to_csv('logs/config_player{}_x{}.csv'.format(self.playerID, timesTrained), index=False)
	
	'''def load(self, src):
		loadedConfig = pd.read_csv(src)
		for index, row in loadedConfig.iterrows():
				boxes[index].boardPosition = list(row['handCombinations'])
				boxes[index].moves = row['trainedConfig']'''
	
	def reduceMoves(self):
		for box in boxes:
			box.reduceMoves()

class Board:
	def __init__(self, initialBoard):
		'''INITIALIZES A Board OBJECT
		ARGS:
			initialBoard: ((x, y), (a, b)), the starting board position'''
		#when initialBoard = ((x, y), (a, b)):
		#	self.player1 = (x, y)
		#	self.player2 = (a, b)
		self.player1 = initialBoard[0]
		self.player2 = initialBoard[1]
		
		#Sorts playerX into an array in ascending order
		#playerX[0] = the lowest value
		#playerX[1] = the highest value
		self.player1 = sorted(self.player1)
		self.player2 = sorted(self.player2)

	def sort(self):
		'''SORTS THE 2 CURRENT HANDS INTO CORRECT HIGHEST AND LOWEST POSITIONS TO ACCOUNT FOR NEW MOVES'''
		player1_low = min(self.player1)
		player1_high = max(self.player1)
		player2_low = min(self.player2)
		player2_high = max(self.player2)

		#Sets values >5 to 5 to match format on the boxes
		if player1_low > 5:
			player1_low = 5
		if player1_high > 5:
			player1_high = 5
		if player2_low > 5:
			player2_low = 5
		if player2_high > 5:
			player2_high = 5
	
		self.player1[0] = player1_low
		self.player1[1] = player1_high
		self.player2[0] = player2_low
		self.player2[1] = player2_high
		

	def export(self):
		'''EXPORTS INTERNAL BOARD STATE TO FORMAT MATCHING THE LABEL IN THE BOX OBJECT'''
		player1_low = self.player1[0]
		player1_high = self.player1[1]
		player2_low = self.player2[0]
		player2_high = self.player2[1]

		return ((player1_low, player1_high), (player2_low, player2_high))

class Game:
	
	def __init__(self, initialBoard):
		'''INITIALIZES GAME OBJECT AND WRAPPS A BOARD OBJECT IN IT'''
		self.board = Board(initialBoard=initialBoard)

	def makeMove(self, playerID, move):
		'''CHANGES THE BOARD ACCORDING TO A CERTAIN MOVE, RETURNS FALSE IF THAT MOVE IS ILLEGAL
		ARGS:
			playerID: int (1 or 2), the player that makes the move
			move: string ('LtH', 'HtL', 'LtL', 'HtL', 'splt'), the move to make'''
		if playerID == 1:
			if move == 'LtH':
				self.board.player2[1] += self.board.player1[0]	
			elif move == 'HtL':
				self.board.player2[0] += self.board.player1[1]	
			elif move == 'LtL':
				self.board.player2[0] += self.board.player1[0]	
			elif move == 'HtH':
				self.board.player2[1] += self.board.player1[1]
			elif move == 'splt':
				if self.board.player1[0] == 2 and self.board.player1[1] >= 5:
					self.board.player1[1] = 1
					self.board.player1[0] = 1
				elif self.board.player1[0] == 4 and self.board.player1[1] >= 5:
					self.board.player1[1] = 2
					self.board.player1[0] = 2
				else:
					#ILLEGAL MOVE
					raise TypeError('Illegal Move')
			else:
				#INVALID/ILLEGAL MOVE
				raise TypeError('Illegal Move')
		elif playerID == 2:
			if move == 'LtH':
				self.board.player1[1] += self.board.player2[0]	
			elif move == 'HtL':
				self.board.player1[0] += self.board.player2[1]	
			elif move == 'LtL':
				self.board.player1[0] += self.board.player2[0]	
			elif move == 'HtH':
				self.board.player1[1] += self.board.player2[1]
			elif move == 'splt':
				if self.board.player2[0] == 2 and self.board.player2[1] >= 5:
					self.board.player2[1] = 1
					self.board.player2[0] = 1
				elif self.board.player2[0] == 4 and self.board.player2[1] >= 5:
					self.board.player2[1] = 2
					self.board.player2[0] = 2
				else:
					#ILLEGAL MOVE
					raise TypeError('Illegal Move')
			else:
				#INVALID/ILLEGAL MOVE
				raise TypeError('Illegal Move')
		self.board.sort()

	def checkWinState(self):
		'''RETURNS A playerID IF ANY PLAYER HAS WON [THE OPPONENTS HAND = (>= 5, >= 5)], RETURNS FALSE OTHERWISE
		TO BE RUN AT THE END OF EVERY TURN'''
		#PLAYER 1 LOSES -> PLAYER 2 WINS
		if self.board.player1[0] >= 5 and self.board.player1[1] >= 5:
			return 2
		#PLAYER 2 LOSES -> PLAYER 1 WINS
		if self.board.player2[0] >= 5 and self.board.player2[1] >= 5:
			return 1
		else:
			return False

#SETUP
player1 = MENACE(playerID=1)
player2 = MENACE(playerID=2)
initialBoard=((1, 1), (1, 1))
game = Game(initialBoard=initialBoard)

def simulateMatch():
	'''PLAYS A MATCH BETWEEN THE TWO SIMULATORS, PRINTING OUT THE MOVES AND BOARDPOSITIONS CONTINIOUSLY.'''
	#EITHER 1 OR 2, DEPENDING ON WHOOSE TURN IT IS
	turnCounter = 1
	print(game.board.export())
	while game.checkWinState() == False:
		if turnCounter == 1:
			move = player1.chooseMove(game.board.export())
			game.makeMove(move=move, playerID=1)
			turnCounter = 2
		elif turnCounter == 2:
			move = player2.chooseMove(game.board.export())
			game.makeMove(move=move, playerID=2)
			turnCounter = 1
		print(game.board.export())
	print('GAME WON BY P{}!'.format(game.checkWinState()))
	print('---------------------------------')

def simulateMatch():
	#EITHER 1 OR 2, DEPENDING ON WHOOSE TURN IT IS
	turnCounter = 1
	print(game.board.export())
	while game.checkWinState() == False:
		if turnCounter == 1:
			move = player1.chooseMove(game.board.export())
			game.makeMove(move=move, playerID=1)
			turnCounter = 2
		elif turnCounter == 2:
			move = player2.chooseMove(game.board.export())
			game.makeMove(move=move, playerID=2)
			turnCounter = 1
		print(game.board.export())
	print('GAME WON BY P{}!'.format(game.checkWinState()))
	print('---------------------------------')

def trainUnsupervised(numberOfMatches):
	'''PLAYS A CERTAIN NUMBER OF MATCHES BETWEEN THE TWO SIMULATORS, TRAINING THEM AFTER EACH MATCH
	ARGS:
		numberOfMatches: int, the number of matches to be played between the two simulators'''
	for n in range(0, numberOfMatches):
		print('GAME NUMBER {}'.format(n))
		simulateMatch()
		winnerID = game.checkWinState()
		if winnerID == 1:
			player1.train(victory=True) 
			player2.train(victory=False) 
		elif winnerID == 2:
			player2.train(victory=True) 
			player1.train(victory=False) 
		#RESETS THE BOARD FOR THE NEXT MATCH
		game.board = Board(initialBoard=initialBoard)
		#REDUCES THE NUMBER OF MOVES IN THE BOXES EVERY TENTH GAME
		if n % 10 == 0:
			player1.reduceMoves()
			player2.reduceMoves()
			print('MOVES REDUCED')
			print('-----------------------')

def playMatch():
	#EITHER 1 OR 2, DEPENDING ON WHOOSE TURN IT IS
	turnCounter = 1

	#THE PLAYER ID OF THE HUMAN AND THE SIMULATOR
	humanID = int(input("PLAY AS P1 OR P2? (ENTER '1' FOR P1 AND '2' FOR P2): "))
	
	print(game.board.export())
	while game.checkWinState() == False:
		if humanID == 1:
			if turnCounter == 1:
				move = input('HUMAN MOVE: ')
				game.makeMove(move=move, playerID=1)
				turnCounter = 2
			elif turnCounter == 2:
				move = player2.chooseMove(game.board.export())
				game.makeMove(move=move, playerID=2)
				turnCounter = 1
			print(game.board.export())
		elif humanID == 2:
			if turnCounter == 2:
				move = input('HUMAN MOVE: ')
				game.makeMove(move=move, playerID=2)
				turnCounter = 1
			elif turnCounter == 1:
				move = player1.chooseMove(game.board.export())
				game.makeMove(move=move, playerID=1)
				turnCounter = 2
			print(game.board.export())
		else:
			print('INVALID PLAYER, EXITING...')
			return	
	print('GAME WON BY P{}!'.format(game.checkWinState()))
	print('---------------------------------')
	game.board = Board(initialBoard=initialBoard)

def trainSupervised(humanID):
	#EITHER 1 OR 2, DEPENDING ON WHOOSE TURN IT IS
	turnCounter = 1
	
	if humanID == 1:
		simulatorObject = player2
	elif humanID == 2:
		simulatorObject = player1
	
	print(game.board.export())
	while game.checkWinState() == False:
		if humanID == 1:
			if turnCounter == 1:
				move = input('HUMAN MOVE: ')
				game.makeMove(move=move, playerID=1)
				turnCounter = 2
			elif turnCounter == 2:
				move = player2.chooseMove(game.board.export())
				game.makeMove(move=move, playerID=2)
				turnCounter = 1
			print(game.board.export())
		elif humanID == 2:
			if turnCounter == 2:
				move = input('HUMAN MOVE: ')
				game.makeMove(move=move, playerID=2)
				turnCounter = 1
			elif turnCounter == 1:
				move = player1.chooseMove(game.board.export())
				game.makeMove(move=move, playerID=1)
				turnCounter = 2
			print(game.board.export())
		else:
			print('INVALID PLAYER, EXITING...')
			return	
	print('GAME WON BY P{}!'.format(game.checkWinState()))
	print('---------------------------------')
	winnerID = game.checkWinState()
	if winnerID == humanID:
		simulatorObject.train(victory=False)
	elif winnerID != humanID:
		simulatorObject.train(victory=True)
	print('UPDATING MODELS...')
	simulatorObject.reduceMoves()
	game.board = Board(initialBoard=initialBoard)

	option = input('CONTINUE TRAINING? (Y/N):')
	if option == 'Y': 
		trainSupervised(humanID)
	elif option == 'N':
		return

option = input("TRAIN NEW SIMULATORS UNSUPERVISED OR SUPERVISED? (ENTER '1' TO TRAIN UNSUPERVISED AND '2' TO TRAIN SUPERVISED): ")
if option == '1':
	inputNumber = input('NUMBER OF MATCHES TO TRAIN ON: ')
	trainUnsupervised(int(inputNumber))
	option = input('SHOULD THE TRAINED CONFIGS BE SAVED? (Y/N): ')
	if option == 'Y':
		player1.save(inputNumber)
		player2.save(inputNumber)
	elif option == 'N':
		_ = 0 
elif option == '2':
	humanID = input('PLAY AS WHICH PLAYER: ')
	trainSupervised(int(humanID))
	option = input('SHOULD THE TRAINED CONFIGS BE SAVED? (Y/N): ')
	if option == 'Y':
		player1.save(inputNumber)
		player2.save(inputNumber)
	elif option == 'N':
		_ = 0 
'''elif option == 'load':
	player1.load(src='config_player1.csv')
	player2.load(src='config_player2.csv')
else:
	print('INVALID OPTION, EXITING...')
'''
while True:
	option = input('PLAY A MATCH AGAINST A SIMULATOR? (Y/N):' )	
	if option == 'Y':
		playMatch()
	elif option == 'N':
		break
