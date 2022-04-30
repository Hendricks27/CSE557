import os
import sys
import json
import urllib.request




def your_function(workdir):

    res = []
    dataset_path = workdir + "/data.txt"

    # Your magic trick to analyze data
    # Your magic trick to generate vis
    # Your magic trick to figure out which vis is the best
    # Then put the image file name into res

    # PSEUDO EXAMPLE
    image_name = "example.jpg"
    urllib.request.urlretrieve(
        "https://upload.wikimedia.org/wikipedia/commons/d/d5/Rue_Jeanne_dArc_Tramway_Orleans.jpg",
        workdir + image_name
    )
    res.append(image_name)

    return res








