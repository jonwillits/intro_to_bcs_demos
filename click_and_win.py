import tkinter as tk
import random


class Display:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Click and Win!")

        self.button_frame = tk.Frame(self.root, height=600, width=400, bg='black')
        self.button_frame.pack(side=tk.LEFT)

        self.a_button = tk.Button(self.button_frame, text="A", fg="black", command=self.clicked_a, width=10, padx=20, pady=50)
        self.b_button = tk.Button(self.button_frame, text="B", fg="black", command=self.clicked_b, width=10, padx=20, pady=50)
        self.a_button.place(x=100, y=100)
        self.b_button.place(x=100, y=300)

        self.results_frame = tk.Frame(self.root, height=600, width=400, bg='grey')
        self.results_frame.pack(side=tk.LEFT)
        self.results_canvas = tk.Canvas(self.results_frame, height=600, width=400, bg="#000000", bd=5,
                                        highlightthickness=0, relief='ridge')
        self.results_canvas.pack(side=tk.LEFT)

        self.clicked_list = []

        choice_list = ['a', 'b']
        random.shuffle(choice_list)
        self.winner = choice_list[0]
        self.loser = choice_list[1]
        self.score = 0
        self.win = None
        self.winner_advantage = 0.80

        self.update_results_canvas()

    def update_results_canvas(self):
        print("HERE")
        self.results_canvas.delete("all")
        score_string = "Score: {}".format(self.score)
        self.results_canvas.create_text(120, 40, fill='white', text=score_string, font="Arial 20 bold")
        if self.win is not None:
            if self.win:
                self.results_canvas.create_text(180, 100, fill='green', text='Win!', font="Arial 20 bold",)
            else:
                self.results_canvas.create_text(180, 100, fill='red', text='Lose!', font="Arial 20 bold")

    def check_winner(self, choice):
        probability = random.random()
        if probability > 0.40:
            the_winner = self.winner
        else:
            the_winner = self.loser
        if choice == the_winner:
            self.win = True
            self.score += 10
        else:
            self.win = False
            self.score -= 10

        self.update_results_canvas()
        print("\t", self.winner, the_winner, choice, self.win, self.score)

    def clicked_a(self):
        print("A")
        self.clicked_list.append('a')
        self.check_winner('a')
        self.update_results_canvas()

    def clicked_b(self):
        print("B")
        self.clicked_list.append('b')
        self.check_winner('b')
        self.update_results_canvas()


def main():
    the_display = Display()
    the_display.root.mainloop()


main()
