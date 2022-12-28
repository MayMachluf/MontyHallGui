import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import random
from mhProblemGp import *
from graph import *
import pandas as pd
import plotly.express as px
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

door_amount = 0
door_list = {}
game_stage = 0
score = {'win': 0, 'loss': 0}
game_count = 0


def check_input():
    global door_amount

    if not entry.get().isnumeric():
        tk.messagebox.showerror("error", "please enter number in digits")
        return

    if int(entry.get()) < 3 or int(entry.get()) > 200:
        tk.messagebox.showerror("error", "your number should be in range 3-200")
        return

    if door_amount != 0 and (door_amount != int(entry.get())):
        answer = tk.messagebox.askyesno(title="Warning",
                                        message="If you change your amount of doors your score will reset.\n"
                                                "Do you wish to continue?")
        if not answer:
            return
        else:
            reset_score()

    door_amount = int(entry.get())
    start_game()


def start_game():
    entry.pack_forget()
    lbl.pack_forget()
    btn.pack_forget()

    if door_amount in range(3, 7):
        show_doors()

    else:
        res = run_mh(door_amount)
        show_graph(res)


def show_graph(res):
    frame.pack_forget()
    doorFrame.pack_forget()
    midGameFrame.pack_forget()

    graphFrame.pack()

    tk.Label(graphFrame, text=f"number of partitions: {res[0]}").pack()
    tk.Label(graphFrame, text=f"number of games: {res[1]}").pack()
    tk.Label(graphFrame, text=f"number of wins because of choice change: {res[2]}").pack()
    tk.Label(graphFrame, text=f"number of losses because of choice change: {res[3]}").pack()
    tk.Label(graphFrame, text=f"number of choice change without influence: {res[4]}").pack()

    fig = Figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    ax.pie([res[2], res[3], res[4]],
           radius=1,
           labels=['wins after choice change',
                   'losses after choice change',
                   'No influence'],
           autopct='%0.2f%%',
           shadow=True)

    chart1 = FigureCanvasTkAgg(fig, graphFrame)
    chart1.get_tk_widget().pack(pady=10)

    score['win'] = score['win'] + int(res[2])
    score['loss'] = score['loss'] + (int(res[1]) - int(res[2]))
    refresh_score()


def show_doors():
    door_closed_image = ImageTk.PhotoImage(Image.open("images/door_closed.png"))

    for i in range(door_amount):
        door = tk.Button(doorFrame,
                         text=str(i + 1),
                         image=door_closed_image,
                         font='Helvetica 15 bold',
                         compound=tk.LEFT,
                         command=lambda x=i: door_pick(x))
        door.image = door_closed_image
        door.pack(side='left', expand=1)
        door_list[door] = "goat"

    key, val = random.choice(list(door_list.items()))
    door_list[key] = 'car'


def door_pick(door):
    global game_stage
    global game_count
    pick = list(door_list.keys())[door]

    if game_stage == 0:
        midGameFrame.pack()
        lbl = tk.Label(midGameFrame,
                       text="The presenter has revealed one of the goats for you, would you like to change your pick?")
        lbl.pack(pady=20)
        btnYes = tk.Button(midGameFrame, text="Yes")
        btnNo = tk.Button(midGameFrame, text="No")
        btnYes['command'] = lambda: yes_btn()
        btnNo['command'] = lambda: no_btn(door)
        btnYes.pack()
        btnNo.pack()

        while True:
            key, val = random.choice(list(door_list.items()))
            if key != pick and val != 'car':
                break

        change_picture(key)

    if game_stage == 1:
        change_picture(pick)
        if door_list.get(pick) == 'goat':
            for key, value in door_list.items():
                if value == 'car':
                    change_picture(key)

            lbl = tk.Label(frame, text="You were wrong!")
            lbl.pack(pady=30)
            score['loss'] = score['loss'] + 1
            game_count += 1

        else:
            lbl = tk.Label(frame, text="You were right!")
            lbl.pack(pady=30)
            score['win'] = score['win'] + 1
            game_count += 1

        againButton = tk.Button(midGameFrame, text="Try again", command=lambda: restart(True))
        againButton.pack(pady=30)
        game_stage = 3

    if game_stage == 2:
        change_picture(pick)

        if door_list.get(pick) == 'goat':
            for key, value in door_list.items():
                if value == 'car':
                    change_picture(key)
                    lbl = tk.Label(midGameFrame, text="You were wrong!")
                    lbl.pack(pady=30)
                    score['loss'] = score['loss'] + 1
                    game_count += 1
                    break

        else:
            lbl = tk.Label(frame, text="You were right!")
            lbl.pack(pady=30)
            score['win'] = score['win'] + 1
            game_count += 1

        againButton = tk.Button(midGameFrame, text="Try again", command=lambda: restart(True))
        againButton.pack(pady=30)
        game_stage = 3

    if game_stage == 3:
        return


def yes_btn():
    global game_stage
    for i in midGameFrame.winfo_children():
        i.pack_forget()

    game_stage = 1


def no_btn(door):
    global game_stage
    for i in midGameFrame.winfo_children():
        i.pack_forget()

    game_stage = 2
    door_pick(door)


def change_picture(labelname):
    if door_list.get(labelname) == 'goat':
        photo1 = ImageTk.PhotoImage(Image.open("images/door_goat.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1

    else:
        photo1 = ImageTk.PhotoImage(Image.open("images/door_car.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1


window = tk.Tk()
doorNumberEntry = tk.Entry(window)


# IMAGE
# img = ImageTk.PhotoImage(Image.open("images/background.jpg"))
# label1 = tk.Label(window, image=img)
# label1.place(x=0, y=0)


def start(skip_check=False):
    refresh_score()
    frame.pack()
    doorFrame.pack()
    lbl.pack(pady=5)
    entry.pack(pady=5)
    btn.pack()

    if skip_check:
        start_game()


def restart(skip_check=False):
    global game_stage, door_list, door_amount
    door_list = {}
    game_stage = 0

    for i in frame.winfo_children():
        i.pack_forget()

    for x in doorFrame.winfo_children():
        x.pack_forget()

    for x in midGameFrame.winfo_children():
        x.pack_forget()

    for x in graphFrame.winfo_children():
        x.pack_forget()

    frame.pack_forget()
    doorFrame.pack_forget()
    midGameFrame.pack_forget()
    graphFrame.pack_forget()

    start(skip_check)


def refresh_score():
    if score['win'] == 0 and score['loss'] == 0:
        statsLbl['text'] = f"No games played yet."

    else:
        statsLbl['text'] = f"Score: {score['win']} Wins, {score['loss']} Losses"


def reset_score():
    global score, door_amount
    score = {'win': 0, 'loss': 0}
    door_amount = 0
    refresh_score()
    restart()


frame = tk.Frame()
doorFrame = tk.Frame()
graphFrame = tk.Frame()
midGameFrame = tk.Frame()
lbl = tk.Label(frame, text="Please enter number of doors here")
entry = tk.Entry(frame)
btn = tk.Button(frame, text="Confirm", command=check_input)

bottomFrame = tk.Frame()
bottomFrame.pack(side=tk.BOTTOM)

btnRestart = tk.Button(bottomFrame, text="Restart Game", command=restart)
btnRestart.pack(side=tk.LEFT, padx=5, pady=10, expand=1)
resetScore = tk.Button(bottomFrame, text="Reset Score", command=reset_score)
resetScore.pack(side=tk.LEFT, padx=5, pady=10, expand=1)
btnStats = tk.Button(bottomFrame, text="Show Statistics")
btnStats.pack(side=tk.LEFT, padx=5, pady=10, expand=1)

statsLbl = tk.Label(window, text=f"Score: {score}")
statsLbl.pack(side=tk.BOTTOM, pady=10)

start()

window.geometry("1100x700")
window.mainloop()
