"""
Date: 29/3/21
Description: encrypt / decrypt text file using XOR cipher
"""


def xor_text(input_string, key):
    result = ''
    for char in input_string:
        ciphered_char = chr(ord(char) ^ key)
        result += ciphered_char
    return result


if __name__ == '__main__':
    input_file = 'input.txt'
    key = 23
    with open(input_file, 'r') as fp:
        file_content = fp.read()
    print(f'Input: {file_content}')
    encrypted_text = xor_text(file_content, key)
    print(f'encrypted text: {encrypted_text}')
    decrypted_text = xor_text(encrypted_text, key)
    print(f'decrypted text: {decrypted_text}')
