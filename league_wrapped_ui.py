"""
Class for League Wrapped ui
"""

from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
import requests

# Colors

PINK = "#f774c4"
LIGHT_GREEN = "#12d861"
ORANGE = "#ff8b1e"
YELLOW = "#f1ff47"
BLACK = "#000000"


class LoL_wrapped_interface:
    def __init__(self):
        SCALE = 0.75

        # Create window
        self.window = Tk()
        self.window.title("League Wrapped")
        self.cwidth = 720 * SCALE
        self.cheight = 1280 * SCALE

        # Create canvas
        self.canvas = Canvas(width=self.cwidth, height=self.cheight, bg=BLACK)
        self.canvas.grid(row=0, column=0)

        # Season 12 splash
        splash_url = "https://cdn1.epicgames.com/offer/24b9b5e323bc40eea252a10cdd3b2f10/LOL_2560x1440-98749e0d718e82d27a084941939bc9d3"
        pull = requests.get(splash_url)
        splash = Image.open(BytesIO(pull.content))
        splash = splash.resize((int(1276 * 0.375), int(718 * 0.375)))
        splash_img = ImageTk.PhotoImage(splash)
        self.canvas.create_image(self.cwidth / 2, self.cheight / 3, image=splash_img)

        # Title
        self.canvas.create_text(
            self.cwidth / 2,
            100,
            width=self.cwidth * 0.75,
            text="Welcome to League Wrapped!",
            fill=YELLOW,
            font=("Arial", 28, "bold"),
            justify="center",
        )

        # Username text
        self.canvas.create_text(
            self.cwidth / 2,
            500,
            width=self.cwidth * 0.75,
            text="Enter username below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Username entry
        self.user_entry = Entry(master=self.canvas, font=("Arial", 20))
        self.canvas.create_window(self.cwidth / 2, 550, window=self.user_entry)

        # Region text
        self.canvas.create_text(
            self.cwidth / 2,
            650,
            width=self.cwidth * 0.75,
            text="Select region below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Username entry
        self.regions = {
            "Brazil": "BR1",
            "Europe East": "EUN1",
            "Europe West": "EUW1",
            "Japan": "JP1",
            "Korea": "KR",
            "Latin America North": "LA1",
            "Latin America South": "LA2",
            "North America": "NA1",
            "Oceania": "OC1",
            "Turkey": "TR1",
            "Russia": "RU",
        }
        self.dropdown_value = StringVar(self.window)
        region_dropdown = OptionMenu(self.canvas, self.dropdown_value, *self.regions)
        self.canvas.create_window(self.cwidth / 2, 700, window=region_dropdown)

        # Confirm Button
        confirm = Button(
            master=self.canvas,
            text="Show Me Stats!",
            command=self.test,
        )
        self.canvas.create_window(self.cwidth / 2, 900, window=confirm)

        self.window.mainloop()

    def test(self):
        user = self.user_entry.get()
        region = self.dropdown_value.get()
        self.canvas.create_text(
            self.cwidth / 2,
            800,
            width=self.cwidth * 0.75,
            text=f"user: {user}, region code: {self.regions[region]}",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )
        # self.canvas.delete("all")
