import tkinter as tk
import tkinter.messagebox
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("350x500")
        self.create_main_menu()
        self.game_mode = None

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack()
        tk.Label(self.main_menu_frame, text="Tic Tac Toe", font=('Helvetica', 18)).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Player vs Player", command=self.start_pvp_game).pack()
        tk.Button(self.main_menu_frame, text="Player vs AI", command=self.start_pva_game).pack()

    def start_pvp_game(self):
        self.game_mode = "PvP"
        self.prepare_new_game()

    def start_pva_game(self):
        self.game_mode = "PvAI"
        self.prepare_new_game()


    # Sets up a new game
        
    def prepare_new_game(self):
        self.main_menu_frame.destroy()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()
        self.current_player = "X"
        self.scoreboard = {'X': {'Wins': 0, 'Losses': 0, 'Draws': 0}, 'O': {'Wins': 0, 'Losses': 0, 'Draws': 0}}
        self.display_scoreboard()
        self.player_label = tk.Label(self.game_frame, text="Player X's Turn", font=('Helvetica', 14))
        self.player_label.grid(row=3, column=0, columnspan=3)
        self.initialize_board()


    # Displays the current scoreboard
        
    def display_scoreboard(self):
        scoreboard_text = f"X - Wins: {self.scoreboard['X']['Wins']} Losses: {self.scoreboard['X']['Losses']} Draws: {self.scoreboard['X']['Draws']}\n"
        scoreboard_text += f"O - Wins: {self.scoreboard['O']['Wins']} Losses: {self.scoreboard['O']['Losses']} Draws: {self.scoreboard['O']['Draws']}"
        self.scoreboard_label = tk.Label(self.game_frame, text=scoreboard_text, font=('Helvetica', 14))
        self.scoreboard_label.grid(row=6, column=0, columnspan=3)


    # Updates the scoreboard based on game result
    # Logic to update wins, losses, and draws

    def update_scoreboard(self, result):
        if result == 'Draw':
            self.scoreboard['X']['Draws'] += 1
            self.scoreboard['O']['Draws'] += 1
        else:
            self.scoreboard[result]['Wins'] += 1
            loser = 'O' if result == 'X' else 'X'
            self.scoreboard[loser]['Losses'] += 1

        self.display_scoreboard()


    # Initializes the game board with buttons
    # Creating a 3x3 grid of buttons for the game

    def initialize_board(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="", height=3, width=6, font=('Helvetica', 20),
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button
        reset_button = tk.Button(self.game_frame, text="Reset Game", command=self.reset_board)
        reset_button.grid(row=4, column=0, columnspan=3)
        end_game_button = tk.Button(self.game_frame, text="End Game", command=self.end_game)
        end_game_button.grid(row=7, column=0, columnspan=3)


    # Handles a button click during the game
    # Logic for player/AI moves, checking for winner or draw

    def on_button_click(self, row, col):
        button = self.buttons[row][col]
        if button["text"] == "" and not self.check_winner():
            button["text"] = self.current_player
            if self.check_winner():
                winner = self.current_player  # Define winner here
                tk.messagebox.showinfo("Tic Tac Toe", f"Player {winner} wins!")
                self.update_scoreboard(winner)  # Now winner is defined
                self.reset_board()
            elif self.check_draw():
                tk.messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.update_scoreboard('Draw')
                self.reset_board()
            else:
                self.toggle_player()
                if self.game_mode == "PvAI" and self.current_player == "O":
                    self.make_ai_move()
    

    # Checks if there is a winner
    # Logic to check all winning conditions
    
    def check_winner(self):
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                return True
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                return True
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return True
        return False


    # Checks if the game is a draw
    # Logic to determine a draw

    def check_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3)) and not self.check_winner()


    # Resets the game board for a new game
    # Logic to clear the board and reset player

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
        self.current_player = "X"
        self.player_label["text"] = "Player X's Turn"
    

    # Switches turn between Player X and Player O
        
    def toggle_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.player_label["text"] = f"Player {self.current_player}'s Turn"
    
    
    # Ends the current game and returns to main menu
        
    def end_game(self):
        self.game_frame.destroy()
        self.create_main_menu()


    # AI makes a move in PvAI mode
    # Logic for AI to choose the best move
        
    def make_ai_move(self):
        move = self.best_move()
        if move:
            self.buttons[move[0]][move[1]]["text"] = "O"
            if self.check_winner():
                tk.messagebox.showinfo("Tic Tac Toe", "AI wins!")
                self.reset_board()
            elif self.check_draw():
                tk.messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_board()
            else:
                self.toggle_player()
    
    
    # Determines the best move for AI
    # Implements the minimax algorithm for AI
                
    def best_move(self):
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move


    # Minimax algorithm to calculate the best move for AI
    # Recursive function for evaluating game states

    def minimax(self, is_maximizing):
        winner = self.check_winner_minimax()
        if winner != None:
            return {'X': -1, 'O': 1, 'Draw': 0}[winner]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "O"
                        score = self.minimax(False)
                        self.buttons[i][j]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "X"
                        score = self.minimax(True)
                        self.buttons[i][j]["text"] = ""
                        best_score = min(score, best_score)
            return best_score


    # Checks for a winner specifically for the minimax function
    # Similar logic as check_winner but tailored for minimax
    
    def check_winner_minimax(self):
        
        # Check rows
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                return self.buttons[i][0]["text"]
        # Check columns
        for i in range(3):
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                return self.buttons[0][i]["text"]
        # Check diagonals
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return self.buttons[0][0]["text"]
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return self.buttons[0][2]["text"]
        # Check for draw
        if all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3)):
            return 'Draw'
        return None


# Main function to run the application
    
if __name__ == "__main__":  
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()