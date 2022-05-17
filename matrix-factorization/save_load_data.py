from pickle import dump, load
import pandas as pd

def loadDatFarame(fileName):
  df = load(open(fileName, 'rb'))
  return df

def saveDatFarame(fileName,df):
  dump(df, open(fileName, 'wb'))

def addNewRowToDatarame(df: pd.DataFrame, row):
    df2 = pd.DataFrame(row)
    df = pd.concat([df, df2], ignore_index=True, axis=0)
    return df