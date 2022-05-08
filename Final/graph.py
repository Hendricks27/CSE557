
import os
import matplotlib
matplotlib.rcParams['figure.dpi'] = 300
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.patches import Patch


sns.set_style("whitegrid")

graph_color = "maroon"
graph_aspect_ratio_long = 10
graph_aspect_ratio_height = 6


def is_categorical(l):
    if len(set(l)) <= 20:
        return True
    return False

def is_numerical(l):
    try:
        list(map(float, l))
        return True
    except:
        return False

def to_numerical(l):
    return list(map(float, filter(lambda x:x>-1e1000 and x<1e1000, l)))


def bargraph(title, data, img_path):

    x = []
    y = []

    distinct_count = len(list(set(data)))

    rotate_xlabel = False
    fig = plt.figure(figsize=(graph_aspect_ratio_long, graph_aspect_ratio_height))

    if is_categorical(data):
        x = list(set(data))
        y = [data.count(x0) for x0 in x]
        x = list(map(str, x))
        tmp = [(x[i], y[i]) for i in range(len(x))]

        x = [p[0] for p in sorted(tmp)]
        y = [p[1] for p in sorted(tmp)]

        colors = sns.color_palette('husl', n_colors=len(x))

        if max(list(map(len, x))) * distinct_count > 100:
            rotate_xlabel = True

        #plt.bar(x, y, color=graph_color, width=0.4)
        p = sns.barplot(x=x, y=y, palette=colors)
        cmap = dict(zip(x, colors))
        patches = [Patch(color=v, label=k) for k, v in cmap.items()]
        plt.legend(handles=patches, bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0)

        plt.ylabel("Count")

    elif is_numerical(data):
        data = list(map(float, data))

        bin_num = 5

        if len(data) > 1000:
            bin_num = 10

        if len(data) > 10000:
            bin_num = 15

        if len(data) > 30000:
            bin_num = 25

        if len(data) / distinct_count > 10 and distinct_count < 80:
            bin_num = distinct_count

        n, bins, patches = plt.hist(data, bin_num, density=True, facecolor=graph_color, alpha=0.75)
        plt.ylabel("Frequency")

    else:
        # pure text
        return
        # raise RuntimeError


    plt.title(title)

    if rotate_xlabel:
        plt.xticks(rotation=45)
    plt.savefig(img_path, bbox_inches='tight')
    return None

def violingraph(title, data, img_path):

    plt.figure()

    if is_numerical(data):
        data = to_numerical(data)
        sns.violinplot(y=data)
        plt.title(title)
        plt.savefig(img_path)
    return None


def densitygraph(title, data, img_path):

    plt.figure()
    if is_numerical(data):
        data = to_numerical(data)
        sns.kdeplot(np.array(data), bw=0.5)
        plt.title(title)
        plt.savefig(img_path)

def boxgraph(title, data, img_path):

    plt.figure()
    if is_numerical(data):
        data = to_numerical(data)
        sns.boxplot(y=data)
        plt.title(title)
        plt.savefig(img_path)
    return None

# Double Columns
def scatter(title, x_label, y_label, x, y, img_path):
    total_len = len(x)
    assert len(x) == len(y)

    fig = plt.figure()
    plt.scatter(x, y)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(img_path)
    return


def heatmap(title, x_label, y_label, x, y, img_path):

    # Assert categorical x categorical

    total_len = len(x)
    assert len(x) == len(y)

    fig = plt.figure()

    x_distinct = list(sorted(set(x)))
    y_distinct = list(sorted(set(y)))

    xd = {}
    for index, item in enumerate(x_distinct):
        xd[item] = index
    yd = {}
    for index, item in enumerate(y_distinct):
        yd[item] = index


    count = np.zeros((len(x_distinct), len(y_distinct)))
    for i in range(total_len):
        x0 = x[i]
        y0 = y[i]
        count[xd[x0], yd[y0]] += 1

    freq = count / total_len * 100


    x_distinct = list(map(str, x_distinct))
    y_distinct = list(map(str, y_distinct))

    fig, ax = plt.subplots()
    im = ax.imshow(freq, cmap="Blues")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("", rotation=-90, va="bottom")

    ax.set_xticks(np.arange(len(y_distinct)), labels=y_distinct)
    ax.set_yticks(np.arange(len(x_distinct)), labels=x_distinct)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(x_distinct)):
        for j in range(len(y_distinct)):
            text = ax.text(j, i, "%0.1f"%(freq[i, j]), ha="center", va="center", color="r")

    ax.set_title(title)
    ax.grid(False)
    fig.tight_layout()

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig(img_path)
    return

def violinplot2(title, x_label, y_label, x, y, img_path):

    # Assert categorical (x) x numerical (y)

    total_len = len(x)
    assert len(x) == len(y)
    assert is_categorical(x)
    assert is_numerical(y)

    fig = plt.figure()

    sns.violinplot(x=x, y=to_numerical(y))

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig(img_path)

    return None



def main(workdir):
    data_path = workdir + "data.txt"
    df = pd.read_csv(data_path, low_memory=False)

    for col_num, col_name in enumerate(df.columns):
        col = list(df.loc[:, col_name])
        # print(col_num, col_name, len(col), is_categorical(col), is_numerical(col))

        image_type = "histogram"
        image_name = image_type + "_" + col_name + ".png"
        image_path = workdir + image_name
        bargraph(col_name + " (%s)" % image_type, col, image_path)

        image_type = "violin_graph"
        image_name = image_type + "_" + col_name + ".png"
        image_path = workdir + image_name
        violingraph(col_name + " (%s)" % image_type, col, image_path)

        image_type = "density_graph"
        image_name = image_type + "_" + col_name + ".png"
        image_path = workdir + image_name
        densitygraph(col_name + " (%s)" % image_type, col, image_path)

        image_type = "box_graph"
        image_name = image_type + "_" + col_name + ".png"
        image_path = workdir + image_name
        boxgraph(col_name + " (%s)" % image_type, col, image_path)


    for col_num1, col_name1 in enumerate(df.columns):
        for col_num2, col_name2 in enumerate(df.columns):
            if col_name1 == col_name2:
                continue

            col1 = list(df.loc[:, col_name1])
            col2 = list(df.loc[:, col_name2])

            # print(col_num1, col_name1, len(col1), is_categorical(col1), is_numerical(col1))
            # print(col_num2, col_name2, len(col2), is_categorical(col2), is_numerical(col2))

            image_type = "scatter_plot"
            image_title = "%s_vs_%s_(%s)" % (col_name1, col_name2, image_type)
            image_name = image_title + ".png"
            image_path = workdir + image_name
            if is_numerical(col1) and is_numerical(col2):
                scatter(image_title, col_num1, col_num2, col1, col2, image_path)

            image_type = "heatmap"
            image_title = "%s_vs_%s_(%s)" % (col_name1, col_name2, image_type)
            image_name = image_title + ".png"
            image_path = workdir + image_name
            if is_categorical(col1) and is_categorical(col2):
                heatmap(image_title, col_num1, col_num2, col1, col2, image_path)

            image_type = "heatmap"
            image_title = "%s_vs_%s_(%s)" % (col_name1, col_name2, image_type)
            image_name = image_title + ".png"
            image_path = workdir + image_name
            if is_categorical(col1) and is_numerical(col2):
                violinplot2(image_title, col_num1, col_num2, col1, col2, image_path)


    return len(df.columns), len(df)



if __name__ == "__main__":

    for i in range(2, 6):

        workdir = './test/sample%i/' % i

        for f in os.listdir(workdir):
            if f.endswith("png"):
                os.remove(workdir + f)

        result = main(workdir)
        print(result)


