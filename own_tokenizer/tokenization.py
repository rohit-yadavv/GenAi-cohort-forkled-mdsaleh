
class Encoder:
    def encode(self, text):
        encode = []
        splittedText = text.split()
        for word in splittedText:
            ascii_value_tokens = "".join(str(ord(char)) for char in word) # converting ascii value in to string
            encode.append(int(ascii_value_tokens))
            
        return encode
        

    def decode(self, tokens):
        decoded = []
        pass



encoder = Encoder()
text = "Hello How are you"
tokens = encoder.encode(text)
print("Tokens: ", tokens)
tokensDecode = encoder.decode([72101108108111, 72111119, 97114101, 121111117])
print("Decode: ", tokensDecode)


# ord() ===> is a built-in Python function that takes a single character (like 'a', 'Z', or '@') and returns its Unicode (ASCII) number.

# The chr() function takes an integer (representing a Unicode/ASCII code) and returns the character for that code.

# ord('A') → 65
# chr(65) → 'A'

# ''.join(...) --> Joins all those strings into one string, with nothing in between ('' means no space or separator).

# list(string) → breaks it into characters
# string.split() → splits it into words using spaces