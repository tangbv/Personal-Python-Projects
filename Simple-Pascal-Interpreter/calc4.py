# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, EOF =  'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        # token type
        self.value = value
        # token value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format (
            type = self.type,
            value = repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
            self.text = text
            # client string input, e.g. "3+5"
            self.pos = 0
            # self.pos is an index into self.text
            self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' var"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """Return an integer eaten from input"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (aka tokenizer)

        This method will break a sentence apart into
        indivdual tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, '+')
        
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == "*":
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == "/":
                self.advance()
                return Token(DIV, '/')

            self.error()
        return Token(EOF, None)
    

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, text=""):
        if text == 0:
            raise Exception("Cannot divide by zero")
        raise Exception('Invalid syntax')
    
    def eat(self, token_type):
        # compare the current token with the passed token type
        # and if they match, "eat" the current token and assign
        # the next token to the self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token() 
        else:
            self.error()
    
    def factor(self):
        """Return an INTEGER token value.

        factor : INTEGER
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter.

        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()
        while self.current_token.type in (PLUS, MINUS, MUL, DIV):            
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = result + self.factor()
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.factor()
            elif op.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            else:
                self.eat(DIV)
                divisor = self.factor()
                if divisor == 0:
                    self.error(0)
                result = result / divisor
        return result

def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)
    
if __name__ == '__main__':
    main()