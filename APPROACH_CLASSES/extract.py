tdc=0
tc=0
to=0
with open('communicative-20threshold_results.txt') as fd:
	x=fd.readlines()
	for l in x:
		l=l.split(':')
		dc=l[-1]
		c=l[-2]
		o=l[-3]
		dc=int(dc.split('\n')[0])
		c=int(c.split(' ')[1])
		o=int(o.split(' ')[1])
		# print(dc,c,o)
		tdc+=dc
		tc+=c
		to+=o
print("Orig: ",to,"Centralized Comm: ",tc,"Decenteralized Comm: ",tdc)