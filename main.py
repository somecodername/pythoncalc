import math
import matplotlib.pyplot as plt
import numpy as np

# Token types
class TokenType:
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
    COMMA = ','
    SIN = 'SIN'
    COS = 'COS'
    TAN = 'TAN'
    POW = '^'  # Added exponent operator

constants = {
    'pi': math.pi,
    'e': math.e,
    'phi': (1 + math.sqrt(5)) / 2,
}

def help():
    """
    This function displays the available commands and their functionalities.
    """
    print("**Available Commands**:")
    print("+ (Addition): Adds two numbers.")
    print("- (Subtraction): Subtracts two numbers.")
    print("* (Multiplication): Multiplies two numbers.")
    print("/ (Division): Divides two numbers.")
    print("() (Parentheses): Used to group expressions for order of operations.")
    print("sqrt(x) (Square Root): Calculates the square root of a number.")
    print("log(x, base) (Logarithm): Calculates the logarithm of x to a specified base (default base e).")
    print("sin(x) (Sine): Calculates the sine of an angle in radians.")
    print("cos(x) (Cosine): Calculates the cosine of an angle in radians.")
    print("tan(x) (Tangent): Calculates the tangent of an angle in radians.")
    print("pi (Constant): Represents the mathematical constant pi.")
    print("e (Constant): Represents the mathematical constant e.")
    print("phi (Constant): Represents the golden ratio (phi).")
    print("^ (Power): Raises a number to a power.")
    print("**Graph Plotting**:")
    print("graph: Starts the process to plot different types of graphs.")
    print("    linear: Plots a linear equation of the form y = mx + b.")
    print("    quadratic: Plots a quadratic equation of the form y = ax^2 + bx + c.")
    print("    cubic: Plots a cubic equation of the form y = ax^3 + bx^2 + cx + d.")
    print("    exponential: Plots an exponential equation of the form y = a * e^(bx).")
    print("    trigonometric: Plots trigonometric functions (sin, cos, tan).")
    print("    triangle: Plots a triangle given the coordinates of its vertices.")
    print("    polygon: Plots a polygon given the coordinates of its vertices.")
    print("Example of using graph plotting:")
    print("    graph -> linear -> Enter the coefficient m: 2 -> Enter the coefficient b: 3")
    print("This will plot the graph of y = 2x + 3.")

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
            return Token(TokenType.EOF, None)

        current_char = self.text[self.pos]

        if current_char.isdigit():
            return self.integer()
        elif current_char in '+-*/':  # Combined arithmetic operators
            return self.handle_operator(current_char)
        elif current_char == '(':
            token = Token(TokenType.LPAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ')':
            token = Token(TokenType.RPAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ',':
            token = Token(TokenType.COMMA, current_char)
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
                    return Token(TokenType.LOG, 'log')
                elif word.lower() == 'ln':
                    return Token(TokenType.LOG, 'ln')
                elif word.lower() == 'sin':
                    return Token(TokenType.SIN, 'sin')
                elif word.lower() == 'cos':
                    return Token(TokenType.COS, 'cos')
                elif word.lower() == 'tan':
                    return Token(TokenType.TAN, 'tan')
                else:
                    return Token(TokenType.SQRT, word.lower())
            elif word.lower() in constants:
                return Token(TokenType.INTEGER, constants[word.lower()])
        elif current_char == '√': 
            self.pos += 1
            return Token(TokenType.SQRT, '√')

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
            return Token(TokenType.FLOAT, float(result))
        else:
            return Token(TokenType.INTEGER, int(result))

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
        if token.type in {TokenType.INTEGER, TokenType.FLOAT}:
            self.eat(token.type)
            return token.value
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        elif token.type == TokenType.SQRT:
            self.eat(TokenType.SQRT)
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return math.sqrt(result)
        elif token.type == TokenType.LOG:
            self.eat(TokenType.LOG)
            self.eat(TokenType.LPAREN)
            arg = self.expr()
            base = None
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                base = self.expr()
            self.eat(TokenType.RPAREN)
            return logarithm(arg, base)
        elif token.type in {TokenType.SIN, TokenType.COS, TokenType.TAN}:
            self.eat(token.type)
            self.eat(TokenType.LPAREN)
            arg = self.expr()
            self.eat(TokenType.RPAREN)
            if token.type == TokenType.SIN:
                return math.sin(arg)
            elif token.type == TokenType.COS:
                return math.cos(arg)
            elif token.type == TokenType.TAN:
                return math.tan(arg)

    def pow(self):
        result = self.factor()
        while self.current_token.type == TokenType.POW:
            self.eat(TokenType.POW)
            result **= self.factor()
        return result

    def term(self):
        result = self.pow()
        while self.current_token.type in {TokenType.MULTIPLY, TokenType.DIVIDE}:
            if self.current_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result *= self.pow()
            elif self.current_token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                result /= self.pow()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in {TokenType.PLUS, TokenType.MINUS}:
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif self.current_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
        return result

def logarithm(arg, base):
    if base is None:
        base = math.e
    return math.log(arg, base)

def plot_linear_graph(m, b):
    x = np.linspace(-10, 10, 400)
    y = m * x + b
    plt.plot(x, y, label=f'y = {m}x + {b}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of y = mx + b')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def plot_quadratic_graph(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    plt.plot(x, y, label=f'y = {a}x^2 + {b}x + {c}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of y = ax^2 + bx + c')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def plot_cubic_graph(a, b, c, d):
    x = np.linspace(-10, 10, 400)
    y = a * x**3 + b * x**2 + c * x + d
    plt.plot(x, y, label=f'y = {a}x^3 + {b}x^2 + {c}x + {d}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of y = ax^3 + bx^2 + cx + d')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def plot_exponential_graph(a, b):
    x = np.linspace(-2, 2, 400)
    y = a * np.exp(b * x)
    plt.plot(x, y, label=f'y = {a}e^({b}x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of y = a * e^(bx)')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def plot_trigonometric_graph(func):
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400)
    if func == 'sin':
        y = np.sin(x)
    elif func == 'cos':
        y = np.cos(x)
    elif func == 'tan':
        y = np.tan(x)
    plt.plot(x, y, label=f'y = {func}(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Graph of y = {func}(x)')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def plot_triangle(vertices):
    vertices.append(vertices[0])  # Repeat the first vertex to close the triangle
    xs, ys = zip(*vertices)
    plt.plot(xs, ys, 'bo-', label='Triangle')
    plt.fill(xs, ys, 'b', alpha=0.1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Triangle')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def plot_polygon(vertices):
    vertices.append(vertices[0])  # Repeat the first vertex to close the polygon
    xs, ys = zip(*vertices)
    plt.plot(xs, ys, 'bo-', label='Polygon')
    plt.fill(xs, ys, 'b', alpha=0.1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Polygon')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def main():
    while True:
        try:
            text = input('Calc> ')
            if not text:
                continue
            if text.lower() == 'help':
                help()
                continue
            if text.lower().startswith('graph'):
                equation_type = input('Enter type of equation (linear, quadratic, cubic, exponential, trigonometric, triangle, polygon): ').strip().lower()
                if equation_type == 'linear':
                    m = float(input('Enter the coefficient m: ').strip())
                    b = float(input('Enter the coefficient b: ').strip())
                    plot_linear_graph(m, b)
                elif equation_type == 'quadratic':
                    a = float(input('Enter the coefficient a: ').strip())
                    b = float(input('Enter the coefficient b: ').strip())
                    c = float(input('Enter the coefficient c: ').strip())
                    plot_quadratic_graph(a, b, c)
                elif equation_type == 'cubic':
                    a = float(input('Enter the coefficient a: ').strip())
                    b = float(input('Enter the coefficient b: ').strip())
                    c = float(input('Enter the coefficient c: ').strip())
                    d = float(input('Enter the coefficient d: ').strip())
                    plot_cubic_graph(a, b, c, d)
                elif equation_type == 'exponential':
                    a = float(input('Enter the coefficient a: ').strip())
                    b = float(input('Enter the coefficient b: ').strip())
                    plot_exponential_graph(a, b)
                elif equation_type == 'trigonometric':
                    func = input('Enter the trigonometric function (sin, cos, tan): ').strip().lower()
                    if func in ['sin', 'cos', 'tan']:
                        plot_trigonometric_graph(func)
                    else:
                        print("Invalid trigonometric function. Please enter 'sin', 'cos', or 'tan'.")
                elif equation_type == 'triangle':
                    vertices = []
                    for i in range(3):
                        x = float(input(f'Enter x{i+1}: ').strip())
                        y = float(input(f'Enter y{i+1}: ').strip())
                        vertices.append((x, y))
                    plot_triangle(vertices)
                elif equation_type == 'polygon':
                    vertices = []
                    num_vertices = int(input('Enter the number of vertices: ').strip())
                    for i in range(num_vertices):
                        x = float(input(f'Enter x{i+1}: ').strip())
                        y = float(input(f'Enter y{i+1}: ').strip())
                        vertices.append((x, y))
                    plot_polygon(vertices)
                else:
                    print("Currently supported types: linear, quadratic, cubic, exponential, trigonometric, triangle, polygon.")
                continue
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            result = interpreter.expr()
            print(result)
        except Exception as e:
            print(f"Error: {e}")
            print("Please check your input and try again.")

if __name__ == '__main__':
    main()
