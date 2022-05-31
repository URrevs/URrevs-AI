from recommenderApi.imports import pd, dump, load

def loadDataFrame(fileName):
    df = load(open(fileName, 'rb'))
    return df

def saveDataFrame(fileName, df):
    dump(df, open(fileName, 'wb'))

def addNewRowToDatarame(df: pd.DataFrame, row):
    df2 = pd.DataFrame(row)
    df = pd.concat([df, df2], ignore_index=True, axis=0)
    return df

# def checkRowExistInDataFrame(df: pd.DataFrame, row) -> bool:
#     df2 = pd.DataFrame(row)
#     return ((df['user_id'] == df2['user_id']) and (df['item_id'] == df2['item_id'])).any()
