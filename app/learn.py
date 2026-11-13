import unicodedata

text = "नेपाल"

for char in text:
    print(char, hex(ord(char)), unicodedata.name(char))

nfc = unicodedata.normalize("NFC", text)
nfd = unicodedata.normalize("NFD", text)

print(nfc)
print(nfd)
print(nfc == nfd)
