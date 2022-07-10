import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin

from abc import ABCMeta, abstractmethod
from typing import Any, Tuple, Union


class RecommenderBase(BaseEstimator, RegressorMixin, metaclass=ABCMeta):
    """
    Abstract base class for all recommender models.
    All subclasses should implement the fit() and predict() methods

    Arguments:
        min_rating {int} -- Smallest rating possible (default: {0})
        max_rating {int} -- Largest rating possible (default: {5})
        verbose {str} -- Verbosity when fitting. Values possible are 0 to not print anything, 1 to print fitting model (default: {1})

    Attributes:
        n_users {int} -- Number of users
        n_items {int} -- Number of items
        global_mean {float} -- Global mean of all ratings
        user_id_map {dict} -- Mapping of user ids to assigned integer ids
        item_id_map {dict} -- Mapping of item ids to assigned integer ids
        known_users {set} -- Set of known user_ids
        known_items {set} -- Set of known item_ids
    """

    @abstractmethod
    def __init__(self, min_rating: float = 0, max_rating: float = 5, verbose: int = 0):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.verbose = verbose
        return

    @property
    def known_users(self):
        """
        List of known user_ids
        """
        return set(self.user_id_map.keys())

    @property
    def known_items(self):
        """
        List of known item_ids
        """
        return set(self.item_id_map.keys())

    def contains_user(self, user_id: Any) -> bool:
        """
        Checks if model was trained on data containing given user_id

        Args:
            user_id (any): User id

        Returns:
            bool: If user_id is known
        """
        return user_id in self.known_users

    def contains_item(self, item_id: Any) -> bool:
        """
        Checks if model was trained on data containing given item_id

        Args:
            item_id (any): Item id

        Returns:
            bool: If item_id is known
        """
        return item_id in self.known_items

    def _preprocess_data(
        self, X: pd.DataFrame, y: pd.Series = None, type: str = "fit"
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, list, list]]:
        """
        Preprocessing steps before doing fit, update or predict

        Arguments:
            X {pd.DataFrame} -- Dataframe containing columns user_id, item_id
            y {pd.Series} -- Series containing rating
            type {str} -- The type of preprocessing to do. Allowed options are ('fit', 'predict', 'update'). Defaults to 'fit'

        Returns:
            X [pd.DataFrame] -- Dataframe with columns user_id, item_id and rating
            known_users [list, 'on update only'] -- List containing already known users in X. Only returned for type update
            new_users [list, 'on update only'] -- List containing new users in X. Only returned for type update
        """
        X = X.loc[:, self.columns[:2]]

        if type != "predict":
            X[self.columns[2]] = y

        if type in ("fit", "update"):
            # Check for duplicate user-item ratings
            if X.duplicated(subset=self.columns[:2]).sum() != 0:
                raise ValueError("Duplicate user-item ratings in matrix")

            # Shuffle rows
            X = X.sample(frac=1, replace=False)

        if type == "fit":
            # Create mapping of user_id and item_id to assigned integer ids
            user_ids = X[self.columns[0]].unique()
            item_ids = X[self.columns[1]].unique()
            self.user_id_map = {user_id: i for (i, user_id) in enumerate(user_ids)}
            self.item_id_map = {item_id: i for (i, item_id) in enumerate(item_ids)}
            self.n_users = len(user_ids)
            self.n_items = len(item_ids)

        elif type == "update":
            # Keep only item ratings for which the item is already known
            items = self.item_id_map.keys()
            X = X.query(f"{self.columns[1]} in @items").copy()

            # Add information on new users
            new_users, known_users = [], []
            users = X[self.columns[0]].unique()
            new_user_id = max(self.user_id_map.values()) + 1

            for user in users:
                if user in self.user_id_map.keys():
                    known_users.append(user)
                    continue

                # Add to user id mapping
                new_users.append(user)
                self.user_id_map[user] = new_user_id
                new_user_id += 1

        # Remap user id and item id to assigned integer ids
        X.loc[:, self.columns[0]] = X[self.columns[0]].map(self.user_id_map)
        X.loc[:, self.columns[1]] = X[self.columns[1]].map(self.item_id_map)

        if type == "predict":
            # Replace missing mappings with -1
            X.fillna(-1, inplace=True)

        if type == "update":
            return X, known_users, new_users
        else:
            return X

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit model to given data

        Args:
            X {pandas DataFrame} -- Dataframe containing columns user_id, item_id
            y {pandas DataFrame} -- Series containing rating
        """
        return self

    @abstractmethod
    def predict(self, X: pd.DataFrame, bound_ratings: bool = True) -> list:
        """
        Predict ratings for given users and items

        Args:
            X (pd.DataFrame): Dataframe containing columns user_id and item_id
            bound_ratings (bool): Whether to bound ratings in range [min_rating, max_rating] (default: True)

        Returns:
            list: List containing rating predictions of all user, items in same order as input X
        """
        return []

    def recommend_mobiles(
        self,
        user: Any,
        amount: int = 10,
        include_user: bool = True,
        bound_ratings: bool = True,
        item_type = None,
    ) -> pd.DataFrame:
        """
        Returns a DataFrame of recommendations of items for a given user sorted from highest to lowest.
        Args:
            user (any): User_id to get recommendations for (not assigned user_id from self.user_id_map)
            items_known (list, optional): List of items already known by user and to not be considered in recommendations. Defaults to None.
            include_user (bool, optional): Whether to include the user_id in the output DataFrame or not. Defaults to True.
            bound_ratings (bool): Whether to bound ratings in range [min_rating, max_rating] (default: True)
        Returns:
            pd.DataFrame: Recommendations DataFrame for user with columns user_id (optional), item_id, rating sorted from highest to lowest rating 
        """
        items = list(self.item_id_map.keys())
        
        # Get rating predictions for given user and all unknown items
        items_recommend = pd.DataFrame({self.columns[0]: user, self.columns[1]: items})
        items_recommend[self.columns[3]] = self.predict(
            X=items_recommend, bound_ratings=False
        )
        # Sort and keep top n items
        items_recommend.sort_values(by=self.columns[3], ascending=False, inplace=True)
        if item_type != None:
            items_recommend = items_recommend[items_recommend[self.columns[1]].astype(str).str[0] == str(item_type)].head(amount)
        else:
            items_recommend = items_recommend.head(amount)
        # Bound ratings
        if bound_ratings:
            items_recommend[self.columns[3]] = items_recommend[self.columns[3]].clip(
                lower=self.min_rating, upper=self.max_rating
            )
        if not include_user:
            items_recommend.drop([self.columns[0]], axis="columns", inplace=True)
        return items_recommend

    def recommend_items(
        self,
        user: Any,
        productReviewAmount: int = 32,
        productQuestionAmount: int = 24,
        companyReviewAmount: int = 16,
        companyQuestionAmount: int = 8,
        items_known: list = None,
        include_user: bool = True,
        bound_ratings: bool = True,
    ) -> Tuple[list, list,list, list,list, list,list, list]:
        """
        Returns a DataFrame of recommendations of items for a given user sorted from highest to lowest.

        Args:
            user (any): User_id to get recommendations for (not assigned user_id from self.user_id_map)
            items_known (list, optional): List of items already known by user and to not be considered in recommendations. Defaults to None.
            include_user (bool, optional): Whether to include the user_id in the output DataFrame or not. Defaults to True.
            bound_ratings (bool): Whether to bound ratings in range [min_rating, max_rating] (default: True)

        Returns:
            pd.DataFrame: Recommendations DataFrame for user with columns user_id (optional), item_id, rating sorted from highest to lowest rating 
        """
        productReviewId=[]
        productReviewRate=[]
        productQuestionId=[]
        productQuestionRate=[]
        companyQuestionId=[]
        companyQuestionRate=[]
        companyreviewId=[]
        companyreviewRate=[]
        items = list(self.item_id_map.keys())

        # If items_known is provided then filter by items that the user does not know
        if items_known is not None:
            items_known = list(items_known)
            items = [item for item in items if item not in items_known]

        # Get rating predictions for given user and all unknown items
        items_recommend = pd.DataFrame({"user_id": user, "item_id": items})
        items_recommend["rating_pred"] = self.predict(
            X=items_recommend, bound_ratings=False
        )

        # Sort and keep top n items
        items_recommend.sort_values(by="rating_pred", ascending=False, inplace=True)
        

        indexs=items_recommend.index
        for index in indexs:
            item_id = items_recommend['item_id'][index]
            rate = items_recommend['rating_pred'][index]
            if item_id[0]=='0':
                productReviewId.append(item_id)
                productReviewRate.append(rate)
            elif item_id[0]=='2':
                productQuestionId.append(item_id)
                productQuestionRate.append(rate)
            elif item_id[0]=='1':
                companyreviewId.append(item_id)
                companyreviewRate.append(rate)
            elif item_id[0]=='3':
                companyQuestionId.append(item_id)
                companyQuestionRate.append(rate)     
                 
        """ print(productReviewId)
        print(productReviewRate)
        print(productQuestionId)
        print(productQuestionRate)
        print(companyreviewId)
        print(companyreviewRate)
        print(companyQuestionId)
        print(companyQuestionRate) """          
        productReviewId = productReviewId[:productReviewAmount]
        productReviewRate = productReviewRate[:productReviewAmount]

        productQuestionId=productQuestionId[:productQuestionAmount]
        productQuestionRate=productQuestionRate[:productQuestionAmount]

        companyreviewId=companyreviewId[:companyReviewAmount]
        companyreviewRate=companyreviewRate[:companyReviewAmount]

        companyQuestionId=companyQuestionId[:companyQuestionAmount]
        companyQuestionRate=companyQuestionRate[:companyQuestionAmount]
        # Bound ratings
        if bound_ratings:
            items_recommend["rating_pred"] = items_recommend["rating_pred"].clip(
                lower=self.min_rating, upper=self.max_rating
            )

        if not include_user:
            items_recommend.drop(["user_id"], axis="columns", inplace=True)
       
        return productReviewId, productReviewRate, productQuestionId, productQuestionRate,\
                companyreviewId, companyreviewRate, companyQuestionId, companyQuestionRate

 