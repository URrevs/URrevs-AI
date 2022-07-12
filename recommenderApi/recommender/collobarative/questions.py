from recommenderApi.imports import dump, load
from recommender.sqliteDB.data import SQLite_Database
from recommender.mobiles1.getPhones import Scaler

def get_questions_by_products(products):
    return SQLite_Database().get_Pquestions_by_products(products=products)

def questions_to_dic(questions, itemType = 2):
    output = {}
    for question in questions:
        if itemType == 2:
            output[question.id] = {
                'has_accepted_answer': question.hasAcceptedAnswer,
                'question_item': question.productId,
                'owner_has_item': question.product_owner,
                'num_of_upvotes': question.upvotesCounter,
                'time': question.time
            }
        elif itemType == 3:
            output[question.id] = {
                'has_accepted_answer': question.hasAcceptedAnswer,
                'question_item': question.companyId,
                'owner_has_item': question.company_owner,
                'num_of_upvotes': question.upvotesCounter,
                'time': question.time
            }
    return output

def get_owned_user_companies(user):
    return SQLite_Database().get_user_companies(user)

def get_owned_user_products(user):
    return SQLite_Database().get_user_products(user)

def getAllQuetion(filterType: int = 2):
    if filterType == 2:
        try: return load(open('recommender/collobarative/pques.pkl', 'rb'))
        except:
            pques = questions_to_dic(SQLite_Database().get_Pquestion())
            dump(pques, open('recommender/collobarative/pques.pkl', 'wb'))
            return pques
    if filterType == 3:
        try: return load(open('recommender/collobarative/cques.pkl', 'rb'))
        except:
            cques = questions_to_dic(SQLite_Database().get_Cquestion())
            dump(cques, open('recommender/collobarative/cques.pkl', 'wb'))
            return cques

def filterQuetions(user:str, ques1:list, sort:list, ques2:list, filterType:int=2):
    """ 
    questions -> the question that we will apply the filter on
    filterTypte-> 3 for filter based on company
                  2 for filter based on product (phone) 
    """
    allQuestions = getAllQuetion(filterType)
    userItems = []; filterQuestions = []; filterRate = []
    if(filterType == 2): userItems = get_owned_user_products(user)
    elif(filterType == 3): userItems = get_owned_user_companies(user)
    counter = 0

    for ques in [ques1, ques2]:
        filteredQuestions = []; filteredRate = []
        if ques != None:
            for i in range(len(ques)):
                if ques[i] not in filterQuestions:
                    length = len(ques[i])
                    if length == 25: ques[i] = ques[i][1:]
                    if length == 23: ques[i] = f'6{ques[i][1:]}'
                    if (counter == 0 and sort[i] > -0.5) or (counter == 1):
                        if(allQuestions[ques[i]]['question_item'] in userItems):
                            if(allQuestions[ques[i]]['owner_has_item'] == 1):
                                filteredQuestions.append(ques[i])
                                if counter == 0: filteredRate.append(sort[i])
                                else: filteredRate.append(allQuestions[ques[i]]['num_of_upvotes'])
                            else:
                                if(allQuestions[ques[i]]['has_accepted_answer'] == 0):
                                    filteredQuestions.append(ques[i])
                                    if counter == 0: filteredRate.append(sort[i])
                                    else: filteredRate.append(allQuestions[ques[i]]['num_of_upvotes'])
                        else:
                            if(allQuestions[ques[i]]['has_accepted_answer'] == 1):
                                filteredQuestions.append(ques[i])
                                if counter == 0: filteredRate.append(sort[i])
                                else: filteredRate.append(allQuestions[ques[i]]['num_of_upvotes'])

        if (counter == 1) and len(filteredRate) > 1:
            maximum = max(filteredRate)
            if maximum == 0:
                maximum = 1
                scaler = Scaler(in_=(0, maximum), out_=(0.5, 0.9))
                filteredRate = [scaler.scale(x) for x in filteredRate]
        if len(filteredQuestions) > 0:
            filterQuestions.extend(filteredQuestions)
            filterRate.extend(filteredRate)
        counter += 1

    return filteredQuestions, filteredRate
    