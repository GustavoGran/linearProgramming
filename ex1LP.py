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
prodMachComb = list(dataFrame['Combinação Máquina-Produto'])

# 	Create dictionaries for cost and production time for each Machine-Product combination
unitProdCost = dict(zip(prodMachComb, dataFrame['Custo Unitário']))
unitProdTime = dict(zip(prodMachComb, dataFrame['Hora-máquina unitário']))

#	Then, we create a dictionary of product items variables with lower bound =0
#	and category continuous i.e. the optimization solution can take any real-numbered 
#	value greater than zero.
prodUnitVars = LpVariable.dicts("Units",prodMachComb,
								lowBound=0,
								cat='Continuous')

# 	Starts the LP modelling by adding the main objective function
# 	The AfflineExpression returns the sum of var[i]*scal[i] where the elements (variable, scalar)

mainObjective = lpSum([(prodUnitVars[i],unitProdCost[i]) for i in prodMachComb])

#prob += lpSum(unitProdCost[i] * prodUnitVars[i] for i in prodMachComb)

# 	Add the number of units of each product constraints

#	First constraint : Number of Products of type 1 = 4000
# 	LpConstrainEq : "=" : 0
p1Index = listIndexesWithPattern(strPattern="P1", strList= prodMachComb)

constrP1 = LpConstraint(e = lpSum([ prodUnitVars[i] for i in p1Index ]),
						sense = 0, 
						name = "Product1Totals", 
						rhs = 4000)

# 	Sum of Products 2 = 5000
p2Index = listIndexesWithPattern(strPattern="P2", strList= prodMachComb)

constrP2 = LpConstraint(e = lpSum([ prodUnitVars[i] for i in p2Index ]),
						sense = 0,
						name = "Product2Totals",
						rhs = 5000)

#	Sum of Products 3 = 3000
p3Index = listIndexesWithPattern(strPattern="P3" , strList= prodMachComb)

constrP3 = LpConstraint(e = lpSum([ prodUnitVars[i] for i in p3Index ]),
						sense = 0,
						name = "Product3Totals",
						rhs = 3000)


#	Add the total production time by machine constraints

# LpConstraintLE : "<=" : -1
# LpConstraintGE : ">=" : 1
# 	Machine 1 <= 1500 h of total production time
m1Index = listIndexesWithPattern(strPattern="M1" , strList= prodMachComb)

constrM1 = LpConstraint(e = lpSum(prodUnitVars[i] * unitProdTime[i] for i in m1Index),
						sense = -1,
						name = "Machine1TotalHours",
						rhs = 1500)

# 	Machine 2 <= 1200 h of total production time
m2Index = listIndexesWithPattern(strPattern="M2" , strList= prodMachComb)

constrM2 = LpConstraint(e = lpSum(prodUnitVars[i] * unitProdTime[i] for i in m2Index),
						sense = -1,
						name = "Machine2TotalHours",
						rhs = 1200)

# 	Machine 3 <= 1500 h of total production time
m3Index = listIndexesWithPattern(strPattern="M3" , strList= prodMachComb)

constrM3 = LpConstraint(e = lpSum(prodUnitVars[i] * unitProdTime[i] for i in m3Index),
						sense = -1,
						name = "Machine3TotalHours",
						rhs = 1500)

# 	Machine 4 <= 2000 h of total production time
m4Index = listIndexesWithPattern(strPattern="M4" , strList= prodMachComb)

constrM4 = LpConstraint(e = lpSum(prodUnitVars[i] * unitProdTime[i] for i in m4Index),
						sense = -1,
						name = "Machine4TotalHours",
						rhs = 2000)

prob += mainObjective 
prob += constrP1 + constrP2 + constrP3 
prob += constrM1 + constrM2 + constrM3 + constrM4
print("\n\n")
print("Função Objetivo: ", mainObjective,"\n")
print("Produto P1: ",constrP1,"\n")
print("Produto P2: ",constrP2,"\n")
print("Produto P3: ",constrP3,"\n")
print("Máquina M1: ",constrM1,"\n")
print("Máquina M2: ",constrM2,"\n")
print("Máquina M3: ",constrM3,"\n")
print("Máquina M4: ",constrM4,"\n")
print("\n")

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
   if v.varValue>0:
   		print("\n",v.name, "=",v.varValue)

obj = value(prob.objective)
print("\nThe total cost of the production is: ${}".format(round(obj,2)))