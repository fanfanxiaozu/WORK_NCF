import pandas as pd
import numpy as np
import json

if __name__ == '__main__':
    with open("Data/Train.json") as train_file:
        data = json.load(train_file)
    df = pd.DataFrame.from_dict(data)
    df = df[['user_id', 'click_article_id', 'ratings']]
    print df
    np.savetxt("Data/ecnu.train.rating", df.values, fmt='%d', delimiter='\t')

    with open("Data/Test.json") as train_file:
        data = json.load(train_file)
    df = pd.DataFrame.from_dict(data)
    df = df[['user_id', 'click_article_id']]
    print df
    np.savetxt("Data/ecnu.test.rating", df.values, fmt='%d', delimiter='\t')
