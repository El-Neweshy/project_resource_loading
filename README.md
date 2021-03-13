Resource Loading and Levelling Suggested Algorithm

Aim:
The aim of this algorithm is to receive the activities data and the maximum allowed duration for the project and to calculate the most optimized resource allocation considering two different ways of optimization.
a-	Checking the least duration available for the project to be executed then considering the best scenario for distributing the resources over this duration.
b-	Checking the best distribution for the resources for the project, without exceeding the maximum allowed duration to avoid any possible resource overloading.

Inputs:
1-	All activities with the following criteria for each activity:
a.	Name
b.	Duration (number of weeks)
c.	Number of resources per week
d.	Predecessor(s) if there
e.	Successor(s) if there
f.	Can the activity be splitted?
2-	The maximum allowed duration (in weeks) for the project.

Algorithm:
We will consider, for now, two resource leveling techniques, resources splitting and resource delaying through the following:
1-	If an activity can be splitted we will divide the activity into small virtual activities (e.g., If we have an activity “A” that should take 5 weeks and it can be splitted then the algorithm will deal with it as 5 consecutive activities “A1”, “A2”, “A3”, “A4”, and “A5”).
2-	The Algorithm should consider all available activities shifts/delays.
3-	Using delaying and splitting for all activities, the algorithm should consider all possible combinations for resource levelling to generate the resources allocation for the whole project.

Outputs:
The algorithm should first check if the “maximum allowed project duration” given is achievable or not? (e.g., if the maximum allowed project duration is given to be 14 weeks and the project can’t be executed by any means in less than 15 weeks, the algorithm should return that the minimum available duration for the project should be 14 weeks).
If the maximum allowed project duration is reasonable then the output will be a report and charts for two different following outcomes:
a-	The resource allocation for minimum project time. 
E.g., if we have scenario “1” that will take 15 weeks and scenario “2” that will take 17 weeks, we will choose scenario “1”.
If there are more than one scenario that can generate the same project duration (15 weeks for example), the most normalized resource allocation will be chosen according to the maximum number of resources in any of the project weeks.
E.g., if we have two scenarios that will take the same duration (15 weeks) and the first scenario will give resource allocation [12, 12, 12, 12, 16, 16, 11, 11, 10, 10, 10, 4, 4, 4, 4] and the second one will be [12, 12, 12, 12, 10, 10, 12, 12, 9, 9, 10, 10, 10, 4, 4], we will choose the second scenario which has less “maximum number of resources in any week” as the maximum in the first scenario is 16 and in the second scenario is 12. The aim here is to choose the scenario with the least overloading problems but in the most compact project duration available.
b-	The second outcome should be the scenario with the least overloading problems without considering the total project time (as long as we are not exceeding the maximum allowed project duration given).
E.g., If we have two scenarios “1” and “2” where scenario “1” will need a duration of 17 weeks and the maximum resources needed in any week is 10 and the second scenario with duration 15 weeks only but with a maximum resources needed in any week equals 12, then we still will go with scenario 1.
If two or more scenarios are same optimized from the resource overloading point of view (having the same value for maximum number of resources in any week), we will currently choose any of them as I am still thinking how to choose one (can we think about considering the standard diviation?).
We aim in this outcome to avoid the resource overloading in the first place as long as we are not exceeding the maximum allowed project duration which is an input to the algorithm.
Notes:
a-	The code that will execute the above algorithm will be in Python and written in OOP (Object Oriented Programming).
b-	The code should create a data log file with all possible scenarios (that do not exceed the maximum allowed duration) whether they are optimized or not optimized.
c-	In resource leveling, I only considered resource delaying and resource splitting techniques but other techniques like resource crashing or resource extending can be applied if required.
