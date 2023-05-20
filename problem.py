# return masked string

def split_arr(cc):
    sub = []
    for i in cc:
        sub.append(i)
    return sub

def maskify(cc):
    sub = split_arr(cc)
    if len(sub) == 4:
        return n
    else:
        for i in range(0, len(sub)-4):
            sub[i] = "#"
        return "".join(sub)
print(maskify('osofosdogishiio44oao'))
