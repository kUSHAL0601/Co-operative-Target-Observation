from sys import argv
script, first = argv
from statistics import median as med
from statistics import mean
from statistics import stdev

def get_sum(arr):
    ans=0
    for i in arr:
        ans+=i
    return ans

def get_robustness(arr):
    m=mean(arr)
    v=stdev(arr)
    if v==0:
        norm=arr
    else:
        norm = []    
        for i in arr:
            norm.append((float)(i-m)/v)
    m=med(norm)
    x=[]
    for i in norm:
        x.append(abs(i-m))
    return med(x)

# print(first)
dh={}
d1={}
d2={}
d3={}
d4={}
with open(first,'r') as fd:
    lines=fd.readlines()
    x=len(lines)
    for i in range(x//7):
        try:
            l1=lines[i*7].split('\n')[0].split(' ')
            l1=(int(l1[3]),int(l1[5]),int(l1[10]))
            l2=int(lines[i*7+1].split('\n')[0].split(' ')[3])
            l3=int(lines[i*7+2].split('\n')[0].split(' ')[3])
            l4=int(lines[i*7+3].split('\n')[0].split(' ')[3])
            l5=int(lines[i*7+4].split('\n')[0].split(' ')[3])
            l6=int(lines[i*7+5].split('\n')[0].split(' ')[3])
            # print(l1,l2,l3,l4,l5,l6)
            try:
                dh[l1].append(l2)
                d1[l1].append(l3)
                d2[l1].append(l4)
                d3[l1].append(l5)
                d4[l1].append(l6)
            except:
                dh[l1]=[l2]
                d1[l1]=[l3]
                d2[l1]=[l4]
                d3[l1]=[l5]
                d4[l1]=[l6]
        except:
            pass
better=0
better_than_best=0
for i in dh:
    print()
    print("Targets:",i[0],"Observers:",i[1],"Sensor range:",i[2])
    print("TARGET COUNT:","Hetero:",get_sum(dh[i]),"Strat1:",get_sum(d1[i]),"Strat2:",get_sum(d2[i]),"Strat3:",get_sum(d3[i]),"Strat4:",get_sum(d4[i]))
    print("ROBUSTNESS MEASURE:","Hetero:",get_robustness(dh[i]),"Strat1:",get_robustness(d1[i]),"Strat2:",get_robustness(d2[i]),"Strat3:",get_robustness(d3[i]),"Strat4:",get_robustness(d4[i]))
    print()
    if(get_sum(dh[i])>=min(get_sum(d1[i]),get_sum(d2[i]),get_sum(d3[i]),get_sum(d4[i]))):
        better+=1
    if(get_sum(dh[i])>=max(get_sum(d1[i]),get_sum(d2[i]),get_sum(d3[i]),get_sum(d4[i]))):
        better_than_best+=1
print()
print()
print("BETTER IN ",better, "OUT OF",len(dh))
print("BETTER THAN BEST IN ",better_than_best, "OUT OF",len(dh))

df={'hetero':[],'strat1':[],'strat2':[],'strat3':[],'strat4':[]}

for i in dh:
    df['hetero']+=dh[i]
    df['strat1']+=d1[i]
    df['strat2']+=d2[i]
    df['strat3']+=d3[i]
    df['strat4']+=d4[i]
print("OVERALL ROBUSTNESS:","Hetero:",get_robustness(df['hetero']),"Strat1:",get_robustness(df['strat1']),"Strat2:",get_robustness(df['strat2']),"Strat3:",get_robustness(df['strat3']),"Strat4:",get_robustness(df['strat4']))