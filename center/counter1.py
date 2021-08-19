import math
import string
import  datetime
def counter1(x,x1,y):
    a=x//y
    l=list(range(1,y+1))
    l.reverse()
    alphabet=list(string.ascii_uppercase)
    slot=dict(zip(l,alphabet))
    r=list(range(len(slot)))
    r.reverse()

    if math.ceil(x1/a) in slot:
        return slot[math.ceil(x1/a)],datetime.time(9+r[math.ceil(x1/a)-1],00,00),datetime.time(9+r[math.ceil(x1/a)-1]+1,00,00)

