import pandas as pd
import openpyxl 
from os.path import exists
from typing import Union

class excel:
    def __init__(self,path):
      self.path=path  
    
    def read_excel(self,sheetName:Union[int, str] =0):
      try:
        if(exists(self.path)):
          return  pd.read_excel(self.path,sheetName)
        else:  
          writer = pd.ExcelWriter(self.path, engine='openpyxl')
          writer.save()
          return  pd.read_excel(self.path)
      except:
        print("Not Found File with path "+self.path)  

    def get_sheet_number(self):
      xl=pd.ExcelFile(self.path)
      return len(xl.sheet_names)

    def get_sheet_names(self):
      xl=pd.ExcelFile(self.path)
      return xl.sheet_names

    def remove_sheet(self,she):
       workbook=openpyxl.load_workbook(self.path)
       '''std=workbook.get_sheet_by_name('aa')
       workbook.remove_sheet(std)
       workbook.save(self.path)'''
       del workbook[she]
       workbook.save(self.path)

    def save_df_to_excel(self,dataFrame,sheetName):
        '''     sheetNames=self.get_sheet_names()
        if(sheetName in sheetNames):
          mode='w'
        else:
          mode='a'
        # create excel writer
        writer = pd.ExcelWriter(self.path,mode=mode)
        # write dataframe to excel sheet named sheetName
        #dataFrame.to_excel(self.path, sheetName)
        # save the excel file
        #writer.save() 
        with pd.ExcelWriter(self.path, engine='openpyxl', mode='a') as writer: 
          
          if(sheetName in self.get_sheet_names()):
            print("tmm")
            print(ex.get_sheet_names())
            self.remove_sheet(sheetName)
            print(ex.get_sheet_names()) 
                        
          print("finally")
          dataFrame.to_excel(writer, sheet_name=sheetName,index=False)
          writer.save()  
          #print(workBook[sheetName])'''
        with pd.ExcelWriter(self.path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            dataFrame.to_excel(writer, sheetName, index=False)
          
          
              
     

ex=excel('data mobiles reviews.xlsx')


df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
     'physics': [68, 74, 77, 78],
     'chemistry': [84, 56, 73, 69],
     'math': [78, 88, 82, 87]})
ex.remove_sheet('aa')