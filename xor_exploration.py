import json
from pathlib import Path
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


def xorfile(infile: Path, outfile="", prefix="decrypted_"):
    if infile.name.startswith(prefix):
        outfile = infile.with_name(infile.name[len(prefix):])
    else:
        outfile = infile.with_name(prefix + infile.name)

    with open(outfile, 'wb') as fd_out:
        with open(infile, 'rb') as fd_in:
            byte = fd_in.read(1)
            while len(byte) == 1:
                fd_out.write(bytes([ord(byte) ^ KEY]))
                byte = fd_in.read(1)
    return outfile


def main():
    xorfile("heavensVaultSave.json")

    with open("decrypted_heavensVaultSave.json", "r") as fd_data:
        fd_data.read(6)
        lines = [line.strip() for line in fd_data]
    game_state = json.loads(lines[6])
    dictionary = game_state["player"]["lexDictionary"]["_lexDictionary"]
    words = list(dictionary.keys())
    known_words = [
        word for word in dictionary
        if dictionary[word].get("known", False)
        ]
    wrong_words = [
        (word, dictionary[word]["_suggestedWordString"])
        for word in dictionary
        if dictionary[word].get("_suggestedWordString", "") != word
        ]

    print(f'{len(words)=}')
    print(f'{len(known_words)=}')
    print(f'{len(wrong_words)=}')


if __name__ == '__main__':
    sys.exit(main())
