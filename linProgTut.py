#	Project: Testing pulp library to solve linear programming problems
#	Author: Gran
#	Created at: 	2019-08-18	| 	Gran
#	Last edited:	2019-08-18	|	Gran

# I'm using the following tutorial to test this library
# https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99

# First we import all packages from pulp
from pulp import *


# Create  a linear problem method in PuLP
 prob = LpProblem("Simple Diet Problem", LpMinimize)

 # Read the first few rows dataset in a Pandas DataFrame
# Read only the nutrition info not the bounds/constraints
df = pd.read_excel("diet - medium.xls",nrows=17)

# Create a list of the food items
food_items = list(df['Foods'])

# Create a dictinary of costs for all food items
costs = dict(zip(food_items,df['Price/Serving']))

# Create a dictionary of calories for all food items
calories = dict(zip(food_items,df['Calories']))

# Create a dictionary of total fat for all food items
fat = dict(zip(food_items,df['Total_Fat (g)']))

# Create a dictionary of carbohydrates for all food items
carbs = dict(zip(food_items,df['Carbohydrates (g)']))

# Then, we create a dictionary of food items variables with lower bound =0 and category continuous i.e. the optimization solution can take any real-numbered value greater than zero.
food_vars = LpVariable.dicts("Food",food_items,lowBound=0,cat='Continuous')

#  start building the LP problem by adding the main objective function.
prob += lpSum([costs[i]*food_vars[i] for i in food_items])

# We further build on this by adding calories constraints,
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) >= 800.0
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) <= 1300.0

# Pile up adding nutrition constraints

# Fat
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) >= 20.0, "FatMinimum"
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) <= 50.0, "FatMaximum"

# Carbs
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) >= 130.0, "CarbsMinimum"
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) <= 200.0, "CarbsMaximum"

# Fiber
prob += lpSum([fiber[f] * food_vars[f] for f in food_items]) >= 60.0, "FiberMinimum"
prob += lpSum([fiber[f] * food_vars[f] for f in food_items]) <= 125.0, "FiberMaximum"

# Protein
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= 100.0, "ProteinMinimum"
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= 150.0, "ProteinMaximum"

prob.solve()

print("Status:", LpStatus[prob.status])

	for v in prob.variables():
	    if v.varValue>0:
	        print(v.name, "=", v.varValue)