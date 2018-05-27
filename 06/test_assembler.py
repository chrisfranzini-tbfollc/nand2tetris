import unittest
from Assembler import Parser, Code, SymbolTable

class TestParser(unittest.TestCase):

    def test_init(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        f = open('./add/Add.asm', "r", encoding="utf-8")
        self.assertEqual(test_parser.file, f.readlines())
        self.assertEqual(test_parser.length, 13)
        self.assertEqual(test_parser.line_counter, -1)
        self.assertEqual(test_parser.current_command, None)
        
        f.close()
        
        
    def test_process_file(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        processed_file = ['@2','D=A','@3','D=D+A','@0','M=D']
        test_parser.process_file()
        self.assertEqual(test_parser.proc_file, processed_file)
        
    
    def test_has_more_commands(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        self.assertTrue(test_parser.hasMoreCommands())
        test_parser.line_counter = test_parser.length - test_parser.length
        self.assertTrue(test_parser.hasMoreCommands())
        test_parser.line_counter = test_parser.length - 1
        self.assertFalse(test_parser.hasMoreCommands())
        test_parser.line_counter = test_parser.length
        self.assertFalse(test_parser.hasMoreCommands())
        test_parser.line_counter = test_parser.length + 1
        self.assertFalse(test_parser.hasMoreCommands())
        
    def test_advance(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        self.assertEqual(test_parser.line_counter, -1)
        test_parser.advance()
        self.assertEqual(test_parser.line_counter, 0)
        test_parser.line_counter = test_parser.length - 1
        test_parser.advance()
        self.assertEqual(test_parser.line_counter, test_parser.length - 1)
        test_parser.advance()
        self.assertEqual(test_parser.line_counter, test_parser.length - 1)
        
    def test_command_type(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'A_COMMAND')
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'C_COMMAND')
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'A_COMMAND')
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'C_COMMAND')
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'A_COMMAND')
        test_parser.advance()
        self.assertEqual(test_parser.commandType(), 'C_COMMAND')
        
    def test_symbol(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), '2')
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), None)
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), '3')
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), None)
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), '0')
        test_parser.advance()
        self.assertEqual(test_parser.symbol(), None)
        
    def test_dest(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        test_parser.advance()
        self.assertEqual(test_parser.dest(), None)
        test_parser.advance()
        self.assertEqual(test_parser.dest(), 'D')
        test_parser.advance()
        self.assertEqual(test_parser.dest(), None)
        test_parser.advance()
        self.assertEqual(test_parser.dest(), 'D')
        test_parser.advance()
        self.assertEqual(test_parser.dest(), None)
        test_parser.advance()
        self.assertEqual(test_parser.dest(), 'M')    
        
    def test_comp(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        test_parser.advance()
        self.assertEqual(test_parser.comp(), None)
        test_parser.advance()
        self.assertEqual(test_parser.comp(), 'A')
        test_parser.advance()
        self.assertEqual(test_parser.comp(), None)
        test_parser.advance()
        self.assertEqual(test_parser.comp(), 'D+A')
        test_parser.advance()
        self.assertEqual(test_parser.comp(), None)
        test_parser.advance()
        self.assertEqual(test_parser.comp(), 'D')    
    
    def test_jump(self):
        file_path = './add/Add.asm'
        test_parser = Parser(file_path)
        test_parser.process_file()
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None)
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None)
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None)
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None)
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None)
        test_parser.advance()
        self.assertEqual(test_parser.jump(), None) 

# class TestCode(unittest.TestCase):

    # def test_dest(self):
    #     file_path = './add/Add.asm'
    #     test_parser = Parser(file_path)
    #     test_parser.process_file()
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "010")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "010")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.dest(self, c), "001")
        

    # def test_comp(self):
    #     file_path = './add/Add.asm'
    #     test_parser = Parser(file_path)
    #     test_parser.process_file()
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(None, c, None), None)
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(self, c), "0110000")
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(self, c), None)
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(self, c), "0000010")
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(self, c), None)
    #     test_parser.advance()
    #     c = test_parser.comp()
    #     self.assertEqual(Code.comp(self, c), "0001100")   


    # def test_jump(self):
    #     file_path = './add/Add.asm'
    #     test_parser = Parser(file_path)
    #     test_parser.process_file()
    #     test_parser.advance()
    #     c = test_parser.jump()
    #     self.assertEqual(Code.jump(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.jump(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.jump(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.jump(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.jump(self, c), "000")
    #     test_parser.advance()
    #     c = test_parser.dest()
    #     self.assertEqual(Code.jump(self, c), "000")   
    #     

class TestSymbolTable(unittest.TestCase):

    def test_constructor(self):
        symbol_table = SymbolTable()
        self.assertEqual(symbol_table.table, dict())

    def test_add_entry(self):
        symbol_table = SymbolTable()
        symbol = 'LOOP'
        address = '12'
        symbol_table.addEntry(symbol, address)
        self.assertEqual(symbol_table.table, {'LOOP': '12'})

    def test_contains(self):
        symbol_table = SymbolTable()
        symbol = 'LOOP'
        address = '12'
        self.assertFalse(symbol_table.contains(symbol))
        symbol_table.addEntry(symbol, address)
        self.assertTrue(symbol_table.contains(symbol))

    def test_get_address(self):
        symbol_table = SymbolTable()
        symbol = 'LOOP'
        address = '12'
        self.assertIsNone(symbol_table.getAddress(symbol))
        symbol_table.addEntry(symbol, address)
        self.assertEqual(symbol_table.getAddress(symbol), '12')



if __name__ == '__main__':
    unittest.main()