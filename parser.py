# class ASTNode:
#     pass

# class Program(ASTNode):
#     def __init__(self, var_declarations, statements):
#         self.var_declarations = var_declarations
#         self.statements = statements

# class VarDeclaration(ASTNode):
#     def __init__(self, var_list):
#         self.var_list = var_list

# class Assignment(ASTNode):
#     def __init__(self, var_name, expression):
#         self.var_name = var_name
#         self.expression = expression

# class ForLoop(ASTNode):
#     def __init__(self, var_name, start_expr, end_expr, statements):
#         self.var_name = var_name
#         self.start_expr = start_expr
#         self.end_expr = end_expr
#         self.statements = statements

# class Read(ASTNode):
#     def __init__(self, var_name):
#         self.var_name = var_name

# class Write(ASTNode):
#     def __init__(self, expression):
#         self.expression = expression

# class BinaryOperation(ASTNode):
#     def __init__(self, left, operator, right):
#         self.left = left
#         self.operator = operator
#         self.right = right

# class Number(ASTNode):
#     def __init__(self, value):
#         self.value = value

# class Variable(ASTNode):
#     def __init__(self, name):
#         self.name = name
        
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
