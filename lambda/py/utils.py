def list_to_speech(l):
    if len(l) == 0:
        return "nothing"
    if len(l) == 1:
        return l[0]
    l = list(map(str, l))
    return ', '.join(l[:-1]) + " and " + l[-1]
