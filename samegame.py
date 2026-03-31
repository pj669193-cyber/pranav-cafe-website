import tkinter as tk
import random

COLORS = ['red', 'blue', 'green', 'yellow', 'purple']
ROWS = 15
COLS = 15
CELL_SIZE = 40

class SameGame:
    def __init__(self, master):
        self.master = master
        self.master.title("SameGame")
        self.canvas = tk.Canvas(master, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg='lightgray')
        self.canvas.pack()
        
        self.score = 0
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=('Arial', 14))
        self.score_label.pack()
        
        self.status_label = tk.Label(master, text="", font=('Arial', 12), fg='red')
        self.status_label.pack()
        
        self.restart_button = tk.Button(master, text="Restart", command=self.start_game)
        self.restart_button.pack()
        
        self.board = []
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.start_game()

    def start_game(self):
        self.score = 0
        self.update_score()
        self.status_label.config(text="")
        self.board = [[random.choice(COLORS) for _ in range(ROWS)] for _ in range(COLS)]
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for col in range(COLS):
            for row in range(ROWS):
                color = self.board[col][row]
                if color:
                    x0 = col * CELL_SIZE
                    y0 = row * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags=f"cell_{col}_{row}")

    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        
        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            return
            
        color = self.board[col][row]
        if not color:
            return
            
        # Find connected components
        group = self.find_group(col, row, color)
        if len(group) >= 2:
            self.status_label.config(text="")
            self.remove_group(group)
            self.apply_gravity()
            self.slide_columns()
            self.draw_board()
            
            # Update score
            points = len(group) * 10
            self.score += points
            self.update_score()
            
            self.check_game_over()
        else:
            self.status_label.config(text="Must select a group of 2 or more same-colored blocks!")

    def find_group(self, c, r, color):
        visited = set()
        queue = [(c, r)]
        group = []
        
        while queue:
            cc, cr = queue.pop(0)
            if (cc, cr) in visited:
                continue
            visited.add((cc, cr))
            
            if 0 <= cc < COLS and 0 <= cr < ROWS and self.board[cc][cr] == color:
                group.append((cc, cr))
                # Add neighbors
                queue.extend([(cc+1, cr), (cc-1, cr), (cc, cr+1), (cc, cr-1)])
                
        return group

    def remove_group(self, group):
        for c, r in group:
            self.board[c][r] = None

    def apply_gravity(self):
        for col in range(COLS):
            # Read from bottom to top
            new_col = []
            for row in range(ROWS - 1, -1, -1):
                if self.board[col][row] is not None:
                    new_col.append(self.board[col][row])
            
            # Fill the rest with None
            while len(new_col) < ROWS:
                new_col.append(None)
                
            # Reverse and put back
            new_col.reverse()
            self.board[col] = new_col

    def slide_columns(self):
        new_board = []
        for col in range(COLS):
            # Check if column is totally empty
            if any(self.board[col][row] is not None for row in range(ROWS)):
                new_board.append(self.board[col])
                
        # Fill remaining columns with all None
        while len(new_board) < COLS:
            new_board.append([None for _ in range(ROWS)])
            
        self.board = new_board

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def check_game_over(self):
        # A simple check: if no groups of 2+ exist, game is over
        for c in range(COLS):
            for r in range(ROWS):
                color = self.board[c][r]
                if color:
                    # Check right and down for same color
                    if c + 1 < COLS and self.board[c+1][r] == color:
                        return # valid move exists
                    if r + 1 < ROWS and self.board[c][r+1] == color:
                        return # valid move exists
                        
        self.canvas.create_text(COLS * CELL_SIZE / 2, ROWS * CELL_SIZE / 2, text="GAME OVER", font=('Arial', 24, 'bold'), fill='black')

if __name__ == "__main__":
    root = tk.Tk()
    game = SameGame(root)
    root.mainloop()
