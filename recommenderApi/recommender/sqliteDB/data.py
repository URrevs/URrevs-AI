from recommender.models import *
from recommenderApi.imports import dt, load, dump
from recommender.collobarative.seenTable import dateAsNumber

class SQLite_Database:
    def __init__(self):
        '''
            This class contains all the functions to interact with the database
            { 
                create_new_user , get_user , update_user_ratios
                create_company , get_company
                create_mobile , get_mobile
                create_Preview , get_Preview
                create_Creview, get_Creview
            }
        '''
        # print('SQLite_Database')
        
    def get_user(self, id: str = ''):
        '''
            This function returns the user object
        '''
        if id == '':
            users = User.objects.all()
        else:
            try:
                users = User.objects.get(pk= id)
            except User.DoesNotExist:
                return None
        return users

    def create_new_user(self, id: str, name: str):
        try:
            user = User(id=id, name=name)
            user.save()
            return user
        except Exception as e:
            print(e)
            return None
    
    def create_new_user_ifNotExist(self, user):
        id, name = str(user['_id']), user['name']
        user = User.objects.get_or_create(id=id, name=name)
        return user

    def update_user_ratios(self, userId: str, PR: int, CR: int, PQ: int, CQ: int):
        try:
            user = User.objects.get(id=userId)
            user.PR = PR
            user.CR = CR
            user.PQ = PQ
            user.CQ = CQ
            user.save()
            return user
        except Exception as e:
            print(e)
            return None

    def get_user_products(self, user):
        user = User.objects.get(id=user)
        lst = []
        if user != None:
            products = ProductOwner.objects.filter(user=user)
            lst = [product.product.id for product in products]
        return lst
    
    def get_user_companies(self, user):
        user = User.objects.get(id=user)
        lst = []
        if user != None:
            companies = CompanyOwner.objects.filter(user=user)
            lst = [company.company.id for company in companies]
        return lst
    
    def create_company(self, id: str = '', name: str = ''):
        try:
            company = Company(id=id, name=name)
            company.save()
            return company
        except Exception as e:
            print(e)
            return None

    def create_new_company_ifNotExist(self, company):
        id, name = str(company['_id']), company['nameLower']
        company = Company.objects.get_or_create(id=id, name=name)
        return company

    def get_company(self, id: str = ''):
        if id == '':
            company = Company.objects.all()
        else:
            try:
                company = Company.objects.get(pk= id)
            except Company.DoesNotExist:
                return None
        return company

    def create_mobile(self, id: str = '', name: str = '', company: str = '', price: int = 0):
        try:
            company = Company.objects.get(id=company)
            mobile = Mobile(id=id, name=name, company=company, price=price)
            mobile.save()
            return mobile
        except Exception as e:
            print(e)
            return None

    def create_new_mobile_ifNotExist(self, mobile):
        id, name, company, price = str(mobile['_id']), mobile['name'], mobile['company'], mobile['price']
        company = Company.objects.get(name=company.lower())
        mobile = Mobile.objects.get_or_create(id=id, name=name, company=company, price=price)
        return mobile

    def get_mobile(self, id: str = ''):
        if id == '':
            mobile = Mobile.objects.all()
        else:
            try:
                mobile = Mobile.objects.get(pk= id)
            except Mobile.DoesNotExist:
                return None
        return mobile

    def get_company_from_mobile(self, mobile: str):
        try:
            mobile = Product.objects.get(id=mobile)
            return mobile.company
        except Mobile.DoesNotExist:
            return None
    
    def create_Preview(self, id: str, user: str, phone: str, rate: int, rate1: int, rate2: int, rate3: int,
                rate4: int, rate5: int, rate6: int, date: dt, pros: str, cons: str):
        try:
            user = User.objects.get(id=user)
            phone: Mobile = Mobile.objects.get(id=phone)
            review = PReview(id=id, userId=user, productId=phone, rating=rate, time=date, pros=pros, cons=cons,
                    rating1=rate1, rating2=rate2, rating3=rate3, rating4=rate4, rating5=rate5, rating6=rate6)
            review.save()
            try:
                ProductOwner.objects.get_or_create(user=user, product=phone)
                CompanyOwner.objects.get_or_create(user=user, company=phone.company)
            except Exception as e:
                print('create owner raws: ', e)
                return None
            return review
        except Exception as e:
            print('create Prev: ', e)
            return None

    def create_new_Preview_ifNotExist(self, review):
        try:
            id, userId, phoneId, rate = str(review['_id']), str(review['user']), str(review['phone']), review['generalRating']
            rate1, rate2, rate3 = review['uiRating'], review['manQuality'], review['valFMon']
            rate4, rate5, rate6 = review['camera'], review['callQuality'], review['batteryRating']
            date, pros, cons = dateAsNumber(review['createdAt']), review['pros'], review['cons']
            user = User.objects.get(id=userId)
            phone = Mobile.objects.get(id=phoneId)
            review = PReview.objects.get_or_create(id=id, userId=user, productId=phone, rating=rate, time=date, 
                pros=pros, cons=cons, rating1=rate1, rating2=rate2, rating3=rate3, rating4=rate4, rating5=rate5,
                rating6=rate6)
            try:
                ProductOwner.objects.get_or_create(user=user, product=phone)
                CompanyOwner.objects.get_or_create(user=user, company=phone.company)
            except Exception as e:
                print('create owner raws: ', e)
                return None
            self.update_Pquestion_owner(user=userId, phone=phoneId)
            return review
        except Exception as e:
            print(e)
            return None

    def get_Preview(self, id: str = ''):
        if id == '':
            review = PReview.objects.all()
        else:
            try:
                review = PReview.objects.get(pk= id)
            except PReview.DoesNotExist:
                return None
        return review

    def get_Prevs(self, limit: int = -1):
        revs = PReview.objects.all()[:limit]
        revs = [[f'0{rev.id}', rev.likesCounter, rev.commentsCounter, rev.time, 
            len(str(rev.pros).split())+len(str(rev.cons).split())] for rev in revs]
        return revs

    def get_Previews_by_mobiles(self, mobiles = []):
        revs = []
        for mobile in mobiles:
            revs.append(PReview.objects.filter(productId=mobile))
        revs_lst = []
        for mobile_revs in revs:
            for rev in mobile_revs:
                revs_lst.append(rev.id)
        return revs_lst
    
    def get_Previews_by_mobile(self, mobilesIds = []):
        revs = []
        for mobile in mobilesIds:
            try: mobile = Mobile.objects.get(id=mobile)
            except: pass
            revs.extend(PReview.objects.filter(productId=mobile))
        revs_lst = []
        for rev in revs:
            revs_lst.append(rev.id)
        return revs_lst

    def get_all_mobiles_have_reviews(self):
        mobiles = PReview.objects.values_list('productId', flat=True).distinct()
        mobiles_lst = []
        for mobile in mobiles:
            mobiles_lst.append(mobile)
        try: vars = load(open('recommenderApi/vars.pkl', 'rb'))
        except: vars = {}
        vars['mobiles'] = mobiles_lst
        dump(vars, open('recommenderApi/vars.pkl', 'wb'))
        return mobiles_lst

    def update_Prev_interaction(self, review: str, interactions: list):
        try:
            review: PReview = PReview.objects.get(id=review)
            review.likesCounter = max([review.likesCounter+interactions[0], 0])
            review.commentsCounter += interactions[1]
            review.hatesCounter += interactions[2]
            review.save()
            return review
        except Exception as e:
            print(e)
            return None

    def check_Prev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            Prev_Likes.objects.get(userId=user, reviewId=review)
            return True
        except Exception as e:
            # print('CHECK: ', e)
            return False

    def add_Prev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            like = Prev_Likes.objects.create(userId=user, reviewId=review)
            # like.save()
            return like
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Prev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            like: Prev_Likes = Prev_Likes.objects.get(userId=user, reviewId=review)
            like.delete()
            return True
        except Exception as e:
            print('REMOVE: ', e)
            return False

    def add_Most_liked_Prev(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            like = Prev_Most_Liked(userId=user, reviewId=review)
            like.save()
            return like
        except Exception as e:
            print(e)
            return None
    
    def update_add_Most_liked_Prev(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            Prev_Most_Liked.objects.update_or_create(userId=user, reviewId=review)
            # like.save()
            # return like
        except Exception as e:
            print(e)
            return None
    
    def get_Most_liked_Prev(self, user: str):
        try:
            user = User.objects.get(id=user)
            like: Prev_Most_Liked = Prev_Most_Liked.objects.get(userId=user)
            return like.reviewId.id
        except Exception as e:
            # print(e)
            return None

    def create_Creview(self, id: str, user: str, company: str, rate: int, date: dt, pros: str, cons: str):
        try:
            user = User.objects.get(id=user)
            company = Company.objects.get(id=company)
            review = CReview(id=id, userId=user, companyId=company, rating=rate, time=date, pros=pros, cons=cons)
            review.save()
            return review
        except Exception as e:
            print(e)
            return None
    
    def create_new_Creview_ifNotExist(self, review):
        try:
            id, userId, companyId, rate = str(review['_id']), str(review['user']), str(review['company']), review['generalRating']
            date, pros, cons = dateAsNumber(review['createdAt']), review['pros'], review['cons']
            user = User.objects.get(id=userId)
            company = Company.objects.get(id=companyId)
            review = CReview.objects.get_or_create(id=id, userId=user, companyId=company, rating=rate, time=date, 
                pros=pros, cons=cons)
            self.update_Cquestion_owner(user=userId, company=companyId)
            return
        except Exception as e:
            print(e)
            return None

    def get_Creview(self, id: str = ''):
        if id == '':
            review = CReview.objects.all()
        else:
            try:
                review = CReview.objects.get(pk= id)
            except CReview.DoesNotExist:
                return None
        return review
    
    def get_Crevs(self, limit: int = -1):
        revs = CReview.objects.all()[:limit]
        revs = [[f'1{rev.id}', rev.likesCounter, rev.commentsCounter, rev.time, 
            len(str(rev.pros).split())+len(str(rev.cons).split())] for rev in revs]
        return revs
    
    def get_Creviews_by_companies(self, companies = []):
        revs = []
        for company in companies:
            revs.append(CReview.objects.filter(companyId=company))
        revs_lst = []
        for company_revs in revs:
            for rev in company_revs:
                revs_lst.append(rev.id)
        return revs_lst

    def update_Crev_interaction(self, review: str, interactions: list):
        try:
            review: CReview = CReview.objects.get(id=review)
            review.likesCounter = max([review.likesCounter+interactions[0], 0])
            review.commentsCounter += interactions[1]
            review.hatesCounter += interactions[2]
            review.save()
            return review
        except Exception as e:
            print(e)
            return None

    def check_Crev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            Crev_Likes.objects.get(userId=user, reviewId=review)
            return True
        except Exception as e:
            # print('CHECK: ', e)
            return False

    def add_Most_liked_Crev(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            like = Crev_Most_Liked(userId=user, reviewId=review)
            like.save()
            return like
        except Exception as e:
            print(e)
            return None
    
    def update_add_Most_liked_Crev(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            Crev_Most_Liked.objects.update_or_create(userId=user, reviewId=review)
            # like.save()
            # return like
        except Exception as e:
            print(e)
            return None
        
    def get_Most_liked_Crev(self, user: str):
        try:
            user = User.objects.get(id=user)
            like: Crev_Most_Liked = Crev_Most_Liked.objects.get(userId=user)
            return like.reviewId.id
        except Exception as e:
            # print(e)
            return None    

    def add_Crev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            like: Crev_Likes = Crev_Likes.objects.create(userId=user, reviewId=review)
            like.save()
            return like
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Crev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            like: Crev_Likes = Crev_Likes.objects.get(userId=user, reviewId=review)
            like.delete()
            return True
        except Exception as e:
            print('REMOVE: ', e)
            return False

    def create_Pquestion(self, id: str, user: str, phone: str, date: float, question: str, 
            accepted_answer: bool):
        try:
            user = User.objects.get(id=user)
            phone = Mobile.objects.get(id=phone)
            question: PQuestion = PQuestion(id=id, userId=user, productId=phone, question=question, time=date, 
                    hasAcceptedAnswer=accepted_answer)
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def create_new_Pquestion_ifNotExist(self, question):
        try:
            id, user, phone = str(question['_id']), str(question['user']), str(question['phone'])
            date, content = dateAsNumber(question['createdAt']), str(question['content'])
            try: accepted_answer = bool(question['acceptedAns']!=None)
            except: accepted_answer = False
            user = User.objects.get(id=user)
            phone = Mobile.objects.get(id=phone)
            question = PQuestion.objects.get_or_create(id=id, userId=user, productId=phone, time=date, 
                question=content, hasAcceptedAnswer=accepted_answer)
            return question
        except Exception as e:
            print(e)
            return None
    
    def update_Pquestion_owner(self, user, phone):
        try:
            pques: PQuestion = PQuestion.objects.filter(userId=user, productId=phone)
            if pques != None:
                try:
                    pques.product_owner = True
                    pques.save()
                except:
                    for pq in pques:
                        pq.product_owner = True
                        pq.save()
        except Exception as e:
            return None

    def get_Pquestion(self, id: str = ''):
        if id == '':
            question = PQuestion.objects.all()
        else:
            try:
                question = PQuestion.objects.get(pk= id)
            except PQuestion.DoesNotExist:
                return None
        return question
    
    def get_Pquestions_by_products(self, products: list):
        try:
            ques_lst = []
            for product in products:
                for ques in PQuestion.objects.filter(productId=product.product):
                    ques_lst.append(ques.id)
            return ques_lst
        except Exception as e:
            print(e)
            return None
    
    def get_Pquestions_by_mobiles(self, mobiles: list):
        try:
            ques_lst = []
            for mobile in mobiles:
                mobile = Product.objects.get(id=mobile)
                for ques in PQuestion.objects.filter(productId=mobile):
                    ques_lst.append(ques.id)
            return ques_lst
        except Exception as e:
            print(e)
            return []

    def set_Pques_accepted_answer(self, question: str, accepted_answer: bool = True):
        try:
            question: PQuestion = PQuestion.objects.get(id=question)
            question.hasAcceptedAnswer = accepted_answer
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def get_answered_Pquestions(self, limit: int = -1, order: bool = False, answer: bool = True):
        if order: questions = PQuestion.objects.filter(hasAcceptedAnswer=answer).order_by(['-upvotesCounter', '-time'])[:limit]
        else: questions = PQuestion.objects.filter(hasAcceptedAnswer=answer)[:limit]
        ques_lst = []
        for question in questions:
            ques_lst.append([f'2{question.id}', question.upvotesCounter, question.answersCounter, question.time, 0])
        return ques_lst
        # return questions

    # This function is only used for tracker (about my page visits)
    def get_owned_mobiles_questions_mongo(self, userId):
        user = User.objects.get(id=userId)
        products = ProductOwner.objects.filter(user=user)
        questions = []
        for question in self.get_Pquestions_by_products(products=products):
            questions.append({
                'id': userId, 
                'question': f'2{question}'
                })
        return questions

    def get_owned_mobiles_mongo(self, userId):
        user = User.objects.get(id=userId)
        products = ProductOwner.objects.filter(user=user)
        questions = []
        for question in self.get_Pquestions_by_products(products=products):
            questions.append(question.id)
        return questions


    def get_all_mobiles_have_questions(self):
        mobiles = PQuestion.objects.values_list('productId', flat=True).distinct()
        mobiles_lst = []
        for mobile in mobiles:
            mobiles_lst.append(mobile)
        try: vars = load(open('recommenderApi/vars.pkl', 'rb'))
        except: vars = {}
        vars['mobiles_questions'] = mobiles_lst
        dump(vars, open('recommenderApi/vars.pkl', 'wb'))
        return mobiles_lst

    def update_Pques_interaction(self, question: str, interactions: list):
        try:
            question: PQuestion = PQuestion.objects.get(id=question)
            question.upvotesCounter = max([question.upvotesCounter+interactions[0], 0])
            question.answersCounter += interactions[1]
            question.hatesCounter += interactions[2]
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def check_Pques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = PQuestion.objects.get(id=question)
            Pques_Upvotes.objects.get(userId=user, questionId=question)
            return True
        except Exception as e:
            # print('CHECK: ', e)
            return False

    def add_Pques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = PQuestion.objects.get(id=question)
            upvote = Pques_Upvotes.objects.create(userId=user, questionId=question)
            # upvote.save()
            return upvote
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Pques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = PQuestion.objects.get(id=question)
            upvote: Pques_Upvotes = Pques_Upvotes.objects.get(userId=user, questionId=question)
            upvote.delete()
            return True
        except Exception as e:
            print('REMOVE: ', e)
            return False

    def create_Cquestion(self, id: str, user: str, company: str, date: float, question: str, 
            accepted_answer: bool):
        try:
            user = User.objects.get(id=user)
            company = Company.objects.get(id=company)
            question: CQuestion = CQuestion(id=id, userId=user, companyId=company, question=question, time=date, 
                    hasAcceptedAnswer=accepted_answer)
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def create_new_Cquestion_ifNotExist(self, question):
        try:
            id, user, company = str(question['_id']), str(question['user']), str(question['company'])
            date, content = dateAsNumber(question['createdAt']), str(question['content']) 
            try: accepted_answer = bool(question['acceptedAns']!=None)
            except: accepted_answer = False
            user = User.objects.get(id=user)
            company = Company.objects.get(id=company)
            question = CQuestion.objects.get_or_create(id=id, userId=user, companyId=company, time=date, 
                question=content, hasAcceptedAnswer=accepted_answer)
            return question
        except Exception as e:
            print(e)
            return None

    def update_Cquestion_owner(self, user, company):
        try:
            user = User.objects.get(id=user)
            company = Company.objects.get(id=company)
            cques: CQuestion = CQuestion.objects.filter(userId=user, companyId=company)
            if cques != None:
                try:
                    cques.company_owner = True
                    cques.save()
                except:
                    for cq in cques:
                        cq.company_owner = True
                        cq.save()
        except Exception as e:
            return None

    def get_owned_companies_mongo(self, userId):
        user = User.objects.get(id=userId)
        companies = CompanyOwner.objects.filter(user=user)
        questions = []
        for question in self.get_Cquestions_by_companies(companies=companies):
            questions.append(question.id)
        return questions

    def get_Cquestions_by_companies(self, companies: list):
        try:
            ques_lst = []
            for company in companies:
                for ques in CQuestion.objects.filter(companyId=company.company):
                    ques_lst.append(ques.id)
            return ques_lst
        except Exception as e:
            print(e)
            return None

    def get_Cquestions_by_company(self, companies: list):
        # try:
            ques_lst = []
            for company in companies:
                for ques in CQuestion.objects.filter(companyId=company):
                    ques_lst.append(ques.id)
            return ques_lst
        # except Exception as e:
        #     print(e)
        #     return None


    def get_Cquestion(self, id: str = ''):
        if id == '':
            question = CQuestion.objects.all()
        else:
            try:
                question = CQuestion.objects.get(pk= id)
            except PQuestion.DoesNotExist:
                return None
        return question

    def set_Cques_accepted_answer(self, question: str, accepted_answer: bool = True):
        try:
            question: CQuestion = CQuestion.objects.get(id=question)
            question.hasAcceptedAnswer = accepted_answer
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def get_answered_Cquestions(self, limit: int = -1, order: bool = False, answer: bool = True):
        if order: questions = CQuestion.objects.filter(hasAcceptedAnswer=answer).order_by(['-upvotesCounter', '-time'])[:limit]
        else: questions = CQuestion.objects.filter(hasAcceptedAnswer=answer)[:limit]
        ques_lst = []
        for question in questions:
            ques_lst.append([f'3{question.id}', question.upvotesCounter, question.answersCounter, question.time, 0])
        return ques_lst
        # return questions

    def update_Cques_interaction(self, question: str, interactions: list):
        try:
            question: CQuestion = CQuestion.objects.get(id=question)
            question.upvotesCounter = max([question.upvotesCounter+interactions[0], 0])
            question.answersCounter += interactions[1]
            question.hatesCounter += interactions[2]
            question.save()
            return question
        except Exception as e:
            print(e)
            return None

    def check_Cques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = CQuestion.objects.get(id=question)
            Cques_Upvotes.objects.get(userId=user, questionId=question)
            return True
        except Exception as e:
            # print('CHECK: ', e)
            return False

    def add_Cques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = CQuestion.objects.get(id=question)
            upvote = Cques_Upvotes.objects.create(userId=user, questionId=question)
            # upvote.save()
            return upvote
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Cques_upvote(self, user: str, question: str):
        try:
            user = User.objects.get(id=user)
            question = CQuestion.objects.get(id=question)
            upvote: Cques_Upvotes = Cques_Upvotes.objects.get(userId=user, questionId=question)
            upvote.delete()
            return True
        except Exception as e:
            print('REMOVE: ', e)
            return False
