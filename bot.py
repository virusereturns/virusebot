"""
    COPYRIGHT INFORMATION
    ---------------------

Some code in this file is licensed under the apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/

This bot was created with Carberra's Tutorial:

https://www.youtube.com/watch?v=lrE8YbyOePk&list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO&index=1

Any help and tips are appreciated.

"""

from irc.bot import SingleServerIRCBot
from requests import get
from logger import Logger

import local_settings as settings


class Bot(SingleServerIRCBot):
    def __init__(self):
        self.NAME = settings.NAME
        self.OWNER = settings.OWNER
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = self.NAME.lower()
        self.CLIENT_ID = settings.CLIENT_ID
        self.TOKEN = settings.OAUTH_TOKEN
        self.CHANNEL = f"#{self.OWNER}"
        # This should create a logger object
        self.logfile = Logger()

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {
            "Client-ID": self.CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json",
        }
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__(
            [(self.HOST, self.PORT, f"oauth:{self.TOKEN}")],
            self.USERNAME,
            self.USERNAME,
        )

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        self.send_message("I'm alive.")
        self.logfile.log("The bot is now alive.")

    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        if message.startswith(self.NAME):
            self.send_message("Yes, I'm here.")

        self.logfile.log(f"{user['name']}: {message}")
        print(f"Message from {user['name']}: {message}")

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
    bot = Bot()
    bot.start()