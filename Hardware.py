'''
Summary
Library of Hardware Functions made by ME
'''

# Imports
import re
import random

# Util Functions
def GetFloatInput():
    return float(input("Enter Float Value: "))

def GetIEEEInput():
    ieeeform = IEEEFormat()
    ieeeform.Sign = input("Enter Sign: ")
    ieeeform.Exponent = input("Enter Exponent: ")
    ieeeform.Mantissa = input("Enter Mantissa: ")
    return ieeeform

def SplitFloat(floatval):
    spl = str(floatval).split('.')
    return [int(spl[0]), int(spl[1])]

def Int2Bin(intval):
    intval_int = int(intval)
    if (intval_int > 1):
        return str((Int2Bin(str(int(intval_int/2)))) + str(intval_int%2))
    else:
        return str(intval)

def Bin2Int(binval):
    decval = 0
    for i in range(len(str(binval))):
        if binval[-1] == '1':
            decval += int(2**i)
        binval = binval[:-1]
    return decval

def DecimalInt2Bin(decimalval, nbits=1):
    binval = ''

    nearestpower_10 = len(str(decimalval))
    #print("dec2bin", decimalval, nearestpower_10)
    for i in range(nbits):
        decimalval *= 2
        if (decimalval >= 10**nearestpower_10):
            binval = binval + '1'
            decimalval -= 10**nearestpower_10
            #print("iterif", binval, decimalval)
        else:
            binval = binval + '0'
            #print("iterelse", binval, decimalval)
    
    return binval

def Bin2DecimalInt(binv):
    decval = 0.0
    for i in range(len(binv)):
        decval += ((1/2)**(i+1)) * int(binv[0])
        binv = binv[1:]
    return decval

# IEEE Classes
class IEEEFormat:
    def __init__(self):
        self.Sign = ''
        self.Exponent = ''
        self.Mantissa = ''

class IEEEFloatingPrecision:
    Bits = {}

    # Half Precision
    # Sign - 1 Bit
    # Exponent - 5 Bits
    # Mantissa - 10 Bits
    Bits['Half'] = [1, 5, 10]

# Main Class
class IEEEConverter:
    def IntFloat2BinFloat(self, floatval, mantissaBits=10):
        # Split the float value
        splitfloat = SplitFloat(floatval)
        # Convert to Binary
        wholepart = int(Int2Bin(str(splitfloat[0])))
        mantissaBits -= len(str(wholepart))
        if mantissaBits > 0:
            decimalpart = DecimalInt2Bin(splitfloat[1], mantissaBits)
        else:
            decimalpart = DecimalInt2Bin(splitfloat[1])

        return [str(wholepart), decimalpart]

    def Float2IEEE(self, floatval, precision='Half'):
        ieeefloat = IEEEFormat()
        # Sign
        if (floatval <  0):
            ieeefloat.Sign = '1'
            floatval = -floatval
        else:
            ieeefloat.Sign = '0'

        exp_offset = 0

        # If no itself is like 0.002 - i.e. whiole part is 0, make exponent offset
        if (floatval < 1.0):
            while(floatval < 1.0):
                exp_offset += 1
                floatval *= 2

        BinFloat = self.IntFloat2BinFloat(floatval, IEEEFloatingPrecision.Bits[precision][2] + 1)
        joinedVal = BinFloat[0] + BinFloat[1]

        # Mantissa
        ieeefloat.Mantissa = joinedVal[1:] # Remove implicit 1.

        # Exponent
        expo = str(Int2Bin(str(len(BinFloat[0]) - 1 + 2**(IEEEFloatingPrecision.Bits[precision][1] - 1) - 1 - exp_offset))) # Offset
        if (len(expo) > IEEEFloatingPrecision.Bits[precision][1]):
            expo = expo[(len(expo) - IEEEFloatingPrecision.Bits[precision][1]):]
        
        ieeefloat.Exponent = expo

        return ieeefloat
    
    def IEEE2Float(self, ieeefloat, precision='Half'):
        # Sign
        Sign = 1.0
        if (ieeefloat.Sign ==  '1'):
            Sign = -1.0
        # Exponent
        exp = int(Bin2Int(str(int(ieeefloat.Exponent))) - (2**(IEEEFloatingPrecision.Bits[precision][1] - 1) - 1))
        fstr = ''
        if exp >= 0:
            fstr = ('1' + ieeefloat.Mantissa)[:exp+1] + '.' + ('1' + ieeefloat.Mantissa)[exp+1:]
        else:
            offset = '0' * int(-1*(exp) - 1)
            fstr = '0' + '.' + offset +  ('1' + ieeefloat.Mantissa)
        splitVals = fstr.split('.')
        floatval = float(Sign * Bin2Int(str(int(splitVals[0])))) + Sign * Bin2DecimalInt(splitVals[1])
        return floatval

# Driver Code
def Convert2IEEEDriver():
    e = IEEEConverter()

    choice = input("Enter choice: ")

    if choice in ['', 'f']:
        # Float to IEEE
        iefloat = e.Float2IEEE(GetFloatInput(), 'Half')
        print("Sign:", iefloat.Sign)
        print("Exponent:", iefloat.Exponent, Bin2Int(iefloat.Exponent))
        print("Mantissa:", iefloat.Mantissa, Bin2Int(iefloat.Mantissa))
        originalValue = e.IEEE2Float(iefloat, 'Half')
        print('OG', originalValue)

    elif choice in ['d2b']:
        # Dec to Binary
        decval = input("Enter Integer Value: ")
        print("Bin: ", Int2Bin(decval))

    elif choice in ['b2d']:
        # Binary to Dec
        binval = input("Enter Binary Value: ")
        print("Int: ", Bin2Int(binval))

    else: 
        # IEEE to Float
        floatv = e.IEEE2Float(GetIEEEInput(), 'Half')
        print("Float Value:", floatv)
        originalIEEE = e.Float2IEEE(floatv, 'Half')
        print("Sign:", originalIEEE.Sign)
        print("Exponent:", originalIEEE.Exponent, Bin2Int(originalIEEE.Exponent))
        print("Mantissa:", originalIEEE.Mantissa, Bin2Int(originalIEEE.Mantissa))

# Activity Factor Computer
class Gate:
	def __init__(self, gate, name, inp, out):
		self.gate = gate
		self.name = name
		self.inp = inp
		self.out = out

class Wire:
	def __init__(self, name, w_type, inp_gates, out_gates, activityFactor_Prob):
		self.name = name
		self.w_type = w_type
		self.inp_gates = inp_gates
		self.out_gates = out_gates
		self.activityFactor_Prob = activityFactor_Prob

def ActivityFactorComputerMain():
    display_Recursions = False

    display_wires = True
    display_gates = False

    fields = ['Verilog Code Location (with filename and filepath)']

    inputfileloc = ''# 'C:\GitHub Codes and Projects\VLSI Files\VLSI_Files\ActivityFactorComputer\TestCodes\\'
    modulename = ''

    gates_names = ['nand', 'nor', 'and', 'or', 'xor', 'not', 'buf']
    alternate_gates_names = {}
    alternate_gates_names['nand'] = ['nand', 'NA', 'NAND']
    alternate_gates_names['nor'] = ['nor', 'NO', 'NOR']
    alternate_gates_names['and'] = ['and', 'AND']
    alternate_gates_names['or'] = ['or', 'OR']
    alternate_gates_names['xor'] = ['xor', 'XOR']
    alternate_gates_names['not'] = ['not', 'NOT', 'IN']
    alternate_gates_names['buf'] = ['buf', 'BU']

    inputs_names = []
    outputs_names = []
    wires_names = []

    gates = []
    wires = []

    n_inputs = 0
    n_outputs = 0
    n_wires = 0

    fetch_inputs_act(fields)

def fetch_inputs_act(fields):
	global inputfileloc

	input_dict = {}

	for field in fields:
		text  = input(field + ": ")
		input_dict[field] = text
	if (not (input_dict == {})):
		print(input_dict)

	if input_dict != {} and input_dict["Verilog Code Location (with filename and filepath)"] != '':
		inputfileloc += input_dict["Verilog Code Location (with filename and filepath)"]

	VerilogParser(filepath=inputfileloc)

#--2--
def FileContents(filepath):
	return open(filepath, "r").read()

def RemoveCommentsAndEmptyLines(contents):
	new_contents = ""
	commented_block = False
	for line in contents:
		if (re.search('^\/\*.*', line)):
			commented_block = True
		if (re.search('^\*\/.*', line)):
			commented_block = False
		if (not (line == "") and not re.search('^\/\/.*', line) and not commented_block):
			if  re.search('.*\/\/.*', line):
				uncommented = re.findall('^(.*)\/\/.*', line)[0]
				if (not (uncommented == "")):
					new_contents += uncommented.strip()
			else:
				new_contents += line.strip()
			
	return new_contents

def GetGateNames(gate_type):
	global gates_names
	global alternate_gates_names
	for gn in gates_names:
		for gt in alternate_gates_names[gn]:
			if re.search('^' + gt + '.*', gate_type):
				return gt
	return 'buf'

#--3--
def VerilogParser(filepath):
	global modulename
	global inputs_names
	global outputs_names
	global wires_names
	global wires
	global n_inputs
	global n_outputs
	global n_wires

	contents = FileContents(filepath)

	contents = RemoveCommentsAndEmptyLines(contents.split('\n'))

	# print(contents)

	contents = contents.split(';')

	#print("; CONTENTS:\n", contents)
	# for iii in contents:
	# 	print(iii)

	for line in contents:
		if (line == ""):
			continue
		# print("Line: ", line)
		# Get Module Name
		if re.search('^\s*module\s+', line):
			modulename = re.findall('^\s*module\s+(.*)\(', line)[0].strip()
		# Get Module Name

		# Get Inputs
		if re.search('^\s*input\s+', line):
			inputs_names = re.findall('^\s*input\s+(.*)', line)[0].strip().split(',')
			InitWires(inputs_names, 'i')
			n_inputs = len(inputs_names)
		# Get Inputs

		# Get Outputs
		if re.search('^\s*output\s+', line):
			outputs_names = re.findall('^\s*output\s+(.*)', line)[0].strip().split(',')
			InitWires(outputs_names, 'o')
			n_outputs = len(outputs_names)
		# Get Outputs

		# Get Wires
		if re.search('^\s*wire\s+', line):
			wires_names = re.findall('^\s*wire\s+(.*)', line)[0].strip().split(',')
			InitWires(wires_names, 'w')
			n_wires = len(wires_names)
		# Get Wires

		# Parse Connections
		FindConnection(line)
		# Parse Connections

	# Compute Activity Factor_Probs
	global display_Recursions
	for o in wires:
		if (o.w_type == 'o'):
			if (display_Recursions):
				print("---------------------------S ", o.name, "----------------------------------\n")
			Recursive_Compute(o, 0)
			if (display_Recursions):
				print("\n---------------------------E ", o.name, "----------------------------------\n\n\n")
	# Compute Activity Factor_Probs

	# Print
	if (display_gates):
		PrintGates()
	if (display_wires):
		PrintWires()
	# Print

	# Print Output Activity Factor_Probs
	print("--------------Output Activity Factor_Probs----------------")
	for o in wires:
		if (o.w_type == 'o'):
			print("Output Name: ", o.name, " - Prob: ", o.activityFactor_Prob, " - Activity Factor: ", o.activityFactor_Prob*(1-o.activityFactor_Prob))
	print("-----------------------------------------------------")
	# Print Output Activity Factor_Probs


def InitWires(wires_names, w_type):
	global wires
	for w in wires_names:
		if (w_type == 'i'):
			wires.append(Wire(w.strip(), w_type, [], [], 0.5))
		else:
			wires.append(Wire(w.strip(), w_type, [], [], -1.0))


def FindConnection(line):
	global gates_names
	global gates
	global wires
	global alternate_gates_names

	# print(line)
	
	for gn_main in gates_names:
		for gn in alternate_gates_names[gn_main]:
			if re.search('^\s*' + gn + '\s+', line):										# Eg. nand NAND2_1 (N10, N1, N3)
				all_text = re.findall('^\s*' + gn + '\s+(.*)', line)[0].strip()				# NAND2_1 (N10, N1, N3)
				instance_name = re.findall('(.*)\s*\(', all_text)[0].strip()				# NAND2_1
				all_wires = re.findall('.*\s*\((.*)\)', all_text)[0].strip().split(',')		# [N10, N1, N3]
				# As only 1 output which is at last index of all_wires
				inp_names = all_wires[1:]													# [N10, N1]
				out_names = [all_wires[0].strip()]											# [N3]
				inp = []
				out = []

				index = 0
				for w in wires:
					for i in inp_names:
						if (w.name == i.strip()):
							inp.append(w)

					for o in out_names:
						if (w.name == o.strip()):
							out.append(w)

					index += 1
				
				new_gate = Gate(GetGateNames(gn), instance_name, inp, out)
				gates.append(new_gate)

				index = 0
				for w in wires:
					for i in inp_names:
						if (w.name == i.strip()):
							wires[index].out_gates.append(new_gate)
							# print("COMPARE_TRUE: |" + w.name + "| and |" + i.strip() + "|")
						# else :
						# 	print("COMPARE: |" + w.name + "| and |" + i.strip() + "|")
					for o in out_names:
						if (w.name == o.strip()):
							wires[index].inp_gates.append(new_gate)
							# print("COMPARE_TRUE: |" + w.name + "| and |" + o.strip() + "|")
						# else :
						# 	print("COMPARE: |" + w.name + "| and |" + o.strip() + "|")

					index += 1

				return

def PrintWires():
	global wires
	index = 0
	for w in wires:
		# print("Wire ", index, ": ", w.name, " - ", w.w_type, " - i: ", len(w.inp_gates), " - o: ", len(w.out_gates), " - actFactor_Prob: ", w.activityFactor_Prob)
		print("Wire ", index, ": ", w.name, " - ", w.w_type, " - actFactor_Prob: ", w.activityFactor_Prob, " - Activity Factor: ", (w.activityFactor_Prob*(1-w.activityFactor_Prob)))

		index += 1

def PrintGates():
	global gates
	index = 0
	for g in gates:
		print("Gate ", index, ": ", g.gate, " - ", g.name, " - i: ", len(g.inp), " - o: ", len(g.out))

		index += 1

def ComputeGateActivityFactor_Prob(gate):
	actFactor_Prob = 1

	if (gate.gate == 'and'):
		for i in gate.inp:
			actFactor_Prob *= i.activityFactor_Prob
	elif (gate.gate == 'buf'):
		actFactor_Prob = gate.inp[0].activityFactor_Prob
	elif (gate.gate == 'not'):
		actFactor_Prob = 1 - gate.inp[0].activityFactor_Prob
	elif (gate.gate == 'or'):
		for i in gate.inp:
			actFactor_Prob *= (1 - i.activityFactor_Prob)
		actFactor_Prob = 1 - actFactor_Prob
	elif (gate.gate == 'nand'):
		for i in gate.inp:
			actFactor_Prob *= i.activityFactor_Prob
		actFactor_Prob = 1 - actFactor_Prob
	elif (gate.gate == 'nor'):
		for i in gate.inp:
			actFactor_Prob *= (1 - i.activityFactor_Prob)
	elif (gate.gate == 'xor'):
		n_w = len(gate.inp)
		actFactor_Prob = (gate.inp[0].activityFactor_Prob * (1 - gate.inp[1].activityFactor_Prob)) + ((1 - gate.inp[0].activityFactor_Prob) * gate.inp[1].activityFactor_Prob)
		for i in range(2, n_w):
			old_act = actFactor_Prob
			actFactor_Prob = (gate.inp[i].activityFactor_Prob * (1 - actFactor_Prob)) + ((1 - gate.inp[i].activityFactor_Prob) * actFactor_Prob)
		
	return actFactor_Prob


def Recursive_Compute(wire, depth):
	global wires
	global gates
	global display_Recursions

	if (display_Recursions):
		print("---------S depth = ", depth, "----------------")

	index = 0

	it_index = 0
	for w in wires:
		if (w.name == wire.name):
			index = it_index
		it_index += 1

	if (display_Recursions):
		print("Recursion: Current Wire ", index, ": ", wire.name, " - ", wire.w_type, " - i: ", len(wire.inp_gates), " - o: ", len(wire.out_gates), " - actFactor_Prob: ", wire.activityFactor_Prob)

	if (len(wires[index].inp_gates) > 0):
		connected_gate = wires[index].inp_gates[0]
		if (display_Recursions):
			print("Recursive Gate: ", connected_gate.gate, " - ", connected_gate.name)
		
		for i in connected_gate.inp:
			if (i.activityFactor_Prob == -1.0):
				if (display_Recursions):
					print("Recursive Wire: ", i.name, " - ", i.activityFactor_Prob)
				Recursive_Compute(i, depth+1)
			if (display_Recursions):
				print("Recursion Wire Done: ", i.name, " - ", i.activityFactor_Prob)
		wires[index].activityFactor_Prob = ComputeGateActivityFactor_Prob(connected_gate)
	
	if (display_Recursions):
		print("---------E depth = ", depth, "----------------")

# Test Bench Generator
def TestBenchGenerator():
    first_input = True

    fields = 'Verilog Code Location (with filename)', 'Verilog Module Name', 'Destination Folder', 'Clock Delay', 'Time Delay', 'No of Test Cases'

    inputfileloc = ''
    modulename = ''
    destfolder = ''

    inputs = []
    inputs_sizes = []
    inputs_withsizes = []

    outputs = []
    outputs_sizes = []
    outputs_withsizes = []

    timedelay = 5
    clockdelay = 5
    nooftestcases = 5

    alltestcases = False

    testbenchcode_format = ['`include "^vtb_modulename^.v"', 'module ^vtb_modulename^_tb;', '^vtb_inputs^', '^vtb_outputs^', 
        'initial begin\n\t$dumpfile("^vtb_modulename^_tb.vcd");\n\t$dumpvars(0, ^vtb_modulename^_tb);\n\t^vtb_monitor^\nend', 
        '^vtb_modulename^ ^vtb_modulename^_(^vtb_inputsparams^, ^vtb_outputsparams^);', 
        '^vtb_clkname^\n', 
        'initial begin\n^vtb_inputinit^\n^vtb_inputchange^\nend', 
        'endmodule']

    format_values = [['^vtb_modulename^', ''], ['^vtb_inputs^', ''], ['^vtb_inputsparams^', ''], ['^vtb_outputs^', ''],  ['^vtb_outputsparams^', ''], ['^vtb_monitor^', ''],  ['^vtb_inputinit^', ''],  ['^vtb_inputchange^', ''], 
                    ['^vtb_clockdelay^', ''], ['^vtb_clkname^', '']]

    clock_inp_names = ['clk', 'clock']

    fetch_inputs_testbench(fields)

def fetch_inputs_testbench(fields):
	global first_input
	input_dict = {}

	for field in fields:
		text  = input(field + ": ")
		if field == "EnterArrayTypeDataFieldHere":
			text = text.split(",")
		input_dict[field] = text
	print(input_dict)

	first_input = False

	global inputfileloc
	global modulename
	global destfolder
	global timedelay
	global clockdelay
	global nooftestcases
	global alltestcases

	if input_dict["Verilog Code Location (with filename)"] != '':
		inputfileloc = input_dict["Verilog Code Location (with filename)"]
	if input_dict["Verilog Module Name"] != '':
		modulename = input_dict["Verilog Module Name"]
	if input_dict["Destination Folder"] != '':
		destfolder = input_dict["Destination Folder"]
	if input_dict["Time Delay"] != '':
		timedelay = int(input_dict["Time Delay"])
	if input_dict["Clock Delay"] != '':
		clockdelay = int(input_dict["Clock Delay"])
	if input_dict["No of Test Cases"] != '':
		nooftestcases = int(input_dict["No of Test Cases"])
	elif input_dict["No of Test Cases"] == '':
		alltestcases = True

	InputOutputVerilogParser(filepath=inputfileloc, destfolder=destfolder)

def VectorSize(name):
	name = name.strip()

	if re.search('^\[', name):
		lval = re.findall('^\[(.*):', name)[0]
		rval = re.findall('^\[.*:(.*)\]', name)[0]
		return (abs(int(rval) - int(lval)) + 1)
	return 1

def ArraySize(name):
	name = name.strip()

	if re.search('^\[', name):
		name = re.findall('^\[.*:.*\](.*)', name)[0]
		return ArraySize(name)
		# if re.search('\[', name):
		# 	name = re.findall('^.+\[.*:.*\]', name)[0]
		# 	return VectorSize(name)
		# return 1

	elif re.search('\[', name):
		name = re.findall('^.+(\[.*:.*\])', name)[0]
		return VectorSize(name)
	return 1

def RemoveVectorArray(name):
	name = name.strip()

	if re.search('^\[.*:.*\].*', name):
		name = re.findall('^\[.*:.*\](.*)', name)[0]
		return RemoveVectorArray(name)

	elif re.search('\[', name):
		name = re.findall('^(.+)(\[.*:.*\])', name)[0]
		return name.strip()
	return name.strip()

def InputOutputVerilogParser(filepath, destfolder):
	global inputs
	global inputs_withsizes
	global outputs
	global outputs_withsizes
	global inputs_sizes
	global outputs_sizes
	global modulename

	contents = FileContents(filepath)
	# contents = contents.split("\n")
	contents = contents.split(";")
	iterindex = 0
	for i in contents:
		contents[iterindex] = i + ";"
		iterindex+=1
	print("\n\nCONTENTS: ", contents, "\n\n")
	for line in contents:
		print ("Line(wos): ", line)
		line = line.strip()	
		print ("Line(ws): ", line)

		line = line.split('\n')
		line = ' '.join(line)
		# print(line)

		if re.search('module\s+', line):
			modulename = re.findall('module\s+(.*)\(', line)[0].strip()

		if re.search('input\s+', line):
			print("\nRE: ", re.findall('input\s+(.*);', line), "\n")
			val = re.findall('input\s+(.*);', line)[0].strip()
			if re.search('^\[', val) == None:
				print ("Input: ", val, " -- ", val.split(","))
				inps = val.split(",")
				for index in range(len(inps)):
					inps[index] = inps[index].strip()

				inpssize = []
				i=0
				for o in inps:
					inps[i] = o.strip()

					inpssize.append([VectorSize(inps[i]), ArraySize(inps[i])])

					i+=1

				inputs_withsizes.extend(inps)
				inputs_sizes.extend(inpssize)
			else:
				vectorprefix = re.findall('^(\[.*:.*\]).*', val)[0]
				val = re.findall('^\[.*:.*\](.*)', val)[0]

				print ("Input: ", val, " -- ", val.split(","))
				inps = val.split(",")
				for index in range(len(inps)):
					inps[index] = inps[index].strip()

				inpssize = []
				i=0
				for o in inps:
					inps[i] = vectorprefix + o.strip()

					inpssize.append([VectorSize(inps[i]), ArraySize(inps[i])])

					i+=1

				inputs_withsizes.extend(inps)
				inputs_sizes.extend(inpssize)


		if re.search('output\s+', line):
			val = re.findall('output\s+(.*);', line)[0].strip()

			if re.search('^\[', val) == None:
				print ("Output: ", val, " -- ", val.split(","))
				outs = val.split(",")
				for index in range(len(outs)):
					outs[index] = outs[index].strip()

				outssize = []
				i=0
				for o in outs:
					outs[i] = o.strip()

					outssize.append([VectorSize(outs[i]), ArraySize(outs[i])])

					i+=1
				
				outputs_withsizes.extend(outs)
				outputs_sizes.extend(outssize)

			else:
				vectorprefix = re.findall('^(\[.*:.*\]).*', val)[0]
				val = re.findall('^\[.*:.*\](.*)', val)[0]

				print ("Output: ", val, " -- ", val.split(","))
				outs = val.split(",")
				for index in range(len(outs)):
					outs[index] = outs[index].strip()
				
				outssize = []
				i=0
				for o in outs:
					outs[i] = vectorprefix + o.strip()

					outssize.append([VectorSize(outs[i]), ArraySize(outs[i])])

					i+=1
				
				outputs_withsizes.extend(outs)
				outputs_sizes.extend(outssize)

	for inp in inputs_withsizes:
		inputs.append(RemoveVectorArray(inp))

	for out in outputs_withsizes:
		outputs.append(RemoveVectorArray(out))

	print ("Inputs with sizes: ", inputs_withsizes)
	print ("Inputsize: ", inputs_sizes)
	print ("Outputs with sizes: ", outputs_withsizes)
	print ("Outputsize: ", outputs_sizes)

	print("Inputs: ", inputs)
	print("Outputs: ", outputs)

	AssignFormatValues()

	CreateOutputFile()

def AssignFormatValues():
	global format_values
	global inputs
	global inputs_withsizes
	global outputs
	global outputs_withsizes
	global inputs_sizes
	global outputs_sizes
	global modulename
	global timedelay
	global clockdelay
	global nooftestcases
	global alltestcases

	for f in format_values:
		if f[0] == '^vtb_modulename^':

			f[1] = modulename.strip()

		if f[0] == '^vtb_inputs^':
			s = ''
			for i in inputs_withsizes:
				s = s + 'reg'
				s = s + ' '+ i
				s = s + ';\n'

			f[1] = s

		if f[0] == '^vtb_outputs^':
			s = ''
			for i in outputs_withsizes:
				s = s + 'wire'
				s = s + ' '+ i
				s = s + ';\n'

			f[1] = s

		if f[0] == '^vtb_inputsparams^':
			s = ''
			for i in inputs:
				s = s + ', .'+ i + '(' + i + ')'

			f[1] = re.findall('^, (.*)', s)[0]

		if f[0] == '^vtb_outputsparams^':
			s = ''
			for i in outputs:
				s = s + ', .'+ i + '(' + i + ')'

			f[1] = re.findall('^, (.*)', s)[0]

		if f[0] == '^vtb_monitor^':
			s = '$monitor($time, ": '
			for i in inputs:
				s = s + ', ' + i + ': %b(%d)'		# 2 prints of inp and output needed
			for i in outputs:
				s = s + ', ' + i + ': %b(%d)'

			s = s + '"'

			for i in inputs:
				s = s + ', ' + i 					# As there is %b and %d
				s = s + ', ' + i
			for i in outputs:
				s = s + ', ' + i
				s = s + ', ' + i
			s = s + ');'

			f[1] = s

		if f[0] == '^vtb_inputinit^':
			s = ''
			i=0
			for ip in inputs:
				svec = inputs_sizes[i][0]
				sarr = inputs_sizes[i][1]
				if sarr > 1:
					for j in range(sarr):
						s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
						for k in range(svec):
							s = s + '0'
						s = s + '; '
					s = s + '\n'
				else:
					s = s + ip + ' = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + '0'
					s = s + '; '
					s = s + '\n'

			f[1] = s

		if f[0] == '^vtb_inputchange^':
			if alltestcases:
				f[1] = AllTestCases(timedelay, inputs, inputs_sizes)
			else:
				f[1] = LimitedTestCases(nooftestcases, timedelay, inputs, inputs_sizes)

		if f[0] == '^vtb_clockdelay^':

			f[1] = str(clockdelay)

		if f[0] == '^vtb_clkname^':
			clkname = ''
			for i in clock_inp_names:
				if i in inputs:
					clkname = i
			if clkname != '':
				f[1] = 'always #' + str(clockdelay)  + '\n\t' + clkname + ' = ! ' + clkname + ';'
			else:
				f[1] = ''


	print("FORMAT: ", format_values)

def LimitedTestCases(nooftestcases, timedelay, inputs, inputs_sizes):
	s = ''
	for i in range(nooftestcases):
		s = s + '#' + str(timedelay) + ' '
		random.randint(1,2)
		i=0
		for ip in inputs:
			svec = inputs_sizes[i][0]
			sarr = inputs_sizes[i][1]
			if sarr > 1:
				for j in range(sarr):
					s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + str(random.randint(0,1))
					s = s + '; '
				#s = s + '\n'
			else:
				s = s + ip + ' = ' + str(svec) + "'b"
				for k in range(svec):
					s = s + str(random.randint(0,1))
				s = s + '; '
				#s = s + '\n'
		s = s + '\n'
	return s

def AllTestCases(timedelay, inputs, inputs_sizes):
	s = ''
	total_size = 0
	for ip in inputs_sizes:
		total_size = total_size + (ip[0]*ip[1])

	noofcombinations = 2 ** total_size

	totinp = [0]*total_size

	print("\n")

	for i in range(noofcombinations):

		print("TestCase: ", i, "/", noofcombinations)

		s = s + '#' + str(timedelay) + ' '
		totinp = GenNextInput(totinp)

		totinpindex = 0
		index=0
		for ip in inputs:
			svec = inputs_sizes[index][0]
			sarr = inputs_sizes[index][1]
			if sarr > 1:
				for j in range(sarr):
					s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + str(totinp[totinpindex])
						totinpindex+=1
					s = s + '; '
				#s = s + '\n'
			else:
				s = s + ip + ' = ' + str(svec) + "'b"
				for k in range(svec):
					s = s + str(totinp[totinpindex])
					totinpindex+=1
				s = s + '; '
				#s = s + '\n'

		s = s + '\n'

	return s

def GenNextInput(totinp):
	newtotinp = totinp
	i = 0
	for t in totinp:
		if t == 1:
			newtotinp[i] = 0
		elif t == 0:
			newtotinp[i] = 1
			break
		i+=1
	return newtotinp

def CreateOutputFile():
	global testbenchcode_format
	global format_values

	global destfolder

	contents = ''
	for c in testbenchcode_format:

		for fv in format_values:
			c = c.replace(fv[0], fv[1])
		contents = contents + c
		contents = contents + '\n'
	print("OutputFileContents: ", contents)

	f = open(destfolder + '\\' + modulename + '_tb.v', 'w+')
	f.write(contents)