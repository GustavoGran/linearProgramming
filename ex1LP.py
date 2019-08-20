# 	Project: Using PuLP to solve exercise 1
#	Created at: 2019-08-18	|	Gran

from pulp import *
import pandas as pd

#	Defining some constants
numProd = 3
numMaq = 4
wkbFilePath = "/home/gran/Projects/linearProgramming"
wkbFileName = "ex1LP.xlsx"
wkbSheetName = "dataFrame"

# Defining some auxiliar functions
def listIndexesWithPattern (strPattern, strList):
	indexes = list()
	for i in range(len(strList)):
		if (strList[i].find(strPattern) != -1)	:
			indexes.append(strList[i])
	return indexes


#	Defining the problem
prob = LpProblem("Minimum Production Costs",LpMinimize)

#	Defining the Data Frame

dataFrame = pd.read_excel(wkbFilePath + "/" + wkbFileName,
						  sheet_name=wkbSheetName,
						  nrows = numProd*numMaq)


#	Creates a list with Products and machines combinations. 
#	These will be associated with our variables
prodMach = list(dataFrame['Combinação Máquina-Produto'])

# 	Create dictionaries for cost and production time for each Machine-Product combination
prodCost = dict(zip(prodMach, dataFrame['Custo Unitário']))
prodTime = dict(zip(prodMach, dataFrame['Hora-máquina unitário']))

#	Then, we create a dictionary of product items variables with lower bound =0
#	and category continuous i.e. the optimization solution can take any real-numbered 
#	value greater than zero.

prodVars = LpVariable.dicts("units",prodMach, lowBound=0, cat='Integer')

#p1Vars = LpVariable.dicts("units",p1Index, lowBound=0, upBound=4000, cat='Integer')
#p2Vars = LpVariable.dicts("units",p2Index, lowBound=0, upBound=5000, cat='Integer')
#p3Vars = LpVariable.dicts("units",p3Index, lowBound=0, upBound=5000, cat='Integer')

# 	Starts the LP modelling by adding the main objective function
# 	The AfflineExpression returns the sum of var[i]*scal[i] where the elements (variable, scalar)

prob += lpSum([prodVars[i] * prodCost[i] for i in prodMach]), "totProductionCost"

######## 	Add the number of units of each product constraints	###########

#	First constraint : Number of Products of type 1 = 4000
p1Index = listIndexesWithPattern(strPattern="P1", strList= prodMach)
prob += lpSum([ prodVars[i] for i in p1Index ]) == 4000, "totProd1"

# 	Sum of Products 2 = 5000
p2Index = listIndexesWithPattern(strPattern="P2", strList= prodMach)
prob += lpSum([ prodVars[i] for i in p2Index ]) == 5000, "totProd2"

#	Sum of Products 3 = 3000
p3Index = listIndexesWithPattern(strPattern="P3" , strList= prodMach)
prob += lpSum([ prodVars[i] for i in p3Index ]) == 3000, "totProd3"

########	Add the total production time by machine constraints	########

# 	Machine 1 <= 1500 h of total production time
m1Index = listIndexesWithPattern(strPattern="M1" , strList= prodMach)
prob += lpSum(prodVars[i] * prodTime[i] for i in m1Index) <= 1500, "totMach1"


# 	Machine 2 <= 1200 h of total production time
m2Index = listIndexesWithPattern(strPattern="M2" , strList= prodMach)
prob += lpSum(prodVars[i] * prodTime[i] for i in m2Index) <= 1200, "totMach2"

# 	Machine 3 <= 1500 h of total production time
m3Index = listIndexesWithPattern(strPattern="M3" , strList= prodMach)
prob += lpSum(prodVars[i] * prodTime[i] for i in m3Index) <= 1500, "totMach3"

# 	Machine 4 <= 2000 h of total production time
m4Index = listIndexesWithPattern(strPattern="M4" , strList= prodMach)
prob += lpSum(prodVars[i] * prodTime[i] for i in m4Index) <= 2000, "totMach4"

print("\n")

prob.solve()

print("\n",prob)

print("Status of the solution:", LpStatus[prob.status])

print("\nDistribution of each product type (P) units in Machines (M):")
for v in prob.variables():
   if v.varValue>0:
   		print("\n",v.name, "=",v.varValue)

obj = value(prob.objective)
print("\nThe total cost of the production is: ${}".format(round(obj,2)))