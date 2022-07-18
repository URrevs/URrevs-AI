from recommenderApi.imports import NearestNeighbors, os, pd, Tuple, MinMaxScaler, dump, load, nltk
from recommenderApi.file import FileData
from recommender.reviews.text import TextFeatureExtraction
from recommender.sqliteDB.data import SQLite_Database

class ReviewContentRecommender:
    def __init__(self) -> None:
        return

    def load_data(self, recommend_type: str = 'product') -> Tuple[pd.DataFrame, bool]:
        '''
            function to load reviews data

            parameters: the file name
            output: the data and the check
        '''
        self.recommend_type = recommend_type
        sqlite = SQLite_Database()
        if self.recommend_type == 'product':
            self.data = sqlite.get_Preview()
        else:
            self.data = sqlite.get_Creview()
        self.data = pd.DataFrame(list(self.data.values()))
        self.data.index = self.data['id']
        self.data.drop('id', axis=1, inplace=True)
        return self.data

    def prepare_data(self, columns: list = []) -> pd.DataFrame:
        '''
            function to prepare data

            parameters: the columns to prepare
            output: the data with the prepared columns
        '''
        if len(columns) == 0:
            columns = ['id', 'rating', 'rating1', 'rating2', 'rating3', 'rating4', 'rating5', 'rating6',
                    'pros', 'cons', 'pros_count', 'cons_count']
        for column in self.data.columns:
            if column not in columns:
                self.data.drop(column, axis=1, inplace=True)
        self.data['data'] = self.data['pros'] + ' ' + self.data['cons']
        self.data.drop('pros', axis=1, inplace=True)
        self.data.drop('cons', axis=1, inplace=True)
        model = TextFeatureExtraction()
        self.data = model.apply_TF_IDF(self.data, 'data', path='recommender/reviews/vectorizer.pkl', inplace=True)
        return self.data

    def scale_data(self) -> pd.DataFrame:
        '''
            function to scale data

            parameters: none
            output: the scaled data
        '''
        scaler = MinMaxScaler()
        self.data.fillna(0, inplace=True)
        data = scaler.fit_transform(self.data)
        self.data = pd.DataFrame(data, columns=self.data.columns, index=self.data.index)
        return self.data
    
    def preprocessing(self, recommend_type='product', path='recommender/reviews/prevs.pkl') -> None:
        '''
            function to train the recommender

            parameters: the file name
            output: none
        '''
        self.load_data(recommend_type=recommend_type)
        print('data loaded')
        self.prepare_data()
        print('data prepared')
        self.scale_data()
        print('data scaled')
        dump(self.data, open(path, 'wb'))
        return

    def recommend(self, referenceId: str = '', recommend_type: str = 'product', n_recommendations: int = -1, 
            items: list = [], known_items:list = []):
        '''
            function to recommend reviews

            parameters: the number of recommendations
            output: the recommendations
        '''
        path = 'recommender/reviews/prevs.pkl' if recommend_type == 'product' else 'recommender/reviews/crevs.pkl'
        if not os.path.exists(path):
            self.preprocessing(recommend_type=recommend_type, path=path)
        data: pd.DataFrame = load(open(path, 'rb'))
        if len(items) != 0:
            data = data[data.index.isin(items)]
            # print(data.shape, len(items))
            # print(data)
            # data.index = items
        if len(known_items) != 0:
            data = data[~data.index.isin(known_items)]
            
        if n_recommendations == -1: n_recommendations = data.shape[0]-1 # len(items)-1
        nbrs: NearestNeighbors = NearestNeighbors(n_neighbors=n_recommendations+1, metric='cosine', algorithm='auto')
        nbrs.fit(data.values)
        distances, indices = nbrs.kneighbors(data.loc[referenceId, :].values.reshape(1, -1))
        recommendations = []
        for i in range(len(indices)):
            recommendations.append(data.iloc[indices[i]].index)
        return recommendations[0].tolist(), distances[0].tolist()

    def evaluate_rmse(self, rating: float, referenceId: str = '', recommend_type: str = 'product', 
        n_recommendations: int = -1, items: list = [], ratings: list = [], known_items:list = []) -> float:
        '''
            function to evaluate the rmse

            parameters: the number of recommendations
            output: the rmse
        '''
        recommendations, distances = self.recommend(referenceId=referenceId, recommend_type=recommend_type, n_recommendations=n_recommendations, 
            items=items, known_items=known_items)
        rmse = 0
        for i in range(len(recommendations)):
            rmse += (ratings[i] - distances[i]*rating)**2 / len(recommendations)
        return rmse**0.5

# model = ReviewContentRecommender()
# model.preprocessing(file_name='/recommender/static/data/reviews.xlsx', path='/recommender/static/data/')
# recs, spaces = model.recommend(3, 9)
# for rec, space in zip(recs, spaces):
#     print(model.data.loc[rec, :])
# print(model.data.head(5))
