import json
import pdb
import copy

import random

import gamma
from math import sin, pi, gamma

import matplotlib.pyplot as plt



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



def fitness_func(pop,to_start,to_end):
    rangs=[]
    for p in pop:
        starts=[]
        ends=[]
        r=[]
        for i in p:
            #начало первой половины серии
            start_1=i['start']-i['max_vyd']
            starts.append(start_1)

            #начало второй половины серии
            start_2=i['start']+i['num1']*i['cyc1']*60-i['max_vyd']
            starts.append(start_2)

            #конец первой половины серии
            end_1=i['start']+i['cyc1']*i['num1']*60-i['min_vyd']
            ends.append(end_1)

            #конец второй половины серии
            end_2=i['start']+i['cyc1']*i['num1']*60+i['cyc2']*i['num2']*60-i['min_vyd']
            ends.append(end_2)

            #плотность первой половины серии
            r1=(i['num1']/((end_1-start_1)/(42*60)))/3
            r.append(r1)

            #плотность первой половины серии
            r2=(i['num2']/((end_2-start_2)/(42*60)))/3
            r.append(r2)

        #Обработка ТО
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

def big_bang(elite,R):
    count=int(R/len(elite))

    new_pop=[]

    for el in elite:
        for j in range(count):
            new_pers=copy.deepcopy(el)
            for i in range(len(el)):
                rand_cyc_delta=random.randrange(-5, 5, 1)      #выбираем рандомное количество минут для изменения цикла
                rand_start_delta=random.randrange(-5*60, 5*60, 60)                      #выбираем рандомное количество секунд для изменения цикла

                new_pers[i]['cyc1']=int((el[i]['cyc1'])+rand_cyc_delta)
                new_pers[i]['start']=int((el[i]['start'])+rand_start_delta)

                if new_pers[i]['cyc1']<new_pers[i]['min_cyc']:
                    new_pers[i]['cyc1']=new_pers[i]['min_cyc']
                if new_pers[i]['cyc1']>new_pers[i]['max_cyc']:
                    new_pers[i]['cyc1']=new_pers[i]['max_cyc']
                if new_pers[i]['start']>new_pers[i]['max_start']:
                    new_pers[i]['start']=new_pers[i]['max_start']
                if new_pers[i]['start']<new_pers[i]['min_start']:
                    new_pers[i]['start']=new_pers[i]['min_start']
            new_pop.append(new_pers)


    return new_pop



def big_crunch_1(pop,rangs,elite_num):
    centre=[]
    for i in range(elite_num):
        centre.append(pop[rangs.index(min(rangs))])
        pop.pop(rangs.index(min(rangs)))
    return centre

def big_crunch_2(pop,rangs,elite_num):
    centre=copy.deepcopy(pop[0])         #обозначаем за центр рандомного представителя поппуляции
    for c in centre:
        c['cyc1']=0
        c['start']=0
    total_f=0
    for i in range(len(pop)):
        for j in range(len(pop[i])):
            centre[j]['cyc1']+=pop[i][j]['cyc1']/rangs[i]
            centre[j]['start']+=pop[i][j]['start']/rangs[i]
        total_f+=(1/rangs[i])

    for i in centre:
        i['cyc1']=int(i['cyc1']/total_f)
        i['start']=int(i['start']/total_f)

    return [centre]




#Основные параметры
R=2000       #Количество новых элементов вокруг каждого центра масс
N=3000       #Начальная популяция
elite_pool_len=2    #Количество центров масс


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

the_best=[]

count_max=0
count_avg=0
max_rang=100
avg=100
rangs=fitness_func(pop,to_start,to_ends)
print(min(rangs))
for i in range(500):
    elite_pool=big_crunch_1(pop,rangs,elite_pool_len)

    pop=big_bang(elite_pool,R)

    pop=death(pop)

    rangs=fitness_func(pop,to_start,to_ends)

    r_max=min(rangs)
    if r_max<max_rang:
        the_best=pop[rangs.index(min(rangs))]
        max_rang=r_max
        count_max=0
        print(r_max,'Поколоение',i)
    else:
        count_max+=1
    if count_max==40:
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
