from sklearn.utils import shuffle
from recommender.collobarative.recommend import MatrixFactorization
from recommender.collobarative.seenTable import SeenTable
from recommender.collobarative.questions import *
from recommender.reviews.reviewsRecommender import ReviewContentRecommender
from recommender.collobarative.reviewTracker import Trackers
from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS, DAILY_ITEMS_QOUTA
from recommenderApi.imports import load, os, dump
from recommender.collobarative.anonymous import calc_anonymous_data
import time

def check_interactions_existance(userId: str, search_in: str = 'items'):
    if search_in == 'items':
        return Trackers(loadfile=True).checkUserExist(userId)
    else:
        return Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).checkUserExist(userId)

def get_most_liked_reviews(userId: str, item_type = 'product'):
    if item_type == 'product':
        return SQLite_Database().get_Most_liked_Prev(userId)
    return SQLite_Database().get_Most_liked_Crev(userId)
    # return Trackers(loadfile=True).getMostLikedReview(userId, item_type)

def get_max_n_liked_mobiles(userId: str, n: int):
    try: return load(open('recommender/collobarative/MF_mobiles.pkl', 'rb'))[userId]['phones']
    except:
        return Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).getMaxNLikedMobile(userId, n)

def get_max_n_liked_companies(mobiles: list):
    companies = []
    sql = SQLite_Database()
    for mobile in mobiles:
        try: companies.append(sql.get_company_from_mobile(mobile))
        except: pass
    return companies

def split(recs: list):
    reviews = []; spaces = []
    if len(recs) > 0:
        for rec in recs[0]:
            reviews.append(rec[0][1:])
            spaces.append(rec[1])
    return reviews, spaces

# def valid_id(id: str):
#     length = len(id)
#     if length == 24: return id
#     elif: length == 25: return id[1:]
#     else: return f'6{id}'

def remove_hates(lst: list, spaces: list, identifier: str, hates: list):
    length = len(lst)
    out = []; out_sp = []
    for i in range(length):
        if f'{identifier}{lst[i]}' not in hates:
            out.append(f'{identifier}{lst[i]}')
            out_sp.append(spaces[i])
    return out, out_sp

def generate_MF_items_file():
    MF_items = {}
    MF_Model = MatrixFactorization()
    users = Trackers(loadfile=True).getAllUsers()
    for user in users:
        MF_items[user] = MF_Model.recommend_items(user)
    dump(MF_items, open('recommender/collobarative/MF_items.pkl', 'wb'))
    return MF_items
    
def generate_MF_mobiles_files():
    MF_mobiles = {}
    sql = SQLite_Database()
    MF_Model = MatrixFactorization()
    users = Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).getAllUsers()
    for user in users:
        phones = MF_Model.recommend_mobiles(user, n_recommendations=5)
        companies = get_max_n_liked_companies(phones)
        prevs = []; crevs = []; pques = []; cques = []
        prevs.extend(sql.get_Previews_by_mobile(phones))
        pques.extend(sql.get_Pquestions_by_mobiles(phones))
        cques.extend(sql.get_Cquestions_by_company(companies))
        crevs.extend(sql.get_Creviews_by_companies(companies))
        MF_mobiles[user] = {
            'phones': phones,
            'companies': companies,
            'lists': (prevs, crevs, pques, cques)
        }
    dump(MF_mobiles, open('recommender/collobarative/MF_mobiles.pkl', 'wb'))
    return MF_mobiles

def recommend(userId: str, round: int, PR: int, CR: int, PQ: int, CQ: int):
    seen_table = SeenTable(loadfile=True)
    
    productQuestions = []
    companyQuestions = []
    productReviews = []
    companyReviews = []
    total = []
    total_spaces = []
    # print(PR, CR, PQ, CQ)

    # t1 = time.time()    
    # first rounds
    if round <= (200//ROUND_NUM_OF_REVIEWS):
        # load MF items file
        try: MF_items = load(open('recommender/collobarative/MF_items.pkl', 'rb'))
        except Exception as e:
            # print(e)
            MF_items = generate_MF_items_file()
        # t2 = time.time()

        # print('file1: ', t2-t1)
        # t1 = time.time()
        # # load MF mobiles file
        try: 
            MF_mobiles = load(open('recommender/collobarative/MF_mobiles.pkl', 'rb'))
            # print('try')
        except Exception as e:
            # print(e)
            MF_mobiles = generate_MF_mobiles_files()
        # t2 = time.time()
        # print('file2: ', t2-t1)

        if userId not in MF_items.keys():
            # load all anonymous as it
            # print('Anonymous User')
            round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
            if not os.path.isfile('recommender/collobarative/anonymous_data.pkl'): calc_anonymous_data()
            
            # t1 = time.time()
            productReviews, companyReviews, productQuestions, companyQuestions, total =\
                    load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[round-1]
            # t2 = time.time()
            # print('file3: ', t2-t1)

            # t1 = time.time()
            seen_table.check_if_review_shown_before(userId, [f'0{rev}' for rev in productReviews])
            seen_table.check_if_review_shown_before(userId, [f'1{rev}' for rev in companyReviews])
            seen_table.check_if_review_shown_before(userId, [f'2{ques}' for ques in productQuestions])
            seen_table.check_if_review_shown_before(userId, [f'3{ques}' for ques in companyQuestions])
            # t2 = time.time()
            # print('loop1: ', t2-t1)
        else:
            # if round == 1:
            #     try: return load(open('recommender/collobarative/gen_round_1.pkl', 'rb'))[userId]
            #     except: pass
            # load user items data
            (prevs1, pr_sp1, pques1, pq_sp1, crevs1, cr_sp1, cques1, cq_sp1) = MF_items[userId]
            # load user mobiles items data
            if userId not in MF_mobiles.keys(): prevs2=[]; pques2=[]; crevs2=[]; cques2=[]
            else: (prevs2, crevs2, pques2, cques2) = MF_mobiles[userId]['lists']
            
            # print('Questions recommendation')
            # check if questions are calculated before
            # t1 = time.time()
            try: users_MF_ques = load(open('recommender/collobarative/gen_MF_ques.pkl', 'rb'))
            except: users_MF_ques = {}
            # t2 = time.time()
            # print('file4: ', t2-t1)
            
            if userId not in users_MF_ques.keys(): 
                pques3,pq_spcs=filterQuetions(user=userId,ques1=pques1,sort=pq_sp1,filterType=2,ques2=pques2)
                cques3,cq_spcs=filterQuetions(user=userId,ques1=cques1,sort=cq_sp1,filterType=3,ques2=cques2)
            # load the saved data
            else:
                (pques3, pq_spcs) = users_MF_ques[userId]['pques']
                (cques3, cq_spcs) = users_MF_ques[userId]['cques']
            
            # t1 = time.time()
            productQuestions = [f'2{ques}' for ques in pques3]
            productQuestions, pq_sp, prest, p_sp_rest = seen_table.check_if_review_shown_before(userId, productQuestions, pq_spcs, num=PQ)
            # t2 = time.time()
            # print('loop2: ', t2-t1)
            total.extend(productQuestions); total_spaces.extend(pq_sp)
            
            # t1 = time.time()
            companyQuestions = [f'3{ques}' for ques in cques3]
            companyQuestions, cq_sp, crest, c_sp_rest = seen_table.check_if_review_shown_before(userId, companyQuestions, cq_spcs, num=CQ)
            # t2 = time.time()
            # print('loop3: ', t2-t1)
            total.extend(companyQuestions); total_spaces.extend(cq_sp)
            
            users_MF_ques[userId] = {'pques': (prest, p_sp_rest), 'cques': (crest, c_sp_rest)}
            dump(users_MF_ques, open('recommender/collobarative/gen_MF_ques.pkl', 'wb'))
        # print(productQuestions, companyQuestions)
        # print(PR, CR, PQ, CQ)
        # print('--------------------------------------')
        # --------------------------------------------------------------------------------------------------
        if len(productQuestions) < PQ: PR += (PQ-len(productQuestions)); PQ = 0
        if len(companyQuestions) < CQ: CR += (CQ-len(companyQuestions)); CQ = 0

        # print('MF_mobile_revs')

        Preference = get_most_liked_reviews(userId)
        Creference = get_most_liked_reviews(userId, item_type='company')
        # print(Preference, Creference)
        items_interactions_existance_check = check_interactions_existance(userId, search_in='items')
        # check existance of products interactions and items interactions
        if items_interactions_existance_check and check_interactions_existance(userId, search_in='mobiles'):
            hates = Trackers(loadfile=True).getHatesReviews(userId)
    
            # t1 = time.time()
            try: users_MF_mobile_revs = load(open('recommender/collobarative/gen_MF_mobile_revs.pkl', 'rb'))
            except: users_MF_mobile_revs = {}
            # t2 = time.time()
            # print('file5: ', t2-t1)
            
            if userId not in users_MF_mobile_revs.keys():
                Precs = []; pr_sp = []; Crecs = []; cr_sp = []
                if Preference != None:
                    # get reviews of these mobiles
                    # print('mobiles CR p')
                    if len(prevs2) > 0:
                        prevs2.append(Preference)
                        model = ReviewContentRecommender()
                        recs, pr_sp = model.recommend(
                            referenceId=Preference,
                            recommend_type='product',
                            items=prevs2,
                            known_items=hates
                            )
                        # check if review not in hates for this user
                        Precs = [f'0{prev}' for prev in recs]
                # -------------------------------
                if Creference != None:
                    # get reviews for these companies
                    # print('mobiles CR c')
                    if len(crevs2) > 0:
                        crevs2.append(Creference)
                        model = ReviewContentRecommender()
                        recs, cr_sp = model.recommend(
                            referenceId=Creference,
                            recommend_type='company',
                            items=crevs2
                            )
                        Crecs = [f'1{crev}' for crev in recs]
            else:
                (Precs, pr_sp) = users_MF_mobile_revs[userId]['prevs']
                (Crecs, cr_sp) = users_MF_mobile_revs[userId]['crevs']

            # t1 = time.time()
            prevs, pr_spcs, prest, p_sp_rest = seen_table.check_if_review_shown_before(userId, Precs[1:], pr_sp, num=ROUND_NUM_OF_REVIEWS//10)
            # t2 = time.time()
            # print('loop4: ', t2-t1)
            productReviews.extend(prevs); total.extend(prevs); total_spaces.extend(pr_spcs)
            PR = PR - len(prevs)

            # t1 = time.time()
            crevs, cr_spcs, crest, c_sp_rest = seen_table.check_if_review_shown_before(userId, Crecs[1:], cr_sp, num=ROUND_NUM_OF_REVIEWS//10)
            # t2 = time.time()
            # print('loop5: ', t2-t1)
            companyReviews.extend(crevs); total.extend(crevs); total_spaces.extend(cr_spcs)
            CR = CR - len(crevs)
            
            users_MF_mobile_revs[userId] = {'prevs': (prest, p_sp_rest), 'crevs': (crest, c_sp_rest)}
            dump(users_MF_mobile_revs, open('recommender/collobarative/gen_MF_mobile_revs.pkl', 'wb'))
        # print(productReviews, companyReviews)
        # print(PR, CR, PQ, CQ)
        # print('--------------------------------------')
        # ------------------------------------------------------------------------------
        # print('MF_item_revs')

        # check user item interactions existance
        if items_interactions_existance_check:
            # First Model recommend PR, CR
            # t1 = time.time()
            try: users_MF_revs = load(open('recommender/collobarative/gen_MF_revs.pkl', 'rb'))
            except: users_MF_revs = {}
            # t2 = time.time()
            # print('file6: ', t2-t1)
            
            if userId in users_MF_revs.keys():
                (prevs1, pr_sp1) = users_MF_revs[userId]['prevs']
                (crevs1, cr_sp1) = users_MF_revs[userId]['crevs']

            # t1 = time.time()
            prevs4, pr_sp4, prest, p_sp_rest = seen_table.check_if_review_shown_before(userId, prevs1, pr_sp1, num=ROUND_NUM_OF_REVIEWS//10, known=productReviews)
            # t2 = time.time()
            # print('loop6: ', t2-t1)
            productReviews.extend(prevs4); total.extend(prevs4); total_spaces.extend(pr_sp4)
            PR = PR - len(prevs4)
            
            # t1 = time.time()
            crevs4, cr_sp4, crest, c_sp_rest = seen_table.check_if_review_shown_before(userId, crevs1, cr_sp1, num=ROUND_NUM_OF_REVIEWS//10, known=companyReviews)
            # t2 = time.time()
            # print('loop7: ', t2-t1)
            companyReviews.extend(crevs4); total.extend(crevs4); total_spaces.extend(cr_sp4)
            CR = CR - len(crevs4)
            
            users_MF_revs[userId] = {'prevs': (prest, p_sp_rest), 'crevs': (crest, c_sp_rest)}
            dump(users_MF_revs, open('recommender/collobarative/gen_MF_revs.pkl', 'wb'))
            # print(productReviews, companyReviews)
            # print(PR, CR, PQ, CQ)
            # print('--------------------------------------')
            # --------------------------------------------------
            # t1 = time.time()
            try: users_CR_revs = load(open('recommender/collobarative/gen_CR_revs.pkl', 'rb'))
            except: users_CR_revs = {}
            # t2 = time.time()
            # print('file7: ', t2-t1)
            
            # print('CR_revs')

            if userId not in users_CR_revs.keys():
                product_recs = []; pr_sp = []; company_recs = []; cr_sp = []
                hates = Trackers(loadfile=True).getHatesReviews(userId)
                # print(Preference)
                #  Second Model recommend PR, CR
                # print('items CR r')
                if Preference != None:
                    # print(productReviews, hates)
                    model = ReviewContentRecommender()
                    Precs, pr_sp = model.recommend(
                        referenceId=Preference,
                        n_recommendations=150,
                        known_items=hates
                        )
                    product_recs = [f'0{review}' for review in Precs]

                # print('items CR c')
                if Creference != None:
                    model = ReviewContentRecommender()
                    Crecs, cr_sp = model.recommend(
                        referenceId=Creference,
                        n_recommendations=150,
                        known_items=hates, 
                        recommend_type='company'
                        )
                    company_recs = [f'1{review}' for review in Crecs]
            
            else:
                (product_recs, pr_sp) = users_CR_revs[userId]['prevs']
                (company_recs, cr_sp) = users_CR_revs[userId]['crevs']

            # t1 = time.time()
            prevs, pr_sp, prest, p_sp_rest = seen_table.check_if_review_shown_before(userId, product_recs, pr_sp, num=PR, known=productReviews)
            # t2 = time.time()
            # print('loop8: ', t2-t1)
            productReviews.extend(prevs); total.extend(prevs); total_spaces.extend(pr_sp)
            PR = PR - len(prevs)

            # t1 = time.time()
            crevs, cr_sp, crest, c_sp_rest = seen_table.check_if_review_shown_before(userId, company_recs, cr_sp, num=CR, known=companyReviews)
            # t2 = time.time()
            # print('loop9: ', t2-t1)
            companyReviews.extend(crevs); total.extend(crevs); total_spaces.extend(cr_sp)
            CR = CR - len(crevs)
            
            users_CR_revs[userId] = {'prevs': (prest, p_sp_rest), 'crevs': (crest, c_sp_rest)}
            dump(users_CR_revs, open('recommender/collobarative/gen_CR_revs.pkl', 'wb'))
            
            # print(productReviews, companyReviews)
            # print(PR, CR, PQ, CQ)
            # print('--------------------------------------')
            # --------------------------------------------------
            # sorting list
            total = [x for x, _ in sorted(zip(total, total_spaces), key=lambda pair: pair[1])]
        # --------------------------------------------------
        # Here we add more recommendations without checking if they are already shown as final solution
            if PR > 0 or CR > 0 or PQ > 0 or CQ > 0:
                round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
                if not os.path.isfile('recommender/collobarative/anonymous_data.pkl'):
                    calc_anonymous_data()
                if (PR+CR+PQ+CQ) == ROUND_NUM_OF_REVIEWS:
                    productReviews, companyReviews, productQuestions, companyQuestions, total = load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[round-1]
                else:
                    prevs, crevs, pques, cques, _ = load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[round-1]
                    if PR > 0:
                        for prev in prevs:
                            if seen_table.check_item_not_exist(userId, f'0{prev}'):
                                productReviews.append(prev)
                                total.append(prev)
                                seen_table.addToSeenTable(userId, [f'0{prev}'])
                                PR -= 1
                            if PR == 0: break
                    # print(PR, CR, PQ, CQ)
                    if CR > 0:
                        for crev in crevs:
                            if seen_table.check_item_not_exist(userId, f'1{crev}'):
                                companyReviews.append(crev)
                                total.append(crev)
                                seen_table.addToSeenTable(userId, [f'1{crev}'])
                                CR -= 1
                            if CR == 0: break
                    # print(PR, CR, PQ, CQ)
                    if PQ > 0:
                        for pque in pques:
                            if seen_table.check_item_not_exist(userId, f'2{pque}'):
                                productQuestions.append(pque)
                                total.append(pque)
                                seen_table.addToSeenTable(userId, [f'2{pque}'])
                                PQ -= 1
                    # print(PR, CR, PQ, CQ)
                    if CQ > 0:
                        for cque in cques:
                            if seen_table.check_item_not_exist(userId, f'3{cque}'):
                                companyQuestions.append(cque)
                                total.append(cque)
                                seen_table.addToSeenTable(userId, [f'3{cque}'])
                                CQ -= 1
                    # Add items from seentable as the last choice
                    # print(PR, CR, PQ, CQ)
                    if PR > 0 or CR > 0:
                        for i in range(len(prevs+crevs)):
                            if i < len(prevs):
                                if prevs[i] not in total:
                                    productReviews.append(prevs[i])
                                    total.append(prevs[i])
                                    PR -= 1; CR -= 1
                            else:
                                if crevs[i-len(prevs)] not in total:
                                    companyReviews.append(crevs[i-len(prevs)])
                                    total.append(crevs[i-len(prevs)])
                                    PR -= 1; CR -= 1
                            if PR <= 0 and CR <= 0: break
                    # print(PR, CR, PQ, CQ)
                    if PR > 0: PQ = PR; PR = 0
                    if CR > 0: CQ = CR; CR = 0
                    # print(PR, CR, PQ, CQ)
                    if PQ > 0 or CQ > 0:
                        for i in range(len(pques+cques)):
                            if i < len(pques):
                                if pques[i] not in total:
                                    # print(pques[i])
                                    productQuestions.append(pques[i])
                                    total.append(pques[i])
                            else:
                                if cques[i-len(pques)] not in total:
                                    companyQuestions.append(cques[i-len(pques)])
                                    total.append(cques[i-len(pques)])
                            PQ -= 1; CQ -= 1
                            if PQ <= 0 and CQ <= 0: break
                    # print(PR, CR, PQ, CQ)
        try: users = load(open('recommender/users.pkl', 'rb'))
        except: users = {}
        if userId not in users.keys():
            users[userId] = {}
        if (round-1) not in users[userId].keys():
            users[userId][round-1] = [total, productReviews, companyReviews, productQuestions, companyQuestions]
            dump(users, open('recommender/users.pkl', 'wb'))
    else:
        round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
        users = load(open('recommender/users.pkl', 'rb'))
        [total, productReviews, companyReviews, productQuestions, companyQuestions] = users[userId][round-1]
        total = shuffle(total)
    return productReviews, companyReviews, productQuestions, companyQuestions, total

def anonymous_recommend(round: int):
    random = (round > (DAILY_ITEMS_QOUTA/ROUND_NUM_OF_REVIEWS))
    round = (round-1) % (DAILY_ITEMS_QOUTA//ROUND_NUM_OF_REVIEWS) + 1
    if not os.path.isfile('recommender/collobarative/anonymous_data.pkl'):
        calc_anonymous_data()
    [prevs, crevs, pques, cques, total] = load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[round-1]
    if random: total = shuffle(total)
    return prevs, crevs, pques, cques, total
