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
