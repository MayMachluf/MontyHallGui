import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import time

num_doors = 0
game_stage = 0


def show_msg():
    n = doorNumberEntry.get()
    if n.isnumeric():
        if int(n) in range(3, 10):
            label.pack_forget()
            doorNumberEntry.pack_forget()
            btn.pack_forget()
            func(int(n))
            return

        tk.messagebox.showerror("error", "your number should be in range 3-9")
        return
    tk.messagebox.showerror("error", "please enter number in digits")


doorList = {}


def func(n: int):
    doorClosedImage = ImageTk.PhotoImage(Image.open("images/door_closed.png"))

    if n == 3 or n == 4:
        for i in range(n):
            print(i)
            door1 = tk.Button(image=doorClosedImage, command=lambda i=i: door_pick(i))
            door1.image = doorClosedImage
            door1.grid(row=2, column=i + 2)
            doorList[door1] = "goat"

    if n == 5 or n == 7 or n == 9:
        k = 0
        j = 0
        for i in range(n):
            door1 = tk.Button(image=doorClosedImage, command=lambda i=i: door_pick(i))
            door1.image = doorClosedImage
            doorList[door1] = "goat"

            if i < (n / 2):
                door1.grid(row=2, column=j)
                j += 2

            else:
                door1.grid(row=3, column=k + 1)
                k += 2

    if n == 6 or n == 8:
        k = 0
        j = 0
        for i in range(n):
            door1 = tk.Button(image=doorClosedImage, command=lambda i=i: door_pick(i))
            door1.image = doorClosedImage
            doorList[door1] = "goat"

            if i < n / 2:
                door1.grid(row=2, column=j)
                j += 2

            else:
                door1.grid(row=3, column=k)
                k += 2

    key, val = random.choice(list(doorList.items()))
    doorList[key] = 'car'


def door_pick(i):
    global game_stage

    if game_stage == 0:
        while True:
            key, val = random.choice(list(doorList.items()))
            if val != 'car' and list(doorList.keys())[i] != key:
                game_stage += 1
                change_pic(key)
                yesBtn = tk.Button(text="Yes")
                noBtn = tk.Button(text="No")
                lbl = tk.Label(text="Would you like to change your choice?")
                yesBtn['command'] = lambda: yes_btn(yesBtn, noBtn, lbl)
                noBtn['command'] = lambda: no_btn(yesBtn, noBtn, lbl, list(doorList.keys())[i])

                x = len(doorList)
                lbl.grid(row=4, column=int(x / 2))
                yesBtn.grid(row=5, columnspan=int(x / 2 - 1))
                noBtn.grid(row=5, columnspan=int(x / 2 + 1))

                return

    if game_stage == 1:
        key = list(doorList.keys())[i]
        change_pic(key)

        if doorList.get(key) == 'goat':
            for key, value in doorList.items():
                if value == 'car':
                    change_pic(key)

        game_stage = 2
        # time.sleep(3)
        # for key in doorList.keys():
        #     key.destroy()
        return

    if game_stage == 2:
        return


def yes_btn(*args):
    global game_stage
    for i in args:
        i.destroy()

    game_stage = 1


def no_btn(btn1, btn2, lbl, door):
    global game_stage
    btn1.destroy()
    btn2.destroy()
    lbl.destroy()

    change_pic(door)

    game_stage = 2


def change_pic(labelname):
    if doorList.get(labelname) == 'goat':
        photo1 = ImageTk.PhotoImage(Image.open("images/door_goat.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1

    else:
        photo1 = ImageTk.PhotoImage(Image.open("images/door_car.png"))
        labelname.configure(image=photo1)
        labelname.photo = photo1


window = tk.Tk()
label = tk.Label(text="Please enter number of doors here")
label.pack()

doorNumberEntry = tk.Entry()
doorNumberEntry.pack()

btn = tk.Button(text="Confirm", command=show_msg)
btn.pack()

window.geometry("1100x700")
window.mainloop()
