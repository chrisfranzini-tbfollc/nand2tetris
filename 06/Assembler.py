import re
import sys

class Parser:
	"""
	The main function of the parser is to break each assembly command into its
	underlying components (fields and symbols).
	"""
	def __init__(self, f):
		"""
		Opens the input file/stream and gets ready to parse it.
   
		f: input file path
		"""
		open_file = open(f, "r", encoding="utf-8")
		self.file = open_file.readlines()
		open_file.close()
		self.length = len(self.file)
		self.line_counter = -1
		self.current_command = None

	def process_file(self):
		"""
		Cleans input file to remove comments and whitespace
		"""
		ipat = re.compile(r"^[^//]*")
		stripf = [ l.strip() for l in self.file ]
		self.proc_file = []
	
		for l in stripf:
			imatch = re.search(ipat, l).group() 
		
			if imatch:
				self.proc_file.append(imatch.strip())

		self.length = len(self.proc_file)

	def hasMoreCommands(self):
		"""
		Are there more commands in the input?
   
		returns Boolean
		"""
		return self.line_counter < self.length - 1
	
	def advance(self):
		"""
		Reads the next command from the input and makes it the current command. 
		Should be called only if hasMoreCommands() is true. Initially there is 
		no current command.
		"""
		# current command
		if self.hasMoreCommands():
			self.line_counter += 1
			self.current_command = self.proc_file[self.line_counter] 
	
	def commandType(self):
		"""
		Returns the type of the current command:
			- A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
			- C_COMMAND for dest=comp;jump
			- L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol
	   
		returns String [A_COMMAND, C_COMMAND, L_COMMAND]
		"""
		command = self.current_command
	
		if command[0] == '@':
			return 'A_COMMAND'
		elif command[0] == '(':
			return 'L_COMMAND'
		else:
			return 'C_COMMAND'

	def symbol(self):
		"""
		Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). 
		Should be called only when commandType() is A_COMMAND or L_COMMAND.
   
		returns String
		"""
		command = self.current_command
	
		if self.commandType() == 'A_COMMAND':
			# if 'R' in command:
			# 	return command[2:]
			# else:
			# 	return command[1:]
			return command[1:]
		elif self.commandType() == 'L_COMMAND':
			return command[1:-1]
		else:
			return None 

	def dest(self):
		"""
		Returns the dest mnemonic in the current C-command (8 possibilities).
		Should be called only when commandType() is C_COMMAND.
	
		returns String
		"""
		command = self.current_command
	
		if self.commandType() == 'C_COMMAND':
			if '=' in command:
				return command.split('=')[0]
			else:
				return None
		else:
			return None

	def comp(self):
		"""
		Returns the comp mnemonic in the current C-command (28 possibilities).
		Should be called only when commandType() is C_COMMAND.
	
		returns String
		"""
		command = self.current_command
	
		if self.commandType() == 'C_COMMAND':
			if '=' in command:
				return command.split('=')[1]
			elif ';' in command:
				return command.split(';')[0]
			else:
				return None
		else:
			return None
	
	def jump(self):
		"""
		Returns the jump mnemonic in the current C-command (8 possibilities).
		Should be called only when commandType() is C_COMMAND.

		returns String
		"""

		command = self.current_command

		if self.commandType() == 'C_COMMAND':
			if ';' in command:
				return command.split(';')[1]
			else:
				return None
		else:
			return None

	def reset(self):
		""" Resets parser to initial state """
		self.line_counter = -1
		self.current_command = None


class Code:
	"""
	Translates Hack assembly language mnemonics into binary codes.
	"""
	def __init__(self, d, c, j):
		self.dest_command = d
		self.comp_command = c  
		self.jump_command = j    

	def dest(self):
		"""
		Returns the binary code of the dest mnemonic.
		"""
		dest_dict = {
			"M": "001",
			"D": "010",
			"MD": "011",
			"A": "100",
			"AM": "101",
			"AD": "110",
			"AMD": "111"
		}
		d = self.dest_command
		if d in dest_dict.keys():
			return dest_dict[d]
		else:
			return "000"

	def comp(self):
		"""
		Returns the binary code of the comp mnemonic.
		"""
		comp_dict = {
			"0": "0101010",
			"1": "0111111",
			"-1": "0111010",
			"D": "0001100",
			"A": "0110000",
			"!D": "0001101",
			"!A": "0110001",
			"-D": "0001111",
			"-A": "0110011",
			"D+1": "0011111",
			"A+1": "0110111",
			"D-1": "0001110",
			"A-1": "0110010",
			"D+A": "0000010",
			"D-A": "0010011",
			"A-D": "0000111",
			"D&A": "0000000",
			"D|A": "0010101",
			"M": "1110000",
			"!M": "1110001",
			"-M": "1110011",
			"M+1": "1110111",
			"M-1": "1110010",
			"D+M": "1000010",
			"D-M": "1010011",
			"M-D": "1000111",
			"D&M": "1000000",
			"D|M": "1010101"
		}
		c = self.comp_command
		if c in comp_dict.keys():
			return comp_dict[c]
		else:
			return "0000000"
		

	def jump(self):
		"""
		Returns the binary code of the jump mnemonic.
        """
		jump_dict = {
			"JGT": "001",
			"JEQ": "010",
			"JGE": "011",
			"JLT": "100",
			"JNE": "101",
			"JLE": "110",
			"JMP": "111"
		}
		j = self.jump_command
		if j in jump_dict.keys():
			return jump_dict[j]
		else:
			return "000"

class SymbolTable:

	def __init__(self):
		""" Creates a new empty symbol table. """
		self.table = {
			'SP': '0',
			'LCL': '1',
			'ARG': '2',
			'THIS': '3',
			'THAT': '4',
			'R0': '0',
			'R1': '1',
			'R2': '2',
			'R3': '3',
			'R4': '4',
			'R5': '5',
			'R6': '6',
			'R7': '7',
			'R8': '8',
			'R9': '9',
			'R10': '10',
			'R11': '11',
			'R12': '12',
			'R13': '13',
			'R14': '14',
			'R15': '15',
			'SCREEN': '16384',
			'KBD': '24576'	
		}

	def addEntry(self, symbol, address):
		""" Adds the pair (symbol, address) to the table."""
		self.table[symbol] = address

	def contains(self, symbol):
		"""Does the symbol table contain the given symbol?"""
		return symbol in self.table.keys()

	def getAddress(self, symbol):
		"""Returns the address associated with the symbol."""
		if self.contains(symbol):
			return self.table[symbol]
		else: 
			return None

	def getOpenAddress(self):
		min = 16
		max = int(self.table['SCREEN'])
		for n in range(min, max):
			if str(n) not in self.table.values():
				return str(n)
			else:
				n += 1
		return None


def c_writer(parser_obj):
	"""
	Given a parser object applies Code module to currentCommand and returns 
	string containing binary representation of command

	specifically for C instructions
	"""
	prefix = '111'
	code = Code(parser_obj.dest(), parser_obj.comp(), parser_obj.jump())
	dest_bits = code.dest()
	comp_bits = code.comp()
	jump_bits = code.jump()
	return prefix + comp_bits + dest_bits + jump_bits

def a_writer(parser_obj, symbol_table):
	"""
	Given a parser object applies Code module to currentCommand and returns 
	string containing binary representation of command

	Additionally, function replaces symbolic address according to symbol
	table specifications.

	specifically for A instructions
	"""
	prefix = '0'
	address = parser_obj.symbol()
	if not is_int(address):
		symbol = address
		if symbol_table.contains(symbol):
			a_num = symbol_table.getAddress(symbol)
		else:
			next_address = symbol_table.getOpenAddress()
			symbol_table.addEntry(symbol, next_address)
			a_num = next_address
	else:
		a_num = address
	a_bits = format(int(a_num), '015b')
	return prefix + a_bits

def is_int(x):
	try:
		int(x)
		return True
	except ValueError:
		return False
	
# start implementation	
input_file_path = sys.argv[1]
file_name = input_file_path.replace('.asm','')
parser = Parser(input_file_path)
parser.process_file()

# first pass (symbols)
counter = 0
symbol_table = SymbolTable()
while parser.hasMoreCommands():
	parser.advance()
	if parser.commandType() == 'L_COMMAND':
		symbol_table.addEntry(parser.symbol(), counter)
	else:
		counter += 1

# reset parser
parser.reset()

# second pass
with open('{}.hack'.format(file_name), 'w') as f:
	while parser.hasMoreCommands():
		parser.advance()
		if parser.commandType() == 'C_COMMAND':
			f.write(c_writer(parser) + '\n')
		elif parser.commandType() == 'A_COMMAND':
			f.write(a_writer(parser, symbol_table) + '\n')
		else:
			pass
			
f.close()