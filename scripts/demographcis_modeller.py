from sklearn.kernel_approximation import RBFSampler
import random, os, json, csv
import numpy as np
from utils import constants
CENSUS_OUTPUT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')


class ORCA_Rate_Model:
    def __init__(self, d):
        self.W = None
        self.dimensions = d
        self.kernel = RBFSampler(gamma=1, n_components=d, random_state=1)

    def PHI(self, L):
        phi_i = np.array(self.kernel.fit_transform(L))
        phi = np.zeros((1, self.dimensions))
        for i in phi_i:
            phi += i
        return np.array(phi[0] / self.dimensions)
     
    def train(self, X, y):
        """
        X: list of Locations which are lists of samples, vectors of demographics
        y: ORCA rate for each location
        """
        phi_arr = []
        for L in X:
            phi_arr.append(self.PHI(L))
        phi_arr = np.array(phi_arr)
        inv = np.linalg.pinv(phi_arr)
        y = np.asarray(y, dtype='float64')
        # print(inv.shape)
        # print(y.shape)
        self.W = np.matmul(inv, y)
    
    def predict(self, X):
        """
        X must be [[ demographics ]]
        """
        # if self.W != None:
        return np.matmul(self.kernel.fit_transform([X]), self.W)
        # else:
        #     return None


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
    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_to_demographics_v2.json', 'r') as f:
        tr_demo = json.load(f)
    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_rates.csv', 'r') as f:
        tract_rates = list(csv.reader(f))
    tract_rates = {tract_rates[idx][0] : tract_rates[idx][1] for idx in range(len(tract_rates))}
    training_data = [] #np.zeros((num_tracts, sample_size, num_dim))
    y = []
    for tract_no in tr_demo:
        if str(int(tract_no)) not in tract_rates:
            continue
        tract = tr_demo[tract_no]
        p_gender = [
            round(tract['gender'][1] / tract['gender'][0], 5), 
            round(tract['gender'][2] / tract['gender'][0], 5)
        ]
        # print(sum(p_gender))
        p_age = [
            round(tract['age'][1] / tract['age'][0], 5),
            round(tract['age'][2] / tract['age'][0], 5),
            round(tract['age'][3] / tract['age'][0], 5),
            round(tract['age'][4] / tract['age'][0], 5),
            round(tract['age'][5] / tract['age'][0], 5),
            round(tract['age'][6] / tract['age'][0], 5),
            round(tract['age'][7] / tract['age'][0], 5),
            round(tract['age'][8] / tract['age'][0], 5),
            round(tract['age'][9] / tract['age'][0], 5),
            round(tract['age'][10] / tract['age'][0], 5),
            round(tract['age'][11] / tract['age'][0], 5),
            round(tract['age'][12] / tract['age'][0], 5),
            round(tract['age'][13] / tract['age'][0], 5),
            round(tract['age'][14] / tract['age'][0], 5),
            round(tract['age'][15] / tract['age'][0], 5),
            round(tract['age'][16] / tract['age'][0], 5),
            round(tract['age'][17] / tract['age'][0], 5),
            round(tract['age'][18] / tract['age'][0], 5),
            round(tract['age'][19] / tract['age'][0], 5),
            round(tract['age'][20] / tract['age'][0], 5),
            round(tract['age'][21] / tract['age'][0], 5),
            round(tract['age'][22] / tract['age'][0], 5)
        ]
        p_age.append(1 - sum(p_age))
        if p_age[22] < 0:
            idx = p_age.index(max(p_age))
            v = -p_age[22]
            p_age[22] = 0
            p_age[idx] -= v

        # print(sum(p_age))
        p_race = [
            round(tract['race'][1] / tract['race'][0], 5),
            round(tract['race'][2] / tract['race'][0], 5),
            round(tract['race'][3] / tract['race'][0], 5),
            round(tract['race'][4] / tract['race'][0], 5),
            round(tract['race'][5] / tract['race'][0], 5),
            round(tract['race'][6] / tract['race'][0], 5),
        ]
        p_race.append(1 - sum(p_race))
        if p_race[6] < 0:
            idx = p_race.index(max(p_race))
            v = -p_race[6]
            p_race[6] = 0
            p_race[idx] -= v
        # print(sum(p_race))
        # print(tract['income'])
        p_income = [
            tract['income'][1] / tract['income'][0],
            tract['income'][2] / tract['income'][0],
            tract['income'][3] / tract['income'][0],
            tract['income'][4] / tract['income'][0],
            tract['income'][5] / tract['income'][0],
            tract['income'][6] / tract['income'][0],
            tract['income'][7] / tract['income'][0],
            tract['income'][8] / tract['income'][0],
            tract['income'][9] / tract['income'][0],
            tract['income'][10] / tract['income'][0],
            tract['income'][11] / tract['income'][0],
            tract['income'][12] / tract['income'][0],
            tract['income'][13] / tract['income'][0],
            tract['income'][14] / tract['income'][0],
            tract['income'][15] / tract['income'][0]
        ]
        p_income.append(1 - sum(p_income))
        if p_income[15] < 0:
            idx = p_income.index(max(p_income))
            v = -p_income[15]
            p_income[15] = 0
            p_income[idx] -= v
            
        # print(sum(p_income))
        p_disability = [
            tract['disability'][1] / tract['disability'][0],
            tract['disability'][2] / tract['disability'][0]
        ]
        # print(sum(p_disability))
        tract_samples = []
        for j in range(sample_size):
            sample = []
            sample.append(int(np.random.choice(len(p_gender), 1, replace=False, p=p_gender)[0]))
            sample.append(int(np.random.choice(len(p_age), 1, replace=False, p=p_age)[0]))
            sample.append(int(np.random.choice(len(p_race), 1, replace=False, p=p_race)[0]))
            sample.append(int(np.random.choice(len(p_income), 1, replace=False, p=p_income)[0]))
            sample.append(int(np.random.choice(len(p_disability), 1, replace=False, p=p_disability)[0]))
            tract_samples.append(sample)
        training_data.append(tract_samples)
        y.append(tract_rates[str(int(tract_no))])
        # print(i, tract_no, tract_rates[str(int(tract_no))])
    to_json = [training_data, y]

    with open(f'{CENSUS_OUTPUT_DATA_DIR}/samples.json', 'w') as outfile:
        json.dump(to_json, outfile)
    return training_data, y

# (X, y) = get_training_data()
with open(f'{CENSUS_OUTPUT_DATA_DIR}/samples.json', 'r') as f:
    j = json.load(f)
X = j[0]
y = j[1]
m = ORCA_Rate_Model(200)
m.train(X, y)
print(m.predict([1,12,3,9,0]))
print(m.predict([1,9,2,1,0]))
print(m.predict([1,17,3,5,0]))
print(m.predict([1,4,8,9,0]))
print(m.predict([1,1,2,7,0]))
print(m.predict([0,7,3,13,0]))
