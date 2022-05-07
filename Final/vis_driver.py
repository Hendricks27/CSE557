## All the import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import table 
import copy
import dataframe_image as dfi
import seaborn as sns
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import copy
from itertools import combinations
# import geopandas as gpd
#https://stackoverflow.com/questions/35402874/global-name-parseerror-is-not-defined-i-used-try-and-except-to-avoid-it-but-t
from pandas.errors import ParserError

"""
Helper Functions
All Functions listed in this section are helper functions.

combination(): For generating possible combinations.
is_categorical(): For deciding if a single row is categorical or not.
get_type_number(): Get the number of types(categorical, numerical, date) for each type.
"""


# https://www.geeksforgeeks.org/itertools-combinations-module-python-print-possible-combinations/
def combination(total_number, count):
    arr = []
    for i in range(0, total_number):
        arr.append(i)
    return list(combinations(arr, count))

CATEGORICAL = 0
NUMERICAL = 1
DATE = 2

# Helper Functions
# See if the current value is categorical
# https://stackoverflow.com/questions/26924904/check-if-dataframe-column-is-categorical
def is_categorical(df):
    return df.dtype.name == 'category' or df.dtype.name == 'object'

# https://stackoverflow.com/questions/69687640/how-to-iterate-over-columns-using-pandas
# first categorical, numberical, date
def get_type_number(df):
    result = [0, 0, 0]
    for i in range(0, len(df.columns)):
        if(is_categorical(new_pd[df.columns[i]])):
            result[0] = result[0] + 1
        else:
            result[1] = result[1] + 1
            ## [NS]
        if(new_pd[df.columns[i]].dtype.name == 'datetime64[ns]'):
            result[2] = result[2] + 1
    return result

"""
One-dimensional Visualization
Functions tailored to make one-dimensional visualization design.

table_visualization(): generating a table various categrories. 
aligned_bar_visualization(): showing aligned bars on categorical/numerical data. 
box_plot(): (only works on numerical data) shows a box plot for distribution and analysis. 
density_plot(): (only works on numerical data) shows a density plot on the numerical value distribution.
"""

# Inspiration: https://d3-graph-gallery.com/index.html
# All valid visualizations listed here.
# average: https://stackoverflow.com/questions/16689514/how-to-get-the-average-of-dataframe-column-values
# https://stackoverflow.com/questions/43725513/pandas-get-average-dataframe/43725615
# https://stackoverflow.com/questions/15360925/how-to-get-the-first-column-of-a-pandas-dataframe-as-a-series

# If categorical, count numbers of occurences for each 
# sns.countplot
# Unique Values
# https://pandas.pydata.org/docs/reference/api/pandas.unique.html
def table_visualization(data, directory='my_visualization.png'):
    #plt.clf()
    return_df = {}
    return_df['Name'] = data.name
    return_df['Total Rows'] = len(data.index)
    if(is_categorical(data)):
        return_df['Count of Unique Values'] = len(pd.unique(data))
        real_return_df = pd.DataFrame(data=[return_df])
        df_styled = real_return_df.style.background_gradient()
        dfi.export(df_styled, directory, table_conversion='matplotlib')
    else:
        # Numerical
        return_df['Average'] = data.mean()
        return_df['Max'] = data.max()
        return_df['Min'] = data.min()
        return_df['standard deviation'] = data.std()
        real_return_df = pd.DataFrame(data=[return_df])
        df_styled = real_return_df.style.background_gradient()
        dfi.export(df_styled, directory, table_conversion='matplotlib')
    return directory
    

def aligned_bar_visualization(df, directory='my_visualization.png'):
    # https://stackabuse.com/matplotlib-bar-plot-tutorial-and-examples/
    # https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean
    plt.clf()
    if(is_categorical(df)):
        #other logic
        # https://stackoverflow.com/questions/5312778/how-to-test-if-a-dictionary-contains-a-specific-key
        x_dict = {}
        x_result = []
        y_result = []
        all_list = df.values.tolist()
        # https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
        for i in range(0, len(all_list)):
            if(all_list[i] not in x_dict):
                x_dict[all_list[i]] = 0
            x_dict[all_list[i]] = x_dict[all_list[i]] + 1
        for key, value in x_dict.items():
            x_result.append(key)
            y_result.append(value)
        plt.title("Aligned Bar Visualization for categorical choice")
        # https://stackoverflow.com/questions/40575067/matplotlib-bar-chart-space-out-bars
        plt.bar(x_result, y_result, width = 0.5)
        plt.savefig(directory)
    else:
        magic_num = 5
        max_value = df.max()
        min_value = df.min()
        x_result = []
        for i in range(0, magic_num):
            x_result.append(i)
        y_result = [0] * magic_num
        step = (int)((max_value - min_value) / magic_num + 1)
        for i in range(0, magic_num):
            if(i == magic_num - 1):
                x_result[i] = "["  + str(min_value + step * i) + "," + str(max_value) + "]"
            x_result[i] = "["  + str(min_value + step * i) + "," + str(min_value + step * (i + 1)) + "]"
        all_list = df.values.tolist()
        for i in range(0, len(all_list)):
            y_result[(int)((all_list[i] - min_value) / step)] = y_result[(int)((all_list[i]  - min_value) / step)] + 1
        plt.title("Aligned Bar Visualization for numerical choice")
        # https://stackoverflow.com/questions/40575067/matplotlib-bar-chart-space-out-bars
        plt.bar(x_result, y_result, width = 0.5)
        plt.savefig(directory)
    return directory
    
# SOURCE
# Not suitable for categorical data.
# https://matplotlib.org/3.5.0/gallery/pyplots/boxplot_demo_pyplot.html
# https://stackoverflow.com/questions/45926230/how-to-calculate-1st-and-3rd-quartiles
def box_plot(df, directory='my_visualization.png'):
    plt.clf()
    if(is_categorical(df)):
        return "N/A"
    fig1, ax1 = plt.subplots()
    ax1.set_title('Box Plot Visualization for numerical choice')
    ax1.boxplot(df)
    fig1.savefig(directory)
    return directory
    
# https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
def density_plot(df, directory='my_visualization.png'):
    plt.clf()
    if(is_categorical(df)):
        return "N/A"
    sns.set_style('whitegrid')
    plot = sns.kdeplot(df, bw=0.5)
    fig = plot.get_figure()
    fig.savefig(directory) 
    
"""
Unstructured Data
This part shows the unstructured data and some possible visualization methods.
It can provide top words and generate wordclouds.
"""

# https://amueller.github.io/word_cloud/auto_examples/simple.html#sphx-glr-auto-examples-simple-py
# For unstuctured data
# text = open('./hamlet.txt').read()
#print(text)
# Generate a word cloud image

def generate_wordcloud(text, directory="my_visualization.png"):
    wordcloud = WordCloud().generate(text)
    
    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    
    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


    #https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
    processed_texts = nltk.word_tokenize(text)
    filtered_words = [word for word in processed_texts if word not in stopwords.words('english')]
    filtered_word = ""
    for i in range(0, len(filtered_words)):
        filtered_word = filtered_word + " " + filtered_words[i] + " "
    wordcloud = WordCloud().generate(filtered_word)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(directory)
    #plt.axis("off")
    
    return directory

# https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
def present_top_words(text, directory="my_visualization.png", top_count=10):
    processed_texts = nltk.word_tokenize(text)
    filtered_words = [word for word in processed_texts if word not in stopwords.words('english') and len(word) > 2]
    allWordDist = nltk.FreqDist(w.lower() for w in filtered_words)
    most_common = []
    most_common_counts = []#allWordDist.most_common(top_count)[0:top_count]
    for i in range(0, min(top_count, len(allWordDist))):
        most_common.append(allWordDist.most_common(top_count)[i][0])
        most_common_counts.append(allWordDist.most_common(top_count)[i][1])
    plt.bar(most_common, most_common_counts, width = 0.5)
    plt.savefig(directory)
    
"""
Multiple Visualization Functions
Suitable for visualization a moderate size of data (2 - 4.)
"""

def scatter_plot_visualization(df1, df2, directory="my_visualization.png"):
    plt.clf()
    plt.plot(df1, df2, 'o')
    plt.savefig(directory)
    return directory

    
def heat_map_visualization(df1, df2, directory="my_visualization.png"):
    ax = sns.heatmap(uniform_data)


# generate all possible visualizations, with C(n, magic_number).
# Some dimensionality reduction features are applied spefically to the data.

def generate_all_vis(directory='../test/sample2/', magic_number = 4, upper_column_constraint=10):
    if(directory[-1] != '/'):
        directory = directory + '/'
    full_data_dir = directory + "/data.txt"
    try:
        df = pd.read_csv(full_data_dir, sep=",", header=0)
    except (IOError, NotADirectoryError, ParserError) as e:
        text = open(full_data_dir).read()
        return_list = []
        
        visualization_name = directory + "wordcloud_visualization_1.png"
        graph_value = generate_wordcloud(text, visualization_name)
        return_list.append([graph_value, "word cloud plot", "Standalone Text"])
        
        
        visualization_name = directory + "top_words_visualization_1.png"
        graph_value = present_top_words(text, visualization_name)
        return_list.append([graph_value, "top words plot", "Standalone Text"])
        return return_list
    else:
        return_list = []
        all_columns = df.columns
        graph_id = 0
        # TODO: remove this after testing
        df = df.head(200)
        for i in range(0, len(all_columns)):
            df[all_columns[i]] = pd.to_numeric(df[all_columns[i]], errors='ignore')
    
        # Dimension Reduction
        # Could be extended to implement; filtered here arbitarily to save time and effort
        # https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
        # https://stackoverflow.com/questions/31328861/python-pandas-replacing-header-with-top-row
        # https://stackoverflow.com/questions/19071199/drop-columns-whose-name-contains-a-specific-string-from-pandas-dataframe

        # remove correlation
        df = df[df.columns.drop(list(df.filter(regex='cooc')))]
        df = df[df.columns.drop(list(df.filter(regex='cellId')))]
        df = df[df.columns.drop(list(df.filter(regex='gymIn')))]
        df = df[df.columns.drop(list(df.filter(regex='pokestopIn')))]
        df = df[df.columns.drop(list(df.filter(regex='id')))]
        df = df[df.columns.drop(list(df.filter(regex='appearedLocalTime')))]
        # read in data from the directory
        # i = 1
        #graph_id = graph_id + 1

        for graph_id in range(0, upper_column_constraint):
            visualization_name = directory + "table_visualization_" + str(graph_id) + ".png"
            graph_value = table_visualization(df.iloc[:,graph_id], visualization_name)
            return_list.append([graph_value, "table", [df.columns[graph_id]]])
        
            visualization_name = directory + "aligned_bar_visualization_" + str(graph_id) + ".png"
            graph_value = aligned_bar_visualization(df.iloc[:,graph_id], visualization_name)
            return_list.append([graph_value, "aligned bar", [df.columns[graph_id]]])
        
            visualization_name = directory + "box_plot_" + str(graph_id) + ".png"
            graph_value = box_plot(df.iloc[:,graph_id], visualization_name)
            return_list.append([graph_value, "box plot", [df.columns[graph_id]]])
        
            visualization_name = directory + "density_plot_" + str(graph_id) + ".png"
            graph_value = density_plot(df.iloc[:,graph_id], visualization_name)
            return_list.append([graph_value, "density plot", [df.columns[graph_id]]])
        #i = 2
        all_list = combination(len(df.columns), 2)
        for i in range(0, len(all_list)):
            visualization_name = directory + "scatter_plot_" + str(i) + ".png"
            graph_value = scatter_plot_visualization(df.iloc[:,all_list[i][0]], df.iloc[:,all_list[i][1]], visualization_name)
            return_list.append([graph_value, "scatter plot", [df.columns[all_list[i][0]], df.columns[all_list[i][1]]]])

        return return_list

if __name__ == "__main__":

    for i in range(1, 7):
        result = generate_all_vis(directory='./test/sample%i/'%i)
        print(result)



