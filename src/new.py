import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import random


class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Monty Hall Gui")
        self.wm_geometry("1500x800")

        # creating a frame and assigning it to container
        container = tk.Frame(self)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, SidePage, CompletionScreen):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)

    def show_frame(self, cont, i=0):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Choose number of doors (3 to 9)")
        entry = tk.Entry(self)
        btn = tk.Button(self, text="Confirm", command=lambda: self.save(entry))
        label.pack(padx=10, pady=10)
        entry.pack(padx=10, pady=10)
        btn.pack(padx=10, pady=10)

        # # We use the switch_window_button in order to call the show_frame() method as a lambda function
        # switch_window_button = tk.Button(
        #     self,
        #     text="Go to the Side Page",
        #     command=lambda: controller.show_frame(SidePage),
        # )
        # switch_window_button.pack(side="bottom", fill=tk.X)

    def save(self, e):
        count = int(e.get())
        self.controller.show_frame(SidePage)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.game_stage = 0
        self.count = 9
        self.door_list = {}
        self.label = tk.Label(self, text="Here are your doors")
        self.label.pack(padx=10, pady=10)
        doorClosedImage = ImageTk.PhotoImage(Image.open("images/door_closed.png"))

        for i in range(self.count):
            door1 = tk.Button(self,
                              image=doorClosedImage,
                              text=str(i),
                              font='Helvetica 15 bold',
                              compound=tk.LEFT,
                              command=lambda x=i: self.door_pick(x))
            door1.image = doorClosedImage
            door1.pack(side='left', expand=1)
            self.door_list[door1] = "goat"

        key, val = random.choice(list(self.door_list.items()))
        self.door_list[key] = 'car'
        print(self.door_list)
        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(CompletionScreen),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

    def door_pick(self, door):
        pick = list(self.door_list.keys())[door]
        key, val = random.choice(list(self.door_list.items()))
        if self.door_list[key] == 'goat':
            self.change_pic(key)
            self.label['text'] = 'The presenter has revealed a goat for you, would you like to change your pick?'




    def change_pic(self, labelname):
        if self.door_list.get(labelname) == 'goat':
            photo1 = ImageTk.PhotoImage(Image.open("images/door_goat.png"))
            labelname.configure(image=photo1)
            labelname.photo = photo1

        else:
            photo1 = ImageTk.PhotoImage(Image.open("images/door_car.png"))
            labelname.configure(image=photo1)
            labelname.photo = photo1


class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()
