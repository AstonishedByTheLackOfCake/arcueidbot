from telepot.namedtuple import InlineQueryResultArticle
import tools.regextools
name = "baka"
description = "Simple baka plugin"
helpStr = "Says you are baka"
usage = "/baka"
regex = tools.regextools.basicRegex(["baka"])
regexInline = regex


def handler(bot, msg, fullMsg, type):
    if type == "normal":
        return "You  baka!"
    if type == "inline_query":
        articles = [InlineQueryResultArticle(id='xyz', title='BAKA!', message_text='YOU ARE STILL BAKA')]
        return articles
