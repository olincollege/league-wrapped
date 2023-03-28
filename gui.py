"""
Functions for setting up GUI for League Wrapped
"""
import tkinter as t
from io import BytesIO
from PIL import Image, ImageTk
import requests


def make_deaths_wrap(death_data):
    # Colors
    YELLOW = "#f1ff47"

    # Set window
    window = t.Tk()
    window.title("League Wrapped Worst Deaths Example")

    # Make canvas
    scale = 0.75
    cwidth = 720 * scale
    cheight = 1280 * scale
    canvas = t.Canvas(width=cwidth, height=cheight, bg="white")
    canvas.grid(row=0, column=0)

    # Add background
    pilImage = Image.open("assets/TEMPLATE_deaths.jpg")
    pilImage = pilImage.resize((int(cwidth), int(cheight)))
    bgimg = ImageTk.PhotoImage(pilImage)
    canvas.create_image(cwidth / 2, cheight / 2, image=bgimg)

    # Create champ images
    champ = death_data[1]
    image_url = (
        f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
    )
    r = requests.get(image_url)
    pilImage = Image.open(BytesIO(r.content))
    pilImage = pilImage.resize((int(400 * scale), int(400 * scale)))
    img = ImageTk.PhotoImage(pilImage)

    # Add champ images
    canvas.create_image(160 * scale, 360 * scale, anchor=t.NW, image=img)

    # Add text
    deaths = death_data[0]
    canvas.create_text(
        cwidth / 2,
        700,
        width=cwidth * 0.7,
        text=f"In Season 12, your most deaths in one game was {deaths} deaths on {champ}. You filthy inter.",
        fill=YELLOW,
        font=("Arial", 12),
        justify="center",
    )

    window.mainloop()


def make_kda_wrap(kda_data):
    # Colors
    YELLOW = "#f1ff47"
    BLACK = "#000000"

    # Set window
    window = t.Tk()
    window.title("League Wrapped Worst KDAs Example")

    # Make canvas
    scale = 0.75
    cwidth = 720 * scale
    cheight = 1280 * scale
    canvas = t.Canvas(width=cwidth, height=cheight, bg="white")
    canvas.grid(row=0, column=0)

    # Add background
    pilImage = Image.open("assets/TEMPLATE_kda.jpg")
    pilImage = pilImage.resize((int(cwidth), int(cheight)))
    bgimg = ImageTk.PhotoImage(pilImage)
    canvas.create_image(cwidth / 2, cheight / 2, image=bgimg)

    # Add champ images
    horrible_kdas = []
    for kda in kda_data:
        horrible_kdas.append(kda["champ"])

    image_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{horrible_kdas[0]}.png"
    r = requests.get(image_url)
    pilImage = Image.open(BytesIO(r.content))
    pilImage = pilImage.resize((int(405 * scale), int(408 * scale)))
    worst_kda_image = ImageTk.PhotoImage(pilImage)

    canvas.create_image(57 * scale, 392 * scale, anchor=t.NW, image=worst_kda_image)

    y = 360
    hkda_images = {}

    for champ in horrible_kdas[1:]:
        image_url = (
            f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
        )
        r = requests.get(image_url)
        pilImage = Image.open(BytesIO(r.content))
        pilImage = Image.open(BytesIO(r.content)).resize(
            (int(167 * scale), int(167 * scale))
        )
        horrible_kda_image = ImageTk.PhotoImage(pilImage)
        hkda_images[f"{champ}"] = horrible_kda_image
        canvas.create_image(
            521 * scale, y * scale, anchor=t.NW, image=horrible_kda_image
        )
        y += 187

    # Add text
    ytext = 660
    KDAs = []

    for kda in kda_data:
        # if len(str(kda["kda"])) > 4:
        KDAs.append(round(kda["kda"], 2))
        # else:
        #     current_kda = str(kda["kda"]) + "0"
        #     KDAs.append(round(float(current_kda) * 100) / 100)

    kda_texts = {}
    for i in range(len(horrible_kdas)):
        KDA = canvas.create_text(
            cwidth / 15,
            ytext,
            width=cwidth * 0.7,
            text=f"{KDAs[i]}",
            fill=BLACK,
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        KDA_champ = canvas.create_text(
            cwidth / 4,
            ytext,
            width=cwidth * 0.7,
            text=f"{horrible_kdas[i]}",
            fill=BLACK,
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        kda_texts[f"{i}"] = KDA_champ
        kda_texts[f"{i}"] = KDA
        if i == 4:
            canvas.itemconfig(KDA, fill=YELLOW)
            canvas.itemconfig(KDA_champ, fill=YELLOW)
        ytext += 33

    window.mainloop()


def make_wr_wrap(wr_data):
    # Colors
    BLACK = "#000000"

    # Set window
    window = t.Tk()
    window.title("League Wrapped Worst Winrates Example")

    # Make canvas
    scale = 0.75
    cwidth = 720 * scale
    cheight = 1280 * scale
    canvas = t.Canvas(width=cwidth, height=cheight)
    canvas.grid(row=0, column=0)

    # Add background
    pilImage = Image.open("assets/TEMPLATE_winrate.jpg")
    pilImage = pilImage.resize((int(cwidth), int(cheight)))
    bgimg = ImageTk.PhotoImage(pilImage)
    canvas.create_image(cwidth / 2, cheight / 2, image=bgimg)

    # Add champ images
    horrible_wr_champs = []
    for wr_dic in wr_data:
        horrible_wr_champs.append(wr_dic["champ"])

    y = 133
    hwr_images = {}

    for champ in horrible_wr_champs:
        image_url = (
            f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
        )
        r = requests.get(image_url)
        pilImage = Image.open(BytesIO(r.content))
        pilImage = Image.open(BytesIO(r.content)).resize(
            (int(200 * scale), int(200 * scale))
        )
        horrible_wr_image = ImageTk.PhotoImage(pilImage)
        hwr_images[f"{champ}"] = horrible_wr_image
        canvas.create_image(
            199 * scale, y * scale, anchor=t.NW, image=horrible_wr_image
        )
        y += 210

    # Add winrate text
    ywrtext = 175
    winrates = []
    for wr_dic in wr_data:
        winrates.append(round(wr_dic["winrate"] * 100))
    wr_texts = {}
    for i in range(len(horrible_wr_champs)):
        wr_text = canvas.create_text(
            cwidth / 4,
            ywrtext,
            width=cwidth * 0.7,
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
        wr_text = canvas.create_text(
            3 * cwidth / 5,
            ywrtext,
            width=cwidth * 0.7,
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
        games_text = canvas.create_text(
            3 * cwidth / 5,
            ywrtext,
            width=cwidth * 0.7,
            text=f"{games_played[i]} games played",
            fill=BLACK,
            font=("Arial", 14),
            anchor="w",
        )
        ywrtext += 157
        games_texts[f"{i}"] = games_text

    window.mainloop()


def make_farm_wrap(farm_data):
    # Colors
    YELLOW = "#f1ff47"

    # Set window
    window = t.Tk()
    window.title("League Wrapped Worst Deaths Example")

    # Make canvas
    scale = 0.75
    cwidth = 720 * scale
    cheight = 1280 * scale
    canvas = t.Canvas(width=cwidth, height=cheight, bg="white")
    canvas.grid(row=0, column=0)

    # Add background
    pilImage = Image.open("assets/TEMPLATE_farm.jpg")
    pilImage = pilImage.resize((int(cwidth), int(cheight)))
    bgimg = ImageTk.PhotoImage(pilImage)
    canvas.create_image(cwidth / 2, cheight / 2, image=bgimg)

    # Create champ images
    champ = farm_data[1]
    image_url = (
        f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{champ}.png"
    )
    r = requests.get(image_url)
    pilImage = Image.open(BytesIO(r.content))
    pilImage = pilImage.resize((int(400 * scale), int(400 * scale)))
    img = ImageTk.PhotoImage(pilImage)

    # Add champ images
    canvas.create_image(160 * scale, 360 * scale, anchor=t.NW, image=img)

    # Add text
    cs = farm_data[0]
    canvas.create_text(
        cwidth / 2,
        700,
        width=cwidth * 0.625,
        text=f"In Season 12, your worst cs per minute when not playing support was {round(cs, 1)} on {champ}. Maybe you should play support instead.",
        fill=YELLOW,
        font=("Arial", 12),
        justify="center",
    )

    window.mainloop()
