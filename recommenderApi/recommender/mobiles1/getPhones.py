# from recommender.mongoDB.getData import MongoConnection
from recommenderApi.imports import dt, dump, load, pd, NearestNeighbors
from recommender.mobiles1.encoder import one_hot_encoder
from recommender.mobiles1.utils import *
from recommenderApi.settings import *
from recommender.sqliteDB.data import SQLite_Database

class Scaler:
    def __init__(self, in_ = (0, 1), out_ = (0, 1)):
        self.in_ = in_
        self.out_ = out_

    def scale(self, input):
        return ((input-self.in_[0])/(self.in_[1]-self.in_[0]))*(self.out_[1]-self.out_[0])+self.out_[0]

    def add_new_range(self, new_range):
        self.in2_ = new_range
    
    def rescale(self, input1):
        old = ((input1-self.out_[0])/(self.out_[1]-self.out_[0]))*(self.in_[1]-self.in_[0])+self.in_[0]
        return ((old-self.in2_[0])/(self.in2_[1]-self.in2_[0]))*(self.out_[1]-self.out_[0])+self.out_[0]
    
    def submit_range(self):
        self.in_ = self.in2_
        self.in2_ = None
    
    def get_range(self):
        return self.in_

    def save(self):
        return self.in_

class Similar_Phones:
    def __init__(self, phone_id = None, mongo = None):
        '''
            class to get similar phones to a given phone
            Args:  phone_id (str)
        '''
        self.phone_id = phone_id
        self.mongo = mongo

    def get_phones_from_DB(self, date: dt):
        phones = self.mongo.get_phones_mongo(date)
        self.mobiles = []
        for phone in phones:
            self.mobiles.append(phone)
        dump(self.mobiles, open('recommender/mobiles1/mobiles.pkl', 'wb'))

    def load_all_phones(self):
        self.mobiles = load(open('recommender/mobiles1/mobiles.pkl', 'rb'))
        return self.mobiles

    def make_comparison_table(self, mobiles):
        # self.load_all_phones()
        # self.table = pd.DataFrame().from_dict(mobiles)
        # print(self.table)
        # self.table.to_excel('recommender/mobiles1/mobiles_table.xlsx')
        return pd.DataFrame().from_dict(mobiles)

    def load_constraints(self):
        try: self.constraints = load(open('recommender/mobiles1/constraints.pkl', 'rb'))
        except:
            # get all phones as dataframe
            self.get_phones_from_DB(dt(2020, 1, 1))
            df = self.make_comparison_table()
            # generate table and constraints
            self.min_max_scale(df)

    def load_specs(self):
        self.specs = {
            'price': SPECS_PRICE, 'releaseDate': SPECS_RELEASE_DATE, 
            'company': SPECS_COMPANY / SPECS_COMPANY_DECREASE_FACTOR, 'dimensions': SPECS_DIMENSIONS, 
            'batteryCapacity': SPECS_BATTERY_CAPACITY, 'os': SPECS_OS / SPECS_OS_DECREASE_FACTOR, 
            'weight': SPECS_WEIGHT, 'hasFastCharging': SPECS_HAS_FAST_CHARGING, 
            'screenType': SPECS_SCREEN_TYPE / SPECS_SCREEN_TYPE_DECREASE_FACTOR, 
            'screenSize': SPECS_SCREEN_SIZE, 'screen2bodyRatio': SPECS_SCREEN_2BODY_RATIO,
            'screenResolution': SPECS_SCREEN_RESOLUTION, 'resolutionDensity': SPECS_RESOLUTION_DENSITY, 
            's0': 0.5*(SPECS_INT_MEM // 2), 'm0': 0.5*(SPECS_INT_MEM // 2), 's1': 0.5*(SPECS_INT_MEM // 2), 
            'm1': 0.5*(SPECS_INT_MEM // 2), 's2': 0.5*(SPECS_INT_MEM // 4), 'm2': 0.5*(SPECS_INT_MEM // 4), 
            'camNum0': (SPECS_MAIN_CAM // 2), 'camMP0': (SPECS_MAIN_CAM // 2), 
            'camNum1': (SPECS_SELFIE_CAM // 2), 'camMP1': (SPECS_SELFIE_CAM // 2), 
            'hasLoudspeaker': SPECS_HAS_LOUDSPEAKER, 'hasStereo': SPECS_HAS_STEREO, 'has3p5mm': SPECS_HAS_3P5MM, 
            'hasNfc': SPECS_HAS_NFC, 'hasGyro': SPECS_HAS_GYRO, 'hasProximity': SPECS_HAS_PROXIMITY,
            'network': SPECS_NETWORK / SPECS_NETWORK_DECREASE_FACTOR, 
            'bluetoothVersion': SPECS_BLUETOOTH_VERSION, 'usbVersion': SPECS_USB_VERSION,
            'usbType': SPECS_USB_TYPE / SPECS_USB_TYPE_DECREASE_FACTOR,
            'cpu': SPECS_CPU / SPECS_CPU_DECREASE_FACTOR, 'gpu': SPECS_GPU / SPECS_GPU_DECREASE_FACTOR,
        }

    def process(self, col: pd.DataFrame, col_names = [], val = 1, data_type: str = 'numeric', fun: str = 'intMem'):
        length = col.shape[0]
        if data_type == 'numeric':
            return pd.to_numeric(col, errors='coerce').fillna(0).astype(float)
        elif data_type == 'boolean':
            return col.apply(lambda x: val if str(x).lower() == 'true' else 0)
        elif data_type == 'date':
            return col.apply(lambda x: date_convert(str(x)))
        elif data_type == 'specific_numeric':
            cols = pd.DataFrame({'specific': length*[1]})
            for col_name in col_names:
                cols['specific']=cols['specific']*pd.to_numeric(col[col_name], errors='coerce').fillna(0).astype(float)
            return cols['specific']
        elif data_type == 'many':
            cols = pd.DataFrame()
            if fun == 'intMem': col = col.apply(lambda x: get_mem_ram(x))
            if fun == 'mainCam': col = col.apply(lambda x: get_cam(x))
            if fun == 'selfieCam': col = col.apply(lambda x: get_cam(x))
            if fun == 'cpu': col = col.apply(lambda x: get_cpu(x))
            for i in range(len(col_names)):
                cols[col_names[i]] = col.apply(lambda x: x[i])
            return cols
        elif data_type == 'specific_string':
            cols = pd.DataFrame({fun: length * ['']})
            if fun == 'os': cols[fun] = col.apply(lambda x: get_os(x))
            if fun == 'screenType': cols[fun] = col.apply(lambda x: get_screen_type(x))
            if fun == 'network': cols[fun] = col.apply(lambda x: get_network(x))
            if fun == 'usbType': cols[fun] = col.apply(lambda x: get_usb_type(x))
            return cols
        elif data_type == 'string':
            cols = pd.DataFrame({fun: length * ['']})
            cols[fun] = col.apply(lambda x: str(x).lower().replace(' ', ''))
            return cols

    def min_max_scale(self, cols: pd.DataFrame = pd.DataFrame(), repeat: bool = False):
        self.load_specs()
        if repeat: oldDF = pd.read_csv('recommender/mobiles1/mobiles_table_mod.csv')
        # cols = pd.read_excel('recommender/mobiles1/mobiles_table.xlsx')
        # cols = cols.loc[:75, :]
        # cols = cols.loc[76:100, :]
        newDF = pd.DataFrame()
        internal = {
            'intMem': ['s0', 'm0', 's1', 'm1', 's2', 'm2'],
            'mainCam': ['camNum0', 'camMP0'],
            'selfieCam': ['camNum1', 'camMP1'],
            'cpu': ['cpu_hz', 'col'],
            'dimensions': ['height', 'width', 'length'],
            'screenResolution': ['resolutionLength', 'resolutionWidth']
        }
        if not repeat: external = {}
        else:
            self.load_constraints()
            external = self.constraints
        for spec in ['price', 'releaseDate', 'company', 'dimensions', 'batteryCapacity', 'weight',
                'hasFastCharging', 'screenSize', 'screen2bodyRatio', 'screenResolution', 'usbVersion',
                'resolutionDensity', 'hasLoudspeaker', 'hasStereo', 'has3p5mm', 'hasNfc', 'hasGyro', 
                'hasProximity', 'bluetoothVersion']:
            #,'mainCam','os','intMem','selfieCam','usbType','network','screenType','usbVersion','cpu','gpu']:
            # --------------------------------------------------------------------------------------------
            # NUMERIC DATA
            if spec == 'price' or spec == 'batteryCapacity' or spec == 'weight' or spec == 'screenSize'\
                or spec == 'screen2bodyRatio' or spec == 'resolutionDensity' or spec == 'bluetoothVersion'\
                or spec == 'usbVersion':
                cols[spec] = self.process(cols[spec], data_type='numeric')
            # --------------------------------------------------------------------------------------------
            # BOOLEAN DATA
            if spec == 'hasFastCharging' or spec == 'hasLoudspeaker' or spec == 'hasStereo'\
                or spec == 'has3p5mm' or spec == 'hasNfc' or spec == 'hasGyro' or spec == 'hasProximity':
                cols[spec] = self.process(cols[spec], val=self.specs[spec], data_type='boolean')
                newDF = pd.concat([newDF, cols[spec]], axis = 1)
            # --------------------------------------------------------------------------------------------
            # DATE DATA
            if spec == 'releaseDate':
                cols[spec] = self.process(cols[spec], data_type='date')
            # --------------------------------------------------------------------------------------------
            # MULTIPLYING NUMERIC DATA
            if spec == 'dimensions' or spec == 'screenResolution':
                cols[spec] = self.process(cols, col_names=internal[spec], data_type='specific_numeric')
            # --------------------------------------------------------------------------------------------
            # GENEATE DIFFERENT NUMERIC DATA
            if spec == 'intMem' or spec == 'mainCam' or spec == 'selfieCam':
                columns = self.process(cols[spec], col_names=internal[spec], data_type='many', fun=spec)
                for val in internal[spec]:
                    col = columns.loc[:, val]
                    if not repeat:
                        minimum = min(col.values)
                        maximum = max(col.values)
                        scaler = Scaler(in_ = (minimum, maximum), out_ = (0, self.specs[val]))
                        col = col.apply(scaler.scale)
                        newDF = pd.concat([newDF, col], axis = 1)
                    else:
                        (old_minimum, old_maximum) = external[val]
                        scaler = Scaler(in_ = external[val], out_ = (0, self.specs[val]))
                        minimum = min(col.values)
                        maximum = max(col.values)
                        if minimum > old_minimum and maximum < old_maximum:
                            col = col.apply(scaler.scale)
                            col = pd.concat([oldDF.loc[:, val], col], axis = 0, ignore_index=True).fillna(0)
                            print(col, newDF)
                            newDF = pd.concat([newDF, col], axis = 1)
                        else:
                            if minimum > old_minimum: minimum = old_minimum
                            if maximum < old_maximum: maximum = old_maximum
                            scaler.add_new_range((minimum, maximum))
                            old_col = oldDF.loc[:, val].apply(scaler.rescale)
                            scaler.submit_range()
                            col = col.apply(scaler.scale)
                            col = pd.concat([old_col, col], axis = 0, ignore_index=True)
                            newDF = pd.concat([newDF, col], axis = 1)
                    external[val] = (minimum, maximum)
            # --------------------------------------------------------------------------------------------
            # STRING DATA
            if spec == 'company' or spec == 'gpu':
                col = self.process(cols[spec], data_type='string', fun=spec)
                if not repeat:
                    enc = one_hot_encoder()
                    col = enc.fit_transform(col.loc[:, spec].values, self.specs[spec]/2)
                    newDF = pd.concat([newDF, col], axis = 1)
                else:
                    enc = one_hot_encoder(external[spec])
                    col = enc.transform(col.loc[:, spec].values, self.specs[spec]/2)
                    old_cols = oldDF.loc[:, enc.get_features()]
                    col = pd.concat([old_cols, col], axis = 0, ignore_index=True).fillna(0)
                    newDF = pd.concat([newDF, col], axis = 1)
                external[spec] = enc
            # --------------------------------------------------------------------------------------------
            # SPECIFIC FUNCTIONS FOR STRING DATA
            if spec == 'os' or spec == 'screenType' or spec == 'network' or spec == 'usbType':
                col = self.process(cols[spec], data_type='specific_string', fun=spec)
                if not repeat:
                    enc = one_hot_encoder()
                    col = enc.fit_transform(col.loc[:, spec].values, self.specs[spec]/2)
                    newDF = pd.concat([newDF, col], axis = 1)
                else:
                    enc = one_hot_encoder(external[spec])
                    col = enc.transform(col.loc[:, spec].values, self.specs[spec]/2)
                    old_cols = oldDF.loc[:, enc.get_features()]
                    col = pd.concat([old_cols, col], axis = 0, ignore_index=True).fillna(0)
                    newDF = pd.concat([newDF, col], axis = 1)
                external[spec] = enc
            # --------------------------------------------------------------------------------------------
            # GENERATE COMBINATION OF NUMERIC AND STRING DATA
            if spec == 'cpu':
                columns = self.process(cols[spec], col_names=internal[spec], data_type='many', fun=spec)
                col = columns.loc[:, 'cpu_hz']
                if not repeat:
                    minimum = min(col.values)
                    maximum = max(col.values)
                    scaler = Scaler(in_ = (minimum, maximum), out_ = (0, self.specs['cpu']/2))
                    col = col.apply(scaler.scale)
                    newDF = pd.concat([newDF, col], axis = 1)
                else:
                    (old_minimum, old_maximum) = external['cpu_hz']
                    scaler = Scaler(in_ = external['cpu_hz'], out_ = (0, self.specs['cpu']/2))
                    minimum = min(col.values)
                    maximum = max(col.values)
                    if minimum > old_minimum and maximum < old_maximum:
                        col = col.apply(scaler.scale)
                        col = pd.concat([oldDF.loc[:, 'cpu_hz'], col], axis = 0)
                        newDF = pd.concat([newDF, col], axis = 1)
                    else:
                        if minimum > old_minimum: minimum = old_minimum
                        if maximum < old_maximum: maximum = old_maximum
                        scaler.add_new_range((minimum, maximum))
                        old_col = oldDF.loc[:, 'cpu_hz'].apply(scaler.rescale)
                        scaler.submit_range()
                        col = col.apply(scaler.scale)
                        col = pd.concat([old_col, col], axis = 0)
                        newDF = pd.concat([newDF, col], axis = 1)
                external['cpu_hz'] = (minimum, maximum)

                if not repeat:
                    enc = one_hot_encoder()
                    col = enc.fit_transform(columns.loc[:, 'col'].values, self.specs['cpu']/4)
                    newDF = pd.concat([newDF, col], axis = 1)
                else:
                    enc = one_hot_encoder(external['cpu'])
                    col = enc.transform(columns.loc[:, 'col'], self.specs['cpu']/4)
                    old_cols = oldDF.loc[:, enc.get_features()]
                    col = pd.concat([old_cols, col], axis = 0, ignore_index=True).fillna(0)
                    newDF = pd.concat([newDF, col], axis = 1)
                external['cpu'] = enc
            # --------------------------------------------------------------------------------------------
            # SCALING NUMERIC DATA
            if spec in ['price', 'releaseDate', 'dimensions', 'batteryCapacity', 'weight', 'screenSize', 
                'screen2bodyRatio', 'screenResolution', 'resolutionDensity', 'bluetoothVersion', 'usbVersion']:
                if not repeat:
                    minimum = min(cols[spec].values)
                    maximum = max(cols[spec].values)
                    scaler = Scaler(in_ = (minimum, maximum), out_ = (0, self.specs[spec]))
                    cols[spec] = cols[spec].apply(scaler.scale)
                    newDF = pd.concat([newDF, cols[spec]], axis = 1)
                else:
                    (old_minimum, old_maximum) = external[spec]
                    scaler = Scaler(in_ = external[spec], out_ = (0, self.specs[spec]))
                    minimum = min(cols[spec].values)
                    maximum = max(cols[spec].values)
                    if minimum > old_minimum and maximum < old_maximum:
                        scaler = Scaler(in_ = (old_minimum, old_maximum), out_ = (0, self.specs[spec]))
                        cols[spec] = cols[spec].apply(scaler.scale)
                        col = pd.concat([oldDF.loc[:, spec], cols[spec]], axis = 0, ignore_index=True).fillna(0)
                        newDF = pd.concat([newDF, col], axis = 1)
                    else:
                        if minimum > old_minimum: minimum = old_minimum
                        if maximum < old_maximum: maximum = old_maximum
                        scaler.add_new_range((minimum, maximum))
                        old_col = oldDF.loc[:, spec].apply(scaler.rescale)
                        # old_col = oldDF.loc[:, spec]
                        scaler.submit_range()
                        cols[spec] = cols[spec].apply(scaler.scale)
                        cols[spec] = pd.concat([old_col, cols[spec]], axis = 0, ignore_index=True)
                        col = pd.concat([oldDF.loc[:, spec], cols[spec]], axis = 0, ignore_index=True).fillna(0)
                        newDF = pd.concat([newDF, col], axis = 1)
                external[spec] = (minimum, maximum)
        if not repeat: newDF.index = cols['_id']
        else: newDF.index = pd.concat([oldDF['_id'], cols['_id']], axis = 0)
        # print(newDF)
        newDF.fillna(0, inplace = True)
        dump(external, open('recommender/mobiles1/constraints.pkl', 'wb'))
        print('finish generating all values')
        # print(newDF)
        # print(external)
        newDF.to_csv('recommender/mobiles1/mobiles_table_mod.csv')
        # newDF.to_csv('recommender/mobiles1/one_spec.csv')

    def generate_n_similars(self, phoneId: str, n: int = 20):
        self.table = pd.read_csv('recommender/mobiles1/mobiles_table_mod.csv', index_col='_id')
        nbrs: NearestNeighbors = NearestNeighbors(n_neighbors=n+1, algorithm='ball_tree')
        nbrs.fit(self.table.values)
        _, indices = nbrs.kneighbors(self.table.loc[phoneId, :].values.reshape(1, -1))
        recommendations = []
        # names = []
        # sql = SQLite_Database()
        recommendations.extend(self.table.iloc[indices[0][1:]].index)
        # for id in recommendations:
        #     mobile = sql.get_mobile(id=id)
        #     names.append(mobile.name)
        # print(names)
        return recommendations
    

