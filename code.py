# --------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

electors_2009 = pd.read_csv(path)
candidate_2009 = pd.read_csv(path1)

# Plot a bar chart to compare the number of male and female candidates in the election
# Finding the value counts of both the genders
gender = candidate_2009.Candidate_Sex.value_counts()

# Stroing the counts in a variable  
count = [gender[0],gender[1]]

x = ['Male candidates','Female Candidates']

# Plotting a bar graph
plt.bar(x,count)

plt.xlabel('Gender')

plt.ylabel('Count')

plt.title('Gender Comparison Bar Chart')

plt.tight_layout()

plt.show()

# Plot a histogram of the age of all the candidates as well as of the winner amongst them. Compare them and note an observation
# Selecting the subset of the data with winner candidates
winner = candidate_2009[candidate_2009.Position == 1]

# Histogram of the age of all the candidates

fig,ax = plt.subplots(nrows=1,ncols=2,tight_layout = True)

ax[0].hist(list(candidate_2009.Candidate_Age),bins = 10)
ax[0].set_xlabel('Age of the Candidates')
ax[0].set_ylabel('Number of Candidates')
ax[0].set_title('All the Candidates')

ax[1].hist(list(winner.Candidate_Age),bins = 10,color = 'red')
ax[1].set_xlabel('Age of the Candidates')
ax[1].set_ylabel('Number of Candidates')
ax[1].set_title('Winner Candidates')

# Plot a bar graph to get the vote shares of different parties
# Group the dataframe by 'Party_Abbreviation' and sum the 'Total _Votes_Polled'
vote_share = candidate_2009.groupby('Party_Abbreviation')['Total_Votes_Polled'].sum()

# Plot the vote share with respect to different parties
party_vote_share = vote_share.sort_values(ascending=False)[:10].plot(kind='bar')
party_vote_share.set_xlabel('Party')
party_vote_share.set_ylabel('Votes in Millions(100)')
party_vote_share.set_title('Vote Shares')

# Plot a barplot to compare the mean poll percentage of all the states

# Mean statistics of all the states
poll_percentage = electors_2009.groupby('STATE').mean()

# Creating a dictionary of states and poll percentage
polls = poll_percentage[['POLL PERCENTAGE']].sort_values('POLL PERCENTAGE',ascending = False).to_dict()

# States and their poll percentage
states = list(polls['POLL PERCENTAGE'].keys())
state_percentage = list(polls['POLL PERCENTAGE'].values())

# Creating a dataframe
Data = {'STATE':states,'Poll_Percentage':state_percentage}
DF = pd.DataFrame(data=Data)

# Generating a bar plot
fig,ax = plt.subplots(figsize=(6, 20))

plt.barh(DF.STATE,DF.Poll_Percentage)
ax.set_xlabel('Poll Percentage')
ax.set_ylabel('States')
ax.set_title('Comparing Statewise Poll Percentage')


# Plot a bar plot to compare the seats won by different parties in Uttar Pradesh
UP_win = candidate_2009[(candidate_2009['Position'] == 1.0) & (candidate_2009['State_name'] == 'Uttar Pradesh') ]

UP = UP_win.Party_Abbreviation.value_counts().to_dict()

plt.bar(UP.keys(),UP.values())

plt.xlabel('Parties')

plt.ylabel('Seats won')

plt.title('UP seats comparison')

# Plot a stacked bar chart to compare the number of seats won by different `Alliances` in Gujarat,Madhya Pradesh and Maharashtra. 
# Subset of winner candidates
winner = candidate_2009[candidate_2009.Position == 1]

# Subset the the dataset for the states of Gujarat, Maharashtra and Madhya Pradesh
states = winner[(winner.State_name == 'Gujarat') | (winner.State_name == 'Maharashtra') | (winner.State_name == 'Madhya Pradesh')]

# Grouping the states by alliances
states.groupby('State_name')['Alliance'].count()

# Stacked bar chart
states.groupby(['State_name', 'Alliance']).size().unstack().plot(kind='bar', stacked=True, figsize=(15,10))

plt.xlabel('States')

plt.ylabel('Seats')

plt.xticks(rotation = 45)
# Plot a grouped bar chart to compare the number of winner candidates on the basis of their caste in the states of Andhra Pradesh, Kerala, Tamil Nadu and Karnataka
# Subset containing data of the given states
cat = candidate_2009[(candidate_2009.State_name == 'Andhra Pradesh') | (candidate_2009.State_name == 'Kerala') | (candidate_2009.State_name == 'Tamil Nadu') | (candidate_2009.State_name == 'Karnataka')]

# Subset the data with the winner of each constituency of the mentioned states
cat = cat[cat.Position == 1]

# Group the data according to `Alliance` and `Candidate_Category`
cat = cat.groupby(['Alliance','Candidate_Category'])['Position'].sum().unstack().reset_index()

# Plotting a grouped bar chart
nx = cat.plot(kind='bar', title ="2009 Winning Category", figsize=(15, 10), legend=True, fontsize=12)
nx.set_xlabel("Candidate Category", fontsize=12)
nx.set_ylabel("Seats Won", fontsize=12)

# Modifying Axis Labels
labels = [item.get_text() for item in nx.get_xticklabels()]
labels[0:11] = cat['Alliance']

nx.set_xticklabels(labels)

# Plot a horizontal bar graph of the Parliamentary constituency with total voters less than 100000
# Constituency with less than 100000 voters
voters = electors_2009[electors_2009.Total_Electors < 1000000]

# Plot a horizontal bar graph to compare constituencies with less than 1000000 voters
plt.figure(figsize=(15,10))

plt.barh(voters['PARLIAMENTARY CONSTITUENCY']  ,voters.Total_Electors)

plt.xlabel('Number of Voters')

plt.ylabel('States')

plt.xticks(rotation = 90)

# Plot a pie chart with the top 10 parties with majority seats in the elections
# Candidates with 1st position in their respective constituiency
winner = candidate_2009[candidate_2009.Position == 1]

# Find the parties with the number of seats won by them 
final = winner.Party_Abbreviation.value_counts()[:6].to_dict()

# count of other regional parties
final['Other_Regional_Parties'] = sum(winner.Party_Abbreviation.value_counts()) - sum(winner['Party_Abbreviation'].value_counts()[:10])

# Pie chart
plt.figure(figsize = (10,10))
plt.pie(final.values(),labels= final.keys(), autopct='%1.1f%%')
plt.axis('equal')

# Plot a pie diagram for top 9 states with most number of seats
# Top 9 states with maximum number of seats
seats = electors_2009.STATE.value_counts()[:9].to_dict()

# Sum of other states
seats['Other States'] = electors_2009.STATE.value_counts().sum() - electors_2009.STATE.value_counts()[:9].sum()

# Function to convert percentages into actual values
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

values = autopct_format(seats.values())

# PLotting the pie chart
plt.figure(figsize=(10,10))

plt.pie(x=seats.values(),labels = seats.keys(), autopct=values)

plt.axis('equal')


