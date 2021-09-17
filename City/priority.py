import bd as bd
from City.models import area


def priority(pk):
    x=area.objects.all()
    k=[]
    for i in x:
        if i.enability == True:
            k.append(i.population-i.total_rgistered)
    p=(sum(k))
    x1=area.objects.get(id=pk)
    n=x1.population-x1.total_rgistered
    t=((n*100)/p)
    t=("%.2f" %t)
    return t

# for i in k:
#     k1.append((i*100//p))
# print(k1)

