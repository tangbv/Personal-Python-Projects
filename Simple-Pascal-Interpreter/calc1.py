# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF =  'INTEGER', 'PLUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        # token type: INTEGER, PLUS, or EOF
        self.value = value
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None

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

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        # client string input, e.g. "3+5"
        self.pos = 0
        # self.pos is an index into self.text
        self.current_token = None
        # current token instance

    def error(self):
        raise Exception('Error parsing input')
    
    def get_next_token(self):
        """Lexical analyzer (aka tokenizer)

        This method will break a sentence apart into
        indivdual tokens. One token at a time.
        """
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)
    
        # Get the current token at self.pos
        current_char = text[self.pos]

        # If character is a digit, then convert it to an 
        # integer. Create Integer token, and increment posistion.
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        # If character is a plus, create plus token, and increment posistion.
        if current_char == "+":
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        # Only digit and plus for now, else return error
        self.error()

    def eat(self, token_type):
        # compare the current token with the passed token type
        # and if they match, "eat" the current token and assign
        # the next token to the self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token() 
        else:
            self.error()
        
    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from input
        self.current_token = self.get_next_token()

        # expect that first token will be an single digit integer
        left = self.current_token
        self.eat(INTEGER)

        # expect current token to now be "+" token
        op = self.current_token
        self.eat(PLUS)

        # expect that first token will be an single digit integer
        right = self.current_token
        self.eat(INTEGER) 

        # self.current_token should now be EOF
        result = left.value + right.value
        return result

def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
    
if __name__ == '__main__':
    main()