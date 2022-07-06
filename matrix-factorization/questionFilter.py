import pandas as pd
"""
return all question as list of dictionary -> the key of dictionary is question_id
{'3627406888cc1cefd58623d6e':
                  {'has_accepted_answer': '0',
                   'question_item': 'iphone 6s+',
                   'owner_has_item' : 0,
                   'num_of_votes': '15', 
                   'date': ''
                  }
                  ,
  '3627406888cc1cefd58623d5a':
                  {'has_accepted_answer': '1',
                  'question_item': 'apple',
                  'owner_has_item' : 1,
                  'num_of_votes': '5', 
                  'date': ''
                  }
}
quetion_id -> prefere to store after add modifer [1 for product ,3 for coompany]
has_accepted_answer -> 0 for false , 1 for true
question_item -> name of item question (product name or comapny name)
owner_has_item-> 1 for true , 0 for false ( owner is the person who write the question , item is product or company )
num_of_votes-> votes number
date -> question date
 """


def getAllQuetion():
    questions = {'1627406988cc1cefd58623ecc':
                 {'has_accepted_answer': 1,
                  'question_item': 'iphone 6s+',
                  'owner_has_item':0,
                  'num_of_votes': 15, 'date': ''
                  },
                 '1627406998cc1cefd58623ee0':
                 {'has_accepted_answer': 0,
                     'question_item': 'samsung',
                     'owner_has_item':1,
                     'num_of_votes': 5, 'date': ''
                  },
                  '16274069d8cc1cefd58623f3a':
                 {'has_accepted_answer': 0,
                  'question_item': 'ipone 11',
                  'owner_has_item':1,
                  'num_of_votes': 15,
                   'date': ''
                  },
                  '16274069a8cc1cefd58623f08':
                 {'has_accepted_answer': 1,
                  'question_item': 'ipone 11',
                  'owner_has_item':1,
                  'num_of_votes': 15,
                   'date': ''
                  },
                  '1627406878cc1cefd58623d50':
                 {'has_accepted_answer': 0,
                  'question_item': 'ipone 11',
                 'owner_has_item':0,
                  'num_of_votes': 1,
                   'date': ''
                  },
                  '16274069c8cc1cefd58623f30':
                 {'has_accepted_answer': 1,
                  'question_item': 'ipone 11',
                  'owner_has_item':0,
                  'num_of_votes': 15,
                   'date': ''
                  },
                 }
    return questions

def getUserCompanies():
  userCompany=['apple']
  return userCompany

def getUserProducts():
  userProducts=['ipone 11','iphone 6s','iphone 13']
  return userProducts

def filterQuetion(questions: list,filterType:int,sortResult:int =0):
    """ 
    questions -> the question that we will apply the filter on
    filterTypte-> 0 for filter based on company
                  1 for filter based on product (phone) 
    """
    allQuestions = getAllQuetion()
    userItems=[]
    filteredQuestions=[]
    filteredRate=[]
    if(filterType==1):
      userItems=getUserProducts()
    elif(filterType==0):
      userItems=getUserCompanies()

    for question in questions:
      if(allQuestions[question]['question_item'] in userItems):

        if(allQuestions[question]['owner_has_item']==1):
          filteredQuestions.append(question)
          filteredRate.append(0.35)
        else:
          if(allQuestions[question]['has_accepted_answer']==0):
            filteredQuestions.append(question)
            filteredRate.append(0.56) 
      else:
        if(allQuestions[question]['has_accepted_answer']==1):
          filteredQuestions.append(question)
          filteredRate.append(0.21515)
    df=pd.DataFrame({'question_id':filteredQuestions,'question_rate':filteredRate}) 
    if(sortResult):
      df.sort_values(by="question_rate", ascending=False, inplace=True)     
    return df    

quetion = ['1627406988cc1cefd58623ecc',
           '1627406998cc1cefd58623ee0',
           '16274069d8cc1cefd58623f3a',
           '16274069a8cc1cefd58623f08',
           '1627406878cc1cefd58623d50',
           '16274069c8cc1cefd58623f30']
result=filterQuetion(quetion,1,1)
print(result)