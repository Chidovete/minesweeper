import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.num_rows = 10
        self.num_cols = 10
        self.num_mines = 15
        self.create_widgets()
        self.create_board()

    def create_widgets(self):
        # Create frame for the game board
        self.board_frame = tk.Frame(self.master)
        self.board_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Label and Entry for Number of Mines
        tk.Label(self.master, text="Number of Mines:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.mines_entry = tk.Entry(self.master)
        self.mines_entry.grid(row=0, column=1, padx=5, pady=5)

        # Start and Restart Buttons
        start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        start_button.grid(row=0, column=2, padx=5, pady=5)

        self.restart_button = tk.Button(self.master, text="Restart Game", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.grid(row=0, column=3, padx=5, pady=5)

        # Create the game board grid of buttons
        self.buttons = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                btn = tk.Button(self.board_frame, width=4, height=2, font=('Helvetica', 10, 'bold'),
                                command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons.append(btn)

    def start_game(self):
        if not hasattr(self, 'mines_entry'):
            messagebox.showerror("Error", "Entry widget not found. Please restart the game.")
            return

        try:
            self.num_mines = int(self.mines_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of mines. Please enter an integer.")
            return

        self.mines_entry.destroy()
        self.create_board()

    def create_board(self):
        self.board = [[0] * self.num_cols for _ in range(self.num_rows)]
        self.plant_mines()

    def plant_mines(self):
        mines_planted = 0
        while mines_planted < self.num_mines:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_planted += 1

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.board[r][c] != -1:
                    self.board[r][c] = self.count_neighboring_mines(r, c)

    def count_neighboring_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r != row or c != col) and 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                    if self.board[r][c] == -1:
                        count += 1
        return count

    def on_click(self, row, col):
        if self.board[row][col] == -1:
            self.reveal_board()
            messagebox.showinfo("Game Over", "You clicked on a mine! Game Over.")
            self.restart_button.config(state=tk.NORMAL)
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                messagebox.showinfo("Congratulations", "You Win! All mines flagged.")
                self.reveal_board()
                self.restart_button.config(state=tk.NORMAL)

    def reveal_cell(self, row, col):
        if self.buttons[row * self.num_cols + col]['state'] == tk.DISABLED:
            return

        value = self.board[row][col]
        self.buttons[row * self.num_cols + col].config(text=str(value), state=tk.DISABLED)

        if value == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                n_row, n_col = row + dr, col + dc
                if 0 <= n_row < self.num_rows and 0 <= n_col < self.num_cols:
                    if self.buttons[n_row * self.num_cols + n_col]['state'] == tk.NORMAL:
                        self.reveal_cell(n_row, n_col)

    def reveal_board(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.buttons[r * self.num_cols + c]['state'] == tk.NORMAL:
                    self.reveal_cell(r, c)

    def check_win(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.board[r][c] != -1 and self.buttons[r * self.num_cols + c]['state'] == tk.NORMAL:
                    return False
        return True

    def restart_game(self):
        self.create_widgets()
        self.restart_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    minesweeper = MinesweeperGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
