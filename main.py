import re
import math

# Token types
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'
SQRT = 'SQRT'
LOG = 'LOG' 
COMMA = 'COMMA' 
SIN = 'SIN'    
COS = 'COS'    
TAN = 'TAN'    
constants = {
    'pi': math.pi,
    'e': math.e,
    'phi': (1 + math.sqrt(5)) / 2,
}
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.keywords = {'sqrt', 'log', 'ln', 'sin', 'cos', 'tan'}

    def error(self, char):
        raise Exception(f'Invalid character: {char}')

    def handle_operator(self, token_type):
        token = Token(token_type, self.text[self.pos])
        self.pos += 1
        return token

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(EOF, None)

        current_char = self.text[self.pos]

        if current_char.isdigit():
            return self.integer()
        elif current_char == '+':
            return self.handle_operator(PLUS)
        elif current_char == '-':
            return self.handle_operator(MINUS)
        elif current_char == '*':
            return self.handle_operator(MULTIPLY)
        elif current_char == '/':
            return self.handle_operator(DIVIDE)
        elif current_char == '(':
            token = Token(LPAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ')':
            token = Token(RPAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ',':
            token = Token(COMMA, current_char)
            self.pos += 1
            return token
        elif current_char.isalpha():
            word = ''
            while current_char.isalpha() and self.pos < len(self.text):
                word += current_char
                self.pos += 1
                if self.pos < len(self.text):
                    current_char = self.text[self.pos]
            if word.lower() in self.keywords:
                if word.lower() == 'log':
                    return Token(LOG, 'log')
                elif word.lower() == 'ln':
                    return Token(LOG, 'ln')
                elif word.lower() == 'sin':
                    return Token(SIN, 'sin')
                elif word.lower() == 'cos':
                    return Token(COS, 'cos')
                elif word.lower() == 'tan':
                    return Token(TAN, 'tan')
                else:
                    return Token(SQRT, word.lower())
            elif word.lower() in constants:
                return Token(INTEGER, constants[word.lower()])
        elif current_char == '√': 
            self.pos += 1
            return Token(SQRT, '√')

        self.error(current_char)

    def integer(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            result += self.text[self.pos]
            self.pos += 1

        if self.pos < len(self.text) and self.text[self.pos] == '.':
            result += self.text[self.pos]
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                result += self.text[self.pos]
                self.pos += 1
            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER or token.type == FLOAT:
            self.eat(token.type)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == SQRT: 
            self.eat(SQRT)
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return math.sqrt(result)
        elif token.type == LOG:
            self.eat(LOG)
            self.eat(LPAREN)
            arg = self.expr()
            self.eat(COMMA)  
            base = self.expr()
            self.eat(RPAREN)
            return logarithm(arg, base)
        elif token.type in (SIN, COS, TAN):
            if token.type == SIN:
                self.eat(SIN)
                self.eat(LPAREN)
                angle = self.expr()
                self.eat(RPAREN)
                return math.sin(angle)
            elif token.type == COS:
                self.eat(COS)
                self.eat(LPAREN)
                angle = self.expr()
                self.eat(RPAREN)
                return math.cos(angle)
            elif token.type == TAN:
                self.eat(TAN)
                self.eat(LPAREN)
                angle = self.expr()
                self.eat(RPAREN)
                return math.tan(angle)

    def pow(self):
        result = self.factor()
        while self.current_token.type == pow:
            token = self.current_token
            if token.type == pow:
                self.eat(pow)
                exponent = self.factor()
                result = result ** exponent
        return result

    def term(self):
        result = self.pow()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.pow()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.pow()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

def logarithm(x, base=2):
    if base == 2:
        return math.log2(x)
    else:
        return math.log(x, base)

def main():
    while True:
        try:
            text = input('Calc> ')
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
