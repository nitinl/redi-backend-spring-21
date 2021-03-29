"""
Date: 29/3/21
Description: Count the frequency of letters in a file.
"""
from collections import defaultdict


def compute_frequencies(input_file):
    letter_frequencies = defaultdict(int)
    with open(input_file, 'r') as input_stream:
        for line in input_stream:
            for character in line.lower():
                if character.isalpha():
                    letter_frequencies[character] = letter_frequencies[character] + 1
    return letter_frequencies


def dictionary_to_sorted_list(data):
    items = list(data.items())
    items.sort(key=lambda x: (-x[1], x[0]))
    return items


def write_list_to_file(data, output_file):
    formatted_list = [f'{letter}: {count}' for letter, count in data]
    with open(output_file, 'w') as output_sink:
        output_sink.write(str(formatted_list))


if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.txt'
    frequencies = compute_frequencies(input_file)
    sorted_frequencies = dictionary_to_sorted_list(frequencies)
    write_list_to_file(sorted_frequencies, output_file)
