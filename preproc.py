import sqlite3
import re
import csv

# TODO mejorar el reonocimiento de palabras con guiones
# y examinar palabras largas


litecon = sqlite3.connect('mfrases.db')
cursor = litecon.cursor()

banned_words = ['the', 'of', 'and', 'that',
                'have', 'for', 'not', 'on', 'with', 'je', 'à', 'il', 'est', 'ou', 'non', 'sia', 'ou', 'qui', 'quando', 'sempre']
#
spanish_words = ['que', 'los', 'se', 'por', 'una', 'uno',
                 'su', 'para', 'como', 'sobre', 'entre', 'porque']

word_dict = {}

usable_count = 0
total_count = 0

fo = open('oraciones.txt', 'w+', encoding='UTF-8')


for (idx, row) in enumerate(cursor.execute("SELECT quote_text FROM wikiquote")):
    # print("{}. {}".format(idx, row[0]))

    full_quote = row[0]

    # oraciones = full_quote.split("")
    oraciones = re.split("[.?!¡¿]", full_quote)
    oraciones = [x.strip().lower()
                 for x in oraciones if re.match(r"[\w]+", x.strip())]
    # print(oraciones)
    for o in oraciones:
        # o = [x for x in o.strip().lower() if re.match("[\w]+", x)]
        palabras = re.split("[ (,)(;)(:)]", o)  # o.split(" ")

        is_banned = any(item in palabras for item in banned_words)
        is_spanish = any(item in palabras for item in spanish_words)
        # if (is_english):
        # print("-> en={}\tes={}\t: {}".format(is_english, is_spanish, o))
        total_count += 1

        if (is_spanish == True and is_banned == False):
            # print(o)
            usable_count += 1
            fo.write(o + '\n')

            for word in palabras:
                word = re.sub(r"[^\w]", "", word)
                if re.match(r"[\w]+", word) == None:
                    continue
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        elif (is_spanish == True and is_banned == True):
            print(o)

    if idx == 100000:
        break

fo.close()

print('{} / {} quotes can be used!'.format(usable_count, total_count))

with open('wordcount.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'frequency'])

    for row in word_dict:
        writer.writerow([row, word_dict[row]])
