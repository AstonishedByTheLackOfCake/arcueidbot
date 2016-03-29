import arconfig
import tools.regextools

description = "help plugin"
helpStr = "prints help"
name = "help"
regex = tools.regextools.basicRegex(["help"])
regexInline = []


def handler(bot, msg, fullMsg, type):
    if type == "normal":
        if len(msg) == 1:
            ans = "Help for *Arcueid* bot\n"
            ans += "List of plugins:\n\n"
            for plug in arconfig.plugins:
                if plug.description is not None:
                    ans += "*%s* - %s\n" % (plug.name, plug.description)
            return ans
        elif len(msg) == 2:
            plugname = msg[1]
            for plug in arconfig.plugins:
                if plug.name == plugname and plug.helpStr is not None:
                    ans = "Help for *%s*\n" % plug.name
                    ans += plug.helpStr
                    return ans
            return "No help on this topic"
