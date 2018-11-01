from matplotlib import pyplot as plt

lines=[]

# with open("./obst3_main_custom_cmp_res.txt", "r") as f:
with open("./obst3_main_custom_cmp_res_mult.txt", "r") as f:
	for line in f:
		lines.append(line)
d1={}
d2={}
no_targets=[]
no_obstacles=[]
for line in lines:
	try:
		x=line.split(' ')
		x=[int(i) for i in x]
		no_targets.append(x[1])
		no_obstacles.append(x[2])
		if (x[1],x[2]) in d1:
			d1[(x[1],x[2])]+=x[3]
		else:
			d1[(x[1],x[2])]=x[3]
		if (x[1],x[2]) in d2:
			d2[(x[1],x[2])]+=x[4]
		else:
			d2[(x[1],x[2])]=x[4]
	except:
		pass
print(d1,d2)
no_targets=list(set(no_targets))
no_targets.sort()
no_obstacles=list(set(no_obstacles))
graph_colors=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

for i in no_obstacles:
	fig1_x=[]
	fig1_y=[]
	fig2_y=[]
	for j in no_targets:
		fig1_x.append(j)
		fig1_y.append(d1[(j,i)])
		fig2_y.append(d2[(j,i)])
	plt.figure(1)
	plt.plot(fig1_x,fig1_y,graph_colors[i],label="Obstacles "+str(i))
	plt.figure(2)
	plt.plot(fig1_x,fig2_y,graph_colors[i],label="Obstacles "+str(i))

plt.figure(1)
plt.xlabel("Targets")
plt.ylabel("Observed Targets")
plt.title("Comparing number of Obstacles and Targets")
plt.legend()
plt.figure(2)
plt.xlabel("Targets")
plt.ylabel("Observed Targets")
plt.title("Comparing number of Obstacles and Targets for stratergy")
plt.legend()
plt.show()
