from recommenderApi.imports import pd, Tuple

class FileData:
    def __init__(self, file_path: str = '', alert: bool = False) -> None:
        ''' 
            show alert message if error is happend
            load file if file_path is not empty

            parameters: file_path, alert
            output: None
        '''
        self.file_path: str = file_path
        self.alert: bool = alert
        try:
            file = pd.ExcelFile(file_path)
            self.sheet_names: int = file.sheet_names
            if self.alert: print('file loaded successfully')
        except:
            self.sheet_names, self.file_path = [], ''
            if self.alert: print("Error: File not found")

    def load_sheet(self, sheet_name: str, index: str = '', na = 'n/a') -> Tuple[pd.DataFrame, bool]:
        '''
            function to load sheet from file

            parameters: sheet_name, index
            output: return dataframe of sheet and boolean value represent if sheet is loaded successfully
        '''
        try:
            if index != '':
                self.data = pd.read_excel(self.file_path, sheet_name, na_values=na, index_col=index)
            else:
                self.data = pd.read_excel(self.file_path, sheet_name, na_values=na)
            return self.data, True
        except:
            if self.alert: print("Error: Sheet not found")
            return pd.DataFrame(), False

    def get_sheet_names(self) -> list:
        '''
            function to get list of sheet names

            parameters: None
            output: return list of sheet names
        '''
        return self.sheet_names
    
    def save_sheet(self, sheet_name: str, file_path: str) -> None:
        '''
            function to save sheet to file

            parameters: sheet_name, file_path
            output: None
        '''
        try:
            self.data.to_excel(file_path, sheet_name)
            if self.alert: print("Sheet saved successfully")
        except:
            if self.alert: print("Error: Sheet not found")

    def __str__(self):
        return self.file_name

# fh = FileData('mobiles.xlsx')
# print(fh.get_sheet_names())
# data = fh.load_sheet('Sheet1')
# print(data.head(10))