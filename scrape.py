import requests
import re
import sqlite3
import concurrent.futures

NUM_OF_PAGES_TO_LOAD = 500

# ?action=query&generator=random&grnnamespace=0&grnlimit=2&prop=info&format=json


def page_parse(page):

    sqls = []
    pp = {'action': 'parse',
          'page': page['title'], 'format': 'json', 'prop': 'sections'}
    page_sections = requests.get(api_url, pp)
    page_id = page_sections.json()['parse']['pageid']
    print('page_title: {} (id={})'.format(page['title'], str(page_id)))
    page_title = page['title']
    # print(page_sections.json())

    matches = [x for x in page_sections.json()['parse']['sections']
               if 'Citas' in x['line']]
    # print(matches)
    if (len(matches) > 0):
        ppp = {'action': 'parse',
               'page': page['title'], 'format': 'json', 'prop': 'text', 'section': matches[0]['index']}
        page_content = requests.get(api_url, ppp)
        page_citas_text = page_content.json()['parse']['text']['*']

        # print(page_citas_text)
        # print(page_citas_text.find('«'))
        all_citas = re.findall("«([^«»<>]+)»", page_citas_text)
        if len(all_citas) < 1:
            return False
        page_title_insert = "INSERT INTO wikiquote_pagenames VALUES({},'{}') ON CONFLICT (pageid) DO NOTHING".format(
            page_id, page_title.replace("'", "''"))
        # cursor.execute(page_title_insert)
        sqls.append(page_title_insert)

        for (idx, cita) in enumerate(all_citas):
            # print(str(idx) + '. '+cita)
            quote_insert = "INSERT INTO wikiquote VALUES({},{},'{}') ON CONFLICT (pageid,quote_index) DO UPDATE SET quote_text=excluded.quote_text".format(
                page_id, idx, cita.replace("'", "''"))
            # print(quote_insert)
            # cursor.execute(quote_insert)
            sqls.append(quote_insert)

    return sqls


if __name__ == "__main__":

    litecon = sqlite3.connect('mfrases.db')
    cursor = litecon.cursor()

    api_url = 'https://es.wikiquote.org/w/api.php'

    while (True):
        p = {'action': 'query', 'list': 'random',
             'rnlimit': NUM_OF_PAGES_TO_LOAD, 'format': 'json'}
        response = requests.get(api_url, params=p)
        response_pages = response.json()['query']['random']

        # print(response)
        # print(response.json())
        # i = 0
        sqls = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
            future_to_page = {executor.submit(
                page_parse, page): page for page in response_pages}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                data = future.result()
                sqls = sqls + data

            except Exception as exc:
                print('%r generated an exception: %s' % (page, exc))
            else:
                print('%r page is ok!' % (page))

        print(sqls)
        for sql in sqls:
            cursor.execute(sql)

        # for page in response_pages:
        #     page_parse(page)
        #     litecon.commit()

        litecon.commit()
    cursor.close()
