from recommenderApi.imports import word_tokenize, load, stopwords, dump, nltk, os, TfidfVectorizer, np, pd

class TextFeatureExtraction:
    def __init__(self, alert: bool = False) -> None:
        '''
            check to download the stopwords list, if not exist, download it

            parameters: boolean value to show error messages or not
            output: Nothing
        '''
        self.alert = alert
        nltk.download('punkt')
        nltk.download("stopwords")
        return

    def eliminateStopWords(self, sentence: str) -> int:
        '''
            function to remove stopwords from the sentence

            parameters: the whole sentence
            output: the sentence without the stopwords
        '''
        tokens: list = word_tokenize(sentence)
        if not os.path.isfile('stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('stopwords.pkl', 'rb'))
        
        count: int = 0
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
        more_stopwords: list = ['آمين', 'أب', 'أخ', 'أفعل', 'أفعله', 'ؤلاء', 'إل', 'إم', 'ات', 'اتان', 'ارتد', 'ان', 'انفك', 'برح', 'تان', 'تبد', 'تحو', 'تعل', 'حد', 'حم', 'حي', 'خب', 'ذار', 'سيما', 'صه', 'ظل', 'ظن', 'عد', 'قط', 'مر', 'مكان', 'مكانكن', 'نب', 'هات', 'هب', 'واها', 'وراء', 'ال']
        if len(lstStopWords) == 0:
            lstStopWords = stopwords.words("English") + stopwords.words("Arabic") + more_stopwords
        dump(lstStopWords, open('stopwords.pkl', 'wb'))

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

    def calculate_TF_IDF(self, sentences: np.array) -> np.array:
        '''
            function to calculate TF-IDF of the sentences

            parameters: the sentences
            output: the TF-IDF of the sentences
        '''
        if not os.path.isfile('stopwords.pkl'):
            self.updateStopWords()
        stopwords: list = load(open('stopwords.pkl', 'rb'))
        
        vectorizer = TfidfVectorizer(stop_words= stopwords)
        tfidf = vectorizer.fit_transform(sentences)
        arr: np.array = np.average(tfidf.toarray(), axis=1)
        return arr
    
    def apply_TF_IDF(self, data: pd.DataFrame, columns: list = [], inplace: bool = False) -> pd.DataFrame:
        '''
            function to apply TF-IDF on the data

            parameters: the data and the columns to apply TF-IDF and boolean value to choose (replace the exist data or new data)
            output: the data with TF-IDF
        '''
        newDF = pd.DataFrame()
        for column in columns:
            if column in data.columns:
                newColumn: str = f'{column}_TF-IDF'
                if inplace:
                    data[newColumn] = self.calculate_TF_IDF(data[column].values.astype('U'))
                    data.drop(column, axis=1, inplace=True)
                else:
                    newDF[newColumn] = self.calculate_TF_IDF(data[column].values.astype('U'))
            else:
                if self.alert: print(f'{column} is not a column in the dataframe')
        if inplace:
            return data
        return newDF


# data = pd.read_excel("../Graduation/Graduation-Project/Data/data mobiles reviews.xlsx", sheet_name=0, na_values='n/a')
# model = TextFeatureExtraction()
# newData = model.applt_TF_IDF(data, ['pros', 'cons', 'brand_pros', 'brand_cons'])
# print(newData)
# new = model.eliminateStopWords('الموبايل بقي فيه لاج غريب كده والframes بقت بتقطع مع التحديث الجديد')
# print(new)
# values = model.calculate_TF_IDF(all_sentences)
# print(values)
