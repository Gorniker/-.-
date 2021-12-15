
import json
import pdb
import copy

import random

import gamma
from math import sin, pi, gamma

def fitness_func(pop,to_start,to_end):
    rangs=[]
    for p in pop:
        starts=[]
        ends=[]
        r=[]
        for i in p:
            starts.append(i['start']-i['max_vyd'])
            ends.append(i['start']+i['cyc']*i['num']*60-i['min_vyd'])
            r0=(i['num']/((ends[-1]-starts[-1])/(42*60)))/3
            r.append(r0)

        for i in range(len(to_start)):
            starts.append(to_start[i])
            ends.append(to_end[i])
            r.append(1/3)

        moments=copy.deepcopy(starts)
        moments.extend(ends)

        r_max=0

        for t in moments:
            r0=0
            for j in range(len(starts)):
                if starts[j]<=t and ends[j]>=t:
                    r0+=r[j]
                if r0>r_max:
                    r_max=r0

        rangs.append(r_max)
    return rangs


with open("input.json",'r') as read_file:
    data = json.load(read_file)

def TO(TO):
    to_starts=[]
    to_ends=[]
    for t in TO:
        if 'КВ' in t['ag']:
            to_starts.append(t['start'])
            to_ends.append(t['end'])

    return to_starts,to_ends

def def_gen(data):
    ind=0
    def_gen=[]
    for i in data['unrs']:
        def_gen.append(dict(un=i['un'],start=i['start'],cyc=i['cycle'],min_vyd=i['min_vyd'],max_vyd=i['max_vyd'],num=i['num'],min_start=i['start']-30*60,max_start=i['start']+30*60,max_cyc=i['cycle']+30,ind=ind,num1=0,num2=0,cyc1=0,cyc2=0))
        ind+=1

    return def_gen

def def_pop(def_gen,N):
    pop=[]
    for i in range(N):
        pop.append([])
        for j in def_gen:
            num1=random.randrange(0,j['num'],1)
            num1=j['num']
            num2=j['num']-num1
            pop[-1].append(dict(un=j['un'],start=random.randrange(j['min_start'], j['max_start'], 60),cyc=random.randrange(j['cyc'], j['max_cyc'], 1),num=j['num'],min_vyd=j['min_vyd'],max_vyd=j['max_vyd'],ind=j['ind'],min_start=j['min_start'],max_start=j['max_start'],max_cyc=j['max_cyc'],min_cyc=j['cyc'],num1=num1,num2=num2,cyc1=random.randrange(j['cyc'], j['max_cyc'], 1),cyc2=random.randrange(j['cyc'], j['max_cyc'], 1)))

    return pop


def alive(rangs,pop,undead):
    alive_pop=[]
    rangs_rev_sort=sorted(rangs)
    for i in range(undead):
        alive_pop.append(pop[rangs.index(rangs_rev_sort[i])])

    return alive_pop

def death(pop):
    del_list=[]
    for i in pop:
        for j in i:
            for k in i:
                if j['un']==k['un'] and j['ind']!=k['ind']:
                    if j['start']>=k['start'] and j['start']<=k['start']+k['num1']*k['cyc1']*60+k['num2']*k['cyc2']*60 and i not in del_list:
                        del_list.append(i)
                    if j['start']+j['num1']*j['cyc1']*60+j['num2']*j['cyc2']*60>=k['start'] and j['start']+j['num1']*j['cyc1']*60+j['num2']*j['cyc2']*60<=k['start']+k['num1']*k['cyc1']*60+k['num2']*k['cyc2']*60 and i not in del_list:
                        del_list.append(i)
    for i in del_list:
        pop.pop(pop.index(i))

    return pop



def fpa(g_,pop,rangs):

    def is_alive(pers):
        for j in pers:
            for k in pers:
                if j['un']==k['un'] and j['ind']!=k['ind']:
                    if j['start']>=k['start'] and j['start']<=k['start']+k['num1']*k['cyc1']*60+k['num2']*k['cyc2']*60:
                        return False
                    if j['start']+j['num1']*j['cyc1']*60+j['num2']*j['cyc2']*60>=k['start'] and j['start']+j['num1']*j['cyc1']*60+j['num2']*j['cyc2']*60<=k['start']+k['num1']*k['cyc1']*60+k['num2']*k['cyc2']*60:
                        return False

        return True


    def local_pollination(pers1,pers2,pers3):
        e=random.random()
        for i in range(len(pers1)):
            pers1[i]['cyc1']+=int((pers3[i]['cyc1']-pers2[i]['cyc1'])*e)
            pers1[i]['cyc2']+=int((pers3[i]['cyc2']-pers2[i]['cyc2'])*e)
            pers1[i]['start']+=(((pers3[i]['start']-pers2[i]['start'])*e)//60)*60
            if pers1[i]['cyc1']<pers1[i]['min_cyc']:
                pers1[i]['cyc1']=pers1[i]['min_cyc']
            if pers1[i]['cyc1']>pers1[i]['max_cyc']:
                pers1[i]['cyc1']=pers1[i]['max_cyc']
            if pers1[i]['cyc2']<pers1[i]['min_cyc']:
                pers1[i]['cyc2']=pers1[i]['min_cyc']
            if pers1[i]['cyc2']>pers1[i]['max_cyc']:
                pers1[i]['cyc2']=pers1[i]['max_cyc']
            if pers[i]['start']>pers1[i]['max_start']:
                pers[i]['start']=pers1[i]['max_start']
            if pers[i]['start']<pers1[i]['min_start']:
                pers[i]['start']=pers1[i]['min_start']
        return pers1


    def levy(s0):


        if s0<0:
            s0=s0*(-1)
            lbm = 1.5
            s=(i*3+301)/1000
            l = (lbm*gamma(lbm)*sin((pi*lbm)/2))/(pi*pow(s,1+lbm))
            return int(-l*2)
        else:
            lbm = 1.5
            s=(i*3+301)/1000
            l = (lbm*gamma(lbm)*sin((pi*lbm)/2))/(pi*pow(s,1+lbm))
            return int(l*2)


    def global_pollination(pers,g_):
        for i in range(len(pers)):
            pers[i]['cyc1']+=int(levy(pers[i]['cyc1']-g_[i]['cyc1']))
            pers[i]['cyc2']+=int(levy(pers[i]['cyc2']-g_[i]['cyc2']))

            if pers[i]['cyc1']<pers[i]['min_cyc']:
                pers[i]['cyc1']=pers[i]['min_cyc']
            if pers[i]['cyc1']>pers[i]['max_cyc']:
                pers[i]['cyc1']=pers[i]['max_cyc']
            if pers[i]['cyc2']<pers[i]['min_cyc']:
                pers[i]['cyc2']=pers[i]['min_cyc']
            if pers[i]['cyc2']>pers[i]['max_cyc']:
                pers[i]['cyc2']=pers[i]['max_cyc']
            pers[i]['start']+=int(levy((pers[i]['start']-g_[i]['start'])//60)*60)

            if pers[i]['start']>pers[i]['max_start']:
                pers[i]['start']=pers[i]['max_start']
            if pers[i]['start']<pers[i]['min_start']:
                pers[i]['start']=pers[i]['min_start']


        return pers

    for i in range(len(pop)):
        pers=pop[i]
        if random.random()>p_switch:              #local pollination
            rand_ind=random.randint(0,len_pop-1)
            rand_ind2=random.randint(0,len_pop-1)
            new_pers=local_pollination(pers,pop[rand_ind],pop[rand_ind2])
        else:                                   #global pollination
            new_pers=global_pollination(pers,g_)

        new_rang=fitness_func([new_pers],to_start,to_ends)[0]

        if new_rang<rangs[i] and is_alive(new_pers):
            rangs[i]=new_rang
            pop[i]=new_pers
    return pop,rangs


#Основные параметры


N=5000                           #начальная популяция


p_switch=0.8                  #biotic probability


to_start,to_ends=TO(data['to'])
def_gen=def_gen(data)

#Количество изуаемых особей минимум 1/20 от начальной полпуляции
while 1:
    pop=def_pop(def_gen,N)
    pop=death(pop)
    if len(pop)>=N/20:
        len_pop=len(pop)
        break
    print(len(pop))
print('В начальной популяции',len(pop),'особей')

count_max=0
count_avg=0
max_rang=100
avg=100
rangs=fitness_func(pop,to_start,to_ends)
print(min(rangs))
for i in range(500):
    g_=pop[rangs.index(min(rangs))]   #лучшее решение на данной итерации

    pop,rangs=fpa(g_,pop,rangs)

    r_max=min(rangs)
    if r_max<max_rang:
        the_best=pop[rangs.index(min(rangs))]
        max_rang=r_max
        count_max=0
        print(r_max,'Поколоение',i)
    else:
        count_max+=1
    if count_max==250:
        break


new_data=copy.deepcopy(data)


def make_input(the_best,data):

    for i in range(len(data)):
        data[i]['cycle']=the_best[i]['cyc1']
        data[i]['start']=the_best[i]['start']
    return data

new_data['unrs']=make_input(the_best,new_data['unrs'])

with open('new_input.json', "w") as write_file:
    json.dump(new_data,write_file,ensure_ascii=False)
