import json
import tools.regextools
import requests
from telepot.namedtuple import InlineQueryResultArticle

name = "animefind"
description = "To search anime on hummingbird"
helpStr = "Search anime by title on Hummingbird \n Example: /animefind Fate Zero"
usage = "[!/]animefind <anime name>"
regex = tools.regextools.basicRegex(["animefind"])
regexInline = regex


def makeRequest(query):
    url = "http://hummingbird.me/api/v1/%s" % query
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return json.loads(resp.text, encoding="utf-8")


def makeAns(anime):
    ans = "\n[pic](%s)" % anime["cover_image"]
    ans += "\n           [%s](%s)" % (anime["title"], anime["url"])
    ans += "\n*Status*: %s" % anime["status"]
    ans += "\n*Airing*: %s - %s" % (anime["started_airing"], anime["finished_airing"])
    ans += "\n*%s* episodes (*%s*)\n" % (anime["episode_count"], anime["show_type"])
    ans += "*Genres*: "
    for i in range(len(anime["genres"])):

        for b in anime["genres"][i].values():
            ans += "%s" % b
            if i != len(anime["genres"]) - 1:
                ans += ', '
    ans += "\n*Age rating*: %s" % anime["age_rating"]
    ans += "\n*User rating*: %s" % anime["community_rating"]
    ans += "\n[MAL link](http://myanimelist.net/anime/%s)" % anime["mal_id"]

    ans += "\n `%s`" % anime["synopsis"]
    return ans


def handler(bot, msg, fullMsg, flavor):
    if not msg[1]:
        if flavor == "normal":
            return usage
        return
    if msg[0] == "animefind":
        results = makeRequest("/search/anime?query=%s" % msg[1])
        if len(results) == 0:
            return "Not found"
        else:
            if flavor == "normal":
                return makeAns(results[0])
            elif flavor == "inline_query":
                articles = []
                for i in range(min(len(results), 3)):
                    articles.append(InlineQueryResultArticle(disable_web_page_preview=False, parse_mode="Markdown",
                                                             id=str(i), title=results[i]["title"],
                                                             message_text=makeAns(results[i])))

                return articles
