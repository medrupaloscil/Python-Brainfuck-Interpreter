import re

class Interpreter(object):
    def __init__(self, text, debug = 0):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.current_memory = 0
        self.memory = [0]
        self.current_loop = 0
        self.loop_position = [0]
        self.startInside = 0
        self.debug = debug

    def nextChar(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skipInside(self):
        while self.current_char is not None:
            self.nextChar()
            if self.current_char == "[":
                self.startInside += 1
            if self.current_char == "]":
                if self.startInside == 0:
                    return
                else:
                    self.startInside -= 1

    def expr(self):
        while self.current_char is not None:
            if self.debug == 1:
                print("Position ", self.pos, ": Memory ", self.current_memory, " of value ", self.memory[self.current_memory])
            if self.current_char == "+":
                self.memory[self.current_memory] += 1
                if self.memory[self.current_memory] == 256:
                    self.memory[self.current_memory] = 0
            elif self.current_char == "-" or self.current_char == "−":
                self.memory[self.current_memory] -= 1
                if self.memory[self.current_memory] < 0:
                    self.memory[self.current_memory] = 255
            elif self.current_char == "[":
                if self.memory[self.current_memory] == 0:
                    self.skipInside()
                else:
                    self.current_loop += 1
                    if len(self.loop_position) <= self.current_loop:
                        self.loop_position.append(self.pos)
                    else:
                        self.loop_position[self.current_loop] = self.pos
            elif self.current_char == "]":
                if self.memory[self.current_memory] <= 0:
                    self.loop_position[self.current_loop] = 0
                    if self.current_loop != 0:
                        self.current_loop -= 1
                    else:
                        return print("Can't exit loop at char " + str(self.pos + 1))
                else:
                    self.pos = self.loop_position[self.current_loop]
            elif self.current_char == ">":
                self.current_memory += 1
                if len(self.memory) <= self.current_memory:
                    self.memory.append(0)
            elif self.current_char == "<":
                self.current_memory -= 1
                if self.current_memory < 0:
                    return print("Can't access memory at char " + str(self.pos + 1))
            elif self.current_char == ".":
                print(chr(self.memory[self.current_memory]), end='')
            elif self.current_char == ",":
                self.memory[self.current_memory] = ord(input(">")[0])
            else:
                if self.debug == 1:
                    print("Skip char")
            self.nextChar()
        if self.debug == 1:
            print("Final memory: ", self.memory)
        return print("")

def main():
    while True:
        debug = 0
        try:
            text = input('bfk> ')
        except EOFError:
            break
        if not text:
            continue
        if text == "help":
            print("write \"debug [your code]\" to activate debug mode")
            print("write \"read [your file]\" to run a brainfuck file (.bfk)")
            print("Hello World: ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>.+.")
        else:
            if text.find("debug") != -1:
                debug = 1
                print("Interpreting script with debug mode")
            if text.find("read") != -1:
                with open(re.search(r"[A-Za-z0-9.-_]+\.[bfk]+", text).group(), 'r') as content_file:
                    text = content_file.read()
            Interpreter(text, debug).expr()

if __name__ == '__main__':
    main()