import re

# Define the keywords
KEYWORDS = {
    'var': 'VAR',
    'for': 'FOR',
    'read': 'READ',
    'write': 'WRITE',
    'to': 'TO',
    'do': 'DO',
    'endfor': 'ENDFOR'
}

# Example token patterns
token_specification = [
    ('NUMBER',   r'\d+'),           # Integer
    ('ASSIGN',   r':='),            # Assignment operator
    ('END',r';'),             # Statement terminator
    ('COMMA',    r','),             # Comma (for variable lists)
    ('LPAREN',   r'\('),            # Left parenthesis
    ('RPAREN',   r'\)'),            # Right parenthesis
    ('ID',       r'[A-Za-z_]\w*'),  # Identifiers
    ('OP',       r'[+\-*/]'),       # Arithmetic operators
    ('SKIP',     r'[ \t]+'),        # Skip over spaces and tabs
    ('NEWLINE',  r'\n'),            # Line endings
    ('MISMATCH', r'.')             # Any other character
]

def lex(source_code):
    # source_code = source_code.replace('\n','').replace('\r','')
    tokens = []
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for match in re.finditer(token_regex, source_code):
        kind = match.lastgroup
        value = match.group(kind)
        
        if kind == 'ID':
            # Check if the identifier is a keyword
            if value in KEYWORDS:
                kind = KEYWORDS[value]
            tokens.append((kind, value))
        elif kind == 'NUMBER':
            tokens.append((kind, int(value)))
        elif kind == 'NEWLINE':
            continue  # Ignore newlines in the token stream
        elif kind == 'SKIP':
            continue  # Ignore spaces and tabs
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character: {value}')
        else:
            tokens.append((kind, value))
    
    return tokens

# Example: Add Parser and Interpreter later

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, var_declarations, statements):
        self.var_declarations = var_declarations
        self.statements = statements

class VarDeclaration(ASTNode):
    def __init__(self, var_list):
        self.var_list = var_list

class Assignment(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

class ForLoop(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, statements):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.statements = statements

class Read(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

class Write(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()
    
    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF', '')

    def parse_program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        if self.current_token[0] == 'VAR':
            return self.parse_var_declaration()
        elif self.current_token[0] == 'READ':
            return self.parse_read_statement()
        elif self.current_token[0] == 'WRITE':
            return self.parse_write_statement()
        elif self.current_token[0] == 'FOR':
            return self.parse_for_statement()
        elif self.current_token[0] == 'ID':  # Identifiers for assignments
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_var_declaration(self):
        self.expect('VAR')
        variables = []
        while self.current_token[0] == 'ID':
            variables.append(self.current_token[1])
            self.next_token()
            if self.current_token[0] == 'COMMA':
                self.next_token()  # Skip comma
        self.expect('END')  # Expect semicolon
        return ('VAR_DECL', variables)

    def parse_read_statement(self):
        self.expect('READ')
        self.expect('LPAREN')
        var_name = self.current_token[1]
        self.expect('ID')
        self.expect('RPAREN')
        self.expect('END')
        return ('READ', var_name)

    def parse_write_statement(self):
        self.expect('WRITE')
        self.expect('LPAREN')
        var_name = self.current_token[1]
        self.expect('ID')
        self.expect('RPAREN')
        self.expect('END')
        return ('WRITE', var_name)

    def parse_for_statement(self):
        self.expect('FOR')
        var_name = self.current_token[1]
        self.expect('ID')
        self.expect('ASSIGN')
        start_expr = self.parse_expression()
        self.expect('TO')
        end_expr = self.parse_expression()
        self.expect('DO')
        body_statements = []
        while self.current_token[0] != 'ENDFOR':
            body_statements.append(self.parse_statement())
        self.expect('ENDFOR')
        self.expect('END')
        return ('FOR', var_name, start_expr, end_expr, body_statements)

    def parse_assignment(self):
        var_name = self.current_token[1]
        self.expect('ID')
        self.expect('ASSIGN')
        expr = self.parse_expression()
        self.expect('END')  # Expect a semicolon here
        return ('ASSIGN', var_name, expr)

    def parse_expression(self):
        # Parse terms and handle operators (+, -, *, /)
        term = self.parse_term()
        while self.current_token[0] == 'OP':
            op = self.current_token[1]
            self.next_token()
            right_term = self.parse_term()
            term = ('BIN_OP', op, term, right_term)
        return term

    def parse_term(self):
        # Parse either a number or a variable
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.next_token()
            return ('NUMBER', value)
        elif self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            self.next_token()
            return ('ID', var_name)
        else:
            raise SyntaxError(f"Expected NUMBER or ID, got {self.current_token}")
    
    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
    
    def interpret(self):
        self.execute_block(self.ast)
    
    def execute_block(self, block):
        for statement in block:
            self.execute(statement)
    
    def execute(self, node):
        node_type = node[0]
        
        if node_type == 'VAR_DECL':
            self.execute_var_decl(node)
        elif node_type == 'ASSIGN':
            self.execute_assign(node)
        elif node_type == 'READ':
            self.execute_read(node)
        elif node_type == 'WRITE':
            self.execute_write(node)
        elif node_type == 'FOR':
            self.execute_for(node)
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def execute_var_decl(self, node):
        _, variables = node
        for var in variables:
            self.variables[var] = 0  # Initialize variables to 0
    
    def execute_assign(self, node):
        _, var_name, expr = node
        value = self.evaluate_expression(expr)
        self.variables[var_name] = value
    
    def execute_read(self, node):
        _, var_name = node
        value = int(input(f"Enter value for {var_name}: "))
        self.variables[var_name] = value
    
    def execute_write(self, node):
        _, var_name = node
        print(f"{var_name} = {self.variables[var_name]}")
    
    def execute_for(self, node):
        _, var_name, start_expr, end_expr, body_statements = node
        start_value = self.evaluate_expression(start_expr)
        end_value = self.evaluate_expression(end_expr)
        
        for i in range(start_value, end_value + 1):
            self.variables[var_name] = i
            self.execute_block(body_statements)
    
    def evaluate_expression(self, expr):
        if expr[0] == 'NUMBER':
            return expr[1]
        elif expr[0] == 'ID':
            return self.variables[expr[1]]
        elif expr[0] == 'BIN_OP':
            op, left, right = expr[1], expr[2], expr[3]
            left_value = self.evaluate_expression(left)
            right_value = self.evaluate_expression(right)
            return self.apply_operator(op, left_value, right_value)
        else:
            raise TypeError(f"Unknown expression type: {expr[0]}")
    
    def apply_operator(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise ValueError(f"Unknown operator: {op}")


# Sample code to lex, parse, and interpret a simple program
source_code = """
var sum, i, n;

read(n);
sum := 0;
for i := 1 to n do
    sum := sum + i;
endfor;
write(sum);
"""

tokens = lex(source_code)  # Tokenize the source code
parser = Parser(tokens)    # Initialize the parser
program_ast = parser.parse_program()  # Parse the program to get the AST
interpreter = Interpreter(program_ast)  # Initialize the interpreter
interpreter.interpret()  # Execute the AST
