def xorfile(input, output="", prefix = "decrypted_"):
    if input.startswith(prefix):
        output = input[len(prefix):]
    else:
        output= prefix+input
    with open(output,'wb') as f:
        with open(input,'rb') as g:
            byte = g.read(1)
            while len(byte) == 1:
                f.write(bytes([ord(byte)^97]))
                byte = g.read(1)

xorfile("heavensVaultSave.json")

with open("decrypted_heavensVaultSave.json", "r") as f:
    f.read(6)
    lines = [l.strip() for l in f]
import json
j = json.loads(lines[6])
word_dict = j["player"]["lexDictionary"]["_lexDictionary"]
words = list(word_dict.keys())
known_words = [i for i in word_dict if word_dict[i].get("known", False)]
wrong_words = [(i,word_dict[i]["_suggestedWordString"]) for i in word_dict if word_dict[i].get("_suggestedWordString", "") != i]
print(len(words))
print(len(known_words))
print(len(wrong_words))