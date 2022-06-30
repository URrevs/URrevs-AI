from recommenderApi.imports import dump, load, pd, np

class one_hot_encoder:
    def __init__(self) -> None:
        pass

    def fit(self, data) -> None:
        self.categories = {}
        self.counter = 0
        for item in data:
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
                self.categories[data[i]] = self.counter; self.counter += 1
                self.outDf[data[i]] = [val if j == i else 0 for j in range(len(data))]
                lst.append(data[i])
        return self.outDf
    
    def fit_transform(self, data, val):
        self.fit(data)
        return self.transform(data, val)

    def get_features(self):
        try: return list(self.categories.keys())
        except: return []
    
    def save_model(self, path):
        dump(self, open(path, 'wb'))

    def load_model(self, path):
        self = load(open(path, 'rb'))
        return self

