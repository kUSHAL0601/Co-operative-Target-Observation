from main_test import Main as m
from centralized_communicative_test import CentralizedComm as cc
from decentralized_communicative_test import DecenteralizedComm as dc
from copy import deepcopy
from random import randint

no_observers_arr=[2,6,10,14,18,20,50]
no_targets_arr=[3,9,15,21,27,50,100]
sensor_range=[5,10,15,20,25]
target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]
c1=0
c2=0
c3=0
threshold=0.2
print("\n\n THRESHOLD: ",threshold*100,"%\n\n")
for _ in range(10):
    for trgt in no_targets_arr:
        for obsver in no_observers_arr:
            for sns_rng_o in sensor_range:
                a1=m()
                sns_rng_t=sensor_range[randint(0,len(sensor_range)-1)]
                tspeed=target_speed[randint(0,len(target_speed)-1)]
                (no_targets,no_observers,targets,observers)=a1.initialize_param(trgt,obsver,sns_rng_t,sns_rng_o,tspeed)
                t1=deepcopy(targets)
                o1=deepcopy(observers)
                t2=deepcopy(targets)
                o2=deepcopy(observers)
                a2=cc()
                a3=dc()
                x1=a1.run(no_targets,no_observers,targets,observers)
                c1+=x1
                x2=a2.run(no_targets,no_observers,t1,o1,threshold)
                c2+=x2
                x3=a3.run(no_targets,no_observers,t2,o2,threshold)
                c3+=x3
                print("No of Targets:",trgt,"No of Observers:",obsver,"Target's sensor range:",sns_rng_t,"Observer's sensor range:",sns_rng_o,"Target speed:",tspeed,"Original:",x1,"Centeralized Comm.:",x2,"Decentralized Comm.:",x3)
print("Normal:",t1,"Centralized",t2,"Decenteralized",t3)