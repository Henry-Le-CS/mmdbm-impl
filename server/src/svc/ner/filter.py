import pandas as pd

class Filter:
	def filter_by_director(self, df: pd.DataFrame, director: str) -> pd.DataFrame:
		return df.loc[df.director.str.lower() == director.lower()]

	def filter_by_actor(self, df: pd.DataFrame, actor: str) -> pd.DataFrame:
		return pd.DataFrame([mov_ for mov_ in df.itertuples() if actor.lower() in mov_.actors.lower()])
		
	def filter_by_genre(self, df: pd.DataFrame, genre: str) -> pd.DataFrame:
		return pd.DataFrame([mov_ for mov_ in df.itertuples() if genre.lower() in mov_.genre.lower()])
	
	def filter_by_title(self, df: pd.DataFrame, title: str) -> pd.DataFrame:
		return df.loc[df.original_title.str.lower() == title.lower()]
		
	def filter_by_year(self, df: pd.DataFrame, year: str) -> pd.DataFrame:
		return df.loc[df.year == year]
	