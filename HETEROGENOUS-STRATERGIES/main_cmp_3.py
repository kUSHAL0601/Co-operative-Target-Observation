from hetero_main_3 import hetero_main_3 as h
x=h()
no_observers_arr=[2,6,10,14,18]
no_targets_arr=[3,9,15,21,27]
sensor_range=[5,10,15,20,25]
dh={}
d1={}
d2={}
d3={}
d4={}

iter=0
for _ in range(10):
    for trgt in no_targets_arr:
        for obsver in no_observers_arr:
            for sns_rng_o in sensor_range:
                iter+=1
                print("Iteration:",iter,"Targets:",trgt,"Observers",obsver,"Sensor Range for observers",sns_rng_o)
                y=x.custom_cmp(trgt,obsver,sns_rng_o)
                print()
                try:
                    dh[(str(trgt),str(obsver),str(sns_rng_o))]+=y[0]
                    d1[(str(trgt),str(obsver),str(sns_rng_o))]+=y[1]
                    d2[(str(trgt),str(obsver),str(sns_rng_o))]+=y[2]
                    d3[(str(trgt),str(obsver),str(sns_rng_o))]+=y[3]
                    d4[(str(trgt),str(obsver),str(sns_rng_o))]+=y[4]
                except:
                    dh[(str(trgt),str(obsver),str(sns_rng_o))]=y[0]
                    d1[(str(trgt),str(obsver),str(sns_rng_o))]=y[1]
                    d2[(str(trgt),str(obsver),str(sns_rng_o))]=y[2]
                    d3[(str(trgt),str(obsver),str(sns_rng_o))]=y[3]
                    d4[(str(trgt),str(obsver),str(sns_rng_o))]=y[4]
print("Targets, Observers, Sensor Range, Heterog, Strat 1, Strat 2, Strat 3, Strat 4")
for i in dh:
    print(' '.join(i),dh[i]/10,d1[i]/10,d2[i]/10,d3[i]/10,d4[i]/10)