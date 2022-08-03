import pyautogui as pg
import pyperclip
import os
from time import sleep
import requests as req

api_key = os.environ.get('weather_api_key')
base_url = "http://api.openweathermap.org/data/2.5/weather?"

sleep(3)
pos_smiley = pg.locateOnScreen("bot/smiley_attachment.png", confidence=0.6)
x = pos_smiley[0]
y = pos_smiley[1]


def receive_message():
    global x, y

    pos = pg.locateOnScreen("bot/smiley_attachment.png", confidence=0.6)
    x = pos[0]
    y = pos[1]
    pg.moveTo(x, y, duration=0.01)  # duration is mandatory for macOS as it has some defense mechanism
    #  (0,0) is top left
    pg.moveRel(120, -50, duration=0.01)
    pg.tripleClick()  # to select all text
    pg.keyDown("ctrl")
    pg.press("c")
    pg.keyUp("ctrl")
    msg = pyperclip.paste()
    sleep(0.1)
    pg.click()
    print("The message received is:" + msg)
    send_message(msg)


def send_message(msg):
    global x, y

    pos = pg.locateOnScreen("bot/smiley_attachment.png", confidence=0.6)
    x = pos[0]
    y = pos[1]
    pg.moveTo(x + 140, y + 20, duration=0.01)
    pg.click()
    pyperclip.copy(generate_response(msg))
    pg.keyDown("ctrl")
    pg.press("v")
    pg.keyUp("ctrl")
    # pg.typewrite(generate_response(msg), interval=0.01)
    pg.press("enter")


def generate_response(msg):
    if str(msg.lower()) == "help":
        resp = "Enter the city name to get the weather update."
        return resp
    else:
        complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + msg
        response = req.get(complete_url)
        res = response.json()
        if res["cod"] != "404":
            mn = res["main"]
            temperature = round(mn["temp"] - 273.15)
            feels_like = round(mn["feels_like"] - 273.15)
            desc = res["weather"][0]["description"]
            ret = "The temperature is " + str(temperature) + " °C\n" + "Feels like " + str(
                feels_like) + " °C\n" + "Description: " + str(desc.capitalize())
            return ret
        return "City not found."


def check_for_unread():
    pg.moveTo(x + 125, y - 30)
    while True:
        try:
            pos = pg.locateOnScreen("bot/unread.png", confidence=0.7)
            if pos is not None:
                pg.moveTo(pos[0] - 70, pos[1])
                pg.click()
            else:
                pos = pg.locateOnScreen("bot/1msg.png", confidence=0.7)
                if pos is not None:
                    pg.moveTo(pos[0] - 70, pos[1])
                    pg.click()
                else:
                    pos = pg.locateOnScreen("bot/2msg.png", confidence=0.7)
                    if pos is not None:
                        pg.moveTo(pos[0] - 70, pos[1])
                        pg.click()
                    else:
                        pos = pg.locateOnScreen("bot/3msg.png", confidence=0.7)
                        if pos is not None:
                            pg.moveTo(pos[0] - 70, pos[1])
                            pg.click()
                        else:
                            pos = pg.locateOnScreen("bot/4msg.png", confidence=0.7)
                            if pos is not None:
                                pg.moveTo(pos[0] - 70, pos[1])
                                pg.click()
                            else:
                                pos = pg.locateOnScreen("bot/5msg.png", confidence=0.7)
                                if pos is not None:
                                    pg.moveTo(pos[0] - 70, pos[1])
                                    pg.click()
        except Exception:
            print("No unread messages")

        if pg.pixelMatchesColor(int(x + 125), int(y - 30), (52, 63, 70), tolerance=20):
            print("New message found")
            receive_message()
        else:
            print("No new messages")
        sleep(3)


check_for_unread()
