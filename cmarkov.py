import csv
import pandas as pd
import markovify


with open('oraciones.txt', encoding='UTF-8') as f:
    text = f.read()

text_model = markovify.NewlineText(text, state_size=3)

for i in range(20):
    print(text_model.make_sentence())

# memdict = []
# with open('wordcount.csv', newline='', encoding='UTF-8') as f:
#     reader = csv.reader(f)

#     for row in reader:
#         # print(row)

#         if (row[1] == 'frequency'):
#             continue
#         word = row[0]
#         freq = int(row[1])

#         if freq >= 5:
#             memdict.append(word)

# print(len(memdict))
