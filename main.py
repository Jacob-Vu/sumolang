from interpreter import Interpreter
from parser import Parser
from tokenizer import Tokenizer

# Helper function to read code from a file
def read_code_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Example usage: Reading code from 'sum.sm'
filename = 'sum.sm'
source_code = read_code_from_file(filename)

tokenizer = Tokenizer()
tokens = tokenizer.lex(source_code)  # Tokenize the source code
parser = Parser(tokens)    # Initialize the parser
program_ast = parser.parse_program()  # Parse the program to get the AST
interpreter = Interpreter(program_ast)  # Initialize the interpreter
interpreter.interpret()  # Execute the AST
