import pandas
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


def scale_data(data: pandas.DataFrame, name: list):
    x = data.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    res = pd.DataFrame(x_scaled, columns=min_max_scaler.get_feature_names_out(name))
    return res


def one_hot_encode(data: pandas.DataFrame, name: list):
    ohe = OneHotEncoder(dtype=int, sparse=False)
    x_scaled = ohe.fit_transform(data.to_numpy().reshape(-1, 1))
    # print(x_scaled)
    res = pd.DataFrame(x_scaled, columns=ohe.get_feature_names())
    return res


def label_data(data: pandas.DataFrame, names: list):
    x = data.values
    le = LabelEncoder()
    x_labeled = le.fit_transform(x)
    res = pd.DataFrame(x_labeled, columns=names)
    return res
def label_data_with_map(data: pandas.DataFrame, names: list):
    x = data.values
    le = LabelEncoder()
    x_labeled = le.fit_transform(x)
    res = pd.DataFrame(x_labeled, columns=names)
    le_name_mapping = dict(zip( le.transform(le.classes_),le.classes_))
    return res, le_name_mapping


def normalize_data(file_name: str, include: list, hot_one_enc: bool):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    data = pd.read_csv(file_name)
    # print((data.head(10)))
    # print(data.describe(include='all'))
    well = data['WELL']
    x_y = data[['X', 'Y']]
    dep_env = data['DEPOSITIONAL_ENVIRONMENT']
    lith_name = data['LITH_NAME']
    lith_c = data['LITH_CODE']
    data = data.drop(['WELL', 'X', 'Y', 'DEPOSITIONAL_ENVIRONMENT', 'LITH_NAME', 'LITH_CODE'], axis=1)

    x_y = scale_data(x_y, ['X', 'Y'])
    # print(x_y.head(10))
    lith_c,map_res= label_data_with_map(lith_c, ['LITH_CODE'])
    print(map_res)
    if hot_one_enc:
        lith_name = one_hot_encode(lith_name, [''])
        well = one_hot_encode(well, ['WELL'])
    else:
        lith_name = label_data(lith_name, ['LITH_NAME'])
        well= label_data(well, ['WELL'])
    dep_env= label_data(dep_env, [''])
    data = scale_data(data, ['MD', 'GR', 'RT', 'CN', 'DEN'])
    if 'WELL' in include:
        data = data.join(well)
    if 'X_Y' in include:
        data = data.join(x_y)
    if 'DEPOSITIONAL_ENVIRONMENT' in include:
        data = data.join(dep_env)
    return data, lith_c, map_res
    # print(well.head(10))
    # print(well.describe(include='all'))


def normalize_train_data(file_name: str, include: list, hot_one_enc: bool):
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    data = pd.read_csv(file_name)
    # print((data.head(10)))
    # print(data.describe(include='all'))
    well = data['WELL']
    x_y = data[['X', 'Y']]
    dep_env = data['DEPOSITIONAL_ENVIRONMENT']

    data = data.drop(['WELL', 'X', 'Y', 'DEPOSITIONAL_ENVIRONMENT', 'Id'], axis=1)

    x_y = scale_data(x_y, ['X', 'Y'])
    # print(x_y.head(10))

    well= label_data(well, ['WELL'])

    dep_env= label_data(dep_env, [''])
    data = scale_data(data, ['MD', 'GR', 'RT', 'CN', 'DEN'])
    if 'WELL' in include:
        data = data.join(well)
    if 'X_Y' in include:
        data = data.join(x_y)
    if 'DEPOSITIONAL_ENVIRONMENT' in include:
        data = data.join(dep_env)
    return data


def class_weights(file_name: str):
    data = pd.read_csv(file_name)
    lith_name = data['LITH_NAME']
    y = label_data(lith_name, ['LITH_NAME'])
    weights = {}
    freq = y['LITH_NAME'].value_counts().to_dict()
    print(freq)
    num_of_elems = y.shape[0]
    for key in freq.keys():
        weights[key] = num_of_elems / (13 * freq[key])
    print(weights)
    return weights

def digits_to_code(digits,map_res):
    codes = []
    for i in digits:
        codes.append(map_res[i])
    for i in range(0, len(codes)):
        codes[i] = int(codes[i])
    return codes
def get_lath_code():
    data = pd.read_csv("Train-dataset.csv")
    return data['LITH_CODE'].tolist()

def get_submission(model,map_res):
    x = normalize_train_data("Test-dataset.csv", include=['WELL', 'X_Y', 'DEPOSITIONAL_ENVIRONMENT'],
                                 hot_one_enc=False)
    print(map_res)
    ids = []
    out = model.predict(x)
    final = []
    for i in out:
        final.append(map_res[i])

    for i in range(1, 28998):
        ids.append(i)

    df = pd.DataFrame({
        'Id': ids, 'LITH_CODE': final
    })
    df.to_csv('submission.csv', index=False)

#x, y = normalize_data("Train-dataset.csv", include=['WELL','X_Y','DEPOSITIONAL_ENVIRONMENT'],hot_one_enc=False)
#print(x.head(1000))
#print(describe(include='all'))
#class_weights("Train-dataset.csv")
# out=normalize_train_data("Test-dataset.csv", include=['WELL','X_Y','DEPOSITIONAL_ENVIRONMENT'],hot_one_enc=False)
