# reset pickle dict if error

import pickle

dick = {x: [] for x in range(81)}
print(dick)
with open('db_sudoku.pickle', 'wb') as f:
      pickle.dump(dick, f)
