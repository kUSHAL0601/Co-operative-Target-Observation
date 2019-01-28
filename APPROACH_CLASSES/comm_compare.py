from main_test import Main as m
from centralized_communicative_test import CentralizedComm as cc
from decentralized_communicative_test import DecenteralizedComm as dc

no_observers_arr=[2,6,10,14,18,20,50]
no_targets_arr=[3,9,15,21,27,50,100]
sensor_range=[5,10,15,20,25]
target_speed=[0.2,0.5,0.8,1.0,1.2,1.5]

for _ in range(10):
    for trgt in no_targets_arr:
        for obsver in no_observers_arr:
            for sns_rng_t in sensor_range:
                for sns_rng_o in sensor_range:
                    for tspeed in target_speed:
                        a1=m()
                        (no_targets,no_observers,targets,observers)=a1.initialize_param(trgt,obsver,sns_rng_t,sns_rng_o,tspeed)
                        a2=cc()
                        a3=dc()
                        x1=a1.run(no_targets,no_observers,targets,observers)
                        x2=a2.run(no_targets,no_observers,targets,observers,0.2)
                        x3=a3.run(no_targets,no_observers,targets,observers,0.2)
                        print("No of Targets:",trgt,"No of Observers:",obsver,"Target's sensor range:",sns_rng_t,"Observer's sensor range:",sns_rng_o,"Target speed:",tspeed,"Original:",x1,"Centeralized Comm.:",x2,"Decentralized Comm.:",x3)