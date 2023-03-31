"""
Class for League Wrapped ui
"""

from io import BytesIO
import math
from tkinter import Tk, Canvas, Entry, StringVar, OptionMenu, Button, NW
from riotwatcher import LolWatcher
from PIL import Image, ImageTk
import requests
from modules.scraper import get_data_from_matchlist, get_season_matchlist
from modules.analysis import most_deaths, worst_kda, least_cs, worst_vs, worst_winrate

# Colors

PINK = "#f774c4"
LIGHT_GREEN = "#12d861"
ORANGE = "#ff8b1e"
YELLOW = "#f1ff47"
BLACK = "#000000"
SCALE = 0.7
WIDTH = 720 * SCALE
HEIGHT = 1280 * SCALE


class LeagueWrappedUI:
    """
    A class to visualize a player's worst statistics.

    ...

    Attributes
    ----------
    player_data : DataFrame
        player's statistics scraped using Riot API
    user : str
        player's username
    matchlist : list
        list of match ids
    region_code : str
        Riot's code for the player's region
    key : str
        API key
    canvas : Canvas
        background that the ui goes on
    images : dict
        dictionary of PhotoImages containing all the images necessary for the ui

    Methods
    -------
    make_images():
        Creates all PhotoImage objects that are not champion squares and
        puts them in the images dictionary.
    make_champ_images():
        Creates all champion square PhotoImage objects and
        puts them in the images dictionary.
    go_loading_screen():
        Shows loading screen, includes input username and region
        code from initial screen.
    load_player_data():
        Creates watcher object, list of match ids, and dataframe of player data.
        Puts list of match ids in matchlist attribute and dataframe of
        player data in player_data attribute.
    show_death_wrap():
        Visualizes the champion the player has died the most on and the number of deaths.
    show_kda_wrap():
        Visualizes the bottom five champions the player has the worst kda
        with and the five worst kdas.
    show_farm_wrap():
        Visualizes the champion the player has the worst farm on and amount of farm per minute.
    show_winrate_wrap():
        Visualizes the five champions the player has the worst winrate with
        and the five worst winrates.
    show_vision_wrap():
        Visualizes the champion the player has gotten the worst vision with in one game
        and the vision score from that game.
    """

    def __init__(self):
        # Create scale and attributes related to API use
        self.player_data = None
        self.user = None
        self.matchlist = None
        self.region_code = None
        self.key = None

        # Create window
        window = Tk()
        window.title("League Wrapped")

        # Create canvas
        self.canvas = Canvas(width=WIDTH, height=HEIGHT, bg=BLACK)
        self.canvas.grid(row=0, column=0)

        # Save images
        self.images = {}
        self.make_champ_images()
        self.make_images()

        # Create season 12 splash
        self.canvas.create_image(WIDTH / 2, HEIGHT / 3, image=self.images["splash"])

        # Title
        self.canvas.create_text(
            WIDTH / 2,
            100,
            width=WIDTH * 0.75,
            text="Welcome to League Wrapped!",
            fill=YELLOW,
            font=("Arial", 28, "bold"),
            justify="center",
        )

        # Username text
        self.canvas.create_text(
            WIDTH / 2,
            500,
            width=WIDTH * 0.75,
            text="Enter username below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Username entry
        user_entry = Entry(master=self.canvas, font=("Arial", 20))
        self.canvas.create_window(WIDTH / 2, 550, window=user_entry)

        # API key text
        self.canvas.create_text(
            WIDTH / 2,
            600,
            width=WIDTH * 0.75,
            text="Enter API key below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # API key entry
        key_entry = Entry(master=self.canvas, font=("Arial", 20), show="*")
        self.canvas.create_window(WIDTH / 2, 650, window=key_entry)

        # Region text
        self.canvas.create_text(
            WIDTH / 2,
            700,
            width=WIDTH * 0.75,
            text="Select region below:",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Region Dropdown
        regions = {
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
        dropdown_value = StringVar(window)
        region_dropdown = OptionMenu(self.canvas, dropdown_value, *regions)
        self.canvas.create_window(WIDTH / 2, 750, window=region_dropdown)

        # Confirm Button
        confirm = Button(
            master=self.canvas,
            text="Show Me Stats!",
            command=lambda: self.go_loading_screen(
                user_entry, key_entry, dropdown_value, regions
            ),
        )
        self.canvas.create_window(WIDTH / 2, 800, window=confirm)

        window.mainloop()

    def make_images(self):
        """
        Creates all PhotoImage objects that are not champion squares and
        puts them in the images dictionary.
        """
        # Make backgrounds
        death_bg = Image.open("assets/TEMPLATE_deaths.jpg")
        death_bg = death_bg.resize((int(WIDTH), int(HEIGHT)))
        self.images["death_bg"] = ImageTk.PhotoImage(death_bg)

        kda_bg = Image.open("assets/TEMPLATE_kda.jpg")
        kda_bg = kda_bg.resize((int(WIDTH), int(HEIGHT)))
        self.images["kda_bg"] = ImageTk.PhotoImage(kda_bg)

        farm_bg = Image.open("assets/TEMPLATE_farm.jpg")
        farm_bg = farm_bg.resize((int(WIDTH), int(HEIGHT)))
        self.images["farm_bg"] = ImageTk.PhotoImage(farm_bg)

        vision_bg = Image.open("assets/TEMPLATE_vision.jpg")
        vision_bg = vision_bg.resize((int(WIDTH), int(HEIGHT)))
        self.images["vision_bg"] = ImageTk.PhotoImage(vision_bg)

        winrate_bg = Image.open("assets/TEMPLATE_winrate.jpg")
        winrate_bg = winrate_bg.resize((int(WIDTH), int(HEIGHT)))
        self.images["winrate_bg"] = ImageTk.PhotoImage(winrate_bg)

        # Make poros/loading image
        loading_url = "https://nexus.leagueoflegends.com/wp-content/uploads/2018/11/poros_banner-1_slno1owbdsxulmdvqomp.jpg"
        pull = requests.get(loading_url, timeout=30)
        loading = Image.open(BytesIO(pull.content))
        loading = loading.resize((int(1276 * 0.375), int(718 * 0.375)))
        self.images["poros"] = ImageTk.PhotoImage(loading)

        # Make splash image
        splash_url = "https://cdn1.epicgames.com/offer/24b9b5e323bc40eea252a10cdd3b2f10/LOL_2560x1440-98749e0d718e82d27a084941939bc9d3"
        pull = requests.get(splash_url, timeout=30)
        splash = Image.open(BytesIO(pull.content))
        splash = splash.resize((int(1276 * 0.375), int(718 * 0.375)))
        splash_img = ImageTk.PhotoImage(splash)
        self.images["splash"] = splash_img

    def make_champ_images(self):
        """
        Creates all champion square PhotoImage objects and
        puts them in the images dictionary.
        """
        # Make champ images
        champ_request = requests.get(
            "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json",
            timeout=30,
        )
        champ_dic = champ_request.json()
        for champ in champ_dic["data"]:
            image_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
            img_request = requests.get(image_url, timeout=30)
            champ_img = Image.open(BytesIO(img_request.content))

            champ_img4 = champ_img.resize((int(405 * SCALE), int(405 * SCALE)))
            self.images[f"{champ}4"] = ImageTk.PhotoImage(champ_img4)

            champ_img3 = champ_img.resize((int(400 * SCALE), int(400 * SCALE)))
            self.images[f"{champ}3"] = ImageTk.PhotoImage(champ_img3)

            champ_img2 = champ_img.resize((int(200 * SCALE), int(200 * SCALE)))
            self.images[f"{champ}2"] = ImageTk.PhotoImage(champ_img2)

            champ_img1 = champ_img.resize((int(167 * SCALE), int(167 * SCALE)))
            self.images[f"{champ}1"] = ImageTk.PhotoImage(champ_img1)

    def go_loading_screen(self, user_entry, key_entry, dropdown_value, regions):
        """
        Shows loading screen, includes input username and region
        code from initial screen.
        """
        # Clear ui
        self.canvas.delete("all")

        # Retrieve inputs
        self.user = user_entry.get()
        self.key = key_entry.get()
        region = dropdown_value.get()
        self.region_code = regions[region]

        # Load data
        watcher = LolWatcher(api_key=self.key)
        self.matchlist = get_season_matchlist(
            watcher=watcher, summoner_name=self.user, region=self.region_code
        )

        # Loading text
        self.canvas.create_text(
            WIDTH / 2,
            150,
            width=WIDTH * 0.75,
            text="Please wait while the poros retrieve your worst moments!",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Loading img
        self.canvas.create_image(WIDTH / 2, 375, image=self.images["poros"])

        # Input description
        self.canvas.create_text(
            WIDTH / 2,
            600,
            width=WIDTH * 0.75,
            text=f"You said...\nUsername: {self.user}\nRegion: {self.region_code}",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Estimation text
        eta = 2 * (math.ceil(len(self.matchlist) / 100) - 1)
        self.canvas.create_text(
            WIDTH / 2,
            700,
            width=WIDTH * 0.75,
            text=f"Estimated wait time is {eta} minutes.\nClick below to continue.",
            fill=YELLOW,
            font=("Arial", 18),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas,
            text="Show Me Stats!",
            command=lambda: self.load_player_data(watcher),
        )
        self.canvas.create_window(WIDTH / 2, 800, window=cont)

    def load_player_data(self, watcher):
        """
        Creates watcher object, list of match ids, and dataframe of player data.
        Puts list of match ids in matchlist attribute and dataframe of
        player data in player_data attribute.
        """

        # Get player data
        self.player_data = get_data_from_matchlist(
            watcher, self.user, self.matchlist, self.region_code
        )

        # Clear ui
        self.canvas.delete("all")

        # Show deaths wrap
        self.show_death_wrap()

    def show_death_wrap(self):
        """
        Visualizes the champion the player has died the most on and the number of deaths.
        """
        # Analyze for death
        death_data = most_deaths(self.player_data)

        # Add background
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.images["death_bg"])

        # Add champ images
        champ = death_data[1]
        self.canvas.create_image(
            160 * SCALE,
            360 * SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
        )

        # Add text
        deaths = death_data[0]
        self.canvas.create_text(
            WIDTH / 2,
            700,
            width=WIDTH * 0.7,
            text=f"""In Season 12, your most deaths in one game was {deaths} deaths on {champ}.
             You filthy inter.""",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_kda_wrap
        )
        self.canvas.create_window(WIDTH / 2, 800, window=cont)

    def show_kda_wrap(self):
        """
        Visualizes the bottom five champions the player has the worst kda
        with and the five worst kdas.
        """
        # Clear ui
        self.canvas.delete("all")

        # Analyze for KDAs
        kda_data = worst_kda(self.player_data)

        # Add background
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.images["kda_bg"])

        # Add champ images
        horrible_kdas = []
        for kda in kda_data:
            horrible_kdas.append(kda["champ"])

        self.canvas.create_image(
            57 * SCALE,
            392 * SCALE,
            anchor=NW,
            image=self.images[f"{horrible_kdas[0]}4"],
        )

        y_disp = 360

        for champ in horrible_kdas[1:]:
            self.canvas.create_image(
                521 * SCALE,
                y_disp * SCALE,
                anchor=NW,
                image=self.images[f"{champ}1"],
            )
            y_disp += 187

        # Add text
        ytext = 660
        kda_list = []

        for kda in kda_data:
            kda_list.append(round(kda["kda"], 2))

        kda_texts = {}
        for i, champ in enumerate(horrible_kdas):
            kda_num = self.canvas.create_text(
                WIDTH / 15,
                ytext,
                width=WIDTH * 0.7,
                text=f"{kda_list[i]}",
                fill=BLACK,
                font=("Arial", 14, "bold"),
                anchor="w",
            )
            kda_champ = self.canvas.create_text(
                WIDTH / 4,
                ytext,
                width=WIDTH * 0.7,
                text=f"{champ}",
                fill=BLACK,
                font=("Arial", 14, "bold"),
                anchor="w",
            )
            kda_texts[f"{i}"] = kda_champ
            kda_texts[f"{i}"] = kda_num
            if i == 4:
                self.canvas.itemconfig(kda_num, fill=YELLOW)
                self.canvas.itemconfig(kda_champ, fill=YELLOW)
            ytext += 33

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_farm_wrap
        )
        self.canvas.create_window(WIDTH / 2, 900, window=cont)

    def show_farm_wrap(self):
        """
        Visualizes the champion the player has the worst farm on and amount of farm per minute.
        """
        # Clear ui
        self.canvas.delete("all")

        # Analyze for farm
        farm_data = least_cs(self.player_data)

        # Add background
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.images["farm_bg"])

        # Add champ image
        champ = farm_data[1]
        self.canvas.create_image(
            160 * SCALE,
            360 * SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
        )

        # Add text
        farm = farm_data[0]
        self.canvas.create_text(
            WIDTH / 2,
            700,
            width=WIDTH * 0.7,
            text=f"""In Season 12, your worst cs per minute when not playing support was
            {round(farm, 1)} on {champ}. Maybe you should play support instead.""",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_winrate_wrap
        )
        self.canvas.create_window(WIDTH / 2, 800, window=cont)

    def show_winrate_wrap(self):
        """
        Visualizes the five champions the player has the worst winrate with
        and the five worst winrates.
        """
        # Clear ui
        self.canvas.delete("all")

        # Analyze for winrate
        wr_data = worst_winrate(self.player_data)

        # Add background
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.images["winrate_bg"])

        # Add champ images
        horrible_wr_champs = []
        for wr_dic in wr_data:
            horrible_wr_champs.append(wr_dic["champ"])

        y_disp = 133

        for champ in horrible_wr_champs:
            # pilImage = Image.open(BytesIO(r.content)).resize(
            #     (int(200 * scale), int(200 * scale))
            # )
            self.canvas.create_image(
                199 * SCALE,
                y_disp * SCALE,
                anchor=NW,
                image=self.images[f"{champ}2"],
            )
            y_disp += 210

        # Add winrate text
        y_disp = 175
        winrates = []
        for wr_dic in wr_data:
            winrates.append(round(wr_dic["winrate"] * 100))
        wr_texts = {}
        for i in range(len(horrible_wr_champs)):
            wr_text = self.canvas.create_text(
                WIDTH / 4,
                y_disp,
                width=WIDTH * 0.7,
                text=f"{winrates[i]}%",
                fill=BLACK,
                font=("Arial", 40, "bold"),
                anchor="e",
            )
            y_disp += 157
            wr_texts[f"{i}"] = wr_text

        # Add champ text
        y_disp = 160
        champ_texts = {}
        for i, champ in enumerate(horrible_wr_champs):
            wr_text = self.canvas.create_text(
                3 * WIDTH / 5,
                y_disp,
                width=WIDTH * 0.7,
                text=f"{i}",
                fill=BLACK,
                font=("Arial", 16, "bold"),
                anchor="w",
            )
            y_disp += 157
            champ_texts[f"{i}"] = wr_text

        # Add games played text
        y_disp = 190
        games_played = []
        for wr_dic in wr_data:
            games_played.append(wr_dic["games_played"])
        games_texts = {}
        for i in range(len(horrible_wr_champs)):
            games_text = self.canvas.create_text(
                3 * WIDTH / 5,
                y_disp,
                width=WIDTH * 0.7,
                text=f"{games_played[i]} games played",
                fill=BLACK,
                font=("Arial", 14),
                anchor="w",
            )
            y_disp += 157
            games_texts[f"{i}"] = games_text

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_vision_wrap
        )
        self.canvas.create_window(WIDTH / 2, 900, window=cont)

    def show_vision_wrap(self):
        """
        Visualizes the champion the player has gotten the worst vision with in one game
        and the vision score from that game.
        """
        # Clear ui
        self.canvas.delete("all")

        # Analyze for vision
        vision_data = worst_vs(self.player_data)

        # Add background
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.images["vision_bg"])

        # Add champ image
        champ = vision_data[1]
        self.canvas.create_image(
            160 * SCALE,
            360 * SCALE,
            anchor=NW,
            image=self.images[f"{champ}3"],
        )

        # Add text
        vision_score = vision_data[0]
        self.canvas.create_text(
            WIDTH / 2,
            700,
            width=WIDTH * 0.7,
            text=f"""In Season 12, your worst vision score per minute was {round(vision_score, 2)}
            on {champ}. Lee Sin support cosplay is not cool.""",
            fill=YELLOW,
            font=("Arial", 12),
            justify="center",
        )

        # Continue button
        cont = Button(
            master=self.canvas, text="Show Me Stats!", command=self.show_death_wrap
        )
        self.canvas.create_window(WIDTH / 2, 800, window=cont)
