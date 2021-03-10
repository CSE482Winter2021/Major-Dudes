from sklearn.kernel_approximation import RBFSampler
import random, os, json
import numpy as np
from utils import constants
CENSUS_OUTPUT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')


class ORCA_Rate_Model:
    def __init__(self, d):
        self.W = None
        self.dimensions = d
        self.kernel = RBFSampler(gamma=1, n_components=d, random_state=1)

    def PHI(L):
        phi_i = np.array(self.kernel.fit_transform(L))
        phi = np.zeros((1, self.d))
        for i in phi_i:
            phi += i
        return np.array(phi[0] / self.d)
     
    def train(X, y):
        """
        X: list of Locations which are lists of samples, vectors of demographics
        y: ORCA rate for each location
        """
        phi_arr = []
        for L in X:
            phi_arr.append(PHI(L, 200))
        phi_arr = np.array(phi_arr)
        inv = np.linalg.pinv(phi_arr)
        self.W = np.matmul(inv, y)
    
    def predict(X):
        """
        X must be [[ demographics ]]
        """
        if self.W:
            return np.matmul(self.kernel.fit_transform(X), self.W)
        else:
            return None


# for each tract, set phi[tract] = rbf.fit_transform(tensor[tract])
# L_0 = [[1,5,2,0,12], [2,4,1,20,1]]
# L_1 = [[1,3,2,5,4], [7,3,2,10,6]]
# # L_2 = [[1,3,2,5,4], [7,3,2,10,6]]
# # L_3 = [[1,3,2,5,4], [7,3,2,10,6]]
# y = np.array([.23, .49])

# phi_arr = []
# phi_arr.append(PHI(L_0, 200))
# phi_arr.append(PHI(L_1, 200))
# phi_arr = np.array(phi_arr)

# inv = np.linalg.pinv(phi_arr)
# W = np.matmul(inv, y)

# kernel = RBFSampler(gamma=1, n_components=200, random_state=1)
# print(np.matmul(kernel.fit_transform([[1,5,2,0,12]]), W))

def get_training_data():
    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_to_demographics.json', 'r') as f:
        tr_demo = json.load(f)

    num_tracts = len(tr_demo)
    sample_size = 5000
    num_dim = 5
    training_data = np.zeros((num_tracts, sample_size, num_dim))
    i = 0
    for tract_no in tr_demo:
        tract = tr_demo[tract_no]
        p_gender = [
            tract['gender'][0] / sum(tract['gender']), 
            tract['gender'][1] / sum(tract['gender'])
        ]
        p_age = [
            tract['age'][0] / sum(tract['age']),
            tract['age'][1] / sum(tract['age']),
            tract['age'][2] / sum(tract['age']),
            tract['age'][3] / sum(tract['age']),
            tract['age'][4] / sum(tract['age']),
            tract['age'][5] / sum(tract['age']),
            tract['age'][6] / sum(tract['age']),
            tract['age'][7] / sum(tract['age']),
            tract['age'][8] / sum(tract['age']),
            tract['age'][9] / sum(tract['age']),
            tract['age'][10] / sum(tract['age']),
            tract['age'][11] / sum(tract['age']),
            tract['age'][12] / sum(tract['age']),
            tract['age'][13] / sum(tract['age']),
            tract['age'][14] / sum(tract['age']),
            tract['age'][15] / sum(tract['age']),
            tract['age'][16] / sum(tract['age']),
            tract['age'][17] / sum(tract['age']),
            tract['age'][18] / sum(tract['age']),
            tract['age'][19] / sum(tract['age']),
            tract['age'][20] / sum(tract['age']),
            tract['age'][21] / sum(tract['age']),
            tract['age'][22] / sum(tract['age'])
        ]
        p_age[22] = 1 - (sum(p_age) - p_age[22]) 
        if p_age[22] < 0:
            p_age[22] = 0
        p_race = [
            (tract['age'][0] + tract['age'][6])/ sum(tract['race']),
            (tract['age'][1] + tract['age'][7])/ sum(tract['race']),
            (tract['age'][2] + tract['age'][8])/ sum(tract['race']),
            (tract['age'][3] + tract['age'][9])/ sum(tract['race']),
            (tract['age'][4] + tract['age'][10])/ sum(tract['race']),
            (tract['age'][5] + tract['age'][11])/ sum(tract['race'])
        ]
        p_race[5] = 1 - (sum(p_race) - p_race[5])
        p_income = [
            tract['income'][0] / sum(tract['income']),
            tract['income'][1] / sum(tract['income']),
            tract['income'][2] / sum(tract['income']),
            tract['income'][3] / sum(tract['income']),
            tract['income'][4] / sum(tract['income']),
            tract['income'][5] / sum(tract['income'])
        ]
        p_income[5] = 1 - (sum(p_income) - p_income[5])
        p_disability = [
            0,
            tract['disability'][0] / tract['population'],
            tract['disability'][1] / tract['population']
        ]
        p_disability[0] = 1 - (p_disability[1] + p_disability[2])

        for j in range(sample_size):
            sample = []
            sample.append(np.random.choice(len(p_gender), 1, replace=False, p=p_gender)[0])
            sample.append(np.random.choice(len(p_age), 1, replace=False, p=p_age)[0])
            sample.append(np.random.choice(len(p_race), 1, replace=False, p=p_race)[0])
            sample.append(np.random.choice(len(p_income), 1, replace=False, p=p_income)[0])
            sample.append(np.random.choice(len(p_disability), 1, replace=False, p=p_disability)[0])
            training_data[i][j] = sample
        i += 1

    return training_data, y
