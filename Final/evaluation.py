import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.spatial.distance import pdist, squareform
from graph import single_column_function, double_column_function, is_categorical, is_numerical

dtype_anno = {0: 'numerical', 1: 'boolean', 2: 'category'}
tasks = {0: 'Correlation', 1: 'Anomalies', 2: 'Clusters', 3: 'Distribution', 4: 'Range'}
title = {'bar': 'Bar Graph ', 'violin1': 'Violin Plot ', 'violin2': 'Violin Plot ', 'density': 'Density Plot ',
         'box': 'Box Plot ', 'scatter': 'Scatter Plot ', 'heatmap': 'Heatmap Plot '}
count_task_fig = {'Correlation': {'bar': 0, 'violin': 0, 'scatter': 0, 'heatmap': 0},
                  'Anomalies': {'bar': 0, 'box': 0, 'scatter': 0},
                  'Clusters': {'bar': 0, 'density': 0, 'scatter': 0},
                  'Distribution': {'bar': 0, 'density': 0, 'violin': 0, 'scatter': 0},
                  'Range': {'bar': 0, 'violin': 0, 'scatter': 0, 'heatmap': 0}}


def judge_dtype(df):
    dtypes = {}
    dtype_col = {0: [], 1: [], 2: [], 3: []}
    for col in df.columns:
        type = df[col].dtypes.name
        if ('int' in type) | ('float' in type):
            num = 0
        elif type == 'bool':
            num = 1
        elif (type == 'object') | (type == 'category'):
            num = 2
        else:
            num = 3
        dtypes[col] = {'type': num}
        dtype_col[num].append(col)
    return dtypes, dtype_col


def extract_features(df, dtypes):
    # descriptions of the distribution of the column
    for col in df.columns:
        if dtypes[col]['type'] == 0:
            dtypes[col]['max'] = max(df[col])
            dtypes[col]['min'] = min(df[col])
            dtypes[col]['median'] = np.nanmedian(df[col])
            dtypes[col]['mean'] = np.nanmean(df[col])
            dtypes[col]['nan'] = np.sum(np.isnan(df[col])) / len(df)
        elif dtypes[col]['type'] == 2:
            if len(df[col].unique()) > len(df) * 0.3:
                dtypes[col]['category'] = 'row'
                dtypes[col]['row'] = 'row'
            else:
                dtypes[col]['category'] = df[col].unique()
                for cate in dtypes[col]['category']:
                    dtypes[col][cate] = np.sum(df[col] == cate) / len(df)
        elif dtypes[col]['type'] == 1:
            dtypes[col]['category'] = ['True', 'False']
            dtypes[col]['True'] = np.sum(df[col] == True) / len(df)
            dtypes[col]['False'] = 1 - dtypes[col]['True']
    return dtypes


def switch_str_2_bool(cate):
    if cate == 'True':
        return True
    elif cate == 'False':
        return False
    else:
        return cate


def distributed_sampling(df, indep, dep, dtype_col, dtypes):
    M = df[[indep, dep]]
    result = pd.DataFrame([])
    if (indep in dtype_col[0]) & (dep in dtype_col[0]):  # 2 variables are both numerical
        rate = max(round(len(df) / 500), 1)  # constant rate sampling for 500 rows
        result = M[::rate]
        result_distance = pdist(np.array(result))  # calculate the eucliean distance
    elif (indep not in dtype_col[0]) & (dep not in dtype_col[0]):  # 2 variables are both categorical/boolean
        for cate_indep in dtypes[indep]['category']:
            for cate_dep in dtypes[dep]['category']:
                cate_dep_n = switch_str_2_bool(cate_dep)
                cate_indep_n = switch_str_2_bool(cate_indep)
                if len(M.loc[(M[indep] == cate_indep_n) & (M[dep] == cate_dep_n), :]) > 0:
                    result = pd.concat([result, M.loc[(M[indep] == cate_indep_n) & (M[dep] == cate_dep_n), :].sample(
                        max(1, round(500 * dtypes[indep][cate_indep] * dtypes[dep][cate_dep])), replace=True)])
        result['new_ind'] = result[indep]
        result['new_dep'] = result[dep]
        for num, cate in enumerate(dtypes[indep]['category']):  # boolean/categorical: one-hot encoding
            result.loc[result[indep] == cate, 'new_ind'] = float(num)
        for num, cate in enumerate(dtypes[dep]['category']):
            result.loc[result[dep] == cate, 'new_dep'] = float(num)
        result = result[['new_ind', 'new_dep']]
        result_distance = pdist(np.array(result), 'jaccard')  # calculate the jaccard distance
    else:  # one variable numerical, the other categorical
        rate = dep
        rate_1 = indep
        if dep in dtype_col[0]:
            rate = indep
            rate_1 = dep
        for cate in dtypes[rate]['category']:
            cate_n = switch_str_2_bool(cate)
            if len(M.loc[M[rate] == cate_n, :]) > 0:
                result = pd.concat([result, M.loc[M[rate] == cate_n, :].sample(max(1, round(500 * dtypes[rate][cate])),
                                                                               replace=True)])
        result['new'] = result[rate]
        for num, cate in enumerate(dtypes[rate]['category']):
            result.loc[result[rate] == cate, 'new'] = num
        result = result[[rate_1, 'new']]
        result_distance = pdist(np.array(result), 'jaccard')  # calculate the jaccard distance
    return result, result_distance


def distributed_sampling_1st(df, indep, dtype_col, dtypes):
    M = df[[indep]]
    result = pd.DataFrame([])
    if indep in dtype_col[0]:  # 1 variable is numerical
        rate = max(round(len(df) / 500), 1)  # constant rate sampling for 500 rows
        result = M[::rate]
        result_distance = pdist(np.array(result))  # calculate the eucliean distance
    else:  # 1 variable is both categorical/boolean
        for cate_indep in dtypes[indep]['category']:
            cate_indep_n = switch_str_2_bool(cate_indep)
            if len(M.loc[M[indep] == cate_indep_n, :]) > 0:
                result = pd.concat([result, M.loc[M[indep] == cate_indep_n, :].sample(
                    max(1, round(500 * dtypes[indep][cate_indep])))])
        result['new_ind'] = result[indep]
        for num, cate in enumerate(dtypes[indep]['category']):  # boolean/categorical: one-hot encoding
            result.loc[result[indep] == cate, 'new_ind'] = float(num)
        result = result[['new_ind']]
        result_distance = pdist(np.array(result), 'jaccard')  # calculate the jaccard distance
    return result, result_distance


def edge_calculate(M, edges):
    length = []
    for edge in edges:
        length.append(np.sqrt((M.iloc[edge[0], 0] - M.iloc[edge[1], 0]) ** 2 +
                              (M.iloc[edge[0], 1] - M.iloc[edge[1], 1]) ** 2))
    return length


def cosine(i, j, k):
    ji = i - j
    jk = k - j
    if (np.linalg.norm(ji) == 0) | (np.linalg.norm(jk) == 0):
        return -1
    else:
        return np.dot(ji, jk) / (np.linalg.norm(ji) * np.linalg.norm(jk))


def vertice_striated(M, edges):
    vertices_striated, vertices = [], []
    for i in range(len(M)):
        if (i in edges[:, 0]) & (i in edges[:, 1]):
            find_j = -1
            for j in range(len(edges[edges[:, 0] == i])):
                if np.sum(M.iloc[edges[edges[:, 0] == i][j][1]].values != M.iloc[i].values) > 0:
                    find_j = j
                    break
            if find_j >= 0:
                find_k = -1
                for k in range(len(edges[edges[:, 1] == i])):
                    if (np.sum(M.iloc[edges[edges[:, 1] == i][k]].values != M.iloc[i].values) > 0) & \
                            (np.sum(M.iloc[edges[edges[:, 1] == i][k]].values != M.iloc[find_j].values) > 0):
                        find_k = k
                        break
                if (find_j >= 0) & (find_k >= 0):
                    vertices.append(M.iloc[i].values)
                    if cosine(M.iloc[i].values, M.iloc[find_j].values, M.iloc[find_k].values) < -0.75:
                        vertices_striated.append(M.iloc[i].values)
    return vertices_striated, vertices


def Minimum_Spanning_Tree(X, copy_X=True):
    # http://peekaboo-vision.blogspot.com/2012/02/simplistic-minimum-spanning-tree-in.html
    # Author: Andreas Mueller
    if copy_X:
        X = X.copy()

    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix of edge weights")
    n_vertices = X.shape[0]
    spanning_edges = []

    # initialize with node 0:
    visited_vertices = [0]
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    X[diag_indices, diag_indices] = np.inf

    while num_visited != n_vertices:
        new_edge = np.argmin(X[visited_vertices], axis=None)
        # 2d encoding of new_edge from flat, get correct indices
        new_edge = divmod(new_edge, n_vertices)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = np.inf
        X[new_edge[1], visited_vertices] = np.inf
        num_visited += 1
    return np.vstack(spanning_edges)


def calculate_overlap(M):
    overlap, area = 0, 0
    col = M.columns[1]
    for i in M.iloc[:, 0].unique():
        ind = M[M.iloc[:, 0] == i].index
        num = len(ind)
        area += num
        overlap += num - len(M.loc[ind, col].unique())
    if area == 0:
        area = 1
    return abs(1 - overlap / area)


def calculate_overlap_1st(M):
    overlap, area = 0, 0
    col = M.columns.values[0]
    N = M[col].astype('int').unique()
    for i in N:
        num = np.sum(M[round(M) == i]).values[0]
        area += num
        overlap += 1
    if area == 0:
        area = 1
    return overlap / area * len(N)


def scagnostic_1st(df, dtype_col, dtypes):
    measure_list = {}
    # low-level perception-related quality metrics, from https://ieeexplore.ieee.org/document/7864468
    # middle-level pattern-driven quality metrics, from https://www.cs.uic.edu/~tdang/file/ScagExplorer.pdf
    for indep_num, indep in enumerate(df.columns):
        # print('working on ', indep)
        if 'row' in dtypes[indep]:
            continue
        # sampling (n = 500) with the same distribution, and return a distance matrix to M
        M, M_pdist = distributed_sampling_1st(df, indep, dtype_col, dtypes)

        # construct the minimal spanning tree
        edge_list = Minimum_Spanning_Tree(squareform(M_pdist))
        edge_length = []
        for edge in edge_list:
            edge_length.append(abs((M.iloc[edge[0]].values[0] - M.iloc[edge[1]].values[0])))
        # print('Done! -- tree')
        q25 = np.quantile(edge_length, 0.25)
        q75 = np.quantile(edge_length, 0.75)
        cut_off = q75 - 1.5 * (q75 - q25)
        if cut_off < 0:
            cut_off = abs(cut_off)
        q50 = np.quantile(edge_length, 0.5)
        q90 = np.quantile(edge_length, 0.9)
        q10 = np.quantile(edge_length, 0.1)
        skewed = (q90 - q50) / max((q90 - q10), 0.001)
        vertices_striated, vertices = vertice_striated(M, edge_list)
        if len(vertices) == 0:
            striated = 1
        else:
            striated = len(vertices_striated) / len(vertices)
        # print('Done! -- vertices')
        measure_list[indep] = {
            # low-level QM
            'overlap': calculate_overlap_1st(M),

            # middle-level QM
            'outlying': np.sum(edge_length > cut_off) / len(df),
            'skewed': max(1 - cut_off * (1 - skewed), 0),
            'sparse': max(min(q90 * cut_off, 1), 0),
            'striated': striated,
            'stringy': max(edge_length) / np.sum(edge_length),
            'monotonic': np.abs(np.polyfit(M.index, M[M.columns[0]].astype(float), 1)[0])
        }
        # print('Done!')
        # print(measure_list[indep])
    return measure_list


def scagnostic_2nd(df, dtype_col, dtypes):
    measure_list = {}
    # low-level perception-related quality metrics, from https://ieeexplore.ieee.org/document/7864468
    # middle-level pattern-driven quality metrics, from https://www.cs.uic.edu/~tdang/file/ScagExplorer.pdf
    for indep_num, indep in enumerate(df.columns):
        for dep_num, dep in enumerate(df.columns):
            if (indep_num <= dep_num) | ('row' in dtypes[indep]) | ('row' in dtypes[dep]):
                continue
            # print('Working on', indep, ' and ', dep)
            # sampling (n = 500) with the same distribution, and return a distance matrix to M
            M, M_pdist = distributed_sampling(df, indep, dep, dtype_col, dtypes)

            # construct the minimal spanning tree
            edge_list = Minimum_Spanning_Tree(squareform(M_pdist))
            edge_length = edge_calculate(M, edge_list)
            # print('Done! -- Tree')

            q25 = np.quantile(edge_length, 0.25)
            q75 = np.quantile(edge_length, 0.75)
            cut_off = q75 - 1.5 * (q75 - q25)
            if cut_off < 0:
                cut_off = abs(cut_off)
            q50 = np.quantile(edge_length, 0.5)
            q90 = np.quantile(edge_length, 0.9)
            q10 = np.quantile(edge_length, 0.1)
            skewed = (q90 - q50) / max((q90 - q10), 0.0001)
            vertices_striated, vertices = vertice_striated(M, edge_list)
            if len(vertices) == 0:
                striated = 1
            else:
                striated = len(vertices_striated) / len(vertices)
            # print('Done! -- vertices')

            measure_list[indep + '.' + dep] = {
                # low-level QM
                'overlap': calculate_overlap(M),

                # middle-level QM
                'outlying': np.sum(edge_length > cut_off) / len(df),
                'skewed': max(1 - cut_off * (1 - skewed), 0),
                'sparse': max(min(q90 * cut_off, 1), 0),
                'striated': striated,
                'stringy': max(edge_length) / np.sum(edge_length),
                'monotonic': pearsonr(M.iloc[:, 0], M.iloc[:, 1])[0] ** 2
            }
            # print('Done!')
            # print(measure_list[indep + '.' + dep])
    return measure_list


def identify_task_figure(scag_1st, scag_2nd, df):
    fig_dic = {'Correlation': [], 'Anomalies': [], 'Clusters': [], 'Distribution': [], 'Range': []}
    # 0: Correlation, 1st: Bar, 2nd: Heatmap > Violin2 > Scatter
    #       Monotonic, Stringy, Outlying (rev)
    for fig in scag_2nd:
        if (scag_2nd[fig]['monotonic'] > 0.3) & (scag_2nd[fig]['stringy'] > 0.1) & \
                (scag_2nd[fig]['outlying'] < 0.3):
            fig_dic['Correlation'].append(fig)

    # 1: Anomalies, 1st: Box, 2nd: Scatter
    #       Outlying, Monotonic (rev)
    for fig in scag_1st:
        if scag_1st[fig]['outlying'] > 0.03:
            fig_dic['Anomalies'].append(fig)
    for fig in scag_2nd:
        if (scag_2nd[fig]['outlying'] > 0.03) & (scag_2nd[fig]['monotonic'] < 0.3):
            fig_dic['Anomalies'].append(fig)

    # 2: Clusters, 1st: Density, 2nd: Scatter
    #       Skewed, Outlying (rev), Striated, Overlapping
    for fig in scag_1st:
        if (scag_1st[fig]['skewed'] > 0.5) & (scag_1st[fig]['outlying'] < 0.1) & \
                (scag_1st[fig]['striated'] > 0.3) & (scag_1st[fig]['overlap'] > 0.3):
            fig_dic['Clusters'].append(fig)
    for fig in scag_2nd:
        if (scag_2nd[fig]['skewed'] > 0.5) & (scag_2nd[fig]['outlying'] < 0.1) & \
                ((len(df[fig.split('.')[0]].unique()) != 2) | (len(df[fig.split('.')[1]].unique()) != 2)):
            fig_dic['Clusters'].append(fig)

    # 3: Distribution, 1st: Density, 2nd: Violin2 > Scatter
    #       Outlying (rev)
    for fig in scag_1st:
        if scag_1st[fig]['outlying'] < 0.03:
            fig_dic['Distribution'].append(fig)
    for fig in scag_2nd:
        if (scag_2nd[fig]['outlying'] < 0.03) & \
                ((len(df[fig.split('.')[0]].unique()) != 2) | (len(df[fig.split('.')[1]].unique()) != 2)):
            fig_dic['Distribution'].append(fig)

    # 4: Range, 1st: Violin_1st, 2nd: Heatmap > Violin2 > Scatter
    #       Outlying (rev), Monotonic (rev)
    for fig in scag_1st:
        if (scag_1st[fig]['outlying'] < 0.09) & (scag_1st[fig]['monotonic'] < 0.3):
            fig_dic['Range'].append(fig)
    for fig in scag_2nd:
        if (scag_2nd[fig]['outlying'] < 0.09) & (scag_2nd[fig]['monotonic'] < 0.3) & \
                ((len(df[fig.split('.')[0]].unique()) != 2) | (len(df[fig.split('.')[1]].unique()) != 2)):
            fig_dic['Range'].append(fig)

    return fig_dic


def map_task_2_plot(df, task_fig, dtypes, dtype_col):
    tasklist = {'Correlation': [], 'Anomalies': [], 'Clusters': [], 'Distribution': [], 'Range': []}
    # Figures available: Bar, Density (smoothed bar graph), scatter, heatmap (chart)
    # 0: Correlation, 1st: Bar, 2nd: Heatmap > Violin2 > Scatter
    # 1: Anomalies, 1st: Box, 2nd: Scatter
    # 2: Clusters, 1st: Density, 2nd: Scatter
    # 3: Distribution, 1st: Density, 2nd: Violin2 > Scatter
    # 4: Range, 1st: Violin_1st, 2nd: Heatmap > Violin2 > Scatter
    for task_num in range(5):
        for task in task_fig[tasks[task_num]]:
            if '.' in task:
                col1 = task.split('.')[0]
                col2 = task.split('.')[1]
                if (task_num in [0, 4]) & (col1 not in dtype_col[0]) & (col2 not in dtype_col[0]) & \
                        is_categorical(df[col1]) & is_categorical(df[col2]):
                    if len(dtypes[col1]['category']) > len(dtypes[col2]['category']):
                        tasklist[tasks[task_num]].append(['heatmap', [col1, col2]])
                    else:
                        tasklist[tasks[task_num]].append(['heatmap', [col2, col1]])
                elif (task_num in [0, 3, 4]) & (col1 not in dtype_col[0]) & (col2 in dtype_col[0]) & \
                        is_categorical(df[col1]) & is_numerical(df[col2]):
                    tasklist[tasks[task_num]].append(['violin2', [col1, col2]])
                elif (task_num in [0, 3, 4]) & (col1 in dtype_col[0]) & (col2 not in dtype_col[0]) & \
                        is_categorical(df[col2]) & is_numerical(df[col1]):
                    tasklist[tasks[task_num]].append(['violin2', [col2, col1]])
                else:
                    if ((is_numerical(df[col1])) | (is_categorical(df[col1]))) & \
                            ((is_numerical(df[col2])) | (is_categorical(df[col2]))):
                        tasklist[tasks[task_num]].append(['scatter', [col1, col2]])
            elif (is_numerical(df[task])) | (is_categorical(df[task])):
                if (task_num == 1) & is_numerical(df[task]):
                    tasklist[tasks[task_num]].append(['box', [task]])
                elif (task_num == 4) & is_numerical(df[task]):
                    tasklist[tasks[task_num]].append(['violin1', [task]])
                elif (task_num in [2, 3]) & is_numerical(df[task]):
                    tasklist[tasks[task_num]].append(['density', [task]])
                else:
                    tasklist[tasks[task_num]].append(['bar', [task]])
    return tasklist


def main(working_dir, file_name, task):
    # file_path = '/Users/haofan/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/22Spring/AdViz/VizRecom'
    # df = pd.read_csv(os.path.join(file_path, '300k.csv'), low_memory=False)
    # df = pd.read_csv(os.path.join(file_path, 'heart.csv'))
    # df = pd.read_csv(os.path.join(file_path, 'movies.csv'))
    # df = pd.read_csv(os.path.join(file_path, 'SpotifyTop100.csv'))
    # df = pd.read_csv(os.path.join(file_path, 'combinedata.csv'))
    # working_dir = file_path + '/result'
    path = os.path.join(working_dir, file_name)
    df = pd.read_csv(path, low_memory=False)

    # judge the data type of each column, and store them as dictionary
    # dtypes: column-wise dictionary, store data type information
    # dtype_col: data type-wise dictionary, store the column names
    df = df.dropna()
    dtypes, dtype_col = judge_dtype(df)
    # if len(dtype_col[3]) > 0:
    #     print(dtype_col)

    # extract key features of each column, and store them in the dtypes dictionary
    dtypes = extract_features(df, dtypes)
    if 'cooc_1' in df.columns:
        col = []
        for i in range(1, 152):
            col.append('cooc_' + str(i))
        for i in df.columns:
            if 'cellId' in i:
                col.append(i)
        df = df.drop(columns=col)

    # extract scagnostics for 1st scatter plots
    scatter_1st = scagnostic_1st(df, dtype_col, dtypes)

    # extract scagnostics for 2nd scatter plots
    scatter_2nd = scagnostic_2nd(df, dtype_col, dtypes)

    # task-specific rules
    task_list = identify_task_figure(scatter_1st, scatter_2nd, df)
    task_fig = map_task_2_plot(df, task_list, dtypes, dtype_col)

    for f in os.listdir(working_dir):
        if f.endswith("png"):
            os.remove(os.path.join(working_dir, f))
    address = []
    col_used = []
    if len(task_list[task]) > 0:
        for num, fig in enumerate(task_fig[task]):
            file_path = os.path.join(working_dir, fig[0] + task_list[task][num] + '.png')
            if len(fig[1]) == 1:
                single_column_function[fig[0]](title[fig[0]] + 'for ' + fig[1][0], list(df[fig[1][0]]), file_path)
                plt.close('all')
            elif len(fig[1]) == 2:
                double_column_function[fig[0]](title[fig[0]] + 'between ' + fig[1][0] + ' and ' + fig[1][1],
                                               fig[1][0], fig[1][1], list(df[fig[1][0]]), list(df[fig[1][1]]),
                                               file_path)
                plt.close('all')
            address.append(file_path)
            for col in fig[1]:
                if col not in col_used:
                    col_used.append(col)
    col_unused = []
    count_col_df = len(df)
    for col in df.columns:
        if col not in col_used:
            count_col_distinct = len(df[col].unique())
            col_unused.append([col, count_col_distinct, count_col_df, count_col_distinct / count_col_df])

    for i in range(0, 5):
        for t in task_fig[tasks[i]]:
            if 'violin' in t[0]:
                count_task_fig[tasks[i]]['violin'] += 1
            else:
                count_task_fig[tasks[i]][t[0]] += 1

    return address, col_unused
