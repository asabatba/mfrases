import sqlite3
import re
import csv

litecon = sqlite3.connect('mfrases.db')
cursor = litecon.cursor()

english_words = ['the', 'of', 'and', 'that',
                 'have', 'for', 'not', 'on', 'with']

spanish_words = ['que', 'los', 'se', 'por', 'una', 'uno',
                 'su', 'para', 'como', 'sobre', 'entre', 'porque']

word_dict = {}

for (idx, row) in enumerate(cursor.execute("SELECT quote_text FROM wikiquote")):
    # print("{}. {}".format(idx, row[0]))

    full_quote = row[0]

    # oraciones = full_quote.split("")
    oraciones = re.split("[.?!¡¿]", full_quote)
    oraciones = [x.strip().lower()
                 for x in oraciones if re.match("[\w]+", x.strip())]
    # print(oraciones)
    for o in oraciones:
        # o = [x for x in o.strip().lower() if re.match("[\w]+", x)]
        palabras = re.split("[ (,)(;)(:)]", o)  # o.split(" ")

        is_english = any(item in palabras for item in english_words)
        is_spanish = any(item in palabras for item in spanish_words)
        # if (is_english):
        # print("-> en={}\tes={}\t: {}".format(is_english, is_spanish, o))
        if (is_spanish):
            # print(o)
            for word in palabras:
                word = re.sub("[^\w]", "", word)
                if re.match("[\w]+", word) == None:
                    continue
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

    if idx == 100000:
        break


with open('wordcount.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'frequency'])

    for row in word_dict:
        writer.writerow([row, word_dict[row]])
