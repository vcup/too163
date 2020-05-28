def isjson(string):
    if not isinstance(string, str):
        string = str(string)
    # noinspection PyBroadException
    try:
        from json import loads
        loads(string)
        return True
    except:
        return False


def lrc_have_timeline(lrc_str):
    from re import findall
    if findall(r'\[\d*?:\d*?\.\d*?\]', lrc_str):
        return False
    else:
        return True


def isfileobj(fileobj):
    from _io import TextIOWrapper
    return isinstance(fileobj, TextIOWrapper)


def isfilename(fn):
    from re import findall
    if findall('/|\\|?|:|"|\||\*|>|<', fn):
        return True
    return False


def setd(s: iter, d):
    s = set(s)
    try:
        s.remove(d)
    except KeyError:
        pass
    return s


def subdir(dp):
    from os import listdir
    from os.path import isdir
    if [x for x in listdir(dp) if isdir(x)]:
        return True
    return False


def format_fn(fn):
    def rename(name):
        if r'/' in name:
            return name.replace('/', r'／')
        elif '\\' in name:
            return name.replace('\\', '＼')
        elif '?' in name:
            return name.replace('?', '？')
        elif ':' in name:
            return name.replace(':', '：')
        elif '"' in name:
            return name.replace('"', " ＂")
        elif '|' in name:
            return name.replace('|', '｜')
        elif '*' in name:
            return name.replace('*', '＊')
        elif '>' in name:
            return name.replace('>', '＞')
        elif '<' in name:
            return name.replace('<', '＜')
        elif '\t' in name:
            return name.replace('', '\t')
        else:
            return False

    n = 0
    while n < 10:
        if not isinstance(rename(fn), bool):
            fn = rename(fn)
        n += 1
    return fn


def i63lrc(lrc_dict):
    status = lrc_dict.get
    if status('nolyric') or status('uncollected') or status('needDesc'):
        return True
    return False
