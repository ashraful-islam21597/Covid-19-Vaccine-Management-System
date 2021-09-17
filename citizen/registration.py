import datetime
import math

from City.models import area
from City.priority import priority
from center.counter1 import counter1
from center.models import schedule
from citizen.models import people


def registration(c,nid):

    x1 = (c.updated_dosses // c.doss_per_day) - (math.ceil(c.available_dosses / c.doss_per_day))
    if x1 < 0:
        x1 = c.updated_dosses // c.doss_per_day
    if c.available_dosses == c.updated_dosses and c.updated_dosses % c.doss_per_day == 1:
        c.num_of_dosses = c.doss_per_day + 1
        c.save()
    slot_name, start, end = counter1(c.doss_per_day, c.num_of_dosses, 4)
    p = schedule(slot=slot_name, start_time=start, end_time=end,
                         date=c.working_time + datetime.timedelta(days=x1),
                         second_date=c.working_time + datetime.timedelta(days=x1+30))
    p.save()
    p.center_name.add(c)
    p.num_user += 1
    p.save()
    c.num_of_dosses -= 1
    c.available_dosses -= 1
    c.save()
    d = people(nid=nid, center_id=c.id, period_id=p.id, registered=True, vaccinated=False, doss_1st=False,
               doss_2nd=False)
    d.save()
    m = area.objects.get(name=c.area_name)

    m.total_rgistered += 1

    m.save()
    area1 = area.objects.all()
    for i in area1:
        print(priority(i.id))
        i.priority = priority(i.id)
        print(i.id)
        i.save()
    d1 = people.objects.get(nid=d.nid)
    if c.num_of_dosses == 0 and 0 < c.available_dosses > c.doss_per_day:
        c.num_of_dosses = c.doss_per_day
        c.save()
    elif c.num_of_dosses == 0 and 0 < c.available_dosses <= c.doss_per_day:
        c.num_of_dosses = c.available_dosses
        c.save()
    elif c.available_dosses == 0 and c.pending_doss_center != 0:
        c.available_dosses = c.pending_doss_center
        c.updated_dosses = c.pending_doss_center
        c.pending_doss_center = c.pending_doss_center - c.updated_dosses
        c.save()
        if math.floor(c.updated_dosses / 7) % 4 == 0:
            c.doss_per_day = math.floor(c.updated_dosses / 7)
        else:
            c.doss_per_day = math.floor(c.updated_dosses / 7) - (math.floor(c.updated_dosses / 7) % 4)
        c.save()
        c.num_of_dosses = c.doss_per_day
        c.save()


