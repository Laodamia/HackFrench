import re
string = 'Je mange9 un énorme sandwich avec un morceau de chat. invraisemblable '

# text = re.search('é', string)

# if text:
	# print(text.group())

# matches 'e' only if: 1/ followed by a space, number or any of the listed punctuation marks (end of word), and 
# 2/ is preceded by g
# replaces 'e' with 0

k = re.sub(r"(?<=g)e(?=[\.,?!:\s0-9])", 'O', string)
print(k)
