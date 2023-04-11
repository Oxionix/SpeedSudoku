import pickle

sud_db = {x: [] for x in range(81)}
difs = {
    "schwer": 50,
    "mittel": 44,
    "leicht": 40,
    "sehr leicht": 20
}

has_new_user = False
user_db = {}  # "username": password

def read_user_db():
    global user_db
    with open('db_users.pickle', 'rb') as f:
        try:
            user_db = pickle.load(f)
        except:
            user_db = {}

def write_user_db():
    global user_db
    with open('db_users.pickle', 'wb') as f:
        pickle.dump(user_db, f)


def read_sud_db():
    global sud_db
    with open('db_sudoku.pickle', 'rb') as f:
        try:
            sud_db = pickle.load(f)
        except:
            sud_db = {}

def write_sud_db():
    global sud_db
    with open('db_sudoku.pickle', 'wb') as f:
        pickle.dump(sud_db, f)
