import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from mhProblemGp import *
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

door_amount = 0
door_list = {}
game_stage = 0
score = {'wins because of change': 0,
         'wins without change': 0,
         'losses due to change': 0,
         'losses without influence': 0,
         'losses without change': 0}
game_count = 0
previous_door_pick = 0
host_revealed = 0
warning = None


def check_input(simulation=False) -> None:
    """
    Check the use input in one of the input boxes

    Parameters:
    simulation (optional): differentiate between simulation and manual play

    Returns:
    None
    """
    global door_amount, warning

    if warning is not None:
        warning.pack_forget()

    if simulation:
        if not simulationDoorsEntry.get().isnumeric():
            warning = tk.Label(simulationFrame, text="please enter number in digits", fg='#f00')
            warning.pack()
            return

        if int(simulationDoorsEntry.get()) < 3 or int(simulationDoorsEntry.get()) > 1000:
            warning = tk.Label(inputFrame, text="your number should be in range 3-1000", fg='#f00')
            warning.pack()
            return

        door_amount = int(simulationDoorsEntry.get())
        if not clicked.get() == "Games Amount":
            start_game(True, games=int(clicked.get().replace(",", "")))

        else:
            start_game(True)

    else:

        if not gameDoorsEntry.get().isnumeric():
            warning = tk.Label(inputFrame, text="please enter number in digits", fg='#f00')
            warning.pack()
            return

        if int(gameDoorsEntry.get()) < 3 or int(gameDoorsEntry.get()) > 6:
            warning = tk.Label(inputFrame, text="your number should be in range 3-6", fg='#f00')
            warning.pack()
            return

        if door_amount != 0 and (door_amount != int(gameDoorsEntry.get())):
            reset_score()

        door_amount = int(gameDoorsEntry.get())

        if warning is not None:
            warning.pack_forget()

        start_game()


def start_game(simulation=False, games=10000) -> None:
    """
    Start the game

    Parameters
    ----------
    simulation (optional): toggle for simulation
    games (optional): games amount for simulation
    """
    gameDoorsEntry.pack_forget()
    gameDoorsLbl.pack_forget()
    gameConfirmBtn.pack_forget()

    for x in inputFrame.winfo_children():
        x.pack_forget()

    for x in simulationFrame.winfo_children():
        x.pack_forget()

    inputFrame.pack_forget()
    simulationFrame.pack_forget()

    if not simulation:
        show_doors()

    else:
        res = mh_helper(games, door_amount)
        show_graph(res)


def show_graph(res):
    """
    Show graph for simulation.
    """
    inputFrame.pack_forget()
    doorFrame.pack_forget()
    gameTextFrame.pack_forget()

    graphFrame.pack()

    tk.Label(graphFrame, text=f"number of partitions: {res[0]}").pack()
    tk.Label(graphFrame, text=f"number of games: {res[1]}").pack()
    tk.Label(graphFrame, text=f"number of wins because of choice change: {res[2]}").pack()
    tk.Label(graphFrame, text=f"number of losses because of choice change: {res[3]}").pack()
    tk.Label(graphFrame, text=f"number of choice change without influence: {res[4]}").pack()

    fig = Figure(figsize=(8, 4))
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

    calc = int(res[2]) / int(res[3])
    tk.Label(graphFrame, text=f"(Wins / Losses) according to this simulation = {round(calc, 3)}").pack(padx=5, pady=5)
    tk.Label(graphFrame, text="General case: ").pack(padx=5, pady=5)

    score['wins because of change'] = score['wins because of change'] + int(res[2])
    score['losses due to change'] = score['losses due to change'] + int(res[3])
    score['losses without influence'] = score['losses without influence'] + int(res[4])

    refresh_score()

    resFrame = tk.Frame(graphFrame)
    resFrame.pack(side=tk.BOTTOM)

    img = Image.open("assets/equation.png")
    img = img.resize((75, 50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    eq = tk.Label(resFrame, image=img)
    eq.image = img
    eq.pack(padx=5, pady=5, side=tk.LEFT, expand=1)

    lbl4 = tk.Label(resFrame,
                    text=f" = {round(((door_amount - 1) / (door_amount - 2)), 3)}")
    lbl4.pack(padx=5, pady=5, side=tk.LEFT, expand=1)


def show_doors():
    """
    Display the doors on screen for manual play
    """
    door_closed_image = ImageTk.PhotoImage(Image.open("assets/door_closed.png"))

    for i in range(door_amount):
        door = tk.Button(doorFrame,
                         text=str(i + 1),
                         image=door_closed_image,
                         font='Helvetica 15 bold',
                         compound=tk.LEFT,
                         command=lambda x=i: door_pick(x))
        door.image = door_closed_image
        door.pack(side=tk.LEFT, expand=1)
        door_list[door] = "goat"

    for i in range(door_amount):
        img = ImageTk.PhotoImage(Image.open("assets/blank.png"))
        lbl = tk.Label(doorTitlesFrame, image=img)
        lbl.image = img
        lbl.pack(side=tk.LEFT, padx=5, expand=1)

    key, val = random.choice(list(door_list.items()))
    door_list[key] = 'car'


def door_pick(door):
    """
    Main game loop. Whenever the player chooses a door, this is being ran.

    Parameters
    ----------
    door: the door number that the player picked.
    """
    global game_stage, game_count, previous_door_pick, host_revealed
    pick = list(door_list.keys())[door]

    if pick == host_revealed:
        return

    change_pick_picutre(doorTitlesFrame.winfo_children()[door], 'player')

    if game_stage == 0:
        gameTextFrame.pack()
        tk.Label(gameTextFrame,
                 text="The presenter has revealed one of the goats for you, would you like to change your pick?") \
            .pack(pady=20)
        previous_door_pick = door

        while True:
            key, val = random.choice(list(door_list.items()))
            if key != pick and val != 'car':
                break

        host_revealed = key
        change_door_picture(key)
        game_stage = 1
        change_pick_picutre(doorTitlesFrame.winfo_children()[list(door_list.keys()).index(key)], 'host')

    elif game_stage == 1:
        for x in gameTextFrame.winfo_children():
            x.pack_forget()

        change_door_picture(pick)
        car = None
        if door_list.get(pick) == 'goat':
            for key, value in door_list.items():
                if value == 'car':
                    change_door_picture(key)
                    car = key

            tk.Label(gameTextFrame, text="You were wrong!").pack(pady=5)
            game_count += 1

        else:
            car = pick
            tk.Label(gameTextFrame, text="You were right!").pack(pady=5)
            game_count += 1

        if previous_door_pick != door:
            change_pick_picutre(doorTitlesFrame.winfo_children()[previous_door_pick], 'original')

        if previous_door_pick != door:
            if car == pick:
                tk.Label(gameTextFrame, text="You won because of your choice change!").pack(pady=5)
                score['wins because of change'] += 1

            elif previous_door_pick == list(door_list.keys()).index(car):
                tk.Label(gameTextFrame, text="You lost because of your choice change...").pack(pady=5)
                score['losses due to change'] += 1

            else:
                tk.Label(gameTextFrame, text="Your choice change had no influence...").pack(pady=5)
                score['losses without influence'] += 1

        else:
            if car == pick:
                tk.Label(gameTextFrame, text="You won because you didn't change your choice!").pack(pady=5)
                score['wins without change'] += 1

            else:
                tk.Label(gameTextFrame, text="You lost without changing your choice...").pack(pady=5)
                score['losses without influence'] += 1

        againButton = tk.Button(gameTextFrame, text="Try again", command=lambda: restart(True))
        againButton.pack(pady=5)
        game_stage = 3

    elif game_stage == 3:
        return


def change_door_picture(labelname):
    """
    Reveal what's behind a specific door

    Parameters
    ----------
    labelname: the door object
    """
    if door_list.get(labelname) == 'goat':
        photo1 = ImageTk.PhotoImage(Image.open("assets/door_goat.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1

    else:
        photo1 = ImageTk.PhotoImage(Image.open("assets/door_car.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1


def change_pick_picutre(lbl, string):
    """
    Display on screen the pick (whether it's a host pick or player pick)

    Parameters
    ----------
    lbl: the image object
    string: host / player
    """
    if string == 'host':
        photo1 = ImageTk.PhotoImage(Image.open("assets/host_pick.png"))
        lbl.configure(image=photo1)
        lbl.image = photo1

    elif string == 'player':
        photo1 = ImageTk.PhotoImage(Image.open("assets/your_pick.png"))
        lbl.configure(image=photo1)
        lbl.image = photo1

    elif string == 'original':
        photo1 = ImageTk.PhotoImage(Image.open("assets/your_original_pick.png"))
        lbl.configure(image=photo1)
        lbl.image = photo1


def start(skip_check=False):
    """
    Main start function for the program

    Parameters
    ----------
    skip_check (optional): If the player pressed the "try again" button
    """
    refresh_score()
    inputFrame.pack()
    simulationFrame.pack()
    doorFrame.pack()
    doorTitlesFrame.pack()

    gameTitle.pack(pady=(10, 5))  # Game Title
    gameDoorsLbl.pack(pady=5)
    gameDoorsEntry.pack(pady=5)
    gameConfirmBtn.pack()

    simulationTitle.pack(pady=(120, 10))  # Simulation Title
    simulationDoorsLbl.pack(pady=5)
    simulationDoorsEntry.pack(pady=5)
    simulationGamesAmount.pack(pady=5)
    simulationConfirmBtn.pack(pady=5)

    if skip_check:
        simulationFrame.pack_forget()
        start_game()


def restart(skip_check=False):
    """
    Restart game

    Parameters
    ----------
    skip_check (optional): for the "try again" option
    """
    global game_stage, door_list, door_amount
    door_list = {}
    game_stage = 0

    for i in mainFrame.winfo_children():
        for j in i.winfo_children():
            for h in j.winfo_children():
                h.pack_forget()
            j.pack_forget()
        i.pack_forget()

    for i in doorTitlesFrame.winfo_children():
        i.destroy()

    start(skip_check)


def refresh_score():
    """
    Display the updated score on screen
    """
    if sum(list(score.values())) == 0:
        statsLbl['text'] = f"No games played yet."

    else:
        text = ""
        for key, value in score.items():
            text += f"{key}: {value}, "

        statsLbl['text'] = f"{text[0:-2]}"


def reset_score():
    """
    Reset score back to 0.
    """
    global score, door_amount
    score = {'wins because of change': 0,
             'wins without change': 0,
             'losses due to change': 0,
             'losses without influence': 0,
             'losses without change': 0}
    door_amount = 0
    refresh_score()
    restart()


def show_statistics():
    """
    Show stats on screen
    """
    f = Figure(figsize=(12, 4))
    ax = f.add_subplot(111)

    data = (score['wins because of change'],
            score['wins without change'],
            score['losses due to change'],
            score['losses without change'],
            score['losses without influence'])

    ind = ('wins because of change', 'wins without change', 'losses due to change', 'losses without change',
           'losses without influence')
    width = 0.5

    ax.bar(ind, data, width)
    ax.set_ylabel('Games Played')

    tk.Label(secondaryFrame, text="Statistics", font=('Arial', 24)).pack(pady=10)

    canvas = FigureCanvasTkAgg(f, master=secondaryFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=10, fill=tk.BOTH)

    tk.Label(secondaryFrame,
             text=f"n = {door_amount}").pack(pady=5, padx=5)


def switch_main_to_secondary():
    """
    Switch to stats screen
    """
    if mainFrame.winfo_ismapped():
        mainFrame.pack_forget()
        secondaryFrame.pack()
        btnStats["text"] = "Show Game"
        show_statistics()

    else:
        secondaryFrame.pack_forget()
        mainFrame.pack()

        for x in secondaryFrame.winfo_children():
            x.pack_forget()

        btnStats["text"] = "Show Statistics"


window = tk.Tk()
window.attributes("-topmost", True)
doorNumberEntry = tk.Entry(window)

mainFrame = tk.Frame()
mainFrame.pack()

secondaryFrame = tk.Frame()

doorFrame = tk.Frame(mainFrame)
doorTitlesFrame = tk.Frame(doorFrame)
graphFrame = tk.Frame(mainFrame)
gameTextFrame = tk.Frame(mainFrame)

inputFrame = tk.Frame(mainFrame)
gameTitle = tk.Label(inputFrame, text="Game", font=('Arial', 20))
gameDoorsLbl = tk.Label(inputFrame, text="Please enter number of doors here (3 to 6)")
gameDoorsEntry = tk.Entry(inputFrame)
gameConfirmBtn = tk.Button(inputFrame, text="Confirm", command=check_input)

simulationFrame = tk.Frame(mainFrame)
simulationTitle = tk.Label(simulationFrame, text="Simulation", font=('Arial', 20))
simulationDoorsLbl = tk.Label(simulationFrame, text="Please enter number of doors here (3 to 1000)")
simulationDoorsEntry = tk.Entry(simulationFrame)
simulationConfirmBtn = tk.Button(simulationFrame, text="Confirm", command=lambda: check_input(True))
clicked = tk.StringVar()
clicked.set("Games Amount")
simulationGamesAmount = tk.OptionMenu(simulationFrame, clicked, *["100", "1,000", "10,000", "100,000"])

bottomFrame = tk.Frame()
bottomFrame.pack(side=tk.BOTTOM)

btnRestart = tk.Button(bottomFrame, text="Restart Game", command=restart)
btnRestart.pack(side=tk.LEFT, padx=5, pady=10, expand=1)
resetScore = tk.Button(bottomFrame, text="Reset Score", command=reset_score)
resetScore.pack(side=tk.LEFT, padx=5, pady=10, expand=1)
btnStats = tk.Button(bottomFrame, text="Show Statistics", command=switch_main_to_secondary)
btnStats.pack(side=tk.LEFT, padx=5, pady=10, expand=1)

statsLbl = tk.Label(font=('Arial', 15))
statsLbl.pack(side=tk.BOTTOM, pady=10)


def main():
    """
    Main program loop
    """
    start()

    window.geometry("1100x750")
    window.mainloop()
