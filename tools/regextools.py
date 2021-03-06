import re

BASICPATTERN = '[!/](%s)\s{,1}(.*)' # example "/animefind baka" -> (animefind, baka)


# returns  compiled  BASICPATTERN for each given string
def basicRegex(strings):
    if not isinstance(strings,list):
        return []
    ans = []
    for string in strings:
        pattern = re.compile(BASICPATTERN % string.strip())
        ans.append(pattern)
    return ans
