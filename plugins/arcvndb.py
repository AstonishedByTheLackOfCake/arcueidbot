import tools.regextools
import tools.pyvndb
import arconfig
import sys
import redis
from telepot.namedtuple import InlineQueryResultArticle
import re
name = "arcvndb"
description = "VNDB API plugin"
helpStr = "[!/]vndb <name> to find VN\n"
usage = helpStr
regex = tools.regextools.basicRegex(["vndb"])
regexInline = regex

PLATFORMS = {"win": "Windows", "lin": "Linux", "mac": "Mac OS", "and": "Android", "psp": "PSP", "ps3": "PlayStation 3",
             "psv": "PS Vita",
             "xb3": "XBox 3", "oth": "other", "dvd": "DVD", "ps2": "PlayStation 2"}

DB = redis.StrictRedis()
vndb = tools.pyvndb.VNDBClient(arconfig.VNDB[0], arconfig.VNDB[1])


def makeAns(vn):
    ans = "[pic](%s)" % vn["image"]
    ans += "\n[%s](%s)" % (vn["title"], "https://vndb.org/v%s" % vn["id"])
    ans += "\n*Released*: %s" % vn["released"]
    ans += "\n*Platforms:* %s " % ", ".join(map(lambda x: PLATFORMS[x] if x in PLATFORMS else x, vn["platforms"]))
    ans += "\n*Popularity:* %s" % vn["popularity"]
    ans += "\n*Rating:* %s" % vn["rating"]
    if vn["description"] is not None:
        ans += "\n`%s`" % re.sub("\[.*\]","",vn["description"])
    return ans


def handler(bot, msg, fullMsg, flavor):
    if not msg[1]:
        return usage
    try:
        vns = vndb.searchVN(msg[1])
    except Exception as e:
        print("e", e, file=sys.stderr)
        return "ERROR"

    if flavor == "normal":
        if len(vns) == 0:
            return "Nothing found"
        return makeAns(vns[0])
    elif flavor == "inline_query":
        if len(vns) == 0:
            return
        ans = []
        for i in range(min(5, len(vns))):
            ans.append(InlineQueryResultArticle(title=vns[i]["title"], id=str(i),
                                                parse_mode="Markdown", disable_web_page_preview=False,
                                                message_text=makeAns(vns[i])))
        return ans
