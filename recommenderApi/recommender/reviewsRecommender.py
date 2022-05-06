from recommenderApi.imports import NearestNeighbors, os, pd, Tuple, MinMaxScaler, dump, load
from recommenderApi.file import FileData
from recommender.text import TextFeatureExtraction

class ReviewContentRecommender:
    def __init__(self) -> None:
        return

    def load_data(self, file_name: str, sheet_name: str = 'product reviews') -> Tuple[pd.DataFrame, bool]:
        '''
            function to load reviews data

            parameters: the file name
            output: the data and the check
        '''
        file = FileData(file_name)
        self.data, check = file.load_sheet(sheet_name, index='id')
        return self.data, check

    def prepare_data(self, columns: list = []) -> pd.DataFrame:
        '''
            function to prepare data

            parameters: the columns to prepare
            output: the data with the prepared columns
        '''
        if len(columns) == 0:
            columns = ['rate', 'rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rate6',
                     'pros', 'cons', 'pros_count', 'cons_count']
        for col in self.data.columns:
            if col not in columns:
                self.data.drop(col, axis=1, inplace=True)
        model = TextFeatureExtraction()
        path = 'recommender/static/data/'
        self.data = model.apply_TF_IDF(self.data, ['pros', 'cons'], path, inplace=True)
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
    
    def train(self, file_name: str = '', path: str = '') -> None:
        '''
            function to train the recommender

            parameters: the file name
            output: none
        '''
        if file_name == '':
            file_name = 'reviews.xlsx'
        self.load_data(file_name)
        # print(list(self.data.columns))
        self.prepare_data()
        self.scale_data()
        dump(self.data, open(path, 'wb'))
        return

    def recommend(self, referenceId: str, path: str = 'reviews.pkl', n_recommendations: int = 5):
        '''
            function to recommend reviews

            parameters: the number of recommendations
            output: the recommendations
        '''
        if not os.path.exists(f'{path}reviews.pkl'):
            self.train(file_name=f'{path}reviews.xlsx', path=f'{path}reviews.pkl')
        data: pd.DataFrame = load(open(f'{path}reviews.pkl', 'rb'))
        nbrs: NearestNeighbors = NearestNeighbors(n_neighbors=n_recommendations+1, algorithm='ball_tree').fit(data.values)
        distances, indices = nbrs.kneighbors(data.loc[referenceId, :].values.reshape(1, -1))
        recommendations = []
        for i in range(len(indices)):
            recommendations.append(data.iloc[indices[i]].index)
        return recommendations[0], distances

# model = ReviewContentRecommender()
# # model.train()
# recs, spaces = model.recommend(3, 9)
# for rec, space in zip(recs, spaces):
#     print(model.data.loc[rec, :])
# print(model.data.head(5))
