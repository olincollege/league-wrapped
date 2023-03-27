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
    description_text = canvas.create_text(
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
        kda["kda"] = round(kda["kda"], 2)
        KDAs.append(kda["kda"])

    kda_texts = {}
    for i in range(len(horrible_kdas)):
        KDA_text = canvas.create_text(
            cwidth / 15,
            ytext,
            width=cwidth * 0.7,
            text=f"{KDAs[i]}    {horrible_kdas[i]}",
            fill=BLACK,
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        ytext += 33
        kda_texts[f"{i}"] = KDA_text
        if i == 4:
            canvas.itemconfig(KDA_text, fill=YELLOW)

    window.mainloop()
