from sys import argv
script, first = argv
# print(first)
dh={}
d3={}
d4={}
with open(first,'r') as fd:
    lines=fd.readlines()
    x=len(lines)
    for i in range(x//5):
        l1=lines[i*5].split('\n')[0].split(' ')
        l1=(int(l1[3]),int(l1[5]),int(l1[10]))
        l2=int(lines[i*5+1].split('\n')[0].split(' ')[3])
        l5=int(lines[i*5+2].split('\n')[0].split(' ')[3])
        l6=int(lines[i*5+3].split('\n')[0].split(' ')[3])
        # print(l1,l2,l3,l4,l5,l6)
        try:
            dh[l1]+=l2
            d3[l1]+=l5
            d4[l1]+=l6
        except:
            dh[l1]=l2
            d3[l1]=l5
            d4[l1]=l6
better=0
for i in dh:
    print()
    print("Targets:",i[0],"Observers:",i[1],"Sensor range:",i[2])
    print("Hetero:",dh[i],"Strat3:",d3[i],"Strat4:",d4[i])
    print()
    if(dh[i]>=min(d3[i],d4[i])):
        better+=1
print()
print()
print("BETTER IN ",better, "OUT OF",len(dh))