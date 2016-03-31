from telepot.namedtuple import InlineQueryResultArticle
import tools.regextools
name = "nigger"
description = "Simple nigger plugin"
helpStr = "Says you are nigger"
usage = "/nigger"
regex = tools.regextools.basicRegex(["nigger"])
regexInline = regex


def handler(bot, msg, fullMsg, type):
    if type == "normal":
        if not msg[1] :
            return "You nigger!"
        else:
            bot.sendMessage(chat_id=fullMsg["chat"]["id"], text = "%s is a nigger" % msg[1])
            return
    if type == "inline_query":
        articles = [InlineQueryResultArticle(id='xyz', title='NIGGER', message_text='YOU ARE STILL A NIGGER')]
        return articles
