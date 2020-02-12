import pandas as pd
from numpy import *

import pytest

class SizeRecommender:
    def  __init__(self, path):
        self.f = pd.ExcelFile(path)
    def _recommend(self, df, param_dic, required_param_lst):
        param_name_lst, idx_lst = self._commonPartRecommend(df, param_dic, required_param_lst)
        if len(idx_lst) == 0:
            param_name_lst, idx_lst = self._mostFrequentRecommend(df, param_dic, required_param_lst)

        # extract most frequent value
        a,b = unique(idx_lst, return_counts=True)
        best_dic = {}
        all_dic = {}
        for p in required_param_lst:
            best_dic[p] = df.loc[a[b.argmax()]][p]
        for name, idx in zip(param_name_lst, idx_lst):
            tmp_dic = {}
            for p in required_param_lst:
                tmp_dic[p] = df.iloc[idx][p]
            all_dic[name] = tmp_dic

        return {"best_dic": best_dic, "all_dic": all_dic}
        
    def _commonPartRecommend(self, df, param_dic, required_param_lst):
        c_max = where(["max" in x for x in df.columns ])[0][-1]
        idx_lst = []
        param_name_lst = []
        for i in range(0, c_max+1, 2):
            n_min, n_max = df.columns[i:i+2]
            df = df[(df[n_min] <= param_dic[n_min.strip("_min")]) == (df[n_max] > param_dic[n_min.strip("_min")])]
            if df.shape[0]:
                param_name_lst += [n_min.strip("_min")]
        if df.shape[0]:
            idx_lst += [df.index[0]] * len(param_name_lst)

        return param_name_lst, idx_lst
            

    def _mostFrequentRecommend(self, df, param_dic, required_param_lst):
        c_max = where(["max" in x for x in df.columns ])[0][-1]
        idx_lst = []
        param_name_lst = []
        for i in range(0, c_max+1, 2):
            n_min, n_max = df.columns[i:i+2]
            result = df[(df[n_min] <= param_dic[n_min.strip("_min")]) == (df[n_max] > param_dic[n_min.strip("_min")])]
            if result.shape[0]:
                idx_lst += [result.index[0]]
                param_name_lst += [n_min.strip("_min")]
        return param_name_lst, idx_lst
    
            
    def _get_df(self, sheet_name):
        df = self.f.parse(sheet_name)
        return df
        
    def recommend(self, param_dic, sheet_name, required_param_lst):
        df = self._get_df(sheet_name)
        return self._recommend(df, param_dic, required_param_lst)
    
        
@pytest.fixture()
def data_male():
    param_dic = {"Height": 170, "Neck":39, "Chest": 90, "Waist":80, "Hip": 90}
    ret = {"param_dic": param_dic}
    return ret

def test_male(data_male):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    truth_value = {"best_dic": {"size": "M"},
                   "all_dic": {"Height": {"size":"M"}, "Neck": {"size": "M"}, "Chest": {"size":"M"}, "Waist": {"size":"M"}, "Hip": {"size":"M"}}
                   }
    assert sr.recommend(data_male["param_dic"], "male", ["size"]) == truth_value

@pytest.fixture()
def data_male2():
    param_dic = {"Height": 160, "Neck":39, "Chest": 100, "Waist":110, "Hip": 98}
    ret = {"param_dic": param_dic}
    return ret

def test_male2(data_male2):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    truth_value = {"best_dic": {"size": "L"},
                   "all_dic": {"Height": {"size":"XS"}, "Neck": {"size": "M"}, "Chest": {"size":"L"}, "Waist": {"size":"3XL"}, "Hip": {"size":"L"}}
                   }
    assert sr.recommend(data_male2["param_dic"], "male", ["size"]) == truth_value

@pytest.fixture()
def data_female():
    param_dic = {"Height": 163, "Chest": 88, "Waist":72, "Hip": 99}
    ret = {"param_dic": param_dic}
    return ret

def test_female(data_female):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    truth_value = {"best_dic": {"size": "L"},
                    "all_dic": {"Height": {"size":"L"}, "Chest": {"size":"L"}, "Waist": {"size":"L"}, "Hip": {"size":"L"}}
                   }
    assert sr.recommend(data_female["param_dic"], "female", ["size"]) == truth_value

@pytest.fixture()
def data_female2():
    param_dic = {"Height": 152, "Chest": 90, "Waist":70, "Hip": 115}
    ret = {"param_dic": param_dic}
    return ret

def test_female2(data_female2):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    truth_value = {"best_dic": {"size": "L"},
                    "all_dic": {"Height": {"size":"XS"}, "Chest": {"size":"L"}, "Waist": {"size":"L"}, "Hip": {"size":"3XL"}}
                   }
    assert sr.recommend(data_female2["param_dic"], "female", ["size"]) == truth_value
