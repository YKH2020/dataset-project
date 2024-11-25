# import required modules
from statsmodels.stats.power import TTestIndPower 

# factors for power analysis
alpha = 0.05
power = 0.8

# perform power analysis to find sample size 
# for given effect 
obj = TTestIndPower() 
n = obj.solve_power(effect_size=0.8, alpha=alpha, power=power, 
					ratio=1, alternative='two-sided') 

print('Sample size/Number needed in each group: {:.3f}'.format(n))