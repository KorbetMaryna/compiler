class LexicalError(Exception):
    pass

class ParsingError(Exception):
    pass

class TokenType:
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    EOF = 'EOF'  # Означає кінець вхідного файлу/рядка

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

#!Переміщуємо 'вказівник' на наступний символ вхідного рядка
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Означає кінець введення
        else:
            self.current_char = self.text[self.pos]

# !Пропускаємо пробільні символи.
    def skip_whitespace(self):  
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

#!Повертаємо ціле число, зібране з послідовності цифр.
    def integer(self): 
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

#!Лексичний аналізатор, що розбиває вхідний рядок на токени.
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            raise LexicalError('Lexical analysis error')

        return Token(TokenType.EOF, None)
    
#!Визначимо базові класи для вузлів AST
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

#!Pеалізуємо клас Parser , який створюватиме AST
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    #!Помилка синтаксичного аналізу
    def error(self):
        raise ParsingError('Parse error')
    
    #!Порівнюємо поточний токен з очікуваним токеном і, якщо вони збігаються, поглинаємо його й переходимо до наступного токена.
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    #!Парсер для 'term' правил граматики. У нашому випадку - це цілі числа.
    def term(self):
        token = self.current_token
        self.eat(TokenType.INTEGER)
        return Num(token)

    #!Парсер для арифметичних виразів.
    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

#!Додамо метод print_ast для візуалізації структури AST
def print_ast(node, level=0):
    indent = '  ' * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")


#!Cтворюємо інтерпретатор, який буде обходити AST (абстрактне синтаксичне дерево), створене парсером, і виконувати обчислення арифметичного виразу
class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'There is no visit_{type(node).__name__} method')       

#!Модифікуємо функцію main для запуску нашого коду та використаємо функцію interpreter.
def main():
    while True:
        try:
            text = input('Enter the expression (or "exit" to exit):')
            if text.lower() == 'exit':
                print("Exit the program.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
