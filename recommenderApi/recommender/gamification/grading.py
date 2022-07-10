from recommenderApi.imports import word_tokenize, load, stopwords, dump, nltk, os, TfidfVectorizer, np, pd, Tuple
from recommender.sqliteDB.data import SQLite_Database

class Grading:
    def __init__(self, alert: bool = False) -> None:
        '''
            check to download the stopwords list, if not exist, download it

            parameters: boolean value to show error messages or not
            output: Nothing
        '''
        self.alert = alert
        nltk.data.path.append(f'{os.getcwd()}/nltk_data')
        nltk.data.path.append(f'{os.getcwd()}/nltk_data/tokenizers')
        return
    
    def readFile(self, path: str = '') -> list:
        '''
            function to read the file

            parameters: the path of the file
            output: the list of the file
        '''
        fh = open(path, 'r', encoding='utf-8')
        lines = fh.readlines()
        fh.close()
        return lines

    def eliminateStopWords(self, sentence: str) -> list:
        '''
            function to remove stopwords from the sentence

            parameters: the whole sentence
            output: the count of words in sentence without the stopwords
        '''
        tokens: list = word_tokenize(sentence)
        if not os.path.isfile('recommender/reviews/stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('recommender/reviews/stopwords.pkl', 'rb'))
        
        count = 0
        for token in tokens:
            if token not in stopwords:
                count += 1
        return count

    def updateStopWords(self, lstStopWords: list = []) -> None:
        '''
            function to update the stopwords list

            parameters: the list of stopwords
            output: file contains list of stopwords is generated
        '''
        english = self.readFile('nltk_data/corpora/stopwords/english')
        arabic = self.readFile('nltk_data/corpora/stopwords/arabic')
        if len(lstStopWords) == 0:
            lstStopWords = english + arabic
        lstStopWords = [word.encode('utf-8') for word in lstStopWords]
        dump(lstStopWords, open('recommender/reviews/stopwords.pkl', 'wb'))

    def update_tf_idf(self):
        sqlite = SQLite_Database()
        prevs = sqlite.get_Preview()
        crevs = sqlite.get_Creview()
        pros = []; cons = []; brand_pros = []; brand_cons = []
        for rev in prevs:
            pros.append(rev.pros)
            cons.append(rev.cons)
        for rev in crevs:
            brand_pros.append(rev.pros)
            brand_cons.append(rev.cons)
        df1 = pd.DataFrame({'pros': pros, 'cons': cons})
        df2 = pd.DataFrame({'brand_pros': brand_pros, 'brand_cons':brand_cons})
        df = pd.concat([df1, df2], axis=1).fillna('')
        self.generate_transformer(df)
    

    def calc_TF_IDF(self, lstReviews: list = []) -> int:
        '''
            function to calculate the TF-IDF of the reviews

            parameters: the list of reviews
            output: the TF-IDF of the reviews
        '''
        if not os.path.isfile('recommender/gamification/tfidf.pkl'):
            self.update_tf_idf()
        data = load(open('recommender/gamification/tfidf.pkl', 'rb'))
        tfidf: list[TfidfVectorizer] = data['tf-idf']
        limits: list[set] = data['min-max']
        count_limits: list[set] = data['count']
        value: int = 0
        for i in range(4):
            tfidf_review: float = np.average(tfidf[i].transform(lstReviews[i]).toarray(), axis=1)[0]
            tfidf_review = 10 * (tfidf_review - limits[i][0]) / (limits[i][1] - limits[i][0])
            if tfidf_review < limits[i][0]: tfidf_review = limits[i][0]
            if tfidf_review > limits[i][1]: tfidf_review = limits[i][1]
            count_review = 30 * (self.eliminateStopWords(lstReviews[i][0]) - count_limits[i][0]) / (count_limits[i][1] - count_limits[i][0]) + 10
            if count_review < count_limits[i][0]: count_review = count_limits[i][0]
            if count_review > count_limits[i][1]: count_review = count_limits[i][1]
            weight = 0.3 if i < 2 else 0.2
            value += int((tfidf_review + count_review) * weight)
        if value > 50: value = 50
        if value < 10: value = 10
        return value 
    
    def generate_transformer(self, data: pd.DataFrame) -> pd.DataFrame:
        '''
            function to generate the Tf-Idf transformer

            parameters: the dataframe of the reviews
            output: the model of the reviews
        '''
        if not os.path.isfile('recommender/reviews/stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('recommender/reviews/stopwords.pkl', 'rb'))
        tfidf = [TfidfVectorizer(stop_words=stopwords) for i in range(4)]
        limits = []
        count_limits = []
        count = 0
        data = data.replace(np.nan, '')
        for column in data.columns:
            data[f'{column}_count'] = data[column].apply(self.eliminateStopWords)
            count_limits.append((data[f'{column}_count'].min(), data[f'{column}_count'].max()))
            data[column] = np.average(tfidf[count].fit_transform(np.array(data[column])).toarray(), axis=1)
            count += 1
            limits.append((data[column].min(), data[column].max()))
        dump({'tf-idf': tfidf, 'min-max': limits, 'count': count_limits}, open('recommender/gamification/tfidf.pkl', 'wb'))
        return data
