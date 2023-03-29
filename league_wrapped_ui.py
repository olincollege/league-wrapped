"""
Class for League Wrapped ui
"""

from tkinter import *
from scraper import *
from analysis import *
from scraper import *
from riotwatcher import LolWatcher
from io import BytesIO
from PIL import Image, ImageTk
import requests
import time
import math

# Colors

PINK = "#f774c4"
LIGHT_GREEN = "#12d861"
ORANGE = "#ff8b1e"
YELLOW = "#f1ff47"
BLACK = "#000000"


class LoL_wrapped_interface:
    def __init__(self):
        self.SCALE = 0.75
        self.player_data = None
        self.watcher = None
        self.user = None
        self.matchlist = None
        self.region_code = None

        # Create window
        self.window = Tk()
        self.window.title("League Wrapped")
        self.cwidth = 720 * self.SCALE
        self.cheight = 1280 * self.SCALE

        # Create canvas
        self.canvas = Canvas(width=self.cwidth, height=self.cheight, bg=BLACK)
        self.canvas.grid(row=0, column=0)

        # Save images
        self.images = {}

        # Make splash image
        splash_url = "https://cdn1.epicgames.com/offer/24b9b5e323bc40eea252a10cdd3b2f10/LOL_2560x1440-98749e0d718e82d27a084941939bc9d3"
        pull = requests.get(splash_url)
        splash = Image.open(BytesIO(pull.content))
        splash = splash.resize((int(1276 * 0.375), int(718 * 0.375)))
        splash_img = ImageTk.PhotoImage(splash)
        self.images["splash"] = splash_img

        # Make poros/loading image
        loading_url = "https://nexus.leagueoflegends.com/wp-content/uploads/2018/11/poros_banner-1_slno1owbdsxulmdvqomp.jpg"
        pull_load = requests.get(loading_url)
        loading = Image.open(BytesIO(pull_load.content))
        loading = loading.resize((int(1276 * 0.375), int(718 * 0.375)))
        self.images["poros"] = ImageTk.PhotoImage(loading)

        # Make backgrounds
        death_bg = Image.open("assets/TEMPLATE_deaths.jpg")
        death_bg = death_bg.resize((int(self.cwidth), int(self.cheight)))
        self.images["death_bg"] = ImageTk.PhotoImage(death_bg)

        # Make champ images
        champ_request = requests.get(
            "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json"
        )
        champ_dic = champ_request.json()
        for champ in champ_dic["data"]:
            image_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
            img_request = requests.get(image_url)
            champ_img = Image.open(BytesIO(img_request.content))
            champ_img = champ_img.resize((int(400 * self.SCALE), int(400 * self.SCALE)))
            self.images[f"{champ}"] = ImageTk.PhotoImage(champ_img)

        # Create season 12 splash
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 3, image=self.images["splash"]
        )

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

        # API key text
        self.canvas.create_text(
            self.cwidth / 2,
            600,
            width=self.cwidth * 0.75,
            text="Enter API key below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # API key entry
        self.key_entry = Entry(master=self.canvas, font=("Arial", 20), show="*")
        self.canvas.create_window(self.cwidth / 2, 650, window=self.key_entry)

        # Region text
        self.canvas.create_text(
            self.cwidth / 2,
            700,
            width=self.cwidth * 0.75,
            text="Select region below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Region Dropdown
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
        self.canvas.create_window(self.cwidth / 2, 750, window=region_dropdown)

        # Confirm Button
        confirm = Button(
            master=self.canvas,
            text="Show Me Stats!",
            command=self.go_loading_screen,
        )
        self.canvas.create_window(self.cwidth / 2, 900, window=confirm)

        self.window.mainloop()

    def go_loading_screen(self):

        # Clear ui
        self.canvas.delete("all")

        # Retrieve inputs
        self.user = self.user_entry.get()
        key = self.key_entry.get()
        region = self.dropdown_value.get()
        self.region_code = self.regions[region]

        # Loading text
        self.canvas.create_text(
            self.cwidth / 2,
            150,
            width=self.cwidth * 0.75,
            text="Please wait while the poros retrieve your worst moments!",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Loading img
        self.canvas.create_image(self.cwidth / 2, 375, image=self.images["poros"])

        # Input description
        self.canvas.create_text(
            self.cwidth / 2,
            600,
            width=self.cwidth * 0.75,
            text=f"You said...\nUsername: {self.user}\nRegion: {region}",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Load data
        self.watcher = LolWatcher(api_key=key)
        self.matchlist = get_season_matchlist(
            watcher=self.watcher, summoner_name=self.user, region=self.region_code
        )

        # Estimation text
        self.canvas.create_text(
            self.cwidth / 2,
            700,
            width=self.cwidth * 0.75,
            text=f"Estimated wait time is {2*(math.ceil(len(self.matchlist)/100)-1)} minutes.\nClick below to continue.",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.load_player_data
        )
        self.canvas.create_window(self.cwidth / 2, 750, window=cont)

    def load_player_data(self):

        # Get player data
        self.player_data = get_data_from_matchlist(
            self.watcher, self.user, self.matchlist, self.region_code
        )

        # Clear ui
        self.canvas.delete("all")

        # Show deaths wrap
        self.show_deaths_wrap()

    def show_deaths_wrap(self):

        # Analyze for death
        death_data = most_deaths(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["death_bg"]
        )

        # Add champ images
        champ = death_data[1]
        self.canvas.create_image(
            160 * self.SCALE, 360 * self.SCALE, anchor=NW, image=self.images[f"{champ}"]
        )

        # Add text
        deaths = death_data[0]
        self.canvas.create_text(
            self.cwidth / 2,
            700,
            width=self.cwidth * 0.7,
            text=f"In Season 12, your most deaths in one game was {deaths} deaths on {champ}. You filthy inter.",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )
