from numpy import minimum
from recommender.mongoDB.getData import MongoConnection
from recommenderApi.imports import dt, dump, load, pd, NearestNeighbors
from recommender.mobiles1.extract import ExtractFeatures
from recommender.mobiles1.encoder import one_hot_encoder

class Scaler:
    def __init__(self, in_ = (0, 1), out_ = (0, 1)):
        self.in_ = in_
        self.out_ = out_

    def scale(self, input):
        return ((input-self.in_[0])/(self.in_[1]-self.in_[0]))*(self.out_[1]-self.out_[0])+self.out_[0]

def dateAsInteger(self, date: dt) -> float:
        reference: dt = dt(1999, 1, 1)
        try:
            return (date - reference).total_seconds()
        except:
            print(f'"{date}" is not valid input')
            return 0

def date_convert(date: str):
    if date == '': out = '1999'
    else: out = date
    try: out = dt.strptime(out, '%Y, %B %d')
    except: 
        try: out = dt.strptime(out, '%Y, %B')
        except: 
            try: out = dt.strptime(out, '%Y')
            except: out = dt(1999, 1, 1)
    return ExtractFeatures().dateAsInteger(out)

class Similar_Phones:
    def __init__(self, phone_id = None):
        '''
            class to get similar phones to a given phone
            Args:  phone_id (str)
        '''
        self.phone_id = phone_id

    def get_phones_from_DB(self, date: dt):
        phones = MongoConnection().get_phones_mongo(date)
        mobiles = []
        for phone in phones:
            mobiles.append(phone)
        dump(mobiles, open('recommender/mobiles1/mobiles.pkl', 'wb'))

    def load_all_phones(self):
        self.mobiles = load(open('recommender/mobiles1/mobiles.pkl', 'rb'))
        return self.mobiles

    def make_comparison_table(self):
        self.load_all_phones()
        self.table = pd.DataFrame().from_dict(self.mobiles)
        print(self.table)
        self.table.to_excel('recommender/mobiles1/mobiles_table.xlsx')

    def min_max_scale(self):
        specs = {
            'price': 15,
            'releaseDate': 9,
            'company': 9,
            'dimensions': 4,
            'batteryCapacity': 4,
            'os': 4,
        }
        self.table = pd.read_excel('recommender/mobiles1/mobiles_table.xlsx')
        length = self.table.shape[0]
        newDF = pd.DataFrame()
        # for spec in ['os']:
        # weight = 2, fast charging = 2
        for spec in ['price', 'releaseDate', 'company', 'dimensions', 'batteryCapacity', 'os']:
            if spec == 'price':
                col = self.table.loc[:, [spec]].astype(float).fillna(0)
                print('nulls are filled')
            if spec == 'batteryCapacity':
                col = pd.DataFrame({'dimensions': length * [0]})
                for i in range(length):
                    try: col.loc[i, 'dimensions'] = float(self.table.loc[i, 'batteryCapacity'])  
                    except: pass
            if spec == 'releaseDate':
                col = self.table.loc[:, ['releaseDate']]
                arr = [date_convert(col.values[i][0]) for i in range(len(col.values))]
                col['releaseDate'] = arr
            if spec == 'dimensions':
                col = pd.DataFrame({'dimensions': length * [0]})
                for i in range(length):
                    try: col.loc[i, 'dimensions'] = float(self.table.loc[i, 'height'])*float(self.table.loc[i, 'width'])*float(self.table.loc[i, 'length'])
                    except: pass
            if spec in ['price', 'releaseDate', 'dimensions', 'batteryCapacity']:
                minimum = min(col.values)[0]
                maximum = max(col.values)[0]
                print(minimum, maximum)
                newDF[spec] = col.apply(Scaler(in_ = (minimum, maximum), out_ = (0, specs[spec])).scale, axis = 1)
            if spec == 'os':
                col = pd.DataFrame({'os': length * ['']})
                for i in range(length):
                    col.loc[i, 'os'] = str(self.table.loc[i, 'os']).split()[0].lower()
                enc = one_hot_encoder()
                col = enc.fit_transform(col.loc[:, 'os'].values, specs['os']/2)
                newDF = pd.concat([newDF, col], axis = 1)
                # newDF[spec] = col.apply(lambda x: x.str.split(',').str[0].str.strip().str.lower().str.replace(' ', '_').str[0])
            if spec == 'company':
                enc = one_hot_encoder()
                col = enc.fit_transform(self.table.loc[:, 'company'].values, specs['company']/2)
                newDF = pd.concat([newDF, col], axis = 1)
            # print(newDF)
        newDF.index = self.table['_id']
        newDF.fillna(0, inplace = True)
        print('price is scaled')
        print(newDF)
        newDF.to_csv('recommender/mobiles1/mobiles_table_mod.csv')

    def generate_20_similars(self, phoneId: str):
        self.table = pd.read_csv('recommender/mobiles1/mobiles_table_mod.csv', index_col='_id')
        self.table.fillna(0, inplace = True)
        # print(self.table)
        nbrs: NearestNeighbors = NearestNeighbors(n_neighbors=21, algorithm='ball_tree')
        nbrs.fit(self.table.values)
        # print(self.table.loc[phoneId, :].values)
        distances, indices = nbrs.kneighbors(self.table.loc[phoneId, :].values.reshape(1, -1))
        recommendations = []
        for i in range(len(indices)):
            recommendations.extend(self.table.iloc[indices[i]].index)
        # print(recommendations[1:])
        return recommendations[1:]

