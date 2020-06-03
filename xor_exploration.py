import json
from pathlib import Path
import sys

from myio.myio import auto_make_open


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


def toggle_prefix(text, prefix):
    ''' If the string starts with the prefix,
    remove it. Otherwise, insert it.
    '''
    if text.startswith(prefix):
        # 3.8: slice off prefix
        # 3.9: removeprefix()
        result = text[len(prefix):]
    else:
        result = prefix + text
    return result


@auto_make_open('infile', mode='rb')
@auto_make_open('outfile', mode='wb')
def _xorfile(infile, outfile, prefix):
    byte = infile.read(1)
    while len(byte) == 1:
        outfile.write(bytes([ord(byte) ^ KEY]))
        byte = infile.read(1)
    return outfile.name


def xorfile(infile, outfile="", prefix="decrypted_"):
    infile = Path(infile)
    if not outfile:
        outfile = infile.with_name(toggle_prefix(infile.name, prefix))

    return Path(_xorfile(infile=infile, outfile=outfile, prefix=prefix))


def main():
    outfile = xorfile("heavensVaultSave.json")

    with open(outfile, "r") as fd_data:
        fd_data.read(6)
        lines = [line.strip() for line in fd_data]

    game_state = json.loads(lines[6])
    dictionary = game_state["player"]["lexDictionary"]["_lexDictionary"]

    words = list(dictionary.keys())
    known_words = [
        word for word in dictionary
        if dictionary[word].get("known", None)
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
