import ast
import string
import re
import collections

class ObfuscationDetector(ast.NodeVisitor):
    def __init__(self):
        self.obfuscation_score = 0
        self.variable_names = []

    def visit_Name(self, node):
        self.variable_names.append(node.id)
        super().visit_Name(node)

    def detect_obfuscation(self, code):
        self.visit(ast.parse(code))

        # Check for non-English or single character variable names
        with open('english_words.txt', 'r') as f:  # A file containing common English words
            words = f.read().split()
        for name in self.variable_names:
            if len(name) == 1 or not any(word in name.lower() for word in words):
                self.obfuscation_score += 1

        # Check for base64 encoded strings
        base64_strings = re.findall(r'"[A-Za-z0-9+/]+={0,2}"', code)
        if base64_strings:
            self.obfuscation_score += len(base64_strings)

        # Check for lack of comments
        if "#" not in code:
            self.obfuscation_score += 1

        # Print obfuscation score
        print(f'Obfuscation score: {self.obfuscation_score}')
        return self.obfuscation_score > 10  # Threshold for considering a code as obfuscated

detector = ObfuscationDetector()
code = """
import base64
a = base64.b64encode(b"Hello, World!")
b = 1
for i in range(10):
    b += i
"""
print(detector.detect_obfuscation(code))