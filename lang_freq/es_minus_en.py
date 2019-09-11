

f_es = open('es_dict.txt', 'r')
f_en = open('en_dict.txt', 'r')

f_out = open('es-en.txt', 'w+')


es_words = f_es.readlines()
en_words = f_en.readlines()

for word in es_words:
    if word not in en_words:
        print(word)
        f_out.write(word)

f_out.close()
f_es.close()
f_en.close()
