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
            phone = Mobile.objects.get(id=phone)
            review = PReview(id=id, userId=user, productId=phone, rating=rate, time=date, pros=pros, cons=cons,
                    rating1=rate1, rating2=rate2, rating3=rate3, rating4=rate4, rating5=rate5, rating6=rate6)
            review.save()
            return review
        except Exception as e:
            print(e)
            return None

    def create_new_Preview_ifNotExist(self, review):
        try:
            id, user, phone, rate = str(review['_id']), str(review['user']), str(review['phone']), review['generalRating']
            rate1, rate2, rate3 = review['uiRating'], review['manQuality'], review['valFMon']
            rate4, rate5, rate6 = review['camera'], review['callQuality'], review['batteryRating']
            date, pros, cons = dateAsNumber(review['createdAt']), review['pros'], review['cons']
            user = User.objects.get(id=user)
            phone = Mobile.objects.get(id=phone)
            review = PReview.objects.get_or_create(id=id, userId=user, productId=phone, rating=rate, time=date, 
                pros=pros, cons=cons, rating1=rate1, rating2=rate2, rating3=rate3, rating4=rate4, rating5=rate5,
                rating6=rate6)
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

    def get_Previews_by_mobiles(self, mobiles = []):
        revs = []
        for mobile in mobiles:
            revs.append(PReview.objects.filter(productId=mobile))
        revs_lst = []
        for mobile_revs in revs:
            for rev in mobile_revs:
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
            review = PReview.objects.get(id=review)
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
            like.save()
            return like
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Prev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = PReview.objects.get(id=review)
            like = Prev_Likes.objects.get(userId=user, reviewId=review)
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
            like = Prev_Most_Liked.objects.update_or_create(userId=user, reviewId=review)['Prev_Most_Liked']
            like.save()
            return like
        except Exception as e:
            print(e)
            return None
    
    def get_Most_liked_Prev(self, user: str):
        try:
            user = User.objects.get(id=user)
            like = Prev_Most_Liked.objects.get(userId=user)
            return like.reviewId
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
            id, user, company, rate = str(review['_id']), str(review['user']), str(review['company']), review['generalRating']
            date, pros, cons = dateAsNumber(review['createdAt']), review['pros'], review['cons']
            user = User.objects.get(id=user)
            company = Company.objects.get(id=company)
            review = CReview.objects.get_or_create(id=id, userId=user, companyId=company, rating=rate, time=date, 
                pros=pros, cons=cons)
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
            review = CReview.objects.get(id=review)
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
            like = Crev_Most_Liked.objects.update_or_create(userId=user, reviewId=review)['Crev_Most_Liked']
            like.save()
            return like
        except Exception as e:
            print(e)
            return None
        
    def get_Most_liked_Crev(self, user: str):
        try:
            user = User.objects.get(id=user)
            like = Crev_Most_Liked.objects.get(userId=user)
            return like.reviewId
        except Exception as e:
            # print(e)
            return None    

    def add_Crev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            like = Crev_Likes.objects.create(userId=user, reviewId=review)
            like.save()
            return like
        except Exception as e:
            print('ADD: ', e)
            return None

    def remove_Crev_like(self, user: str, review: str):
        try:
            user = User.objects.get(id=user)
            review = CReview.objects.get(id=review)
            like = Crev_Likes.objects.get(userId=user, reviewId=review)
            like.delete()
            return True
        except Exception as e:
            print('REMOVE: ', e)
            return False
