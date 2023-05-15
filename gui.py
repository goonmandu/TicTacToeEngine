import tkinter as tk
from tictactoe import TicTacToe, move_evaluations, InvalidBoardException

jb16 = ("JetBrains Mono", 16)
jb14 = ("JetBrains Mono", 14)


class ChooseXOClear(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Choose a symbol")
        self.geometry("300x100+500+500")
        self.result = None

        label = tk.Label(self, text="Choose a symbol:", font=jb16)
        label.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack()

        x_button = tk.Button(button_frame, text="X", width=3, command=lambda: self.set_result("X"))
        x_button.grid(row=0, column=0, padx=5)

        o_button = tk.Button(button_frame, text="O", width=3, command=lambda: self.set_result("O"))
        o_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(button_frame, text="Clear", width=3, command=lambda: self.set_result("Clear"))
        clear_button.grid(row=0, column=2, padx=5)

    def set_result(self, result):
        self.result = result
        self.destroy()


class TTTApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x520+600+300")
        self.window.title("Tic Tac Toe Engine")

        label = tk.Label(self.window, text="Board", font=jb16)
        label.pack()

        self.boardframe = tk.Frame()
        for i in range(3):
            self.boardframe.columnconfigure(i, weight=1)

        for k, label in enumerate(('A', 'B', 'C')):
            lbl = tk.Label(self.boardframe, text=label, font=jb16)
            lbl.grid(row=0, column=k+1)

        for i, label in enumerate(('1', '2', '3')):
            lbl = tk.Label(self.boardframe, text=label, font=jb16)
            lbl.grid(row=i+1, column=0)

        self.buttons = []
        for i in range(3):
            for k in range(3):
                button = tk.Button(self.boardframe, text="", width=4, height=3, font=jb16, command=lambda i=i, k=k: self.fill_button(self.buttons[3*i+k]))
                button.grid(row=i+1, column=k+1)
                self.buttons.append(button)

        self.boardframe.pack()

        evalbutton = tk.Button(self.window, text="Evaluate", width=10, height=1, font=jb16, command=self.get_board_state)
        evalbutton.pack()

        self.moves = tk.Label(self.window, text="Evaluations will appear here.", font=jb14, justify='left')
        self.moves.pack(padx=10, pady=10)

        self.window.mainloop()

    def fill_button(self, button: tk.Button):
        dialog = ChooseXOClear(self.window)
        self.window.wait_window(dialog)
        choice = dialog.result

        if choice == "X":
            button.config(text="X")
        elif choice == "O":
            button.config(text="O")
        else:
            button.config(text="")

        self.moves.config(text="Evaluations will appear here.")

    def get_board_state(self):
        raw: list[list[int]] = [[] for _ in range(3)]
        for i in range(3):
            for k in range(3):
                btntext = self.buttons[3*i+k].cget("text")
                if btntext == "X":
                    raw[i].append(-1)
                elif btntext == "O":
                    raw[i].append(1)
                else:
                    raw[i].append(0)
        board = TicTacToe(raw)
        try:
            moves = move_evaluations(board)
        except InvalidBoardException as e:
            popup = tk.Toplevel(self.window)
            popup.geometry("300x65+750+600")
            lbl = tk.Label(popup, text=str(e))
            lbl.pack(pady=10)
            return
        moves_message = ""
        for move in moves:
            moves_message += f"{move.guistring()}\n"
        self.moves.config(text=moves_message)


TTTApp()
