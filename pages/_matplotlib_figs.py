# python 3.9.13 ('base':conda)
# shortcut to run python file: shift + enter
# shortcut to organize imports: shift + cmd + p, select 'organize imports'
# shortcut to collpse all: cmd + k + 0
# http://localhost:8050/

import ast
import collections
import time

## imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from plotly.subplots import make_subplots
from scipy import stats

## ------------- init dataframes and specify data types ------------- ##

## movie dataframe
df_movies = pd.read_csv('./data/tmdb_5000_movies.csv', parse_dates=['release_date'],
                       dtype = {'budget' : int, 'genres' : object, 'homepage' : str, 'id' : int,
                                'keywords' : object, 'original_language' : str, 'original_title' : str,
                                'overview' : str, 'popularity' : float, 'production_companies' : object,
                                'production_countries' : object,
                                'revenue' : int, 'runtime' : float, 'spoken_languages' : object,
                                'status' : str, 'tagline' : str, 'title' : str, 'vote_average' : float,
                                'vote_count' : int}
                                
                       )
## credits dataframe
df_credits = pd.read_csv('./data/tmdb_5000_credits.csv',
                        dtype = {'movie_id' : int, 'title' : str, 'cast' : object, 'crew' : object }
                            )
## remove extra (empty) col at end of dataframe
df_credits = df_credits.drop(df_credits.columns[-1], axis=1)


## ------------- generate queries and charts ------------- ##

# (1.1) what are the most popular 50 movies in the dataset?

## create new df with relevant parameters, sort in descending order
df_pop = df_movies[['popularity', 'title', 'vote_average', 'id']].sort_values('popularity', ascending=False)

## get 50 most popular films
df_pop50 = df_pop.iloc[:50]

## generate figure
fig11, ax11 = plt.subplots(figsize=(12, 12))

## plot with lollipop chart
plt.stem(df_pop50['popularity'], linefmt='#69b3a2', orientation='horizontal',
        basefmt='k:')
plt.scatter(df_pop50['popularity'], df_pop50['title'], color='#76A7B2', zorder=3)

## adjust labels
plt.xlabel("Popularity", fontsize=14)
plt.ylabel("Title", fontsize=14)
plt.title('Most Popular 50 Films', fontsize=15)
plt.tight_layout()
plt.close(fig11)



# (1.2) what are the 50 highest rated movies in the dataset? 
## create new df with relevant parameters, sort in descending order
df_vote = df_movies[['title', 'vote_average', 'id']].sort_values('vote_average', ascending=False)

## get 50 most highest rated movies
df_vote50 = df_vote.iloc[:50]

## generate figure
fig12, ax12 = plt.subplots(figsize=(12, 12))



## plot with lollipop chart
plt.stem(df_vote50['vote_average'], linefmt='#b8bddb', orientation='horizontal',
        basefmt='k:', bottom=7.87)
plt.scatter(df_vote50['vote_average'], df_vote50['title'], color='#76A7B2', zorder=3)

## adjust labels
plt.xlabel("Average Rating (of 10)", fontsize=14)
plt.ylabel("Title", fontsize=14)
plt.title('Highest Rated 50 Films', fontsize=15)
ax12.set_xticks([8, 8.5, 9, 9.5, 10])
ax12.set_xlim([7.75, 10.25])

plt.tight_layout()
plt.close(fig12)




# (1.3) which of the 50 most popular films are also amongst the 50 highest rated?

## create combined dataframe
df_popvote50 = pd.concat([df_pop50[['title', 'id']].reset_index(), df_vote50[['title', 'id']].reset_index()])

# find duplicate values (appear in both dataframes)
df_popvote50 = df_popvote50[df_popvote50.duplicated(keep=False)].drop(df_popvote50.columns[0], axis=1)
df_popvote50 = df_popvote50.drop_duplicates()


## create color legend to highlight duplicates
colors_pop50 = []
colors_vote50 = []
for film in df_pop50['title']:
    if film in df_popvote50['title'].values: colors_pop50.append('k')
    else: colors_pop50.append('#69b3a2')
    
for film in df_vote50['title']:
    if film in df_popvote50['title'].values: colors_vote50.append('k')
    else: colors_vote50.append('#b8bddb')
        
legend_elements_pop50 = [Line2D([0], [0], marker='o', color='w', 
                          label='most popular and highest rated', markerfacecolor='k', markersize=10),
                         Line2D([0], [0], marker='o', color='w', 
                          label='most popular', markerfacecolor='#69b3a2', markersize=10)
                        ]
legend_elements_vote50 = [Line2D([0], [0], marker='o', color='w', 
                          label='most popular and highest rated', markerfacecolor='k', markersize=10),
                         Line2D([0], [0], marker='o', color='w', 
                          label='highest rated', markerfacecolor='#b8bddb', markersize=10)
                        ]



# (1.4) are there any trends regarding which movies are both popular and highly rated?

# ### budget and revenue
## get information about the most popular and highest rated films

## from movies csv file
df_top50 = df_movies[df_movies.set_index(['id']).index.isin(df_popvote50.set_index(['id']).index)]

## from credits csv file
df_top50_c = df_credits[df_credits.set_index(['movie_id']).index.isin(df_popvote50.set_index(['id']).index)]
                     

'''
movies: features to observe

budget
genres
keywords?
production_companies
release_date? (time of year)
revenue?

''';

# print(df_top50['budget'])

## budget/revenue

## scale budget/revenue data ($s to millions of $s)
# fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 20))
fig14a, ax14a = plt.subplots(figsize=(12, 12))
fig14b, ax14b = plt.subplots(figsize=(12, 12))

plt.close(fig14a)
plt.close(fig14b)



df_top50_tmpb = df_top50['budget'].div(1000000)
df_top50_tmpb = pd.concat([df_top50_tmpb, df_top50['title']], axis=1)

df_top50_tmpr = df_top50['revenue'].div(1000000)
df_top50_tmpr = pd.concat([df_top50_tmpr, df_top50['title']], axis=1)
df_top50_tmpr = df_top50_tmpr.sort_values(['revenue'], ascending=False).reset_index(drop=True)

## create plots
sns.set(style="darkgrid")
sns.barplot(
    x='budget', 
    y='title', 
    data=df_top50_tmpb, 
    estimator=sum, 
    ci=None, 
    color='#76A7B2',
    ax=ax14a
)
ax14a.set(xlabel="Budget (millions)", ylabel="Title", title='Budget for Films in Top 50 Most Popular and Highest Rated')

sns.barplot(
    x='revenue', 
    y='title', 
    data=df_top50_tmpr, 
    estimator=sum, 
    ci=None, 
    color='#BCC0D6',
    ax=ax14b
)
ax14b.set(xlabel="Revenue (millions)", ylabel="Title", title='Revenue for Films in Top 50 Most Popular and Highest Rated')


## vs: average/median budgets/revenues

## get all films not in our top list

df_nottop50 = df_movies[~df_movies.set_index(['id']).index.isin(df_popvote50.set_index(['id']).index)]

# df_nottop50['budget'] = df_nottop50['budget'].div(1000000)

## average budget/revenue for top 12/all other films
avg_12b = int((df_top50['budget'].mean()))/1000000
med_12b = int((df_top50['budget'].median()))/1000000
avg_12r = int((df_top50['revenue'].mean()))/1000000
med_12r = int((df_top50['revenue'].median()))/1000000
avg_b = int((df_nottop50['budget'].mean()))/1000000
avg_r = int((df_nottop50['revenue'].mean()))/1000000



## from credits csv file
df_nottop50_c = df_credits[~df_credits.set_index(['movie_id']).index.isin(df_popvote50.set_index(['id']).index)]
# sns.violinplot(x=df_nottop50_c["budget"], ax=ax3)


# print('average budget top 12: {0}\naverage revenue top 12: {1}\n'.format(avg_12b, avg_12r))

# print('average budget non-top 12: {0}\naverage revenue non-top 12: {1}\n'.format(avg_b, avg_r))





#                                             title      id
# 1                                    Interstellar  157336
# 12                                       Whiplash  244786
# 13                                The Dark Knight     155
# 15                                      Inception   27205
# 19                                     Fight Club     550
# 23                                  The Godfather     238
# 31                                   Forrest Gump      13
# 34                       The Shawshank Redemption     278
# 41                One Flew Over the Cuckoo's Nest     510
# 44                                      Star Wars      11
# 46  The Lord of the Rings: The Return of the King     122
# 47                                   Pulp Fiction     680


plt.tight_layout()
# plt.show()


# ### production companies


'''
movies: features to observe

genres
keywords?
production_companies
release_date? (time of year)
revenue?

''';


# (1.4) production companies
    
## get all production companies
arr_production = []
arr_production_tmp = []

for i in range(len(df_top50)): ## iterate through top films
    for value in ast.literal_eval((df_top50.iloc[[i]]['production_companies'].values[0])):
        arr_production.append(value)    
# print(arr_production)

## see if any duplicates
for x in arr_production:
    for k, v in x.items():
        if k == 'name':
            arr_production_tmp.append(v)

## also need to find their counts
arr_production = dict(collections.Counter(arr_production_tmp))
arr_production_tmp = []
arr_production_counts = []
tmp_a = []
tmp_c = []

for x, y in arr_production.items():
    if y > 1:
        arr_production_tmp.append(x)
        arr_production_counts.append(y)
    tmp_a.append(x)
    tmp_c.append(y)

# arr_production = [item for item, count in collections.Counter(arr_production_tmp).items() if count > 1]
# print(arr_production_tmp)
# print(arr_production_counts)

## pie/donut chart for production companies


# wedges1, texts1 = ax1.pie(tmp_c, wedgeprops=dict(width=0.5), startangle=-40)
# my_circle = plt.Circle((0,0), 0.7, color='white')
my_circle2 = plt.Circle((0,0), 0.7, color='white')
# ax1.add_patch(my_circle)

colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']



# (2.1) are certain genres more popular than others? 

## average rating

## get set of all genres
# set_genres = {"Family", "Fantasy", "Crime", "War", "Music", "Thriller", "Documentary", "Romance", 
#                  "Comedy", "TV Movie", "Action", "Science Fiction", "Horror", "Western", "Foreign", "Mystery",
#                  "History", "Adventure", "Drama", "Animation"}
                

## create dictionaries to hold the films associated with each genre --> 'Genre' : ['Film1.id', 'Film2.id', ...]
# dict_movies_by_genre = {}
# for item in set_genres: # ~20
#     dict_movies_by_genre[item] = []

## get data for each genre
df_genres = df_movies.filter(['title', 'id', 'vote_average', 'revenue'], axis=1)
df_genres.rename(columns={'vote_average':'rating'}, inplace=True) ## to match current name
df_genres['genre'] = ''


## fill in data for genres dict
for i in range(len(df_movies)): # ~5000, for each film
    film_id = df_movies.iloc[[i]]['id'].values[0]
    for value in ast.literal_eval((df_movies.iloc[[i]]['genres'].values[0])): # for each genre it's associated with
        # film_id = df_movies.iloc[[i]]['id'].values[0]
        genre_name = value['name']
        df_genres.loc[df_genres.id == film_id, 'genre'] += genre_name

    

        










## separate large dataframe into smaller ones

df_family = df_genres.loc[df_genres['genre'].str.contains('Family')]
df_crime = df_genres.loc[df_genres['genre'].str.contains('Crime')]
df_thriller = df_genres.loc[df_genres['genre'].str.contains('Thriller')]
df_romance = df_genres.loc[df_genres['genre'].str.contains('Romance')]
df_comedy = df_genres.loc[df_genres['genre'].str.contains('Comedy')]
df_action = df_genres.loc[df_genres['genre'].str.contains('Action')]
df_horror = df_genres.loc[df_genres['genre'].str.contains('Horror')]
df_scifi = df_genres.loc[df_genres['genre'].str.contains('Science Fiction')]
df_mystery = df_genres.loc[df_genres['genre'].str.contains('Mystery')]
df_adventure = df_genres.loc[df_genres['genre'].str.contains('Adventure')]
df_drama = df_genres.loc[df_genres['genre'].str.contains('Drama')]

## use df_other for smaller genres (under 500 films)
df_other = df_genres.loc[df_genres['genre'].str.contains(
    'Fantasy|War|Music|Documentary|TV Movie|Western|Foreign|History|Animation')]



## generate labels
labels = [
        'Family','Crime',
        'Thriller', 'Romance',
        'Comedy', 'Action',
        'Horror', 'Science Fiction',
        'Mystery', 'Adventure',
        'Drama', 'Other' ]

 
## connect medians with line
medians = [ df_family['rating'].median(), df_crime['rating'].median(),
        df_thriller['rating'].median(), df_romance['rating'].median(),
        df_horror['rating'].median(), df_scifi['rating'].median(),
        df_mystery['rating'].median(), df_adventure['rating'].median(),
        df_drama['rating'].median(), df_other['rating'].median() ]







## z-scores
## get average revenue for each and total
means = [ df_family['revenue'].mean(), df_crime['revenue'].mean(),
        df_thriller['revenue'].mean(), df_romance['revenue'].mean(),
        df_comedy['revenue'].mean(), df_action['revenue'].mean(),
        df_horror['revenue'].mean(), df_scifi['revenue'].mean(),
        df_mystery['revenue'].mean(), df_adventure['revenue'].mean(),
        df_drama['revenue'].mean(), df_other['revenue'].mean() ]

for i in range(len(means)): means[i] = means[i] / 1000000 ## show revenue in millions

mean_all = sum(means) / len(means)
std = np.std(means)

z_scores = [ ((i - mean_all) / std) for i in means ]
z_scores.sort()


## adding animation to bar chart, but not removing from other category
## added for clarity/visualization, not accuracy
z_scores.append((225.69302506410256 - mean_all) / std)
if 'Animation' not in labels:
    labels.append('Animation')



other_genres = ['Fantasy', 'War', 'Music', 'Documentary', 'TV Movie', 'Western', 'Foreign', 'History', 'Animation']

for val in other_genres:
    df_a = df_other.loc[df_other['genre'].str.contains(val)]    
    
# # 193.35424510613208 fantasy
# print( (193.35424510613208 - mean_all) / std ) 
# # 225.69302506410256 animation
# print( (225.69302506410256 - mean_all) / std ) 
# ## animation and fantasy
    

colors21b = [(105, 179, 162) for i in range(len(labels)-1) ]
colors21b.append((105, 179, 162))





## for adding animation from other category
labels.pop();

print('finished!')

