import sys
import copy

intitalVal=None
DBtransactions=[]
x=None
diskVars={}
ramVars={}
tempVars={}
class Transaction(object):
	"""docstring for Transaction"""
	




def readInput(filename):
	global ramVars
	#read all instructions
	instructions=open(filename, "r").readlines()
	
	# read initial values of disk variable and create dict
	intitalVals=instructions[0].split(" ")
	j=0
	while j<len(intitalVals):
		diskVars[intitalVals[j]]=int(intitalVals[j+1])
		j+=2
	
	# create ram varibles intialized with none
	ramVars=copy.deepcopy(diskVars)
	for x in ramVars.keys():
		ramVars[x]=None


	# create transtion objects and set
	# n=total instructions
	# name=name of transaction
	# actions= All of its instructions
	# current= pointed to current instruction to execute

	t=Transaction()
	count=2
	for i in range(count,len(instructions)):
		if instructions[i]=="\n" or i==len(instructions)-1:
			if i==len(instructions)-1:
				i+=1
			
			t.actions=[x.replace("\n","") for x in instructions[count:i]]
			t.name, t.n=t.actions[0].split(" ")
			t.current=0
			DBtransactions.append(t)
			t=Transaction()
			count=i+1
	
def printVars():
	printNtg=True
	for var in sorted(ramVars.keys()):
		if ramVars[var]!=None:
			print(var,ramVars[var],end=" ")
			printNtg=False
	print()
	for var in sorted(diskVars.keys()):
		print(var,diskVars[var],end=" ")
	print()

def executeInst(instruction,trans):
	if "READ" in instruction:
		# print("Read")
		var,temp=instruction[5:-1].split(",")
		var,temp=var.strip(),temp.strip()
		if ramVars[var]==None:
			ramVars[var]=diskVars[var]
		tempVars[temp]=ramVars[var]

	elif "WRITE" in instruction:
		# print("Write")
		var,temp=instruction[6:-1].split(",")
		print("<%s, %s, %d>"%(trans.name,var,ramVars[var]))
		var,temp=var.strip(),temp.strip()
		ramVars[var]=tempVars[temp]
		printVars()
		
	elif "OUTPUT" in instruction:
		# print("Output")
		var=instruction[7:-1]
		diskVars[var]=ramVars[var]
		# printVars()

	if ":=" in instruction:
		destTemp,operation=instruction.split(":=")
		destTemp,operation=destTemp.strip(),operation.strip()
		if "-" in operation:
			sourceTemp,number=operation.split("-")
			sourceTemp,number=sourceTemp.strip(),int(number.strip())
			tempVars[destTemp]=tempVars[sourceTemp]-number
		if "+" in operation:
			sourceTemp,number=operation.split("+")
			sourceTemp,number=sourceTemp.strip(),int(number.strip())
			tempVars[destTemp]=tempVars[sourceTemp]+number
		if "*" in operation:
			sourceTemp,number=operation.split("*")
			sourceTemp,number=sourceTemp.strip(),int(number.strip())
			tempVars[destTemp]=tempVars[sourceTemp]*number
		if "/" in operation:
			sourceTemp,number=operation.split("/")
			sourceTemp,number=sourceTemp.strip(),int(number.strip())
			tempVars[destTemp]=tempVars[sourceTemp]/number


def createUndoLog():
	totalInst=0
	count=0
	for trans in DBtransactions:
		totalInst+=int(trans.n)
	while True:
		if count==totalInst:
			break
		for trans in DBtransactions:
			if trans.current==0:
				print("<START %s>"%(trans.name))
				printVars()
				trans.current=1

			for i in range(trans.current,trans.current+x):
				if i==len(trans.actions):
					break
				executeInst(trans.actions[i],trans)
				if i==int(trans.n):
					print("<COMMIT %s>"%(trans.name))
					printVars()
				count+=1
			trans.current=trans.current+x


if __name__ == "__main__":
	if len(sys.argv)!=3:
		print("Invalid parameter: pass filename,x")
		exit(0)
	x=int(sys.argv[2])
	readInput(sys.argv[1])
	createUndoLog()

	
