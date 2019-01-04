Target stratergy to avoid clustering
====================================
+ Targets split up their paths when they observe a observer coming in their direction

Observer stratergy
==================
1. The paper suggested(http://teamcore.usc.edu/papers/2013/ijcai13.pdf)
	+ The paper considers that some of the stratergy will give an optimal solution, but as we have randomization none will
	+ To see which algorithm performs better we look at the number of targets that will be observed
	+ We need multiple weak performing algos. As we have randomization into consideration it is already satisfied

2. Multiple stratergies
	1. Dont consider the obstacles and consider they dont exist
	2. Consider the obstacles as a reward itself, hence including them in the reward of BRLP-CTO
	3. Consider the obstacles as targets itself and hence including them as a weighted mean while computing the mean position of targets
	4. Consider the task to be finding the targets, if no targets go for the obstacles, if no obstacles go for exploration
	5. Choose a ML based classification path to choose the optimal path.
		+ SVM
		+ Polynomial fitting
	6. Go from centre to outside and oscillated until a target is found. Here we are assuming ny stratergy is cover the ground looking for everything.

RESULTS
=======

