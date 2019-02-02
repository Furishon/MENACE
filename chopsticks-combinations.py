import itertools as it

#Creates list of all possible configuration a hand can consist of [(1, 1), (2, 3) etc.]
handPositions = list(it.combinations_with_replacement( range(1, 6), 2 ))
#Removes (5, 5) since the game is over when it appears
handPositions.remove((5, 5))

#handCombinations = list(it.combinations_with_replacement( handPositions, 2 ))
handCombinations = list(it.product( handPositions, repeat=2 ))
#print(handCombinations)
#################################
print('Number of unique hand positions: {}'.format(len(handPositions)))
#print('All unique hand positions: {}'.format(handPositions))

print('Number of unique match positions (combinations of two hands): {}'.format(len(handCombinations)))
#print('All unique match positions (combinations of two hands): {}'.format(handCombinations))


'''Writes handCombinations to "./handCombinations.csv"
import pandas as pd
printCSV = pd.DataFrame({'handCombinations':handCombinations})
printCSV.to_csv(path_or_buf='handCombinations.csv', index=False)
'''
