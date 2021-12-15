import json
import pdb
import copy

import random

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
        def_gen.append(dict(un=i['un'],start=i['start'],cyc=i['cycle'],min_vyd=i['min_vyd'],max_vyd=i['max_vyd'],num=i['num'],min_start=i['start']-30*60,max_start=i['start']+30*60,max_cyc=i['cycle']+30,ind=ind))
        ind+=1

    return def_gen

def def_pop(def_gen,N):
    pop=[]
    for i in range(N):
        pop.append([])
        for j in def_gen:
            pop[-1].append(dict(un=j['un'],start=random.randrange(j['min_start'], j['max_start'], 60),cyc=random.randrange(j['cyc'], j['max_cyc'], 1),num=j['num'],min_vyd=j['min_vyd'],max_vyd=j['max_vyd'],ind=j['ind'],min_start=j['min_start'],max_start=j['max_start'],max_cyc=j['max_cyc'],min_cyc=j['cyc']))
    return pop

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
                    if j['start']>=k['start'] and j['start']<=k['start']+k['num']*k['cyc']*60 and i not in del_list:
                        del_list.append(i)
                    if j['start']+j['num']*j['cyc']*60>=k['start'] and j['start']+j['num']*j['cyc']*60<=k['start']+k['num']*k['cyc']*60 and i not in del_list:
                        del_list.append(i)

    for i in del_list:
        pop.pop(pop.index(i))

    return pop

def new_pop(pop,m,c):
    new_pop=[]


    def crossover(parent1,parent2):
        c1=copy.deepcopy(parent1)
        for p in range(len(c1)):
            if random.random()>0.5:
                c1[p]['start']=parent1[p]['start']
                c1[p]['cyc']=parent2[p]['cyc']
            else:
                c1[p]['start']=parent2[p]['start']
                c1[p]['cyc']=parent1[p]['cyc']
        return c1



    def mutation(pers):
        for i in range(m):
            index=random.randint(0,len(pers)-1)
            pers[index]['start']=random.randrange(pers[index]['min_start'], pers[index]['max_start'], 60)
            pers[index]['cyc']=random.randint(pers[index]['min_cyc'],pers[index]['max_cyc'])

        return pers


    for i in range(len(pop)//2):
        for j in range(c):
            new_pop.append(mutation(crossover(pop[i],pop[-i-1])))

    #всегда оставляем лучшего в исконном виде
    new_pop.append(pop[0])

    return new_pop

def best_max_avg(p,to_start,to_end):
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
    r_all=[]

    for t in moments:
        r0=0
        for j in range(len(starts)):
            if starts[j]<=t and ends[j]>=t:
                r0+=r[j]
            if r0>r_max:
                r_max=r0
            r_all.append(r0)
    r_avg=sum(r_all)/len(r_all)
    r_delta=0
    for i in r_all:
        r_delta+=(r_avg-i)**2

    return r_max,r_delta

#Основные параметры

children=50                      #количество потомков от каждой пары родителей

al=30                        #количество выживших в каждом поколении

N=1000                           #начальная популяция

mut=2                           #количество мутировавших генов в у каждого потомка


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

for i in range(500):
    rangs=fitness_func(pop,to_start,to_ends)
    pop=alive(rangs,pop,al)
    pop=new_pop(pop,mut,children)
    pop=death(pop)
    #Определение среднего значения графика плотности
    r_max,r_delta=best_max_avg(pop[-1],to_start,to_ends)
    if r_max<max_rang:
        max_rang=r_max
        count_max=0
        print(r_max,'Поколоение',i)
    else:
        count_max+=1
    if count_max==40:
        break


new_data=copy.deepcopy(data)
rangs=fitness_func(pop,to_start,to_ends)
the_best=pop[rangs.index((min(rangs)))]

def make_input(the_best,data):

    for i in range(len(data)):
        data[i]['cycle']=the_best[i]['cyc']
        data[i]['start']=the_best[i]['start']
    return data

new_data['unrs']=make_input(the_best,new_data['unrs'])

with open('new_input.json', "w") as write_file:
    json.dump(new_data,write_file,ensure_ascii=False)
