import websockets

class alg:
    def __init__(self, alg_string, letter_pair, piece):
        self.alg_string = alg_string
        self.letter_pair = letter_pair
        self.piece = piece
        self.solves_times = []
        self.recognize_times = []
        self.row_excel = None
        self.col_excel = None
        self.sheet_excel = None

    def __init__(self, alg_string, letter_pair, piece, row_excel, col_excel, sheet_excel ):
        self.alg_string = alg_string
        self.letter_pair = letter_pair
        self.piece = piece
        self.solves_times = []
        self.recognize_times = []
        self.row_excel = row_excel
        self.col_excel = col_excel
        self.sheet_excel = sheet_excel

    def parse_alg_moves(self):
        pass