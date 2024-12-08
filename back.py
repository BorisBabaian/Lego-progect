import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import Literal


df = pd.read_csv('./data/lego_sets.csv')

Jur_w = ['Indoraptor Rampage at Lockwood Estate',
       'Carnotaurus Gyrosphere Escape', 'T. rex Transport',
       'Jurassic Park Velociraptor Chase', 'Dilophosaurus Outpost Attack',
       "Blue's Helicopter Pursuit", 'Stygimoloch Breakout',
       'Pteranodon Chase']
for theme in Jur_w:
    df['theme_name'] = df['theme_name'].replace(theme, 'Jurassic World')

df['theme_name'] = df['theme_name'].replace('THE LEGO® NINJAGO® MOVIE™', 'NINJAGO®')
df['theme_name'] = df['theme_name'].replace('DC Super Hero Girls', 'DC Comics™ Super Heroes')
df['theme_name'] = df['theme_name'].replace('THE LEGO® BATMAN MOVIE', 'DC Comics™ Super Heroes')
df['theme_name'] = df['theme_name'].replace('BOOST', 'MINDSTORMS®')
df['theme_name'] = df['theme_name'].replace('BrickHeadz', 'Minifigures')
df['theme_name'] = df['theme_name'].replace('LEGO® Creator 3-in-1', 'Creator 3-in-1')
df['theme_name'] = df['theme_name'].replace('Heartlake City Playground', 'Friends')
df['theme_name'] = df['theme_name'].replace('Power Functions', 'Technic')

df['price_per_piece'] = df['list_price'] / df['piece_count']
aver = df.groupby('theme_name')['price_per_piece'].mean().reset_index()
aver.columns = ['theme_name', 'average_price_per_piece']
aver.sort_values('average_price_per_piece', inplace=True) 


class Regr(LinearRegression):
        def __init__(
        self,
        *,
        fit_intercept=True,
        copy_X=True,
        n_jobs=None,
        positive=False):
            
            self.fit_intercept = fit_intercept
            self.copy_X = copy_X
            self.n_jobs = n_jobs
            self.positive = positive
        
    
        def theme_fit(self, df: pd.DataFrame, col: str) -> tuple:
            x = pd.DataFrame(df[df['theme_name'] == col]['list_price']) 
            y = pd.DataFrame(df[df['theme_name'] == col]['piece_count'])
            self.fit(x, y)
            
            return x


themes = ['DC Comics™ Super Heroes', 'Star Wars™', 'NINJAGO®', 'Architecture']


    
def Price_vs_Number_of_pieces(df: pd.DataFrame, themes: list | str, country: str = 'FI', on: bool = False) -> any:
    tar = df[df['theme_name'].isin(themes) & df['country'].isin([country]) & (df['piece_count'] < 3000)]

    categories = np.unique(tar['theme_name'])
    colors = [plt.cm.tab10(i / float(len(categories))) for i in range(len(categories))]

    fig, ax = plt.subplots(figsize=(18, 10), dpi=400, facecolor='w', edgecolor='k')
    leg = []

    for i, theme in enumerate(categories):
        ax.scatter(x='list_price', y='piece_count',
                   data=tar.loc[tar.theme_name == theme, :],
                   s=20, c=colors[i], label=str(theme))
        
        leg.append(theme)
        if on:
            m = Regr()
            x = m.theme_fit(tar, theme)
            # x = pd.DataFrame(tar.list_price)
            ax.plot(x, m.predict(x), c=colors[i])

            leg.append('regression of ' + theme + ' sets')

    ax.legend(leg)
    ax.set(xlabel='price', ylabel='a number of pieces')
    ax.set_title("Scatterplot of sets Price vs Number of pieces", fontsize=22)

    return fig



def theme_hist():
    df_pie = df.groupby('theme_name').size()

    fig, ax = plt.subplots(figsize=(16,7), dpi= 400)
    
    ax.bar(df_pie.index, df_pie.values, color='#ff9999', width=.5)

    for i, val in enumerate(df_pie.values):
        ax.text(i, val, float(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})
    fig.gca().set_xticklabels(df_pie.index, rotation=60, horizontalalignment= 'right')

    plt.title("Themes in Dataset", fontsize=22)
    
    return fig

def av():
    fig, ax = plt.subplots(figsize=(16,6), facecolor='white', dpi=200)
    ax.vlines(x=aver.theme_name[:-2],
            ymin=0, ymax=aver.average_price_per_piece[:-2],
            color='#cc66ff', alpha=0.7, linewidth=20)

    for i, ave in enumerate(aver.average_price_per_piece[:-2]):
        ax.text(i, ave+0.1, round(ave, 2), horizontalalignment='center')
        
    ax.set_title('Bar Chart for Average Price Per Piece (without outliners)', fontdict={'size':22})
    ax.set(ylabel='Average Price', ylim=(0, 2))
    plt.xticks(aver.theme_name[:-2], rotation=60, horizontalalignment='right', fontsize=12)
    
    return fig

def Lol(df: pd.DataFrame, col: str, mode: Literal['max', 'min', 'mean']) -> any:
    if mode == 'max':
        new_df = df.groupby('theme_name')[col].max().reset_index()
    elif mode == 'min':
        new_df = df.groupby('theme_name')[col].min().reset_index()
    elif mode == 'mean':
        new_df = df.groupby('theme_name')[col].mean().reset_index()
    else:
        raise ValueError(f'mode hasn`t got attribute {mode}')
    
    fig, ax = plt.subplots(figsize=(16,7), dpi=200)
    a = new_df[col].mean() / 20
    ax.vlines(x=new_df.theme_name, ymin=0, ymax=new_df[col], color='#009933', alpha=0.7, linewidth=2)
    ax.scatter(x=new_df.theme_name, y=new_df[col], s=75, color='#009933')
    
    if col == 'list_price':
        ax.set_ylabel('Price in $')
        ax.set_title(f'Lollipop {mode} prices in themes', fontdict={'size':22})
    elif col == 'piece_count':
        ax.set_ylabel('pieces')
        ax.set_title(f'Lollipop {mode} pieces in themes', fontdict={'size':22})
        
    ax.set_xticks(new_df.theme_name)
    ax.set_xticklabels(new_df.theme_name, rotation=60, fontdict={'horizontalalignment': 'right', 'size':12})

    for row in new_df.itertuples():
        ax.text(row.Index, new_df.loc[row.Index][col]+a, s=round(new_df.loc[row.Index][col]), horizontalalignment='center', verticalalignment='bottom', fontsize=14)

    return fig