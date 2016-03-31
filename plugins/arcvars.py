import tools.regextools
import random
import redis
DB = redis.StrictRedis()

name = "arcvars"
description = "Getter/Setter plugin"
helpStr = ""
usage = "[!/]getv <variable to get>\n" \
        "[!/]setv <variable to set>\n"
regex = tools.regextools.basicRegex(["getv","setv"])
regexInline = []

def handler(bot,msg,fullMsg, flavor):
    if not msg[1]:
        return usage
    if fullMsg["chat"]["type"] == "private":
        return "Can't be used in private"
    DBKeyPrefix = "arcueid:uservars:%s" % fullMsg["chat"]["id"]

    if msg[0] == "getv":
        var = msg[1].strip()
        if DB.exists("%s:%s" % (DBKeyPrefix,var)):
            return "*%s* = %s for %s" %(var, DB.get("%s:%s" % (DBKeyPrefix,var)).decode("utf-8"),fullMsg["chat"]["title"])
        else:
            return "Key not found"
    if msg[0] == "setv":
        var, value = msg[1].split()
        DB.set("%s:%s"%(DBKeyPrefix,var),value)
        return "*%s* = %s for %s" %(var, value, fullMsg["chat"]["title"])