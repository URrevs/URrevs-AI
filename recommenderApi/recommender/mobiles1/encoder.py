from recommenderApi.imports import dump, load, pd, np

class one_hot_encoder:
    def __init__(self, apply = 0, missing_values: str = 'added') -> None:
        self.apply = apply
        self.missing_values = missing_values

    def fit(self, data) -> None:
        self.categories = {}
        self.counter = 0
        for item in data:
            if self.apply == 1: item = str(item).replace('"', '').strip().lower()
            try: self.categories[item]
            except: self.categories[item] = self.counter; self.counter += 1

    def transform(self, data, val):
        lst = self.get_features()
        if len(lst) == 0: return None
        self.outDf = pd.DataFrame(0, index=np.arange(len(data)), columns=lst)
        for i in range(len(data)):
            if data[i] in lst:
                self.outDf.loc[i, data[i]] = val
            else:
                if self.missing_values == 'added':
                    self.categories[data[i]] = self.counter; self.counter += 1
                    self.outDf[data[i]] = [val if j == i else 0 for j in range(len(data))]
                    lst.append(data[i])
                else: pass
        return self.outDf
    
    def fit_transform(self, data, val):
        self.fit(data)
        return self.transform(data, val)

    def get_features(self):
        try: return list(self.categories.keys())
        except: return []

    def set_features(self, features):
        self.categories = {}
        for i in range(len(features)):
            self.categories[features[i]] = i
        self.counter = len(features)

    def append_features(self, features):
        for feature in features:
            self.categories[feature] = self.counter
            self.counter += 1

    def save_model(self, path):
        dump(self, open(path, 'wb'))

    def load_model(self, path):
        self = load(open(path, 'rb'))
        return self

