def first_move(data):
    new=[]
    for val in data:
        if val[0] == "N":
            new.append((val)[0:3])
        else:
            new.append((val)[0:2])
    return(new)

def label(data):
    new=[]
    for val in data:
        if val in ("1+0","2+1"):
            new.append("Bullet")
        elif val in ("3+0","3+2","5+0","5+3"):
            new.append("Blitz")
        elif val in ("10+0","10+5","15+10"):
            new.append("Rapid")
        elif val in ("30+0", "30+20"):
            new.append("Classical")
        else:
            new.append("Custom")
    return(new)
            