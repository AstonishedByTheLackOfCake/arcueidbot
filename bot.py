import telepot
import arconfig
from pprint import pprint
import time
import sys
import re

bot = telepot.Bot(arconfig.TOKEN)
arconfig.BOTINFO = bot.getMe()
print(bot.getMe())
arconfig.registerPlugins()


def scanRegex(regexes, msgText):
    msgText = msgText.replace("@%s" % bot.getMe()["username"], "")
    for regex in regexes:
        if isinstance(regex, str):
            m = re.match(regex, msgText)
        else:
            m = regex.match(msgText)
        if m:
            print(m.groups())
            return m.groups()
    return None


def handle_msg(msg):
    flavor = telepot.flavor(msg)
    # print(flavor)
    pprint(msg)
    if flavor == "normal":
        content_type, chat_type, chat_id = telepot.glance(msg, flavor)
        if content_type != "text":
            return
        msgText = msg["text"].strip()
        for plugin in arconfig.plugins:
            scan = scanRegex(plugin.regex, msgText)
            if scan is not None:
                ans = plugin.handler(bot, scan, msg, flavor)
                if ans is not None:
                    bot.sendMessage(chat_id, ans, reply_to_message_id=msg["message_id"], parse_mode="Markdown",
                                    disable_web_page_preview=False)
                    # print(content_type, chat_type, chat_id)

    elif flavor == "inline_query":
        query_id, from_id, query_string = telepot.glance(msg, flavor)
        for plugin in arconfig.plugins:
            groups = scanRegex(plugin.regexInline, query_string)
            if groups:
                ans = plugin.handler(bot, groups, msg, flavor)
                if ans is not None:
                    bot.answerInlineQuery(query_id, ans)


bot.notifyOnMessage(handle_msg)
while 1:
    time.sleep(10)
