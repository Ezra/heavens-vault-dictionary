import json
import sys


# File format:
# Six-byte header. Constant. By inspection you can tell
#       whether the xor encryption has been applied.
# line 0 (JSON): file format info (format version number)
# blank line
# line 2 (JSON): originating software (Heaven's Vault, version number)
# blank line
# line 4 (JSON): save file description
# blank line
# line 6 (JSON): major state (most of the useful info, over half the file)
# blank line
# line 8 (JSON): execution status
#       (huge lists of minor trivia, most of the rest of the file)

''' xor-key for decrypting the save file '''
KEY = ord('a')

''' headers for valid save files '''
HEADERS = {
    b'HV\x01\xb6\x87\x4d': 'encrypted',
    b')7\x60\xd7\xe6\x2c': 'decrypted',
}


def xorfile(input, output="", prefix="decrypted_"):
    if input.startswith(prefix):
        output = input[len(prefix):]
    else:
        output = prefix+input
    with open(output, 'wb') as f:
        with open(input, 'rb') as g:
            byte = g.read(1)
            while len(byte) == 1:
                f.write(bytes([ord(byte) ^ KEY]))
                byte = g.read(1)


def main():
    xorfile("heavensVaultSave.json")

    with open("decrypted_heavensVaultSave.json", "r") as f:
        f.read(6)
        lines = [l.strip() for l in f]
    j = json.loads(lines[6])
    word_dict = j["player"]["lexDictionary"]["_lexDictionary"]
    words = list(word_dict.keys())
    known_words = [i for i in word_dict if word_dict[i].get("known", False)]
    wrong_words = [(i, word_dict[i]["_suggestedWordString"])
                   for i in word_dict if word_dict[i].get("_suggestedWordString", "") != i]

    print(f'{len(words)=}')
    print(f'{len(known_words)=}')
    print(f'{len(wrong_words)=}')


if __name__ == '__main__':
    sys.exit(main())
