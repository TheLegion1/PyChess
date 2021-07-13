from tkinter import Tk, Canvas, Frame, BOTH
import tkinter as tk
from PIL import Image, ImageTk

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

pTMask = 0b00111
pBMask = 0b10000
pWMask = 0b01000
cMask = pBMask | pWMask

img_paths = [
	'wKing.png',      #0
	'wPawn.png',      #1
	'wRook.png',      #2
	'wQueen.png',     #3
	'wBishop.png',    #4
	'wKnight.png',    #5
	'bKing.png',      #6
	'bPawn.png',      #7
	'bRook.png',      #8
	'bBishop.png',    #9
	'bQueen.png',     #10
	'bKnight.png'     #11
]
fen_dict = {
	'k': KING,
	'p': PAWN,
	'n': KNIGHT,
	'b': BISHOP,
	'r': ROOK,
	'q': QUEEN
}
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
ran_fen = "ppppkppp/pppppppp/8/8/8/8/QQQQQQQQ/QQQQKQQQ"
board_data = [0] * 64

themes = [
		("#fcc692", "#5e3610"),
		("#ffffff", "#000000"),
		("#ffc7a8", "#21060f"),
		("#BFFF00", "#000000"),
		("#FF00FF", "#000000")

]


def getColor(rank, file, light_color, dark_color):
	isDark = ((file + rank) % 2) != 0
	if isDark:
		color = dark_color
	else:
		color = light_color
	return color


class ChessBoard(Frame):
	
	def onPieceClick(self, trash, piece):
			print("You Clicked on a Piece. This piece was located at: " + str(piece))
		


	def convertFEN(self, fen_str):
		#code here to convert fen string to meaningful data
		fen_board = fen_str.split(' ')
		file = 0
		rank = 0

		for symb in fen_board[0]:
			if symb == '/':
				file = 0
				rank += 1
			else:
				if symb.isdigit():
					file += int(symb)
				else:
					isDark = symb.isupper()
					if isDark:
						color = WHITE
					else:
						color = BLACK
					piece = fen_dict[symb.lower()]
					board_data[rank * 8 + file] = piece | color
					file += 1

	def fillBoardWithPieces(self, canvas, light_color, dark_color):
		self.img = [0] * 64
		sq_size = 50
		init_x = 20
		init_y = 20
		cur_x = init_x
		cur_y = init_y
		for rank in range(8):
			for file in range(8):
				piece = board_data[rank * 8 + file] & pTMask
				color = board_data[rank * 8 + file] & cMask
				pieceLocation = (rank*8 + file)
				img_str = ''
				if piece == PAWN:
					if(color == WHITE): img_str = img_paths[1] #white pawn
					if(color == BLACK): img_str = img_paths[7] #black pawn
				elif piece == KNIGHT:
					if(color == WHITE): img_str = img_paths[5] #white kngiht
					if(color == BLACK): img_str = img_paths[11] #black knight
				elif piece == BISHOP:
					if(color == WHITE): img_str = img_paths[4] #white bishop
					if(color == BLACK): img_str = img_paths[9] #black bishop
				elif piece == KING:
					if(color == WHITE): img_str = img_paths[0] #white king
					if(color == BLACK): img_str = img_paths[6] #black king
				elif piece == QUEEN:
					if(color == WHITE): img_str = img_paths[3] #white queen
					if(color == BLACK): img_str = img_paths[10] #black queen
				elif piece == ROOK:
					if(color == WHITE): img_str = img_paths[2] #white rook
					if(color == BLACK): img_str = img_paths[8] #black rook
				
				if img_str != "":
					#self.img[rank * 8 + file] = ImageTk.PhotoImage(file=img_str)
					tmp_img = Image.open(str(img_str), 'r')
					#print(tmp_img.mode)
					self.img[rank * 8 + file] = ImageTk.PhotoImage(tmp_img)
				else:
					self.img[rank * 8 + file] = ImageTk.PhotoImage(Image.new(mode="RGBA", size=(sq_size, sq_size), color=(0,0,0,0)))
				#canvas.create_image(cur_x, cur_y, anchor='nw', image=self.img[rank * 8 + file])
				l = tk.Label(canvas, image= self.img[rank * 8 + file])
				l.config(bg=getColor(rank, file, light_color, dark_color))
				l.pack()
				l.place(x=cur_x, y=cur_y, anchor='nw')
				
				l.bind('<Button-1>', lambda trash= '', arg2 = pieceLocation : self.onPieceClick(trash, arg2))
				cur_x += sq_size
			cur_y += sq_size
			cur_x = init_x



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

		canvas = Canvas(self, width=440, height=440)
		current_theme = 0
		light_color = themes[current_theme][0]
		dark_color = themes[current_theme][1]
		canvas.pack(fill=BOTH, expand=1)
		self.draw_board(canvas, light_color, dark_color)
		self.convertFEN(starting_fen)
		self.fillBoardWithPieces(canvas, light_color, dark_color)

def main():
	root = Tk()
	ex = ChessBoard()
	root.mainloop()

if __name__ == "__main__":
	main()
