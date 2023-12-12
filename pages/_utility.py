
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.decomposition import PCA
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
from plotly.tools import mpl_to_plotly


## ------------- init dataframes and specify data types ------------- ##


## old cleaning for csv
    #region
## movie dataframe
# df_movies = pd.read_csv('./data/tmdb_5000_movies.csv', parse_dates=['release_date'],
#                        dtype = {'budget' : int, 'genres' : object, 'homepage' : str, 'id' : int,
#                                 'keywords' : object, 'original_language' : str, 'original_title' : str,
#                                 'overview' : str, 'popularity' : float, 'production_companies' : object,
#                                 'production_countries' : object,
#                                 'revenue' : int, 'runtime' : float, 'spoken_languages' : object,
#                                 'status' : str, 'tagline' : str, 'title' : str, 'vote_average' : float,
#                                 'vote_count' : int}
                                
#                        )
# ## credits dataframe
# df_credits = pd.read_csv('./data/tmdb_5000_credits.csv',
#                         dtype = {'movie_id' : int, 'title' : str, 'cast' : object, 'crew' : object }
#                             )
# ## remove extra (empty) col at end of dataframe
# df_credits = df_credits.drop(df_credits.columns[-1], axis=1)

## clean dataframes
# df_movies.rename(columns={'id':'movie_id'}, inplace=True)
# df_movies['cast'] = df_credits['cast']
# df_movies['crew'] = df_credits['crew']
# df_movies = df_movies.drop(['homepage', 'original_language', 'overview', 
#                             'release_date', 'spoken_languages', 'status',
#                             'tagline', 'original_title', 'vote_count'], axis=1)
# print(df_movies.columns)
# df_movies.to_csv('./data/movies_cleaned.csv', index=False)

    #endregion

'''
## get new clean dataframe
    #region
df_movies = pd.read_csv('./data/movies_cleaned.csv',
                       dtype = {'budget' : int, 'genres' : object, 'movie_id' : int,
                                'keywords' : object, 'popularity' : float, 'production_companies' : object,
                                'production_countries' : object, 'revenue' : int, 'runtime' : float,
                                'title' : str, 'vote_average' : float, 'crew' : object, 'cast' : object}      
                       )


tmp = []
actors = [] ## format: [ [movie_id, actor1, actor2, actor3], [...], ...]
for film in range(len(df_movies)):
    actors_tmp = []
    actor_num = 0
    actors_tmp.append(df_movies.loc[film, 'movie_id'])
    for value in ast.literal_eval(df_movies.iloc[[film]]['cast'].values[0]):
        if actor_num < 3:
            tmp.append(value) 
            actor_num += 1
            for k, v in value.items():
                if k == 'name':
                    actors_tmp.append(v)
        else:
            actors.append(actors_tmp)
            break

df_new = df_movies.copy()
df_new = df_new.set_index('movie_id')
for film in actors:
    movie_id = film[0]
    df_new.at[movie_id, 'cast'] = film[1:]


df_new = df_new.drop(['production_countries', 'production_companies', 'crew', 'keywords'], axis=1)
df_new.to_csv('./data/movies_cleaned_cast.csv', index=False)
    #endregion
'''
'''
## clean genres
    #region

df_movies = pd.read_csv('./data/movies_cleaned_cast.csv',
                       dtype = {'budget' : int, 'genres' : object, 'movie_id' : int,
                                 'popularity' : float,
                                'revenue' : int, 'runtime' : float,
                                'title' : str, 'vote_average' : float,  'cast' : object}      
                       )


genres = [] ## format: [ [movie_id, actor1, actor2, actor3], [...], ...]
df_movies = df_movies.reset_index()
df_movies = df_movies.rename(columns={'index':'movie_id'})
print(df_movies.columns)
for film in range(len(df_movies)):
    genres_tmp = []
    genres_tmp.append(df_movies.loc[film, 'movie_id']) ## append movie id
    for value in ast.literal_eval(df_movies.iloc[[film]]['genres'].values[0]):
        for k, v in value.items():
            if k == 'name':
                genres_tmp.append(v)
    genres.append(genres_tmp)

df_new = df_movies.copy()
df_new = df_new.set_index('movie_id')
for film in genres:
    movie_id = film[0]
    df_new.at[movie_id, 'genres'] = film[1:]

# print(df_new['genres'])
print(df_new['genres'])
df_new.to_csv('./data/movies_cleaned_final.csv', index=False)



    #endregion
'''

df_movies = pd.read_csv('./data/movies_cleaned_final.csv',
                       dtype = {'budget' : int, 'genres' : object, 'movie_id' : int,
                                 'popularity' : float,
                                'revenue' : int, 'runtime' : float,
                                'title' : str, 'vote_average' : float,  'cast' : object}      
                       )











## ------------- cast vs. measures ------------- ## (make bar graphs or pie charts)
    #region

## get highest revenue films (matters a bit)
df_util = df_movies[['cast', 'revenue','title', 'popularity']]
df_util = df_util.sort_values('revenue')
df_util = df_util.head(50)
rev_cast = []
rev_cast_count = []
for row in df_util['cast']:
    # print(row)
    for actor in ast.literal_eval(row):
        # print(actor)
        if actor not in rev_cast:
            rev_cast.append(actor)
            rev_cast_count.append(1)
        else:
            # print(actor)
            rev_cast_count[rev_cast.index(actor)] += 1
# print(df_util['cast'])
# print(rev_cast_count)
# for i in range(len(rev_cast_count)): 
#     if rev_cast_count[i] > 1: print('{1}: {0}'.format(rev_cast_count[i], rev_cast[i]))
# print('..')
# John Hurt 3, Minnie Driver 3, Ron Perlman 2, Gabriel Byrne 2


## get highest grossing films (matters a bit)
df_util = df_movies[['cast', 'revenue','title', 'budget']].copy()
df_util['gross'] = df_movies['revenue'] + df_movies['budget']
df_util = df_util.sort_values('gross')
df_util = df_util.head(50)
rev_cast = []
rev_cast_count = []
for row in df_util['cast']:
    for actor in ast.literal_eval(row):
        if actor not in rev_cast:
            rev_cast.append(actor)
            rev_cast_count.append(1)
        else: rev_cast_count[rev_cast.index(actor)] += 1
# for i in range(len(rev_cast_count)): 
#     if rev_cast_count[i] > 1: print('{1}: {0}'.format(rev_cast_count[i], rev_cast[i]))

# Anthony Hopkins 3, Billy Bob Thornton 2, Chow Yun-fat 2, Hugh Jackman 2, Bruce Willis 2,
# Nicole Kidman 2, John Turturro 2, Brendan Fraser 2, John Travolta

## get highest popularity films (doesn't matter much)
df_util = df_movies[['cast', 'title', 'popularity']]
df_util = df_util.sort_values('popularity')
df_util = df_util.head(50)
rev_cast = []
rev_cast_count = []
for row in df_util['cast']:
    for actor in ast.literal_eval(row):
        if actor not in rev_cast:
            rev_cast.append(actor)
            rev_cast_count.append(1)
        else: rev_cast_count[rev_cast.index(actor)] += 1
# print(max(rev_cast_count))

## get highest rated films (doesn't matter much)
df_util = df_movies[['cast', 'vote_average', 'title', 'popularity']]
df_util = df_util.sort_values('vote_average')
df_util = df_util.head(50)
rev_cast = []
rev_cast_count = []
for row in df_util['cast']:
    for actor in ast.literal_eval(row):
        if actor not in rev_cast:
            rev_cast.append(actor)
            rev_cast_count.append(1)
        else: rev_cast_count[rev_cast.index(actor)] += 1
# print(max(rev_cast_count))

## separate numeric/string columns
# str_list = []
# for colname, colvalue in df_movies.iteritems():
#     if(len(colvalue)) == 0:
#         str_list.append(colname)
#     elif type(colvalue[1]) == str:
#         str_list.append(colname)
# num_list = df_movies.columns.difference(str_list)
# movie_num = df_movies[num_list]
# movie_num = movie_num.fillna(value=0, axis=1)
# X = movie_num.values
# X_std = StandardScaler().fit_transform(X)
# util1 = df_movies.plot(x='popularity', y='revenue', kind='hexbin') ## note: vote avg and popularity not very well correlated

# plt.show()
# plt.clf()

    #endregion

## ------------- bar charts (cast) ------------- ##
    #region

## revenue and cast
# John Hurt 3, Minnie Driver 3, Ron Perlman 2, Gabriel Byrne 2
cast_r = ['John Hurt', 'Minnie Driver', 'Ron Perlman', 'Gabriel Byrne']
vals_r = [3, 3, 2, 2]
fig_cast_rev, axU1 = plt.subplots(figsize=(12, 12))
# plt.close()
axU1.bar(x=cast_r, height=vals_r, color='#76A7B2')
plt.xlabel("Lead actor", fontsize=14)
plt.ylabel("Number of films", fontsize=14)
plt.title('Actors who Appear Multiple Times Amongst the 50 Highest Revenue Films', fontsize=15)
plt.yticks([0, 1, 2, 3])
plt.tight_layout()

plt.clf()
plt.close()
# fig_cast_rev = go.Figure(data=[go.Bar(x=cast_r, y=vals_r)])


cast_g = ['Anthony Hopkins', 'Billy Bob Thornton', 'Chow Yun-fat', 'Hugh Jackman', 'Bruce Willis',
            'Nicole Kidman', 'John Turturro', 'Brendan Fraser', 'John Travolta']
vals_g = [3, 2, 2, 2, 2, 2, 2, 2, 2]
fig_cast_g, axU2 = plt.subplots(figsize=(12, 12))
# plt.close(fig_cast_g)
axU2.bar(x=cast_g, height=vals_g, color='#76A7B2')
plt.xlabel("Lead actor", fontsize=14)
plt.ylabel("Number of films", fontsize=14)
plt.title('Actors who Appear Multiple Times Amongst the 50 Highest Grossing Films', fontsize=15)
plt.yticks([0, 1, 2, 3])
plt.tight_layout()
plt.xticks(rotation=0)
# plt.show()
plt.clf()
plt.close()

    #endregion

## ------------- complex analytics ------------- ##
    #region

## separate numeric/string columns
str_list = []
for colname, colvalue in df_movies.iteritems():
    if(len(colvalue)) == 0:
        str_list.append(colname)
    elif type(colvalue[1]) == str:
        str_list.append(colname)
# get numeric only by inversion
num_list = df_movies.columns.difference(str_list)

movie_num = df_movies[num_list]
movie_num = movie_num.fillna(value=0, axis=1)

## hexbin plot ##
X = movie_num.values ## shows how correlations between different features compare to one another     
# y = movie_num.columns
X_std = StandardScaler().fit_transform(X)
# figU1 = df_movies.plot(x='popularity', y='revenue', kind='hexbin') ## note: vote avg and popularity not very well correlated
# plt.show()
# plt.clf()
# plt.close()
# figU2 = df_movies.plot(x='popularity', y='vote_average', kind='hexbin')
# plt.show()
# plt.clf()
# plt.close(figU2)

'''
## heatmap ##
figU3, axU3 = plt.subplots(figsize=(12, 10))
plt.close()
plt.title('Pearson Correlation of Movie Features')
sns.heatmap(movie_num.astype(float).corr(), linewidths=0.25, vmax=1.0, square=True, cmap='YlGnBu', linecolor='black', annot=True)
# plt.show()
plt.clf()
plt.close(figU3)



## explained variances ##
mean_vec = np.mean(X_std, axis=0)
cov_mat = np.cov(X_std.T)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)

eig_pairs = [ (np.abs(eig_vals[i]),eig_vecs[:,i]) for i in range(len(eig_vals))]
eig_pairs.sort(key = lambda x: x[0], reverse= True)
tot = sum(eig_vals)
var_exp = [(i/tot)*100 for i in sorted(eig_vals, reverse=True)] # Individual explained variance
cum_var_exp = np.cumsum(var_exp) # Cumulative explained variance
print('cum. explained variance: {0}'.format(cum_var_exp))

## plot explained variances ##
figU4, axU4 = plt.subplots(figsize=(12, 10))
## 90% of the variance can be explained with  3 principal components; so let's use 3 components
plt.bar(range(5), var_exp, alpha=0.3333, align='center', label='individual explained variance', color='g')
plt.step(range(5), cum_var_exp, where='mid', label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')
# plt.show()
plt.clf()
plt.close(figU4)

## pca ##
figU5, axU5 = plt.subplots(figsize=(12, 10))
pca = PCA(n_components=3)
x_9d = pca.fit_transform(X_std)
pca1 = x_9d[:,0]
pca2 = x_9d[:,1]
pca3 = x_9d[:,2]
## can't discern any clusters, so try kmeans ## projection of 1 and 2 (components)
sns.scatterplot(
    x=pca1, y=pca2,
    # hue=y,
    # palette=sns.color_palette('hls', len(y)),
    legend='full',
    alpha=0.3,
    ax=axU5
) 
plt.clf()
plt.close(figU5)
# plt.figure(figsize = (9,7)) ## projection of 1 and 3
# sns.scatterplot(
#     x=pca1, y=pca3,
#     legend='full',
#     alpha=0.3
# ) 
# plt.figure(figsize = (9,7)) ## projection of 2 and 3
# sns.scatterplot(
#     x=pca2, y=pca3,
#     legend='full',
#     alpha=0.3
# ) 
## plotting this to see if there are any distinct clusters immediately (no, from the first 2 projections
## try k-means instead


# plt.scatter(x_9d[:,0],x_9d[:,1], c='goldenrod',alpha=0.5)
# plt.ylim(-10,15)
# plt.show()





kmeans = KMeans(n_clusters=3)
X_clustered = kmeans.fit_predict(x_9d)
# LABEL_COLOR_MAP = {0 : 'r',1 : 'g',2 : 'b'}
# label_color = [LABEL_COLOR_MAP[l] for l in X_clustered]
# plt.figure(figsize = (7,7))
# plt.scatter(x_9d[:,0],x_9d[:,2], c= label_color, alpha=0.5) 
# plt.show()

## kmeans, plots all features in the dataframe in a pairwise manner
figU6, axU6 = plt.subplots(figsize=(12, 10))
df = pd.DataFrame(x_9d)
df = df[[0, 1, 2]]
df['X_cluster'] = X_clustered
sns.pairplot(df, hue='X_cluster', palette='Dark2', diag_kind='kde', height=1.86)
# plt.show()

plt.clf()
plt.close(figU6)

'''

    #endregion

## ------------- analytics misc charts ------------- ##

util_colors = ['#FF88B4', '#FFB3D2', '#E3E3FF', '#BCC0D6', '#89C3CF', 
               '#76A7B2', '#FDC899', '#FDAB62', '#CDE4CF', '#FFEDAE', 
               '#FFE072', '#C28F4F']
util_colors_past = ['#FDF2C6', '#FAD8B8', '#F7C491', '#DCECDD', '#ACD5DD', 
                    '#9EC1C9', '#D0D3E2', '#EBEBFF', '#F8C9DF', '#F5ABCA', 
                    '#A5C0AD', '#AED9BE']

## bar highest budget films ##
    # re-done in graph objects
df_budget = df_movies.sort_values(by='budget', ascending=False).head(10)
df_budget['budget'] = df_budget['budget'].div(1000000)

# figU7, axU7 = plt.subplots(figsize=(10, 8))

# axU7.barh('title', 'budget', data=df_budget, color=util_colors)
axU7_labels = df_budget['title'].values


# plt.show()
plt.clf()
plt.close()

# val = mpl_to_plotly(figU7)

## box budget, revenue across all flms ##


## box average vote, popularity, runtime across all flms ##

## proportion of each genre ##