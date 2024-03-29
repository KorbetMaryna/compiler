class LexicalError(Exception):
    pass

class SyntaxError(Exception):
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

def main():
    while True:
        try:
            text = input('Enter the expression (or "exit" to exit):')
            if text.lower() == 'exit':
                print("Exit the program.")
                break
            lexer = Lexer(text)
            token = lexer.get_next_token()
            while token.type != TokenType.EOF:
                print(token)
                token = lexer.get_next_token()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

