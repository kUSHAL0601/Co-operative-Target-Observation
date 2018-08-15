STATIC OBSTACLES STRATERGIES
============================

+ The length of the obstacle would be randomly picked from 2,5,8,12,20
+ The orientation of the obstacle would be random

For observers:
--------------
  1. Including them in reward function:
    + They will be given a positive reward equal to their length
    + The weight for the targets would be 0.9 and the weight for the obstacles would be 0.1
  2. Including them while computing mean:
    + A pseudo-target will be kept on the other side of the obstacle and will be used to compute the mean
    + The reward function would remain the same
  3. Exploring obstacles when probability to exploit is zero:
    + Obstacles will only be observed when there is complete exploration

For targets:
------------
  + Reward function now introduced for targets
  + Reward is equal to length of obstacles(in the direction it is approaching), which helps choosing which obstacles to go to.
  + For chosen obstacle:
  	+ While moving away from observer, they will try to hide behind a obstacle if there.
  + If no obstacle in range:
  	+ They will move with randomization as before.
  + If behind a obstacle, on sensing an approaching observer from the same side, it first tries to go on other side of the obstacle, then continues with same of the above two startegies.
