import csv
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

def getdays(date1):
	year1 = int(date1[0] + date1[1] + date1[2] + date1[3])
	month1 = int(date1[4] + date1[5])
	date1 = int(date1[6] + date1[7])

	answer = 365*year1 + 30*month1 + date1
	return answer

def getmonth(date1):
	month1 = int(date1[4] + date1[5])
	return month1

# Reorders all csv files to fixed column ordering and loads to a ndarray
def create_add_year_matches(input_path, output_path):

	with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
	    # Output dict needs a list for new column ordering
	    fieldnames = ['tourney_id', #0
	                  'tourney_name', #1
	                  'surface', #2
	                  'draw_size', #3
	                  'tourney_level', #4
	                  'tourney_date', #5
	                  'match_num', #6
	                  'winner_id', #7
	                  'winner_seed', #8
	                  'winner_entry', #9
	                  'winner_name', #10
	                  'winner_hand', #11
	                  'winner_ht', #12
	                  'winner_ioc', #13
	                  'winner_age', #14
	                  'winner_rank', #15
	                  'winner_rank_points', #16
	                  'loser_id', #17
	                  'loser_seed', #18
	                  'loser_entry', #19
	                  'loser_name', #20
	                  'loser_hand', #21
	                  'loser_ht', #22
	                  'loser_ioc', #23
	                  'loser_age', #24
	                  'loser_rank', #25
	                  'loser_rank_points', #26
	                  'score', #27
	                  'best_of', #28
	                  'round', #29
	                  'minutes', #30
	                  'w_ace', #31
	                  'w_df', #32
	                  'w_svpt', #33
	                  'w_1stIn', #34
	                  'w_1stWon', #35
	                  'w_2ndWon', #36
	                  'w_SvGms', #37
	                  'w_bpSaved', #38
	                  'w_bpFaced', #39
	                  'l_ace', #40
	                  'l_df', #41
	                  'l_svpt', #42
	                  'l_1stIn', #43
	                  'l_1stWon', #44
	                  'l_2ndWon', #45
	                  'l_SvGms', #46
	                  'l_bpSaved', #47
	                  'l_bpFaced'] #48

	    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
	    # reorder the header first
	    writer.writeheader()
	    for row in csv.DictReader(infile):
	        # writes the reordered rows to the new file
	        writer.writerow(row)

	inputs = np.loadtxt(output_path, dtype=np.dtype(str), delimiter=',', skiprows=1)
	return inputs

with open('atp_matches_1997.csv', 'r') as infile, open('reordered_atp_matches_1997.csv', 'w') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['tourney_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date', 'match_num', 'winner_id', 'winner_seed', 'winner_entry', 'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points' ,'loser_id', 'loser_seed'	,'loser_entry', 'loser_name', 'loser_hand', 'loser_ht' , 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points', 'score', 'best_of' ,'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

inputs = np.loadtxt("reordered_atp_matches_1997.csv", dtype=np.dtype(str), delimiter=',', skiprows=1)

for i in range(1998, 2019):
	input_path = 'atp_matches_' + str(i) + '.csv'
	output_path = 'reordered_atp_matches' + str(i) + '.csv'

	inputs_temp = create_add_year_matches(input_path, output_path)
	inputs = np.concatenate((inputs, inputs_temp))

for i in range(2010, 2018):
	input_path = 'atp_matches_qual_chall_' + str(i) + '.csv'
	output_path = 'reordered_atp_matches_qual_chall_matches' + str(i) + '.csv'

	inputs_temp = create_add_year_matches(input_path, output_path)
	inputs = np.concatenate((inputs, inputs_temp))

for i in range(2019, 2020):
	input_path = 'atp_matches_' + str(i) + '.csv'
	output_path = 'reordered_atp_matches' + str(i) + '.csv'

	inputs_temp = create_add_year_matches(input_path, output_path)
	inputs = np.concatenate((inputs, inputs_temp))

print(inputs.shape)

print(inputs[1])

num_rows, num_cols = inputs.shape
print(num_rows, num_cols)

print(inputs[0])

# Sanity checking tourney_id

ct = 0

for i in range(num_rows):
	if(inputs[i][0] == ""):
		ct = ct + 1

print(ct)

#Sanity checking tourney_name

ct = 0

for i in range(num_rows):
	if(inputs[i][1] == ""):
		ct = ct + 1

print(ct)

# Sanity checking surface and creating dict of surfaces

ct = 0
tc = 0
none_surfaces_rows = list()

for i in range(num_rows):
	if(inputs[i][2] == ""):
		ct = ct + 1
		none_surfaces_rows.append(i)

	if(inputs[i][2] == "None"):
		tc = tc + 1
		none_surfaces_rows.append(i)

inputs = np.delete(inputs, none_surfaces_rows, 0)

print(ct)
print(tc)

ct = 0
surfaces = dict()
size = 0

num_rows, num_cols = inputs.shape

for i in range(num_rows):
	if(inputs[i][2] == ""):
		ct = ct + 1
	else:
		if inputs[i][2] not in surfaces:
			surfaces[inputs[i][2]] = size
			size = size + 1		

print(ct)
print(surfaces)

# Sanity checking draw_size

ct = 0
tc = 0
draw_sizes = dict()
size = 0

for i in range(num_rows):
	if(inputs[i][3] == ""):
		ct = ct + 1

	else:
		if inputs[i][3] not in draw_sizes:
			draw_sizes[inputs[i][3]] = size
			size = size + 1		

print(draw_sizes)

print(ct)

# Drop tourey_name column
#inputs = np.delete(inputs, 1, axis=1)

# Drop draw_size column
#inputs = np.delete(inputs, 3, axis=1)

# Drop tourey_level column
#inputs = np.delete(inputs, 4, axis=1)

# Drop match_num column
#inputs = np.delete(inputs, 6, axis=1)

# Drop winner_name column
#inputs = np.delete(inputs, 10, axis=1)

# Drop loser_name column
#inputs = np.delete(inputs, 20, axis=1)

# Drop winner_ioc column - country of winner
#inputs = np.delete(inputs, 13, axis=1)

# Drop loser_ioc column - country of loser
#inputs = np.delete(inputs, 23, axis=1)

# Drop score
#inputs = np.delete(inputs, 27, axis=1)

# Sanity checking and sanitizing month from time of match

ct = 0

for i in range(num_rows):
	if(inputs[i][5] == ""):
		ct = ct + 1

print(ct)

# Sanity checking winner_id

ct = 0
federer_win = 0

for i in range(num_rows):
	if(inputs[i][7] == ""):
		ct = ct + 1

	if(inputs[i][17] == ""):
		ct = ct + 1

	if(inputs[i][7] == "103819"):
		federer_win = federer_win + 1

print(ct) # It comes out to be 0\
print(federer_win)

# Sanitizing winner_seed

ct = 0
federer_win = 0

for i in range(num_rows):
	if(inputs[i][8] == ""):
		ct = ct + 1
		inputs[i][8] = '40'

	if(inputs[i][18] == ""):
		ct = ct + 1
		inputs[i][18] = '40'

	if(not inputs[i][8].isdigit()):
		ct = ct + 1
		inputs[i][8] = '40'

	if(not inputs[i][18].isdigit()):
		ct = ct + 1
		inputs[i][18] = '40'

print(ct)

# Sanitizing winner_entry

ct = 0
federer_win = 0
entries = dict()
entry_type = 0

for i in range(num_rows):
	if inputs[i][9].lower() not in entries:
		entries[inputs[i][9].lower()] = entry_type
		entry_type = entry_type + 1

	if inputs[i][19].lower() not in entries:
		entries[inputs[i][19].lower()] = entry_type
		entry_type = entry_type + 1

	inputs[i][9] = entries[inputs[i][9].lower()]
	inputs[i][19] = entries[inputs[i][19].lower()]

print(entries)

# Sanitizing winner_hand - can only be left or right handed

for i in range(num_rows):
	if inputs[i][11].lower() == 'l':
		inputs[i][11] = '0'
	else:
		inputs[i][11] = '1'

	if inputs[i][21].lower() == 'l':
		inputs[i][21] = '0'
	else:
		inputs[i][21] = '1'

# Sanitizing winner_ht
# Making all winners without a height as height = -1

ct = 0

for i in range(num_rows):
	if inputs[i][12].lower() == "":
		ct = ct + 1
		inputs[i][12] = '-1'

	if inputs[i][22].lower() == "":
		ct = ct + 1
		inputs[i][22] = '-1'

# Too many players without a height - so just going to take difference in height as feature
# and make it 0 when input doesn't have it
print(ct) 

# Sanitizing winner_age

ct = 0
total = 0.0
total_matches = 0

for i in range(num_rows):
	if inputs[i][14].lower() == "":
		ct = ct + 1
		inputs[i][14] = "26.08"
	else:
		total = total + float(inputs[i][14])
		total_matches = total_matches + 1

	if inputs[i][24].lower() == "":
		ct = ct + 1
		inputs[i][24] = "26.08"
	else:
		total = total + float(inputs[i][24])
		total_matches = total_matches + 1

# Seems like 26 is the average age of the winner
print(total/total_matches)

# Seems like 18 winners overall don't have an age - default to 26
print(ct)

# Sanitizing winner_rank and loser_rank - if no rank then replacing with 2000 which refers to a very high rank which
# represents the last rank

ct = 0

for i in range(num_rows):
	if(inputs[i][15] == ""):
			inputs[i][15] = 2000
			rank_1 = 2000
	else:
			rank_1 = int(inputs[i][15])

	if(inputs[i][25] == ""):
			inputs[i][25] = 2000
			rank_2 = 2000
	else:
			rank_2 = int(inputs[i][25])

	if(rank_1 < rank_2):
		ct = ct + 1

print(ct*100/num_rows)

benchmark_higher_rankings = ct*100/num_rows

# Sanitizing winner_rank points - if rankings points is empty replacing with 0

ct = 0

for i in range(num_rows):
	if(inputs[i][16] == ""):
		ct = ct + 1
		inputs[i][16] = 0

	if(inputs[i][26] == ""):
		ct = ct + 1
		inputs[i][26] = 0

print(ct)

# Sanity checking score

ct1 = 0
ct2 = 0
walkover_matches = list()

for i in range(num_rows):
	if(inputs[i][27] == ""):
		ct1 = ct1 + 1
		walkover_matches.append(i)
	if(inputs[i][27].lower() == "w/o"):
		ct2 = ct2 + 1
		walkover_matches.append(i)


print(ct1)
print(ct2)

inputs = np.delete(inputs, walkover_matches, 0)

num_rows, num_cols = inputs.shape

# Sanity checking best_of

ct = 0

for i in range(num_rows):
	if(inputs[i][28] == ""):
		ct = ct + 1

print(ct)

# Sanity checking and converting rounds to numbers

ct = 0
rounds = {'Q1' : -3, 'Q2' : -2, 'Q3': -3, 'R128': 0, 'RR': 0, 'BR': 0, 'R64': 1, 'R32': 2, 'R16': 3, 'QF': 4, 'SF': 5, 'F': 6}
type_rounds = 0

for i in range(num_rows):
	if(inputs[i][29] == ""):
		ct = ct + 1
	else:
		inputs[i][29] = rounds[inputs[i][29].upper()]

print(num_rows)
print(rounds)
print(ct)

# Sanity checking minutes

ct = 0
no_minutes = list()

for i in range(num_rows):
	if(inputs[i][30] == ""):
		ct = ct + 1
		no_minutes.append(i)

# Lots of rows without minutes
print(ct)

inputs = np.delete(inputs, no_minutes, 0)

num_rows, num_cols = inputs.shape

# Sanity checking all numerical features of the match - double faults, aces, first serve, etc.
#and deleting all rows that have any missing

ct = 0
missing_values = list()

for i in range(num_rows):
	for j in range(31, 49):
		if(inputs[i][j] == ""):
			ct = ct + 1
			missing_values.append(i)

print(ct)

inputs = np.delete(inputs, missing_values, 0)

num_rows, num_cols = inputs.shape

print(num_rows) #63770 rows in total

career_stats_winner = np.zeros((num_rows, 49))
career_stats_loser = np.zeros((num_rows, 49))
career_stats_winner_total = np.zeros((num_rows, 49))
career_stats_loser_total = np.zeros((num_rows, 49))

x = 0

player_id_stats_overall_sum = [dict() for x in range(num_cols)]
player_id_stats_overall_count = [dict() for x in range(num_cols)]
player_name = dict()

delete_list = []

count_2019 = 0

for i in range(num_rows):
	if inputs[i][5][0] == '2' and inputs[i][5][1] == '0' and inputs[i][5][2] == '1' and inputs[i][5][3] == '9' and getmonth(inputs[i][5]) > 6:
		count_2019+=1

# Delete davis cup matches in prediction - they are generally extremely hard to predict
# If Davis Cup matches needs to be predicted the most likely best way to do is to have a different model for davis cup
for i in range(num_rows - count_2019, num_rows):
	if "davis" in inputs[i][1].lower():
		delete_list.append(i)

inputs = np.delete(inputs, delete_list, 0)

num_rows, num_cols = inputs.shape

count_2019 = 0

for i in range(num_rows):
	if inputs[i][5][0] == '2' and inputs[i][5][1] == '0' and inputs[i][5][2] == '1' and inputs[i][5][3] == '9' and getmonth(inputs[i][5]) > 6:
		count_2019+=1

X_inputs = np.zeros((2*(num_rows - count_2019), 51))
Y_inputs = np.zeros(2*(num_rows - count_2019))

X_prediction = np.zeros((2*count_2019, 51))
Y_prediction = np.zeros(2*count_2019)

print(count_2019)

matches_won_lost = dict()

head_to_head = dict()
head_to_head_surface = dict()
matches_won_lost_surface = dict()

rank_count = dict()
rank_total = dict()
rankings_points_total = dict()

form = dict()
form_surface = dict()

tournament_form_win = dict()
tournament_form_count = dict()

common_head_to_head = dict()
total_no_head_to_head = 0

for i in range(num_rows):
	player_id_winner = inputs[i][7]
	player_id_loser = inputs[i][17]


	# Start of Tournament level form

	if (player_id_winner, inputs[i][0][5:]) not in tournament_form_win:
		tournament_form_win[(player_id_winner, inputs[i][0][5:])] = 0
		tournament_form_count[(player_id_winner, inputs[i][0][5:])] = 0

	if (player_id_loser, inputs[i][0][5:]) not in tournament_form_win:
		tournament_form_win[(player_id_loser, inputs[i][0][5:])] = 0
		tournament_form_count[(player_id_loser, inputs[i][0][5:])]  = 0

	tournament_form_win[(player_id_winner, inputs[i][0][5:])] += 1
	tournament_form_win[(player_id_loser, inputs[i][0][5:])] += 0

	tournament_form_count[(player_id_winner, inputs[i][0][5:])] += 1
	tournament_form_count[(player_id_loser, inputs[i][0][5:])] += 1

	if i < num_rows - count_2019:
		X_inputs[2*i][44] = tournament_form_win[(player_id_winner, inputs[i][0][5:])] - 1 - tournament_form_win[(player_id_loser, inputs[i][0][5:])]
		X_inputs[2*i][45] = tournament_form_count[(player_id_winner, inputs[i][0][5:])] - tournament_form_count[(player_id_loser, inputs[i][0][5:])]
		
		temp11 = 1
		temp12 = 1

		if tournament_form_count[(player_id_winner, inputs[i][0][5:])] != 1:
			temp11 = tournament_form_count[(player_id_winner, inputs[i][0][5:])]
		if tournament_form_count[(player_id_loser, inputs[i][0][5:])]  != 1:
			temp12 = tournament_form_count[(player_id_loser, inputs[i][0][5:])] 

		X_inputs[2*i][46] = ((tournament_form_win[(player_id_winner, inputs[i][0][5:])] - 1)*100/temp11) - ((tournament_form_win[(player_id_loser, inputs[i][0][5:])])*100/temp12)

		X_inputs[2*i+1][44] =  -X_inputs[2*i][44]
		X_inputs[2*i+1][45] = -X_inputs[2*i][45]
		X_inputs[2*i+1][46] = -X_inputs[2*i][46]
	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))

		X_prediction[x1][44] = tournament_form_win[(player_id_winner, inputs[i][0][5:])] - 1 - tournament_form_win[(player_id_loser, inputs[i][0][5:])]
		X_prediction[x1][45] = tournament_form_count[(player_id_winner, inputs[i][0][5:])] - tournament_form_count[(player_id_loser, inputs[i][0][5:])]
		
		temp11 = 1
		temp12 = 1

		if tournament_form_count[(player_id_winner, inputs[i][0][5:])] != 1:
			temp11 = tournament_form_count[(player_id_winner, inputs[i][0][5:])]
		if tournament_form_count[(player_id_loser, inputs[i][0][5:])]  != 1:
			temp12 = tournament_form_count[(player_id_loser, inputs[i][0][5:])] 

		X_prediction[x1][46] = ((tournament_form_win[(player_id_winner, inputs[i][0][5:])] - 1)*100/temp11) - ((tournament_form_win[(player_id_loser, inputs[i][0][5:])])*100/temp12)

		X_prediction[x1+1][44] =  -X_prediction[x1][44]
		X_prediction[x1+1][45] = -X_prediction[x1][45]
		X_prediction[x1+1][46] = -X_prediction[x1][46]


	# End of Tournament level form

	# Start of overall form

	if player_id_winner not in form:
		form[player_id_winner] = []

	form[player_id_winner].append((1, inputs[i][5]))

	if player_id_loser not in form:
		form[player_id_loser] = []

	form[player_id_loser].append((0, inputs[i][5]))

	total_winner_5 = -1
	total_winner_10 = -1
	total_winner_15 = -1
	total_winner_25 = -1

	total_loser_5 = -1
	total_loser_10 = -1
	total_loser_15 = -1
	total_loser_25 = -1

	winner_win_5 = 0
	winner_win_10 = 0
	winner_win_15 = 0
	winner_win_25 = 0

	loser_win_5 = 0
	loser_win_10 = 0
	loser_win_15 = 0
	loser_win_25 = 0

	for (a1, a2) in reversed(form[player_id_winner]):
		if total_winner_5 == -1:
			total_winner_5 = 0
		else:
			if total_winner_5 < 5:
				winner_win_5 = winner_win_5 + a1
				total_winner_5 += 1

	for (a1, a2) in reversed(form[player_id_winner]):
		if total_winner_10 == -1:
			total_winner_10 = 0
		else:
			if total_winner_10 < 10:
				winner_win_10 = winner_win_10 + a1
				total_winner_10 += 1

	for (a1, a2) in reversed(form[player_id_winner]):
		if total_winner_15 == -1:
			total_winner_15 = 0
		else:
			if total_winner_15 < 15:
				winner_win_15 = winner_win_15 + a1
				total_winner_15 += 1

	for (a1, a2) in reversed(form[player_id_winner]):
		if total_winner_25 == -1:
			total_winner_25 = 0
		else:
			if total_winner_25 < 25:
				winner_win_25 = winner_win_25 + a1
				total_winner_25 += 1


	for (a1, a2) in reversed(form[player_id_loser]):
		if total_loser_5 == -1:
			total_loser_5 = 0
		else:
			if total_loser_5 < 5:
				loser_win_5 = loser_win_5 + a1
				total_loser_5 += 1

	for (a1, a2) in reversed(form[player_id_loser]):
		if total_loser_10 == -1:
			total_loser_10 = 0
		else:
			if total_loser_10 < 10:
				loser_win_10 = loser_win_10 + a1
				total_loser_10 += 1

	for (a1, a2) in reversed(form[player_id_loser]):
		if total_loser_15 == -1:
			total_loser_15 = 0
		else:
			if total_loser_15 < 15:
				loser_win_15 = loser_win_15 + a1
				total_loser_15 += 1

	for (a1, a2) in reversed(form[player_id_loser]):
		if total_loser_25 == -1:
			total_loser_25 = 0
		else:
			if total_loser_25 < 25:
				loser_win_25 = loser_win_25 + a1
				total_loser_25 += 1


	if i < num_rows - count_2019:
		X_inputs[2*i][36] = winner_win_5 - loser_win_5
		X_inputs[2*i][37] = winner_win_10 - loser_win_10
		X_inputs[2*i][38] = winner_win_15 - loser_win_15
		X_inputs[2*i][39] = winner_win_25 - loser_win_25

		X_inputs[2*i+1][36] = loser_win_5 - winner_win_5
		X_inputs[2*i+1][37] = loser_win_10 - winner_win_10
		X_inputs[2*i+1][38] = loser_win_15 - winner_win_15
		X_inputs[2*i+1][39] = loser_win_25 - winner_win_25

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))

		X_prediction[x1][36] = winner_win_5 - loser_win_5
		X_prediction[x1][37] = winner_win_10 - loser_win_10
		X_prediction[x1][38] = winner_win_15 - loser_win_15
		X_prediction[x1][39] = winner_win_25 - loser_win_25

		X_prediction[x1+1][36] = loser_win_5 - winner_win_5
		X_prediction[x1+1][37] = loser_win_10 - winner_win_10
		X_prediction[x1+1][38] = loser_win_15 - winner_win_15
		X_prediction[x1+1][39] = loser_win_25 - winner_win_25

	# End of overall form

	# Start of last 1 month form overall

	total_winner_1 = -1
	total_loser_1 = -1
	winner_win_1 = 0
	loser_win_1 = 0

	for (a1, a2) in reversed(form[player_id_winner]):
		if total_winner_1 == -1:
			total_winner_1 = 0
		else:
			if getdays(inputs[i][5]) - getdays(a2) < 30 and getdays(inputs[i][5]) - getdays(a2) >= 0:
				winner_win_1 = winner_win_1 + a1
				total_winner_1 += 1
				#print(getdays(inputs[i][5]) - getdays(a2), a2, inputs[i][5], i, 1, total_winner_1)
			else:
				break

	for (a1, a2) in reversed(form[player_id_loser]):
		if total_loser_1 == -1:
			total_loser_1 = 0
		else:
			if getdays(inputs[i][5]) - getdays(a2) < 30 and getdays(inputs[i][5]) - getdays(a2) >= 0:
				loser_win_1 = loser_win_1 + a1
				total_loser_1 += 1
				#print(getdays(inputs[i][5]) - getdays(a2), a2, inputs[i][5], i, 5, total_loser_1)
			else:
				break


	if i < num_rows - count_2019:
		X_inputs[2*i][47] = winner_win_1 - loser_win_1
		X_inputs[2*i+1][47] = loser_win_1 - winner_win_1
		X_inputs[2*i][48] = total_winner_1 - total_loser_1
		X_inputs[2*i+1][48] = total_loser_1 - total_winner_1

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))

		X_prediction[x1][47] = winner_win_1 - loser_win_1
		X_prediction[x1+1][47] = loser_win_1 - winner_win_1
		X_prediction[x1][48] = total_winner_1 - total_loser_1
		X_prediction[x1+1][48] = total_loser_1 - total_winner_1

	# End of last 1 month form overall
	# I tried adding 3, 6 and 12 month forms as well - it didn't seem to help - in fact made the prediction worse

	# Start of surface level form
	
	if player_id_winner not in form_surface:
		form_surface[(player_id_winner, inputs[i][2])] = []

	form_surface[(player_id_winner, inputs[i][2])].append((1, inputs[i][5]))

	if player_id_loser not in form_surface:
		form_surface[(player_id_loser, inputs[i][2])] = []

	form_surface[(player_id_loser, inputs[i][2])].append((0, inputs[i][5]))

	total_winner_5 = -1
	total_winner_10 = -1
	total_winner_15 = -1
	total_winner_25 = -1

	total_loser_5 = -1
	total_loser_10 = -1
	total_loser_15 = -1
	total_loser_25 = -1

	winner_win_5 = 0
	winner_win_10 = 0
	winner_win_15 = 0
	winner_win_25 = 0

	loser_win_5 = 0
	loser_win_10 = 0
	loser_win_15 = 0
	loser_win_25 = 0

	for (a1, a2) in reversed(form_surface[(player_id_winner, inputs[i][2])]):
		if total_winner_5 == -1:
			total_winner_5 = 0
		else:
			if total_winner_5 < 5:
				winner_win_5 = winner_win_5 + a1
				total_winner_5 += 1

	for (a1, a2) in reversed(form_surface[(player_id_winner, inputs[i][2])]):
		if total_winner_10 == -1:
			total_winner_10 = 0
		else:
			if total_winner_10 < 10:
				winner_win_10 = winner_win_10 + a1
				total_winner_10 += 1

	for (a1, a2) in reversed(form_surface[(player_id_winner, inputs[i][2])]):
		if total_winner_15 == -1:
			total_winner_15 = 0
		else:
			if total_winner_15 < 15:
				winner_win_15 = winner_win_15 + a1
				total_winner_15 += 1

	for (a1, a2) in reversed(form_surface[(player_id_winner, inputs[i][2])]):
		if total_winner_25 == -1:
			total_winner_25 = 0
		else:
			if total_winner_25 < 25:
				winner_win_25 = winner_win_25 + a1
				total_winner_25 += 1


	for (a1, a2) in reversed(form_surface[(player_id_loser, inputs[i][2])]):
		if total_loser_5 == -1:
			total_loser_5 = 0
		else:
			if total_loser_5 < 5:
				loser_win_5 = loser_win_5 + a1
				total_loser_5 += 1

	for (a1, a2) in reversed(form_surface[(player_id_loser, inputs[i][2])]):
		if total_loser_10 == -1:
			total_loser_10 = 0
		else:
			if total_loser_10 < 10:
				loser_win_10 = loser_win_10 + a1
				total_loser_10 += 1

	for (a1, a2) in reversed(form_surface[(player_id_loser, inputs[i][2])]):
		if total_loser_15 == -1:
			total_loser_15 = 0
		else:
			if total_loser_15 < 15:
				loser_win_15 = loser_win_15 + a1
				total_loser_15 += 1

	for (a1, a2) in reversed(form_surface[(player_id_loser, inputs[i][2])]):
		if total_loser_25 == -1:
			total_loser_25 = 0
		else:
			if total_loser_25 < 25:
				loser_win_25 = loser_win_25 + a1
				total_loser_25 += 1


	if i < num_rows - count_2019:
		X_inputs[2*i][40] = winner_win_5 - loser_win_5
		X_inputs[2*i][41] = winner_win_10 - loser_win_10
		X_inputs[2*i][42] = winner_win_15 - loser_win_15
		X_inputs[2*i][43] = winner_win_25 - loser_win_25

		X_inputs[2*i+1][40] = loser_win_5 - winner_win_5
		X_inputs[2*i+1][41] = loser_win_10 - winner_win_10
		X_inputs[2*i+1][42] = loser_win_15 - winner_win_15
		X_inputs[2*i+1][43] = loser_win_25 - winner_win_25

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))

		X_prediction[x1][40] = winner_win_5 - loser_win_5
		X_prediction[x1][41] = winner_win_10 - loser_win_10
		X_prediction[x1][42] = winner_win_15 - loser_win_15
		X_prediction[x1][43] = winner_win_25 - loser_win_25

		X_prediction[x1+1][40] = loser_win_5 - winner_win_5
		X_prediction[x1+1][41] = loser_win_10 - winner_win_10
		X_prediction[x1+1][42] = loser_win_15 - winner_win_15
		X_prediction[x1+1][43] = loser_win_25 - winner_win_25

	# End of surface level form

	# Start of Overall win loss

	p1, p2 = (0, 0)
	b1, b2 = (0, 0)
	
	if player_id_winner not in matches_won_lost:
		matches_won_lost[player_id_winner] = (1, 0)
		(p1, p2) = (0, 0)
	else:
		(a1, a2) = matches_won_lost[player_id_winner]
		matches_won_lost[player_id_winner] = (a1 + 1, a2)
		(p1, p2) = (a1, a2)

	if player_id_loser not in matches_won_lost:
		matches_won_lost[player_id_loser] = (0, 1)
		(b1, b2) = (0, 0)
	else:
		(a1, a2) = matches_won_lost[player_id_loser]
		matches_won_lost[player_id_loser] = (a1, a2 + 1)
		(b1, b2) = (a1, a2)

	if((p1 + p2) != 0):
		temp1 = (p1*100/(p1+p2))
	else:
		temp1 = 0

	if((b1 + b2) != 0):
		temp2 = (b1*100/(b1+b2))
	else:
		temp2 = 0

	if i < num_rows - count_2019:
		X_inputs[2*i][25] = p1 - b1
		X_inputs[2*i+1][25] = b1 - p1	

		X_inputs[2*i][26] =  temp1 - temp2 
		X_inputs[2*i+1][26] = temp2 - temp1

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
		X_prediction[x1][25] = p1 - b1
		X_prediction[x1+1][25] = b1 - p1

		X_prediction[x1][26] = temp1 - temp2
		X_prediction[x1+1][26] = temp2 - temp1

# End of Overall win loss

# Start of section for win loss based on surface

	p1, p2 = (0, 0)
	b1, b2 = (0, 0)
	
	if (player_id_winner, inputs[i][2]) not in matches_won_lost_surface:
		matches_won_lost_surface[(player_id_winner, inputs[i][2])] = (1, 0)
		(p1, p2) = (0, 0)
	else:
		(a1, a2) = matches_won_lost_surface[(player_id_winner, inputs[i][2])]
		matches_won_lost_surface[(player_id_winner, inputs[i][2])] = (a1 + 1, a2)
		(p1, p2) = (a1, a2)

	if (player_id_loser, inputs[i][2]) not in matches_won_lost_surface:
		matches_won_lost_surface[(player_id_loser, inputs[i][2])] = (0, 1)
		(b1, b2) = (0, 0)
	else:
		(a1, a2) = matches_won_lost_surface[(player_id_loser, inputs[i][2])]
		matches_won_lost_surface[(player_id_loser, inputs[i][2])] = (a1, a2 + 1)
		(b1, b2) = (a1, a2)

	if((p1 + p2) != 0):
		temp1 = (p1*100/(p1+p2))
	else:
		temp1 = 0

	if((b1 + b2) != 0):
		temp2 = (b1*100/(b1+b2))
	else:
		temp2 = 0

	if i < num_rows - count_2019:
		X_inputs[2*i][33] = p1 - b1
		X_inputs[2*i+1][33] = b1 - p1	

		X_inputs[2*i][34] =  temp1 - temp2 
		X_inputs[2*i+1][34] = temp2 - temp1

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
		X_prediction[x1][33] = p1 - b1
		X_prediction[x1+1][33] = b1 - p1

		X_prediction[x1][34] = temp1 - temp2
		X_prediction[x1+1][34] = temp2 - temp1

# End of section for win loss based on surface

# Start of Overall Head to Head

	if (player_id_winner, player_id_loser) not in head_to_head:	
		head_to_head[(player_id_winner, player_id_loser)] = (1, 0)
		head_to_head[(player_id_loser, player_id_winner)] = (0, 1)
		if i < num_rows - count_2019:
			X_inputs[2*i][15] = 1
			X_inputs[2*i+1][15] = -1
		else:
			x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
			total_no_head_to_head = total_no_head_to_head + 1
			print(inputs[i][10], inputs[i][20])
			X_prediction[x1][15] = 1
			X_prediction[x1+1][15] = -1

	else:
		(a1, a2) = head_to_head[(player_id_winner, player_id_loser)]

		if i < num_rows - count_2019:
			X_inputs[2*i][15] = a1 - a2
			X_inputs[2*i+1][15] = a2 - a1			
		else:
			x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
			X_prediction[x1][15] = a1 - a2
			X_prediction[x1+1][15] = a2 - a1

		head_to_head[(player_id_winner, player_id_loser)] = (a1 + 1, a2)
		head_to_head[(player_id_loser, player_id_winner)] = (a2, a1 + 1)

# End of Overall Head to Head

# Start of Common Opponent Head to Head

	if player_id_winner not in common_head_to_head:	
		common_head_to_head[player_id_winner] =  {player_id_loser: (0, 0)}

	if player_id_loser not in common_head_to_head:	
		common_head_to_head[player_id_loser] = {player_id_winner: (0, 0)}

	if player_id_loser not in common_head_to_head[player_id_winner]:
		common_head_to_head[player_id_winner][player_id_loser] = (0, 0)
	
	if player_id_winner not in common_head_to_head[player_id_loser]:
		common_head_to_head[player_id_loser][player_id_winner] = (0, 0)
	
	(x11, y11) = common_head_to_head[player_id_winner][player_id_loser]
	(x22, y22) = common_head_to_head[player_id_loser][player_id_winner]
	common_head_to_head[player_id_winner][player_id_loser] = (x11+1, y11)
	common_head_to_head[player_id_loser][player_id_winner] = (x22, y22+1)

	new_head_to_head_winner = (0, 0)
	new_head_to_head_loser = (0, 0)
		
	for player_id in common_head_to_head[player_id_winner]:
		if player_id in common_head_to_head[player_id_loser]:
			(temp1, temp2) = common_head_to_head[player_id_winner][player_id]
			t1, t2 = new_head_to_head_winner 
			new_head_to_head_winner = t1 + temp1, t2 + temp2

	for player_id in common_head_to_head[player_id_loser]:
		if player_id in common_head_to_head[player_id_winner]:
			(temp1, temp2) = common_head_to_head[player_id_loser][player_id]
			t1, t2 = new_head_to_head_loser 
			new_head_to_head_loser = t1 + temp1, t2 + temp2

	temp1, temp2 = new_head_to_head_winner
	temp3, temp4 = new_head_to_head_loser

	temp5 = 0
	temp6 = 0

	if(temp1 + temp2) != 0:
		temp5 = ((temp1*100)/(temp1+temp2))

	if(temp3 + temp4) != 0:
		temp6 = ((temp3*100)/(temp3+temp4))

	if i < num_rows - count_2019:
		X_inputs[2*i][49] = temp1 - temp3
		X_inputs[2*i][49] =  temp5 - temp6
		X_inputs[2*i+1][50] = temp3 - temp1
		X_inputs[2*i+1][50] = temp6 - temp5

	else:
		x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
		X_prediction[x1][49] = temp1 - temp3
		X_prediction[x1][49] = temp5 - temp6
		X_prediction[x1+1][50] = temp3 - temp1
		X_prediction[x1+1][50] = temp6 - temp5

# End of Common Opponent Head to Head

# Start of surface level head to head

	if (player_id_winner, player_id_loser, inputs[i][2]) not in head_to_head_surface:
		if i < num_rows - count_2019:
			X_inputs[2*i][35] = 0
			X_inputs[2*i+1][35] = 0			
		else:
			x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
			X_prediction[x1][35] = 0
			X_prediction[x1+1][35] = 0
		
		head_to_head_surface[(player_id_winner, player_id_loser, inputs[i][2])] = (1, 0)
		head_to_head_surface[(player_id_loser, player_id_winner, inputs[i][2])] = (0, 1)
	else:
		(a1, a2) = head_to_head_surface[(player_id_winner, player_id_loser, inputs[i][2])]

		if i < num_rows - count_2019:
			X_inputs[2*i][35] = a1 - a2
			X_inputs[2*i+1][35] = a2 - a1			
		else:
			x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
			X_prediction[x1][35] = a1 - a2
			X_prediction[x1+1][35] = a2 - a1

		head_to_head_surface[(player_id_winner, player_id_loser, inputs[i][2])] = (a1 + 1, a2)
		head_to_head_surface[(player_id_loser, player_id_winner, inputs[i][2])] = (a2, a1 + 1)

# End of surface level head to head

	for j in range(31, 40):
		if player_id_winner not in player_id_stats_overall_count[j-31]:

			career_stats_winner[i][j] = 0
			career_stats_winner_total[i][j] = 0

			player_id_stats_overall_count[j-31][player_id_winner] = 1
			player_id_stats_overall_sum[j-31][player_id_winner] = int(inputs[i][j])
			player_name[player_id_winner] = inputs[i][10]
		else:
			career_stats_winner[i][j] = player_id_stats_overall_sum[j-31][player_id_winner]/player_id_stats_overall_count[j-31][player_id_winner]
			career_stats_winner_total[i][j] = player_id_stats_overall_sum[j-31][player_id_winner]

			player_id_stats_overall_count[j-31][player_id_winner] = player_id_stats_overall_count[j-31][player_id_winner] + 1 
			player_id_stats_overall_sum[j-31][player_id_winner] = player_id_stats_overall_sum[j-31][player_id_winner] + int(inputs[i][j])
			player_name[player_id_winner] = inputs[i][10]


	for j in range(40, 49):
		if player_id_loser not in player_id_stats_overall_count[j-40]:

			career_stats_loser[i][j] = 0
			career_stats_loser_total[i][j] = 0

			player_id_stats_overall_count[j-40][player_id_loser] = 1
			player_id_stats_overall_sum[j-40][player_id_loser] = int(inputs[i][j])
			player_name[player_id_loser] = inputs[i][20]
		else:
			career_stats_loser[i][j] = player_id_stats_overall_sum[j-40][player_id_loser]/player_id_stats_overall_count[j-40][player_id_loser]
			career_stats_loser_total[i][j] = player_id_stats_overall_sum[j-40][player_id_loser]

			player_id_stats_overall_count[j-40][player_id_loser] = player_id_stats_overall_count[j-40][player_id_loser] + 1 
			player_id_stats_overall_sum[j-40][player_id_loser] = player_id_stats_overall_sum[j-40][player_id_loser] + int(inputs[i][j])
			player_name[player_id_loser] = inputs[i][20]


		if i < num_rows - count_2019:
			X_inputs[2*i][j-40] = career_stats_winner[i][j-9] - career_stats_loser[i][j]
			X_inputs[2*i+1][j-40] = career_stats_loser[i][j] - career_stats_winner[i][j-9]
			X_inputs[2*i][j-24] = career_stats_winner_total[i][j-9] - career_stats_loser_total[i][j]
			X_inputs[2*i+1][j-24] = career_stats_loser_total[i][j] - career_stats_winner_total[i][j-9]

		else:
			x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
			X_prediction[x1][j-40] = career_stats_winner[i][j-9] - career_stats_loser[i][j]
			X_prediction[x1+1][j-40] = career_stats_loser[i][j] - career_stats_winner[i][j-9]
			X_prediction[x1][j-24] = career_stats_winner_total[i][j-9] - career_stats_loser_total[i][j]
			X_prediction[x1+1][j-24] = career_stats_loser_total[i][j] - career_stats_winner_total[i][j-9]

	#15, 16, 25, 26
	
	if player_id_winner not in rank_count:
		rank_count[player_id_winner] = 1
		rank_total[player_id_winner] = inputs[i][15]
		rankings_points_total[player_id_winner] = inputs[i][16]
	else:
		rank_count[player_id_winner] += 1
		rank_total[player_id_winner] += inputs[i][15]
		rankings_points_total[player_id_winner] += inputs[i][16]

	if player_id_loser not in rank_count:
		rank_count[player_id_loser] = 1
		rank_total[player_id_loser] = inputs[i][25]
		rankings_points_total[player_id_loser] = inputs[i][26]
	else:
		rank_count[player_id_loser] += 1
		rank_total[player_id_loser] += inputs[i][25]
		rankings_points_total[player_id_loser] += inputs[i][26]

	# 26, 25, 24, 22, 21, 18 - 16, 15, 14, 12, 11, 8
	k = 9

	for j in range(18, 27):
		if j != 19 and j != 20 and j != 23:
			if i < num_rows - count_2019:
				X_inputs[2*i][k] = float(inputs[i][j-10])
				X_inputs[2*i][k+18] = float(inputs[i][j])
				X_inputs[2*i+1][k] = float(inputs[i][j])
				X_inputs[2*i+1][k+18] = float(inputs[i][j-10])

				if j == 22 and (int(inputs[i][j-10]) == -1 or int(inputs[i][j]) == -1):
					X_inputs[2*i][k] = 0
					X_inputs[2*i][k+18] = 0
					X_inputs[2*i+1][k] = 0
					X_inputs[2*i+1][k+18] = 0
				k += 1
			else:
				x1 = int(2*i - 2*int(num_rows) + 2*int(count_2019))
				X_prediction[x1][k] = float(inputs[i][j-10])
				X_prediction[x1][k+18] = float(inputs[i][j])
				X_prediction[x1+1][k] = float(inputs[i][j])
				X_prediction[x1+1][k+18] = float(inputs[i][j-10])

				if j == 22 and (int(inputs[i][j-10]) == -1 or int(inputs[i][j]) == -1):
					X_prediction[x1][k] = 0
					X_prediction[x1][k+18] = 0
					X_prediction[x1+1][k] = 0
					X_prediction[x1+1][k+18] = 0

				k += 1
	
	if i < num_rows - count_2019:
		Y_inputs[2*i] = 1
		Y_inputs[2*i+1] = 0
	else:
		x1 = 2*i - 2*int(num_rows) + 2*int(count_2019)
		Y_prediction[x1] = 1
		Y_prediction[x1+1] = 0


clf = LogisticRegression(multi_class='ovr', random_state=0, solver='liblinear', penalty='l2').fit(X_inputs, Y_inputs)
training_prediction = clf.predict_proba(X_prediction)

np.savetxt("training_data.csv", X_inputs, delimiter=",")

total = count_2019
right = 0

print(training_prediction.shape)

for i in range(count_2019):
	(a, b) = training_prediction[2*i]
	(c, d) = training_prediction[2*i+1]

	if a < b and c > d:
		predicted = 1
	else: 
		if a > b and c < d:
			predicted = 0
		else:
			if a + d < b + c:
				predicted = 1
			else:
				predicted = 0

	if Y_prediction[2*i] == predicted:
		right = right + 1

print(total)
print(right)
print(right*100/total)

training_prediction_1 = clf.predict(X_inputs)

total = 2*(num_rows - count_2019)
right = 0

for i in range(2*(num_rows - count_2019)):
	if Y_inputs[i] == training_prediction_1[i]:
		right = right + 1

print(total)
print(right)
print(right*100/total)

print(total_no_head_to_head)

# it was 59.5% with 9 features which were just stats,
# with ranking, seed, ranking points, basically values known pre-match which describe the player - improved to 62.5%
#62.654205607476634 - l1 penalty
# lbfgs - l2 - 62.57943925233645

#clf = svm.SVC(kernel='linear')
#clf.fit(X_inputs, Y_inputs)

#svm.SVC(kernel='linear')
#svm.SVC(kernel='rbf')
#svm.SVC(kernel=‘sigmoid’)
#svm.SVC(kernel=‘poly')
#logistic regression - penaltystr, ‘l1’, ‘l2’, ‘elasticnet’ or ‘none’, optional (default=’l2’)

#predictions_svm_svc = clf.predict(X_prediction)

#right = 0 

#for i in range(2*count_2019):
#	if Y_prediction[i] == predictions_svm_svc[i]:
#		right = right + 1

#print(total)
#print(right)
#print(right*100/total)

# Sanity testing whether the total number of aces of Federer calculated the real aces - it matches!!
for player_id in player_id_stats_overall_count[0]:
	if "Federer" in player_name[player_id]:
		print(player_name[player_id], player_id_stats_overall_sum[0][player_id], player_id_stats_overall_count[0][player_id])
