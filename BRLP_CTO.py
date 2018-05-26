from LP_CTO import LP_CTO
import numpy

def BRLP_CTO(reward,template_probability_distribution,E_min):
	beta_low=0
	beta_high=1
	beta_mid=(beta_low+beta_high)/2
	temp=LP_CTO(reward,beta_mid,template_probability_distribution)
	E=temp[0]
	alpha=temp[1]
	if E<E_min:
		while(abs(E-E_min)>0.05):
			if(E>E_min):
				beta_low=beta_mid
			else:
				bet_high=beta_mid
			beta_mid=(beta_low+beta_high)/2
			temp=LP_CTO(reward,beta_mid,tempelate_probability_distribution)
			E=temp[0]
			alpha=temp[1]
	return numpy.random.choice(range(1,len(alpha)+1),p=alpha)
