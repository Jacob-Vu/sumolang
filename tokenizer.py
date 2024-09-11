# Define the keywords
import re

class Tokenizer:    
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
    TOKEN_SPECS = [
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

    def lex(self, source_code):
    # source_code = source_code.replace('\n','').replace('\r','')
        tokens = []
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECS)
        for match in re.finditer(token_regex, source_code):
            kind = match.lastgroup
            value = match.group(kind)
            
            if kind == 'ID':
                # Check if the identifier is a keyword
                if value in self.KEYWORDS:
                    kind = self.KEYWORDS[value]
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