from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS
from recommenderApi.imports import dump

def calc_anonymous_data():
    sql = SQLite_Database()
    items = []
    cques = sql.get_answered_Cquestions(answer=True, limit=50)
    pques = sql.get_answered_Pquestions(answer=True, limit=100-len(cques))
    rest = 100 - len(pques) - len(cques)
    if rest % 2 == 0: prevs = sql.get_Prevs(limit=50+rest//2)
    else: prevs = sql.get_Prevs(limit=51+rest//2)
    crevs = sql.get_Crevs(limit=50+rest//2)
    items.extend(cques); items.extend(pques); items.extend(crevs); items.extend(prevs)
    items.sort(key=lambda x: (-x[1], -x[2], -x[3], -x[4]))
    counter = 0; iter = 0
    pques = []; cques = []; prevs = []; crevs = []; total = []; final = []
    for item in items:
        total.append(item[0][1:])
        if item[0][0] == '0': prevs.append(item[0][1:])
        if item[0][0] == '1': crevs.append(item[0][1:])
        if item[0][0] == '2': pques.append(item[0][1:])
        if item[0][0] == '3': cques.append(item[0][1:])
        counter += 1
        if counter == ROUND_NUM_OF_REVIEWS: 
            counter = 0
            final.append([prevs, crevs, pques, cques, total])
            pques = []; cques = []; prevs = []; crevs = []; total = []
            iter += 1
    dump(final, open('recommender/collobarative/anonymous_data.pkl', 'wb'))
    return final
