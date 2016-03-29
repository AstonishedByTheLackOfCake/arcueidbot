import tools.regextools
import random

name = "slap"
description = "Simple slap plugin"
helpStr = "Slap smbd"
usage = "[!/]slap <anime name>\n" \
        "May be used in reply to smbd"
regex = tools.regextools.basicRegex(["slap"])
regexInline = []

SLAPS = open("data/slaps.txt",encoding="utf-8").readlines()

def handler(bot, msg, fullMsg, flavor):
    initiator = fullMsg["from"]["first_name"]
    if flavor == "normal":
        if "reply_to_message" in fullMsg:
            victim = fullMsg["reply_to_message"]["from"]["first_name"]
        else:
            if not msg[1]:
                return usage
            victim = msg[1]
        slap = random.choice(SLAPS).replace("VICTIM", "*%s*" % victim).replace("INITIATOR", "*%s*" % initiator)
        return slap
