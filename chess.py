from tkinter import Tk, Canvas, Frame, BOTH

#the "static" values for the colors and pieces
NONE = 0
KING = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
WHITE = 8
BLACK = 16

fen_dict = {
	'k': KING,
	'p': PAWN,
	'n': KNIGHT,
	'b': BISHOP,
	'r': ROOK,
	'q': QUEEN
}
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class ChessBoard(Frame):
	board_data = []
	def convertFEN(self, fen_str):
		#code here to convert fen string to meaningful data
		fen_board = fen_str.split(' ')[0]
		file = 0
		rank = 0

		for symb in fen_board:
			if symb == '/':
				file = 0
				rank -= 1
			else:
				if symb.isdigit():
					file += int(symb)
				else:
					isLight = symb.isUpper()
					if isLight:
						color = WHITE
					else:
						color = BLACK
					piece = fen_dict[symb.lower()]
					board_data[rank * 8 + file] = piece | color

	#rank - row
	#file - column
	def draw_board(self, canvas, light_color, dark_color):
		sq_size = 50
		init_x = 20
		init_y = 20
		cur_x = init_x
		cur_y = init_y
		for file in range(8):
			for rank in range(8):
				isDark = ((file + rank) % 2) != 0
				if isDark:
					color = dark_color
				else:
					color = light_color
				canvas.create_rectangle(cur_x, cur_y, cur_x + sq_size, cur_y + sq_size, outline="", fill=color)
				
				cur_x += sq_size
			cur_x = init_x
			cur_y += sq_size

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.master.title("ChessBoard")
		self.pack(fill=BOTH, expand=1)

		canvas = Canvas(self)
		light_color = "#fcc692"
		dark_color = "#5e3610"
		self.draw_board(canvas, light_color, dark_color)
		canvas.pack(fill=BOTH, expand=1)

def main():
	root = Tk()
	ex = ChessBoard()
	root.mainloop()

if __name__ == "__main__":
	main()
