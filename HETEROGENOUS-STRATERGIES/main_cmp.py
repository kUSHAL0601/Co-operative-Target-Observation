from hetero_main import hetero_main as h
x=h()
no_observers_arr=[2,6,10,14,18]
no_targets_arr=[3,9,15,21,27]
sensor_range=[5,10,15,20,25]

iter=0
for _ in range(10):
    for trgt in no_targets_arr:
        for obsver in no_observers_arr:
            for sns_rng_o in sensor_range:
                iter+=1
                print("Iteration:",iter,"Targets:",trgt,"Observers",obsver,"Sensor Range for observers",sns_rng_o)
                x.custom_cmp(trgt,obsver,sns_rng_o)
                print()