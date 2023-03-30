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

        kda_bg = Image.open("assets/TEMPLATE_kda.jpg")
        kda_bg = kda_bg.resize((int(self.cwidth), int(self.cheight)))
        self.images["kda_bg"] = ImageTk.PhotoImage(kda_bg)

        farm_bg = Image.open("assets/TEMPLATE_farm.jpg")
        farm_bg = farm_bg.resize((int(self.cwidth), int(self.cheight)))
        self.images["farm_bg"] = ImageTk.PhotoImage(farm_bg)

        vision_bg = Image.open("assets/TEMPLATE_vision.jpg")
        vision_bg = vision_bg.resize((int(self.cwidth), int(self.cheight)))
        self.images["vision_bg"] = ImageTk.PhotoImage(vision_bg)

        winrate_bg = Image.open("assets/TEMPLATE_winrate.jpg")
        winrate_bg = winrate_bg.resize((int(self.cwidth), int(self.cheight)))
        self.images["winrate_bg"] = ImageTk.PhotoImage(winrate_bg)

        # Make champ images
        champ_request = requests.get(
            "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json"
        )
        champ_dic = champ_request.json()
        for champ in champ_dic["data"]:
            image_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
            img_request = requests.get(image_url)
            champ_img = Image.open(BytesIO(img_request.content))

            champ_img4 = champ_img.resize(
                (int(405 * self.SCALE), int(405 * self.SCALE))
            )
            self.images[f"{champ}4"] = ImageTk.PhotoImage(champ_img4)

            champ_img3 = champ_img.resize(
                (int(400 * self.SCALE), int(400 * self.SCALE))
            )
            self.images[f"{champ}3"] = ImageTk.PhotoImage(champ_img3)

            champ_img2 = champ_img.resize(
                (int(200 * self.SCALE), int(200 * self.SCALE))
            )
            self.images[f"{champ}2"] = ImageTk.PhotoImage(champ_img2)

            champ_img1 = champ_img.resize(
                (int(167 * self.SCALE), int(167 * self.SCALE))
            )
            self.images[f"{champ}1"] = ImageTk.PhotoImage(champ_img1)

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
        self.show_death_wrap()

    def show_death_wrap(self):

        # Analyze for death
        death_data = most_deaths(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["death_bg"]
        )

        # Add champ images
        champ = death_data[1]
        self.canvas.create_image(
            160 * self.SCALE,
            360 * self.SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
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

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_kda_wrap
        )
        self.canvas.create_window(self.cwidth / 2, 800, window=cont)

    def show_kda_wrap(self):

        # Clear ui
        self.canvas.delete("all")

        # Analyze for KDAs
        kda_data = worst_kda(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["kda_bg"]
        )

        # Add champ images
        horrible_kdas = []
        for kda in kda_data:
            horrible_kdas.append(kda["champ"])

        self.canvas.create_image(
            57 * self.SCALE,
            392 * self.SCALE,
            anchor=NW,
            image=self.images[f"{horrible_kdas[0]}4"],
        )

        y = 360

        for champ in horrible_kdas[1:]:
            self.canvas.create_image(
                521 * self.SCALE,
                y * self.SCALE,
                anchor=NW,
                image=self.images[f"{champ}1"],
            )
            y += 187

        # Add text
        ytext = 660
        KDAs = []

        for kda in kda_data:
            KDAs.append(round(kda["kda"], 2))

        kda_texts = {}
        for i in range(len(horrible_kdas)):
            KDA = self.canvas.create_text(
                self.cwidth / 15,
                ytext,
                width=self.cwidth * 0.7,
                text=f"{KDAs[i]}",
                fill=BLACK,
                font=("Arial", 14, "bold"),
                anchor="w",
            )
            KDA_champ = self.canvas.create_text(
                self.cwidth / 4,
                ytext,
                width=self.cwidth * 0.7,
                text=f"{horrible_kdas[i]}",
                fill=BLACK,
                font=("Arial", 14, "bold"),
                anchor="w",
            )
            kda_texts[f"{i}"] = KDA_champ
            kda_texts[f"{i}"] = KDA
            if i == 4:
                self.canvas.itemconfig(KDA, fill=YELLOW)
                self.canvas.itemconfig(KDA_champ, fill=YELLOW)
            ytext += 33

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_farm_wrap
        )
        self.canvas.create_window(self.cwidth / 2, 900, window=cont)

    def show_farm_wrap(self):

        # Clear ui
        self.canvas.delete("all")

        # Analyze for farm
        farm_data = least_cs(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["farm_bg"]
        )

        # Add champ image
        champ = farm_data[1]
        self.canvas.create_image(
            160 * self.SCALE,
            360 * self.SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
        )

        # Add text
        farm = farm_data[0]
        self.canvas.create_text(
            self.cwidth / 2,
            700,
            width=self.cwidth * 0.7,
            text=f"In Season 12, your worst cs per minute when not playing support was {round(farm, 1)} on {champ}. Maybe you should play support instead.",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_winrate_wrap
        )
        self.canvas.create_window(self.cwidth / 2, 800, window=cont)

    def show_winrate_wrap(self):

        # Clear ui
        self.canvas.delete("all")

        # Analyze for winrate
        wr_data = worst_winrate(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["winrate_bg"]
        )

        # Add champ images
        horrible_wr_champs = []
        for wr_dic in wr_data:
            horrible_wr_champs.append(wr_dic["champ"])

        y = 133

        for champ in horrible_wr_champs:
            # pilImage = Image.open(BytesIO(r.content)).resize(
            #     (int(200 * scale), int(200 * scale))
            # )
            self.canvas.create_image(
                199 * self.SCALE,
                y * self.SCALE,
                anchor=NW,
                image=self.images[f"{champ}2"],
            )
            y += 210

        # Add winrate text
        ywrtext = 175
        winrates = []
        for wr_dic in wr_data:
            winrates.append(round(wr_dic["winrate"] * 100))
        wr_texts = {}
        for i in range(len(horrible_wr_champs)):
            wr_text = self.canvas.create_text(
                self.cwidth / 4,
                ywrtext,
                width=self.cwidth * 0.7,
                text=f"{winrates[i]}%",
                fill=BLACK,
                font=("Arial", 40, "bold"),
                anchor="e",
            )
            ywrtext += 157
            wr_texts[f"{i}"] = wr_text

        # Add champ text
        ywrtext = 160
        champ_texts = {}
        for i in range(len(horrible_wr_champs)):
            wr_text = self.canvas.create_text(
                3 * self.cwidth / 5,
                ywrtext,
                width=self.cwidth * 0.7,
                text=f"{horrible_wr_champs[i]}",
                fill=BLACK,
                font=("Arial", 16, "bold"),
                anchor="w",
            )
            ywrtext += 157
            champ_texts[f"{i}"] = wr_text

        # Add games played text
        ywrtext = 190
        games_played = []
        for wr_dic in wr_data:
            games_played.append(wr_dic["games_played"])
        games_texts = {}
        for i in range(len(horrible_wr_champs)):
            games_text = self.canvas.create_text(
                3 * self.cwidth / 5,
                ywrtext,
                width=self.cwidth * 0.7,
                text=f"{games_played[i]} games played",
                fill=BLACK,
                font=("Arial", 14),
                anchor="w",
            )
            ywrtext += 157
            games_texts[f"{i}"] = games_text

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_vision_wrap
        )
        self.canvas.create_window(self.cwidth / 2, 900, window=cont)

    def show_vision_wrap(self):

        # Clear ui
        self.canvas.delete("all")

        # Analyze for vision
        vision_data = worst_vs(self.player_data)

        # Add background
        self.canvas.create_image(
            self.cwidth / 2, self.cheight / 2, image=self.images["vision_bg"]
        )

        # Add champ image
        champ = vision_data[1]
        self.canvas.create_image(
            160 * self.SCALE,
            360 * self.SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
        )

        # Add text
        vs = vision_data[0]
        self.canvas.create_text(
            self.cwidth / 2,
            700,
            width=self.cwidth * 0.7,
            text=f"In Season 12, your worst vision score per minute was {round(vs, 2)} on {champ}. Lee Sin support cosplay is not cool.",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_death_wrap
        )
        self.canvas.create_window(self.cwidth / 2, 800, window=cont)
