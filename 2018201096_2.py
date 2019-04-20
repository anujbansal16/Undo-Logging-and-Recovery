import sys

diskVars={}
transactions={}
instructions=[]

def readInput(filename):
	#read all instructions
	instructions=open(filename, "r").readlines()	
	# read initial values of disk variable and create dict
	intitalVals=instructions[0].split(" ")
	j=0
	while j<len(intitalVals):
		diskVars[intitalVals[j]]=int(intitalVals[j+1])
		j+=2

	instructions=instructions[1:]
	instructions=instructions[::-1]
	instructions=[x.replace("\n","")[1:-1].strip() for x in instructions if x!="\n"]
	return instructions


def makeChanges(trans,var,val):
	#change values if transaction is incomplete
	if trans in transactions.keys():
		if transactions[trans]==True:
			return
	transactions[trans]=False
	diskVars[var]=val
	print(diskVars)

def handleIncomActive(incmTrans,index):
	print("handleIncomActive")
	print(incmTrans)
	totalInc=len(incmTrans)
	for i in range(index,len(instructions)):
		inst=instructions[i]
		if totalInc==0:
			break
		if "START" in inst:
			cmd,trans=inst.split(" ")
			cmd,trans=cmd.strip(),trans.strip()
			print(cmd,trans)
			if transactions[trans]==False:
				totalInc-=1
				transactions[trans]=True
		else:
			trans,var,val=inst.split(",")
			trans,var,val=trans.strip(),var.strip(),val.strip()
			print(trans,var,val)
			makeChanges(trans,var,val)

def recover():
	print(instructions)
	endCheckPt=False
	for index,inst in enumerate(instructions):
		if "END CKPT" in inst:
			endCheckPt=True
		elif "START CKPT" in inst:
			if endCheckPt:
				#scaned all incomplete transactions b/w start and end chkpt
				print("Im done")
				print(diskVars)
				break
			else:
				print("Need to search active list")
				activeList=inst.split("(")[-1][:-1]
				activeTransactions=activeList.split(",")
				print(activeTransactions)
				incmTrans=[]
				print(transactions)
				for t in activeTransactions:
					t=t.strip()
					if t in transactions.keys():
						if transactions[t]==False:
							incmTrans.append(t)
					else:
						transactions[t]=False
						incmTrans.append(t)
				handleIncomActive(incmTrans,index+1)
				print("ads", diskVars)
				break


				# add incomplete active transactions
		elif "COMMIT" in inst:
			cmd,trans=inst.split(" ")
			cmd,trans=cmd.strip(),trans.strip()
			print(cmd,trans)
			transactions[trans]=True
		elif "START" in inst:
			cmd,trans=inst.split(" ")
			cmd,trans=cmd.strip(),trans.strip()
			print(cmd,trans)
			transactions[trans]=True
		else:
			trans,var,val=inst.split(",")
			trans,var,val=trans.strip(),var.strip(),val.strip()
			print(trans,var,val)
			makeChanges(trans,var,val)


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print("Invalid parameter: pass filename")
		exit(0)
	instructions=readInput(sys.argv[1])
	recover()