import os
import sys
import json
import urllib.request
import itertools


def bargraph(dataset, column_name, image_path):
    data_single_column = dataset.get_column(column_name)
    image = draw(data_single_column)
    image.saveTo(image_path)
    return None

def histogram():
    # Similar graph generation
    return None

def whatever_some_kind_of_graph():
    return None



def draw_all_graph(workdir):

    res = []
    dataset_path = workdir + "/data.txt"
    dataset = some_magic_trick_to_read_entire_data(dataset_path)

    for column_name in dataset.get_column():
        # 2 steps
        # 1. call your modular function to draw a single image
        # 2. Put the image name into the variable res

        image_name = "bargraph_" + column_name + ".png"
        bargraph(dataset, column_name, os.path.join(workdir, image_name))
        res.append(image_name)

        image_name = "histogram_" + column_name + ".png"
        bargraph(dataset, column_name, os.path.join(workdir, image_name))
        res.append(image_name)

        image_name = "whatever_" + column_name + ".png"
        bargraph(dataset, column_name, os.path.join(workdir, image_name))
        res.append(image_name)

    for any_2_columns in itertools.combinations(dataset.get_column(), 2):
        # Well, draw all possible graphs
        pass

    for any_3_columns in itertools.combinations(dataset.get_column(), 3):
        # Well, draw all possible graphs
        pass

    return res





if __name__ == "__main__":

    # For testing purposes only
    for workdir in ["./test/sample1/", "./test/sample2/"]:

        image_names = draw_all_graph(workdir)
        print(image_names)

        # Expected result like ["graphType1_book", "graphType1_price", "graphType2_book", "graphType2_price", ... ]




