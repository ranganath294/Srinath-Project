import pandas as pd
import numpy as np
import yaml
from yaml.loader import SafeLoader
import os

from ga_freq import cal_pop_fitness,select_mating_pool,crossover,mutation
from overallcost import overallcost
from freq_range import freq_range
from Initial_frequency import ini_freq

with open('parameters.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)

globals().update(data)

dob= seatcap*min_c_lvl
cob= int (seatcap*max_c_lvl)

#FREQUENCY RANGE CALCULATIONS
#---------------------------------

#INPUT FILES

passengerarrivalDN = pd.read_csv(r'D:\Function files\Input files\Passenger_arrival_DN.csv').set_index('Passenger arrival')
distanceDN= pd.read_csv(r'D:\Function files\Input files\distanceDN.csv').set_index('Distance')
alightrateDN = pd.read_csv(r"D:\Function files\od_output\alighting_rateDN.csv").set_index('Alighting Rate')

passengerarrivalUP = pd.read_csv(r'D:\Function files\Input files\Passenger_arrival_UP.csv').set_index('Passenger arrival')
distanceUP= pd.read_csv(r'D:\Function files\Input files\distanceUP.csv').set_index('Distance')
alightrateUP = pd.read_csv(r"D:\Function files\od_output\alighting_rateUP.csv").set_index('Alighting Rate')
timeperiod = pd.read_csv(r'D:\Function files\Input files\tmeperiodDN.csv', header=0)
#---------------------------------------------------------------------------------------------------
#2. Initial frequency setting using ride check and point check
#---------------------------------------------------------------------------------------------------


directionDN= 'Dowm direction'
directionUP= 'Up direction'
print('-------------------------------------------------------------------------')
print('\n Initial frequency setting using ride check ')
print('-------------------------------------------------------------------------')
frequencyDN =ini_freq(passengerarrivalDN,alightrateDN,distanceDN,cob,dob,hrinperiod,frequencydefault,directionDN)
frequencyUP =ini_freq(passengerarrivalUP,alightrateUP,distanceUP,cob,dob,hrinperiod,frequencydefault,directionUP)


frequencyDN=frequencyDN.reset_index(drop=True)
frequencyUP=frequencyUP.reset_index(drop=True)

frequencyDN.to_csv(r'D:\Function files\Output GA\IniFrequencyDN.csv')
frequencyUP.to_csv(r'D:\Function files\Output GA\IniFrequencyUP.csv')

ppse='Initial frequency'
print('Full day simulations of bus operations using initial frequency and cost calculations:\n')
overall_initial = overallcost(frequencyDN,frequencyUP,ppse)
print('\n overall cost for full day operations using initial frequency              :₹',overall_initial)



#---------------------------------------------------------------------------------------------------
#2. FREQUENCY RANGE SETTING
#---------------------------------------------------------------------------------------------------
frequencyDN_min, frequencyDN_max= freq_range(passengerarrivalDN,alightrateDN,distanceDN,cob,dob,hrinperiod,frequencydefault)
frequencyUP_min, frequencyUP_max= freq_range (passengerarrivalUP,alightrateUP,distanceUP,cob,dob,hrinperiod,frequencydefault)

frequencyDN= pd.DataFrame({'Time Period':frequencyDN_min.index, 'Frequency Min':frequencyDN_min, 'Frequency Max':frequencyDN_max}).set_index('Time Period')
frequencyUP= pd.DataFrame({'Time Period':frequencyUP_min.index, 'Frequency Min':frequencyUP_min, 'Frequency Max':frequencyUP_max}).set_index('Time Period')

frequencycomb=pd.concat([frequencyDN, frequencyUP],axis=0)
frequencycomb.reset_index(inplace=True)
frequencycomb.drop(columns=['Time Period'], inplace=True)
print('FREQUENCY RANGE: \n')
print(frequencycomb)

frequencycomb.to_csv(r'D:\Function files\Output GA\frequency_range.csv', index=False)


#---------------------------------------------------------------------------------------------------
# 3.0   O P T I M I Z A T I O N

#-------------------------------------------------------------------------------------------------------------------------------------------------------
# 4.1 GENETIC ALGORITHM MODE
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#length of chromosome= number of decision variables = service hours X 2
num_weights = ser_period*2
#number of solutions per population

num_parents_mating =int(sol_per_pop/2)       #sol_per_pop/2

print("\n---------------------------------------------------------------------------\nInitiating Genetic Algorithm for", A ,"to", B ,"to Optimise Overall Cost(₹)\n---------------------------------------------------------------------------")

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop (chromosome) where each chromosome has num_weights (genes).
#Creating the initial population.
new_populationDN = np.random.randint(low=frequencycomb.iloc[:,0], high=frequencycomb.iloc[:,1]+1, size=pop_size)        ## NEED TO HAVE A SYNTAX THAT GENERATE MIN FREQUENCY AND MAX FREQUENCY INSTEAD LOW AND HIGH MANUAL INPUT

print("\nInitial population  : ", new_populationDN)
# Measuring the fitness of each chromosome in the population.
fitness = cal_pop_fitness(new_populationDN,sol_per_pop)
print('cost for initial pop', fitness)

for generation in range(num_generations):
    print("\nGeneration : ", generation)
    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_populationDN, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover,frequencycomb)

    # Creating the new population based on the parents and offspring.
    new_populationDN[0:parents.shape[0], :] = parents
    new_populationDN[parents.shape[0]:, :] = offspring_mutation
    # The best result in the current iteration.
    fitness = cal_pop_fitness(new_populationDN, sol_per_pop)

    print('Cost of new population:', generation,'Generation',fitness )



print('Final frequency population :', new_populationDN)
print('Fitness of populationm',fitness)

#finding out the frequency sequence with minimum cost in the final population
final_pop=pd.DataFrame(new_populationDN)
final_pop['Overallcost']= fitness
min_cost_idx=final_pop[['Overallcost']].idxmin()
min_cost_idx=min_cost_idx.iloc[0]
FrequencyDNO= final_pop.iloc[min_cost_idx,0:16]
FrequencyUPO= final_pop.iloc[min_cost_idx,16:32]
optimised_cost=final_pop.iloc[min_cost_idx,32]




frequency_set=pd.DataFrame()

frequency_set['Time Period from'] = timeperiod ['Time']
frequency_set['Time Period from']=frequency_set['Time Period from']/100

frequency_set['Optimised Frequency down']= FrequencyDNO.values
frequency_set['Optimised headway down']= 60/frequency_set['Optimised Frequency down']
frequency_set['Optimised Frequency up']= FrequencyUPO.values
frequency_set['Optimised headway up']= 60/frequency_set['Optimised Frequency up']
print('\n ------------------------------------------------------------------')
print('Optimisation results:')
print('\n ------------------------------------------------------------------')
print('Optimised frequency for full day operations:\n',frequency_set.to_string())
print('Optimised cost=', optimised_cost)
#exporting output files
path= r'D:\Function files\Output GA'
isExist = os.path.exists(path)

if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)


final_pop.to_csv(r'D:\Function files\Output GA\Final_pop_fitness.csv')
frequency_set.to_csv(r'D:\Function files\Output GA\Optimised frequency set.csv', index=False)
FrequencyDNO.to_csv(r'D:\Function files\Output GA\OpFrequencyDN.csv', index=False)
FrequencyUPO.to_csv(r'D:\Function files\Output GA\OpFrequencyUP.csv', index=False)

frequencyDN=FrequencyDNO.to_numpy()
frequencyUP=FrequencyUPO.to_numpy()
ppse='optmised frequency'
overall_opt= overallcost(frequencyDN,frequencyUP,ppse)
print('\n overall cost for the operations using optimised frequency              :₹',overall_opt)
print('\n overall cost for the operations using initial frequency              :₹',overall_initial)
cost_reduction= 100-(overall_opt/overall_initial*100)
print('\n cost of reduction using optimisation:  ', cost_reduction,'%')
path='D:\Function files\Input_files_holding'
print('all the simulated results related to the full day bus operations using the optimised frequency is in the following directory:\n', path)




print ("End!!!")


