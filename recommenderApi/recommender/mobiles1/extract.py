from recommenderApi.imports import dt, OneHotEncoder, LabelEncoder

class ExtractFeatures:
    def __init__(self, alert: bool = False) -> None:
        ''' show alert message if error is happend '''
        self.alert: bool = alert
    
    def dateAsInteger(self, date: dt) -> float:
        ''' 
            function to convert date to float number
            ex: dt(2022, 5, 1) -> 704678400.0

            parameters: date
            output: return float number that represent time in seconds from 1/1/2000 to this date
        '''
        reference: dt = dt(2000, 1, 1)
        try:
            return (date - reference).total_seconds()
        except:
            if self.alert: print(f'"{date}" is not valid input')
            return 0

    def uniString(self, string: str) -> str:
        ''' 
            function to unidied all strings to lowercase
            ex: 'Xiomi Redmi Note 8' -> 'xiomi redmi note 8'

            parameters: sentence
            output: return the lowercase version from this sentence
        '''
        string = string.replace(' ', '')
        return string.lower()

    def isNumeric(self, string: str) -> bool:
        ''' 
            function to check if string is a number or not
            ex: '"12.53"' -> True

            parameters: numeric string
            output: return boolean value represent if string is number
        '''
        try:
            float(string)
            return True
        except:
            if self.alert: print(f'"{string}" is not a number')
            return False

    def get_Number(self, num: str, sep: str = 'x') -> float:
        ''' 
            function to extract number/s from sentence contain multiple numbers seperated by (sep)
            ex: '12.5x2x3' -> 75.0

            parameters: sentence contains numbers seperated by sep, seperator between numbers
            output: return the float number that result from multiplying all numbers
        '''
        num: str = self.uniString(num)
        if '*' in num:
            num: str = num.replace('*', sep)
        nums: list = num.split(sep)
        result = 1
        for n in nums:
            if self.isNumeric(n):
                result *= float(n)
            else:
                result = 0
                break
        return result

    def unit_Number(self, num: str, unit: str) -> float:
        ''' 
            function to extract number from sentence before specific unit
            ex: 'Single 5 MP, AF', 'MP' -> 5.0

            parameters: whole sentence, the unit after number
            output: return the float number before the unit
        '''
        num, unit = self.uniString(num), self.uniString(unit)
        strings: list = num.split(unit)
        temp: str = strings[0][-1::-1]
        counter = 1
        while counter < len(temp):
            if self.isNumeric(temp[: counter]):
                counter += 1
            else: 
                break
        result: str = temp[:counter - 1][-1::-1]
        if result == '':
            result = 0
        return float(result)

# model = ExtractFeatures()
# print(model.get_Number('45.12x5'))
# print(model.uniString('الموبايل بيه واجهة جميلة'))
# print(model.unit_Number())
# print(model.dateAsInteger(dt(2022, 5, 1)))

# def encode(data: pd.DataFrame, type: str = 'OneHot') -> pd.DataFrame:
#     model = OneHotEncoder() if type == 'OneHot' else LabelEncoder()
#     newdata = pd.DataFrame(model.fit_transform(data.values.reshape(-1, 1)).toarray(), 
#                     columns=model.categories_[0], index=data.index)
#     return newdata

# data = FileData('Graduation-Project/mobiles.xlsx')
# # print(data.get_sheet_names())
# data, check = data.load_sheet('Sheet1', index='_id')
# # print(data.columns)
# print(encode(data.loc[:, 'company']))
