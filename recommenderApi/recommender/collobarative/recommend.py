from recommenderApi.imports import *
from recommender.collobarative.matrix_factorization import BaselineModel, KernelMF, train_update_test_split
from recommender.collobarative.seenTable import *
from recommender.collobarative.save_load_data import *
# from recommender.asyn_tasks.tasks import *
    
class MatrixFactorization:
    def __init__(self, n_epochs: int = 20, alert: bool = False, columns = ['user_id', 'item_id', 'rating', 'rating_pred']):
        self.n_epochs = n_epochs
        self.alert = alert
        self.columns = columns
    
    def split_data(self, path: str = 'recommender/collobarative/itemsTrackers.pkl', test_size: float = 0.2):
        # self.review_data = pd.read_csv(path)
        self.review_data: pd.DataFrame = loadDataFrame(path)

        rand_seed = 41
        np.random.seed(rand_seed)
        random.seed(rand_seed)

        X = self.review_data[self.columns[:2]]
        y = self.review_data[self.columns[2]]
        
        # Prepare data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size)
        if self.alert: print('data splitted successfully')

    def train(self, path: str = 'recommender/collobarative/itemsTrackers.pkl',  
        test_size: float = 0.2, lr = 0.001, reg = 0.005, gamma = 'auto'):
        self.matrix_fact = KernelMF(n_epochs=self.n_epochs, n_factors = 100, verbose = self.alert, 
            lr = lr, reg = reg, columns=self.columns, gamma=gamma)
        try:
            self.split_data(path=path, test_size=test_size)
            if self.alert: print('training started')
            self.matrix_fact.fit(self.X_train, self.y_train, start=True)
            if self.alert: print('model trained successfully')
            return self.matrix_fact.train_rmse[-1]
        except Exception as e:
            print("may be no new data: ", e)
            return 0

    def online_train(self, path: str = 'recommender/collobarative/itemsTrackers.pkl', 
        model_path: str = 'recommender/collobarative/MF_items_model.pkl', test_size: float = 0.2):
        try:
            if self.load_model(path=model_path):
                self.split_data(path=path, test_size=test_size)
                if self.alert: print('training started')
                self.matrix_fact.fit(self.X_train, self.y_train)
                if self.alert: print('model trained successfully')
                return self.matrix_fact.train_rmse[-1]
            return 0
        except Exception as e:
            print("may be no new data: ", e)
            return 0

    def save_model(self, model_path: str = 'recommender/collobarative/MF_items_model.pkl'):
        try:
            dump(self.matrix_fact, open(model_path, 'wb'))
            print('model saved successfully')
        except:
            print('model not saved')
            
        
    def test(self):
        try:
            predictions = self.matrix_fact.predict(self.X_test)
            mse = mean_squared_error(self.y_test, predictions)
            return mse
        except Exception as e:
            print("may be no new data: ", e)
            return 0

    def load_model(self, path: str = 'recommender/collobarative/MF_items_model.pkl'):
        try: 
            self.matrix_fact = load(open(path, 'rb'))
            return True
        except:
            if path == 'recommender/collobarative/MF_items_model.pkl': 
                self.train()
                self.save_model(model_path=path)
            else: 
                self.train(path = 'recommender/collobarative/mobileTrackers.pkl')
                self.save_model(model_path=path)
            return False

    def recommend_items(self, user: str): 
        self.load_model()
        seen_table = SeenTable('recommender/collobarative/seenTable.pkl', loadfile=True)
        items_known = seen_table.df.query(f'{self.columns[0]} == @user')[self.columns[1]]
        result = self.matrix_fact.recommend_items(user=user, items_known=items_known, productReviewAmount=32,
            productQuestionAmount=24, companyReviewAmount = 16, companyQuestionAmount = 8)
        return result
        # recommendations = list(result[self.columns[1]].values)
        # spaces = list(result[self.columns[3]].values)
        # the following line will be asynchronously executed
        # addToSeenTable(seenTable=seen_table, userId=user, itemIds=recommendations)
        # return recommendations, spaces

    def recommend_mobiles(self, user: str, n_recommendations: int = 10):
        self.load_model(path = 'recommender/collobarative/MF_mobiles_model.pkl')
        result = self.matrix_fact.recommend_mobiles(user=user, amount=n_recommendations)
        return result['product_id'].tolist()
        # recommendations = result[[self.columns[1]]].values
        # return recommendations
        
