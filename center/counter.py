import math
import string
import  datetime
#x1=(c.updated_dosses//c.doss_per_day)-(math.ceil(c.available_dosses/c.doss_per_day))
def counter(x,x1,y):
    a=x//y
    l=list(range(1,y+1))
    l.reverse()
    alphabet=list(string.ascii_uppercase)
    slot=dict(zip(l,alphabet))
    r=list(range(len(slot)))
    r.reverse()
    max=y+1
    if math.ceil(x1/a) in slot:
        return slot[math.ceil(x1/a)],datetime.time(9+r[math.ceil(x1/a)-1],00,00),datetime.time(9+r[math.ceil(x1/a)-1]+1,00,00)
    elif math.ceil(x1/a)==max:
        return slot[math.ceil(x1/a)-1],datetime.time(9+r[max-2],00,00),datetime.time(9+r[max-2]+1,00,00)
# k=list(range(1,10))
# k.reverse()
# for i in k:
#     k,l,j=(counter(9,i,4))
#     print(k,l,j)



