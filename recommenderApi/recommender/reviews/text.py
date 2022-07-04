from recommenderApi.imports import word_tokenize, load, stopwords, dump, nltk, os, TfidfVectorizer, np, pd, Tuple
from recommenderApi.file import FileData

class TextFeatureExtraction:
    def __init__(self, alert: bool = False) -> None:
        '''
            check to download the stopwords list, if not exist, download it

            parameters: boolean value to show error messages or not
            output: Nothing
        '''
        self.alert = alert
        nltk.data.path.append(f'{os.getcwd()}/nltk_data')
        nltk.data.path.append(f'{os.getcwd()}/nltk_data/tokenizers')
        # nltk.download('punkt')
        # nltk.download("stopwords")
        return

    def eliminateStopWords(self, sentence: str) -> int:
        '''
            function to remove stopwords from the sentence

            parameters: the whole sentence
            output: the count of words in sentence without the stopwords
        '''
        tokens: list = word_tokenize(sentence)
        if not os.path.isfile('recommender/reviews/stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('recommender/reviews/stopwords.pkl', 'rb'))
        
        count: int = 0
        for token in tokens:
            if token not in stopwords:
                count += 1
        return count
    
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

    def updateStopWords(self, lstStopWords: list = []) -> None:
        '''
            function to update the stopwords list

            parameters: the list of stopwords
            output: file contains list of stopwords is generated
        '''
        # more_stopwords: list = ['آمين', 'أب', 'أخ', 'أفعل', 'أفعله', 'ؤلاء', 'إل', 'إم', 'ات', 'اتان', 'ارتد', 'ان', 'انفك', 'برح', 'تان', 'تبد', 'تحو', 'تعل', 'حد', 'حم', 'حي', 'خب', 'ذار', 'سيما', 'صه', 'ظل', 'ظن', 'عد', 'قط', 'مر', 'مكان', 'مكانكن', 'نب', 'هات', 'هب', 'واها', 'وراء', 'ال']
        english = self.readFile('nltk_data/corpora/stopwords/english')
        arabic = self.readFile('nltk_data/corpora/stopwords/arabic')
        if len(lstStopWords) == 0:
            lstStopWords = english + arabic
        lstStopWords = [word.encode('utf-8') for word in lstStopWords]
        dump(lstStopWords, open('recommender/reviews/stopwords.pkl', 'wb'))

    def apply_Tokenization(self, data: pd.DataFrame, columns: list = [], inplace: bool = False) -> pd.DataFrame:
        '''
            function to apply tokenization on the data

            parameters: the data and the columns to apply tokenization and boolean value to choose (replace the exist data or new data)
            output: the length of data with tokenization
        '''
        newDF = pd.DataFrame()
        for column in columns:
            if column in data.columns:
                newColumn: str = f'{column}_count'
                if inplace:
                    data[newColumn] = data[column].apply(self.eliminateStopWords)
                    data.drop(column, axis=1, inplace=True)
                else:
                    newDF[newColumn] = data[column].apply(self.eliminateStopWords)
            else:
                if self.alert: print(f'{column} is not a column in the dataframe')
        if inplace:
            return data
        return newDF

    def calculate_TF_IDF(self, data: pd.DataFrame, sentences: np.array) -> Tuple[pd.DataFrame, TfidfVectorizer]:
        '''
            function to calculate TF-IDF of the sentences

            parameters: the sentences
            output: the TF-IDF of the sentences and the vectorizer model
        '''
        if not os.path.isfile('recommender/reviews/stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('recommender/reviews/stopwords.pkl', 'rb'))
        
        vectorizer = TfidfVectorizer(stop_words= stopwords)
        matrix = vectorizer.fit_transform(sentences)
        df = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=data.index)
        return df, vectorizer
    
    def apply_TF_IDF(self, data: pd.DataFrame, column: str = '', path: str = 'vectorizer.pkl',
        inplace: bool = False) -> pd.DataFrame:
        '''
            function to apply TF-IDF on the data

            parameters: the data and the columns to apply TF-IDF and boolean value to choose (replace the exist data or new data)
            output: the data with TF-IDF
        '''
        df, vect = self.calculate_TF_IDF(data, data[column].values.astype('U'))
        dump(vect, open(path, 'wb'))
        if inplace:
            data = pd.concat([data, df], axis=1)
            data.drop(column, axis=1, inplace=True)
            return data
        return df

    def calc_Instance_TF_IDF(self, sentence: str = '', index: str = '', path: str = 'vectorizer.pkl') -> pd.DataFrame:
        '''
            function to calculate TF-IDF of the sentence

            parameters: the sentence
            output: the TF-IDF of the sentence
        '''
        # if not os.path.exists(path):
        #     file = FileData('recommenderApi/recommender/static/data/reviews.xlsx')
        #     df, check = file.load_sheet('product reviews')
        #     for col in ['user', 'date_rev', 'mobile']:
        #         df.drop(col, axis=1, inplace=True)
        #     self.apply_TF_IDF(df, ['pros', 'cons'], path=path,inplace=True)
        vect: TfidfVectorizer = load(open(path, 'rb'))
        matrix = vect.transform([sentence])
        df = pd.DataFrame(matrix.toarray(), columns=vect.get_feature_names_out(), index=[index])
        return df

# path = 'recommenderApi/recommender/static/data/'
# data = pd.read_excel(f'{path}reviews.xlsx', sheet_name=0, na_values='n/a')
# model = TextFeatureExtraction()
# # newData = model.apply_TF_IDF(data,['pros', 'cons'],path='recommenderApi/recommender/static/data/vectorizer.pkl',inplace=True)
# newData = model.calc_Instance_TF_IDF('الكاميرا كويسة جدا', '40', f'{path}vectorizer.pkl')
# print(newData)
# newDF = pd.DataFrame(df.toarray(), columns=vect.get_feature_names_out(), index=data.index)
# new = model.eliminateStopWords('الموبايل بقي فيه لاج غريب كده والframes بقت بتقطع مع التحديث الجديد')
# print(new)
# values = model.calculate_TF_IDF(data, all_sentences)
# print(values)
