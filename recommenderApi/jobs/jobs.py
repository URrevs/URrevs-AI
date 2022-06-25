from recommender.collobarative.train import train_and_update
from recommenderApi.imports import dt

class schedule:
	def __init__(self, date: dt, first: bool = False) -> None:
		self.date = date
		self.first = first

	def schedule_job(self):
		train_and_update(self.date, self.first)