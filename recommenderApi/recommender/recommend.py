from sklearn.utils import shuffle
from recommender.asyn_tasks.tasks import addToSeenTable
from recommender.collobarative.recommend import MatrixFactorization
from recommender.collobarative.seenTable import SeenTable
from recommender.reviews.reviewsRecommender import ReviewContentRecommender
from recommender.collobarative.reviewTracker import Trackers
from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS
from recommenderApi.imports import load, os, dump
from recommender.collobarative.train import calc_anonymous_data

def check_interactions_existance(userId: str, search_in: str = 'items'):
    if search_in == 'items':
        return Trackers(loadfile=True).checkUserExist(userId)
    else:
        return Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).checkUserExist(userId)

def get_most_liked_reviews(userId: str, item_type = 'product'):
    return Trackers(loadfile=True).getMostLikedReview(userId, item_type)

def get_max_n_liked_mobiles(userId: str, n: int):
    return Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).getMaxNLikedMobile(userId, n)

def split(recs: list):
    reviews = []; spaces = []
    if len(recs) > 0:
        for rec in recs[0]:
            reviews.append(rec[0][1:])
            spaces.append(rec[1])
    return reviews, spaces

def recommend(userId: str, round: int, PR: int, CR: int, PQ: int, CQ: int):
    # first recommend questions
    productQuestions = []
    companyQuestions = []
    if len(productQuestions) < PQ: PR += (PQ-len(productQuestions))
    if len(companyQuestions) < CQ: CR += (CQ-len(companyQuestions))
    # then recommend reviews
    productReviews = []
    companyReviews = []
    total = []
    total_spaces = []
    # 3rd Model Recommend only PR
    seen_table = SeenTable(loadfile=True)
    if round <= (200//ROUND_NUM_OF_REVIEWS):
        items_interactions_existance_check = check_interactions_existance(userId, search_in='items')
        if check_interactions_existance(userId, search_in='mobiles') and items_interactions_existance_check:
            mobiles = get_max_n_liked_mobiles(userId, n=5)
            reviews = SQLite_Database().get_Previews_by_mobiles(mobiles)
            reference = get_most_liked_reviews(userId)[1:]
            reviews.append(reference)
            model = ReviewContentRecommender()
            recs, spaces = model.recommend(
                referenceId=reference, 
                recommend_type='product',
                n_recommendations=min([len(reviews)-1, 4+min([4, PQ])]), # 8 is calculated from 4 PR + 4 PQ but there is no PQ
                items=reviews
                )
            recs = [f'0{review}' for review in recs]
            productReviews, spaces = seen_table.check_if_review_shown_before(userId, recs[1:], spaces)
            PR = PR - len(productReviews)
        # --------------------------------------------------
        if items_interactions_existance_check:
            #  First Model recommend PR, CR
            items_recommender = MatrixFactorization()
            product_recs, spaces1 = items_recommender.recommend_items(userId, n_recommendations=PR)
            reviews, spaces1 = seen_table.check_if_review_shown_before(userId, product_recs, spaces1)
            productReviews.extend(reviews); spaces.extend(spaces1)
            PR = PR - len(reviews)

            company_recs, spaces2 = items_recommender.recommend_items(userId, n_recommendations=CR, item_type=1)
            companyReviews, spaces2 = seen_table.check_if_review_shown_before(userId, company_recs, spaces2)
            CR = CR - len(companyReviews)
            # --------------------------------------------------
            #  Second Model recommend PR, CR
            product_recs, spaces3 = model.recommend(referenceId=reference, n_recommendations=2*PR, known_items=total)
            product_recs = [f'0{review}' for review in product_recs]
            reviews, spaces3 = seen_table.check_if_review_shown_before(userId, product_recs, spaces3)
            productReviews.extend(reviews[:PR]); spaces.extend(spaces3[:PR])
            total.extend(productReviews); total_spaces.extend(spaces)
            PR = PR - len(reviews[:PR])

            reference = get_most_liked_reviews(userId, item_type='company')[1:]
            company_recs, spaces4 = model.recommend(referenceId=reference, n_recommendations=2*CR,
                known_items=total, recommend_type='company')
            company_recs = [f'1{review}' for review in company_recs]
            reviews, spaces4 = seen_table.check_if_review_shown_before(userId, company_recs, spaces4)
            companyReviews.extend(reviews[:CR]); spaces2.extend(spaces4[:CR])
            total.extend(companyReviews); total_spaces.extend(spaces4)
            CR = CR - len(reviews[:CR])
            # --------------------------------------------------
            # sorting list
            total = [x for x, _ in sorted(zip(total, total_spaces), key=lambda pair: pair[1])]
        # --------------------------------------------------
        more = (round > (200//ROUND_NUM_OF_REVIEWS))
        if PR > 0 or CR > 0:
            round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
            start = int((round - 1) * ROUND_NUM_OF_REVIEWS)
            end = int(round * ROUND_NUM_OF_REVIEWS)
            reviews = load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[start: end]
            for review in reviews:
                if review[1:] not in total:
                    if PR > 0 and review[0] == '0':
                        productReviews.append(review[1:])
                        total.append(review[1:])
                        seen_table.addToSeenTable(userId, [review])
                        PR -= 1
                    if CR > 0 and review[0] == '1':
                        companyReviews.append(review[1:])
                        total.append(review[1:])
                        seen_table.addToSeenTable(userId, [review])
                        CR -= 1
            if PR > 0 or CR > 0:
                for review in reviews:
                    if review[1:] not in total:
                        total.append(review[1:])
                        seen_table.addToSeenTable(userId, [review])
                        if review[0] == '0':
                            productReviews.append(review[1:]);PR -= 1
                        if review[0] == '1':
                            companyReviews.append(review[1:]);CR -= 1
                        if PR == 0 and CR == 0: break
        # save user data to not calculate it again
        users = load(open('recommender/users.pkl', 'rb'))
        if userId not in users.keys():
        # if round == 1 and not more:
            users[userId] = {}
        users[userId][round-1] = [total, productReviews, companyReviews, productQuestions, companyQuestions]
        dump(users, open('recommender/users.pkl', 'wb'))
    else:
        round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
        users = load(open('recommender/users.pkl', 'rb'))
        [total, productReviews, companyReviews, productQuestions, companyQuestions] = users[userId][round-1]
        total = shuffle(total)
    return productReviews, companyReviews, productQuestions, companyQuestions, total

def anonymous_recommend(round: int):
    random = (round > (200/ROUND_NUM_OF_REVIEWS))
    round = (round-1) % (200//ROUND_NUM_OF_REVIEWS) + 1
    start = int((round - 1) * ROUND_NUM_OF_REVIEWS)
    end = int(round * ROUND_NUM_OF_REVIEWS)
    if not os.path.isfile('recommender/collobarative/anonymous_data.pkl'):
        calc_anonymous_data()
    reviews = load(open('recommender/collobarative/anonymous_data.pkl', 'rb'))[start: end]
    product = [review[1:] for review in reviews if review[0] == '0']
    company = [review[1:] for review in reviews if review[0] == '1']
    if random: reviews = shuffle(reviews)
    total = [review[1:] for review in reviews]
    return product, company, total
