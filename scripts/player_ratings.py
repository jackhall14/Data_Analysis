# Author: Jack Hall
# Last Updated: 27/10/2018
# Updates to make: Find a way to remove values that select wrong validation question
#					Need to remove duplicated plotting code
# 
# Directions for us: python player_ratings.py -s <y> or -s2 <y> for single or season analysis respectively.
#						Single match options (use in addition to -s <y>):
# 							[-f <y> file to analysis]
#							[-v <y> for validation question check]
#							[-m <y> for pie plot of motm]
#							[-p <y> for bar chart of player ratings]
# 

import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
import argparse

# Plot settings
plt.style.use("ggplot")
sns.set_style("whitegrid")
sns.set()
sns.color_palette("Paired", 10)

# Create parse arguements
parser = argparse.ArgumentParser(description='Data analysis of avg. player ratings')
parser.add_argument('-f','--file',type=str,help='(CSV) File for (single match) analysis')
parser.add_argument('-v','--valid_check',type=str,help='<y> to analyse validation question - used as boolean expression')
parser.add_argument('-m','--motm_analysis',type=str,help='<y> to analyse motm')
parser.add_argument('-p','--player_analysis',type=str,help='<y> to analyse player ratings')
parser.add_argument('-s','--single',type=str,help='<y> for single match analysis')
parser.add_argument('-s2','--season',type=str,help='<y> for season analysis')
args = parser.parse_args()

class Arsenal_Analysis:
	def __init__(self, filename, season, home, score, away):
		self.filename = filename
		self.season = season
		self.home = home
		self.score = score
		self.away = away

	def File_Input(self):
		df = pd.read_csv(self.filename)
		return df

	@classmethod
	def from_string(cls, filename):
		filename = str(filename)
		changed_filename = filename[:-4]
		parsed_filename = changed_filename.split('_')
		season, home, score, away = parsed_filename[2:]
		return cls(filename, season, home, score, away)

def Data_Reduction(dataframe):
	df = dataframe.dropna()
	df_og = df
	df_reduced = dataframe.drop(["Timestamp"], axis=1)
	return df_og,df

def Data_Reduction_2(dataframe,column):
	# Remove validation column
	list_of_column_names = dataframe.columns.values.tolist()
	df = dataframe.drop([list_of_column_names[column]], axis=1)
	
	# Split dataframes
	df.columns = df.columns.map(Delete_Emojis)
	df_players = df.drop(["Referee", "Man", "Who"], axis=1)
	# Late addition to remove empty strings
	df_players = df_players[df_players != ' ']
	df_players = df_players.dropna()
	# Ensures all data is of float type not object
	df_players = pd.DataFrame(data= df_players, dtype=float)
	return df_players

def Validation_Check(dataframe,column):
	# Print out unique values submitted by users
	validation_question = dataframe.columns[column]
	print("Results of unique values submitted:")
	test_frame = dataframe.groupby(validation_question)['Timestamp'].nunique()
	print(test_frame)
	print("Is this correct?")

def Delete_Emojis(player_name):
	if " " in player_name:
		first_name = player_name.split()[0]
		player_name = first_name
	if type(player_name) != str:
		new_player_name = player_name.str()	
	else:
		new_player_name = player_name
	return new_player_name

def Motm_Analysis(dataframe):
	df_motm = dataframe.groupby('Man of the Match')['Timestamp'].nunique()
	motm_candidates = list(df_motm.index)

	plt.pie(df_motm, labels=motm_candidates, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
	plt.title('Votes for Man of the Match: '+ file1_class.home + " " + file1_class.score + " " + file1_class.away)
	plt.show()

def Player_Rating_DF(dataframe):
	df_players = dataframe.transpose()
	df_players['average'] = df_players.mean(numeric_only=True, axis=1)
	df_players['std'] = df_players.std(numeric_only=True, axis=1)
	df_players = df_players.filter(["average","std"], axis=1)
	df_players.index = df_players.index.map(Delete_Emojis)
	return df_players

def Player_Rating_Plot(dataframe):
	X=dataframe.index
	y=dataframe.average

	plt.figure(figsize=(14,7))
	ax = sns.barplot(x=X, y=y,data=dataframe, palette="Paired")

	# Errors
	errs = dataframe.ix[:,'std']
	plt.errorbar(X, y, yerr=errs, fmt='.k', capsize=0)

	# Plot properties
	plt.ylim(0,11)
	plt.xlabel("Player")
	plt.ylabel("Average Rating")
	plt.title('Average Player Ratings: ' + file1_class.home + " " + file1_class.score + " " + file1_class.away)
	ax.set(yticks=[0,1,2,3,4,5,6,7,8,9,10])

	for index, row in dataframe.iterrows():
	    ax.text(row.name,row.average, round(row.average,1), color='black', ha="right", size="smaller")

	team_average = y.mean()
	ax.text(11.5,10.5, "Team rating:",color='black')
	ax.text(12,10.1, round(team_average,1),color='black')
	plt.show()

def Get_OG_Files(txt_file):
	subfile = open(txt_file,"r")
	arr = []
	for line in subfile:
		l = list(line)
		n = len(line)
		l[n-1:n] = []
		x = "".join(l)
		arr.append(x)
	return arr

def Get_Class_Files(array):
	game_class_array = []
	for i in range (0,len(array)):
		x = "file_"+str(i)
		game_class_array.append(x)
		game_class_array[i] = Arsenal_Analysis.from_string(array[i])
	return game_class_array

def Get_Dfs_From_Class_Files(array):
	array_of_dfs_for_games = []
	for i in range (0,len(array)):
		x = "df_for_game_"+str(i)
		array_of_dfs_for_games.append(x)
		array_of_dfs_for_games[i] = Arsenal_Analysis.File_Input(array[i])
	return array_of_dfs_for_games

def Array_Data_Reduction(array):
	array_of_dfs_for_games_og = []
	for i in range (0, len(array)):
		array_of_dfs_for_games_og.append(array[i].dropna())
	array_of_dfs_for_games_reduced = array_of_dfs_for_games_og.copy()
	for i in range (0, len(array_of_dfs_for_games_reduced)):
		array_of_dfs_for_games_reduced[i] = Data_Reduction_2(array_of_dfs_for_games_reduced[i],0)
		array_of_dfs_for_games_reduced[i] = Player_Rating_DF(array_of_dfs_for_games_reduced[i])
	return array_of_dfs_for_games_og, array_of_dfs_for_games_reduced

def Concat_Season_Ratings(array):
	combined_season_ratings_df = pd.concat(array, axis=1,sort=True)
	# combined_season_ratings_df = combined_season_ratings_df.fillna(0.0)
	return combined_season_ratings_df

def Create_List_Of_Games(array):
	list_of_games = []
	for i in range(0,len(array)):
		list_of_games.append(array[i].home + "-" + array[i].away)
	return list_of_games

def Players_Season_Performance(og_df, player_index):
	# Plotting
	dataframe = og_df
	print(dataframe.index)
	X = dataframe.ix[player_index,:]
	X_player = dataframe.index[player_index]
	# Create modified dataframe of ratings per game
	average = []
	std = []
	i = 0
	for index, row in X.iteritems():
		if i % 2 == 0:
			average.append(row)
		else:
			std.append(row)
		i = i + 1
	d = {'average': average, 'std': std}
	df = pd.DataFrame(data=d,dtype=float)

	# Linear Regression
	plt.figure(figsize=(14,7))
	ax = sns.regplot(x=df.index.values, y=df.average, data=df)	

	# Error Bars
	errs = df.ix[:,'std']
	plt.errorbar(x=df.index, y=df.average, yerr=errs, fmt='.k', capsize=0)

	# Plot properties
	ax.set(ylim=[1,11])
	ax.yaxis.set(ticks=range(0,11))
	ax.xaxis.set(ticks=range(0,len(array_of_games)),ticklabels=list_of_games)	
	plt.xlabel("Match")
	plt.ylabel("Average Rating")
	plt.title('Average Rating Per Match: ' + X_player)
	plt.show()
	input()

if bool(args.single) is True:
	# Creates classes from files
	file1 = args.file
	file1_class = Arsenal_Analysis.from_string(file1)

	# Change to dataframes (Doesnt matter if you overwrite OG filename (above))
	df = Arsenal_Analysis.File_Input(file1_class)

	df_reduced,df_og = Data_Reduction(df) 							# Need two data frames for player and motm analyses

	# Validation question check
	if bool(args.valid_check) is True:
		Validation_Check(df_reduced,1)

	# Further Data Reduction and formation
	df_players = Data_Reduction_2(df_reduced,0)

	# Motm Analysis
	if bool(args.motm_analysis) is True:
		Motm_Analysis(df_og)

	# Player analysis
	df_players = Player_Rating_DF(df_players)
	if bool(args.player_analysis) is True:
		Player_Rating_Plot(df_players)

if bool(args.season) is True:
	# Turn files from a txt file into an array of class instances
	f1 = '/Users/ElJackador/programming/data_analysis/arsenal_analysis/18-19_season_games.txt'
	array_of_games = Get_OG_Files(f1)
	game_class_array = Get_Class_Files(array_of_games)

	# Create list of games from previous array
	list_of_games = Create_List_Of_Games(game_class_array)

	# Turns files into an array of dfs for the files
	array_of_dfs_for_games = Get_Dfs_From_Class_Files(game_class_array)
	array_of_dfs_for_games_og, array_of_dfs_for_games_reduced = Array_Data_Reduction(array_of_dfs_for_games)
	# Final combining of season averages
	combined_season_ratings_df = Concat_Season_Ratings(array_of_dfs_for_games_reduced)
	# Plotting (every ith player)
	for i in range(0,len(combined_season_ratings_df)):
		Players_Season_Performance(combined_season_ratings_df,i)



