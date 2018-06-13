PROBLEM STATEMENT
=================
+ We want to introduce obstacles into this setup.
+ We will have targets that try to move out of sight by moving away or by moving behind obstacles.
+ Observers can observe for certain radius but not in the arc cut off by obstacle
+ Introducing ways in which we can model this setup (i.e. what sort of obstacles we can introduce etc.)
+ Develop heuristics for the observer and target.

APPROACH
========
1. Stationary obstacles
  + For observers:
	1. At every update step predict the stationary points sensed(obstacles).
	2. At every update step predict if given target(moving) will be behind a obstacle or not.
	3. If a obstacle suddenly disappears from sensor range, consider it to compute the mean for some delta time steps.
	4. Reward function should be weighted, considering some weight for the number of obstacles in range.
	5. Consider the position of obstacles into the mean too. Their proportion of contribution in mean should be less.
	6. Target oscillating around the obstacle should be considered a potential threat.
  + For targets:
	1. The basic objective would still be to go away from the observers.
	2. The target would be to stay behind the obstacle as much as possible.
	3. Randomization would also be included.
	4. Getting away from observer would have a reward and getting behind a obstacle would have(comparatively lesser) reward.
2. Moving targets
  + For observers:
	1. Everything pretty much remains same, we just consider obstacles also as targets.
  + For targets:
	1. Try to go away from observers.
	2. Try to go near the obstacles, match its speed if possible.
	3. Have a bit randomization in the motion
