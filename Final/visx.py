
import copy
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
import dataframe_image as dfi

import matplotlib.pyplot as plt

from pandas.plotting import table
from wordcloud import WordCloud
from nltk.corpus import stopwords
from itertools import combinations




# https://www.geeksforgeeks.org/itertools-combinations-module-python-print-possible-combinations/
def combination(total_number, count):
    arr = []
    for i in range(0, total_number):
        arr.append(i)
    return list(combinations(arr, count))

CATEGORICAL = 0
NUMERICAL = 1
DATE = 2



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


def rule_based_filtering(df, all_recommend_dict):
    all_recommend_dict = copy.deepcopy(all_recommend_dict)
    all_valid_charts = []
    df_categorical_status = get_type_number(df)
    if (len(df.columns) > 0):
        all_valid_charts.append("text_table")
    if (df_categorical_status[1] >= 1):
        all_valid_charts.append("aligned_bar")
        all_recommend_dict["aligned_bar"] = 2  # 2
    if (df_categorical_status[0] >= 2 and df_categorical_status[1] >= 1):
        all_valid_charts.append("stacked_bar")
        all_recommend_dict["stacked_bar"] = 2
        if (df_categorical_status[0] >= 3):
            all_recommend_dict["stacked_bar"] = 3
    # https://stackoverflow.com/questions/43214204/how-do-i-tell-if-a-column-in-a-pandas-dataframe-is-of-type-datetime-how-do-i-te
    if (df_categorical_status[2] >= 1 and df_categorical_status[1] >= 1):
        all_valid_charts.append("discrete_line")
        all_recommend_dict["discrete_line"] = 4
    if (df_categorical_status[1] >= 2 and df_categorical_status[1] <= 4):
        all_valid_charts.append("scatter_plot")
        all_recommend_dict["scatter_plot"] = 3
    if (df_categorical_status[1] == 2):
        all_recommend_dict["scatter_plot"] = 5

    return all_recommend_dict


def table_visualization(data, directory='my_visualization.png'):
    # plt.clf()
    return_df = {}
    return_df['Name'] = data.name
    return_df['Total Rows'] = len(data.index)
    if (is_categorical(data)):
        return_df['Count of Unique Values'] = len(pd.unique(data))
        real_return_df = pd.DataFrame(data=[return_df])
        df_styled = real_return_df.style.background_gradient()
        dfi.export(df_styled, directory)
    else:
        # Numerical
        return_df['Average'] = data.mean()
        return_df['Max'] = data.max()
        return_df['Min'] = data.min()
        return_df['standard deviation'] = data.std()
        real_return_df = pd.DataFrame(data=[return_df])
        df_styled = real_return_df.style.background_gradient()
        dfi.export(df_styled, directory)
    return directory


def aligned_bar_visualization(df, directory='my_visualization.png'):
    # https://stackabuse.com/matplotlib-bar-plot-tutorial-and-examples/
    # https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean
    plt.clf()
    if (is_categorical(df)):
        # other logic
        # https://stackoverflow.com/questions/5312778/how-to-test-if-a-dictionary-contains-a-specific-key
        x_dict = {}
        x_result = []
        y_result = []
        all_list = df.values.tolist()
        # https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
        for i in range(0, len(all_list)):
            if (all_list[i] not in x_dict):
                x_dict[all_list[i]] = 0
            x_dict[all_list[i]] = x_dict[all_list[i]] + 1
        for key, value in x_dict.items():
            x_result.append(key)
            y_result.append(value)
        plt.title("Aligned Bar Visualization for categorical choice")
        # https://stackoverflow.com/questions/40575067/matplotlib-bar-chart-space-out-bars
        plt.bar(x_result, y_result, width=0.5)
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
            if (i == magic_num - 1):
                x_result[i] = "[" + str(min_value + step * i) + "," + str(max_value) + "]"
            x_result[i] = "[" + str(min_value + step * i) + "," + str(min_value + step * (i + 1)) + "]"
        all_list = df.values.tolist()
        for i in range(0, len(all_list)):
            y_result[(int)((all_list[i] - min_value) / step)] = y_result[(int)((all_list[i] - min_value) / step)] + 1
        plt.title("Aligned Bar Visualization for numerical choice")
        # https://stackoverflow.com/questions/40575067/matplotlib-bar-chart-space-out-bars
        plt.bar(x_result, y_result, width=0.5)
        plt.savefig(directory)
    return directory


# SOURCE
# Not suitable for categorical data.
# https://matplotlib.org/3.5.0/gallery/pyplots/boxplot_demo_pyplot.html
# https://stackoverflow.com/questions/45926230/how-to-calculate-1st-and-3rd-quartiles
def box_plot(df, directory='my_visualization.png'):
    plt.clf()
    if (is_categorical(df)):
        return "N/A"
    fig1, ax1 = plt.subplots()
    ax1.set_title('Box Plot Visualization for numerical choice')
    ax1.boxplot(df)
    fig1.savefig(directory)
    return directory


# https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
def density_plot(df, directory='my_visualization.png'):
    plt.clf()
    if (is_categorical(df)):
        return "N/A"
    sns.set_style('whitegrid')
    plot = sns.kdeplot(df, bw=0.5)
    fig = plot.get_figure()
    fig.savefig(directory)


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

    # https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
    processed_texts = nltk.word_tokenize(text)
    filtered_words = [word for word in processed_texts if word not in stopwords.words('english')]
    filtered_word = ""
    for i in range(0, len(filtered_words)):
        filtered_word = filtered_word + " " + filtered_words[i] + " "
    wordcloud = WordCloud().generate(filtered_word)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(directory)
    # plt.axis("off")

    return directory


# https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
def present_top_words(text, directory="my_visualization.png", top_count=10):
    processed_texts = nltk.word_tokenize(text)
    filtered_words = [word for word in processed_texts if word not in stopwords.words('english') and len(word) > 2]
    allWordDist = nltk.FreqDist(w.lower() for w in filtered_words)
    most_common = []
    most_common_counts = []  # allWordDist.most_common(top_count)[0:top_count]
    for i in range(0, min(top_count, len(allWordDist))):
        most_common.append(allWordDist.most_common(top_count)[i][0])
        most_common_counts.append(allWordDist.most_common(top_count)[i][1])
    plt.bar(most_common, most_common_counts, width=0.5)
    plt.savefig(directory)



def scatter_plot_visualization(df1, df2, directory="my_visualization.png"):
    if(is_categorical(df1) or is_categorical(df2)):
        return "N/A"
    else:
        plt.plot(df1, df2, 'o')
        plt.savefig(directory)
        return directory

def heat_map_visualization(df1, df2, directory="my_visualization.png"):
    ax = sns.heatmap(uniform_data)


def generate_all_vis(directory='./test/sample2/data.txt', magic_number = 4):
    df = pd.read_csv(directory, sep=",", header=None)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    graph_id = 0
    df = df.head(200)
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
    # read in data from the directory
    # i = 1
    #graph_id = graph_id + 1
    print(len(df))
    all_list = combination(len(df), 1)

    for graph_id in range(0, 10):
        visualization_name = "table_visualization_" + str(graph_id) + ".png"
        table_visualization(df.iloc[:,graph_id], visualization_name)
        visualization_name = "aligned_bar_visualization_" + str(graph_id) + ".png"
        aligned_bar_visualization(df.iloc[:,graph_id], visualization_name)
        visualization_name = "box_plot_" + str(graph_id) + ".png"
        box_plot(df.iloc[:,graph_id], visualization_name)
        visualization_name = "density_plot_" + str(graph_id) + ".png"
        density_plot(df.iloc[:,graph_id], visualization_name)

generate_all_vis()















