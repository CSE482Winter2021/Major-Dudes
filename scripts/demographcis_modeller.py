from sklearn.kernel_approximation import RBFSampler
import random
import os
import json
import csv
import math
import numpy as np
from tqdm import tqdm
from utils import constants
CENSUS_OUTPUT_DATA_DIR = os.path.join(
    constants.DATA_DIR, 'census_data', 'pipeline_output')


SAMPLE_SIZE = 15000

# TODO:
#   Can't use a Logistic Regression with continuous output (y).
#       Option: calculate W manually: W = pinv(phi_arr) * inverse_sigmoid(y),
#           But Motoya says that it’s not squared loss so it would not be robust.
#           Need a solution for this? More consultation with Motoya likely needed here
#   Split the sampling data into training and testing data (multiple times) to get % error
#       Current state of X given by CreateSamplesInputs.get_training_data is [ 295 x [ sample_size x 5 ] ]
#           that is 295 locations (tracts), so split into 245 training, 50 data (have to change d in model to be < num_locations, Motoya suggested 240)
#
# Assumptions to add to writeup:
#   Hyperparameter in our transform less than number of data points we have is okay here
#   ORCA rate / demographics can be represented by the approximation where d < (295, # of locations).
#       As data increases, this assumption is less restrictive.
#   Assumes independence in demographics. Need to report that this is something to improve on to make the model less biased.
#       Would need more data within one location - should inform in assignment 6 what kind of data we will need to get rid of this bias.
#       Sample number 15000 might be small, but we should report that this could be edited / tuned to make the model better (put this in report)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class ORCA_Rate_Model:
    def __init__(self, d):
        self.W = None
        self.dimensions = d
        self.kernel = RBFSampler(gamma=1, n_components=d, random_state=1)
        # might want to tune this to make better

    def PHI(self, L):
        phi_i = np.array(self.kernel.fit_transform(L))
        phi = np.zeros((1, self.dimensions))
        # sum up all 5000 vectors to make [d x 1] & divide by 5000 -> d x 1
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
        self.W = np.matmul(inv, y)

    def predict(self, X):
        """
        X must be [[ demographics ]]
        """
        y = np.matmul(self.kernel.fit_transform([X]), self.W)
        y = sigmoid(y)
        y *= 100
        return y


class CreateSamplesInputs:
    def __init__(self):  # Make d 290 since we have 295 tracts
        self.gender_size = 2
        self.age_size = 23
        self.race_size = 6
        self.income_size = 16
        self.disability_size = 2
        self.sample_size = 15000

    def get_training_data(self):
        with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_to_demographics_v2.json', 'r') as f:
            tr_demo = json.load(f)
        with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_rates.csv', 'r') as f:
            tract_rates = list(csv.reader(f))
        tract_rates = {tract_rates[idx][0] : tract_rates[idx][1] for idx in range(len(tract_rates))}
        training_data = []
        y = []
        for tract_no in tqdm(tr_demo):

            rates_key = str(int(tract_no))

            if rates_key not in tract_rates:
                supertr = int((int(tract_no) - (int(tract_no) % 100)) / 100)
                if str(int(supertr)) not in tract_rates:
                    continue
                else:
                    rates_key = str(int(supertr))

            tract = tr_demo[tract_no]
            p_gender = [
                round(tract['gender'][1] / tract['gender'][0], 5),
                round(tract['gender'][2] / tract['gender'][0], 5)
            ]

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

            p_race = [
                round(tract['race'][1] / tract['race'][0], 5),
                round(tract['race'][2] / tract['race'][0], 5),
                round(tract['race'][3] / tract['race'][0], 5),
                round(tract['race'][4] / tract['race'][0], 5),
                round(tract['race'][5] / tract['race'][0], 5)
            ]
            p_race.append(1 - sum(p_race))
            if p_race[5] < 0:
                idx = p_race.index(max(p_race))
                v = -p_race[5]
                p_race[5] = 0
                p_race[idx] -= v

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

            p_disability = [
                tract['disability'][1] / tract['disability'][0],
                tract['disability'][2] / tract['disability'][0]
            ]

            tract_samples = []
            for j in range(self.sample_size):
                sample = []
                # Assumes independence. Need to report that this is something to improve on to make the model less biased.
                # Would need more data within one location - should inform in assignment 6 what kind of data we will need to get rid of this bias.
                # Sample number 5000 might be small, but we should report that this could be edited to make the model better (put this in report)
                sample.append((int(np.random.choice(len(p_gender), 1, replace=False, p=p_gender)[0])) / (len(p_gender) - 1))
                sample.append((int(np.random.choice(len(p_age), 1, replace=False, p=p_age)[0])) / (len(p_age) - 1))
                sample.append((int(np.random.choice(len(p_race), 1, replace=False, p=p_race)[0])) / len(p_race))
                sample.append((int(np.random.choice(len(p_income), 1, replace=False, p=p_income)[0])) / (len(p_income) - 1))
                sample.append((int(np.random.choice(len(p_disability), 1, replace=False, p=p_disability)[0])) / (len(p_disability) - 1))
                tract_samples.append(sample)
            training_data.append(tract_samples)
            y.append(tract_rates[rates_key])
        return training_data, y


    # Params:
    #   gender: {0, 1} ~ {Male, Female}
    #   age: {0 - 22} ~ {0-4, 5-9, 10-14, 15-17, 18-19, 20, 21, 22-24, 25-29, 30-34, 35-39, 40-44,
    #                   45-29, 50-54, 55-59, 60-61, 62-64, 65-66, 67-69, 70-74, 75-79, 80-84, 85+}
    #   race: {0 - 5} ~ {White, Black, Native, Asian, Pacific Islander, Other}
    #   income: {0 - 15} ~ {<10k, 10k-14999, 15k-19999, 20k-24999, 25k-29999, 30k-34999, 35k-39999,
    #                       40k-44999, 45k-49999, 50k-59999, 60k-74999, 75k-99999, 100k-124999,
    #                       125k-149999, 150k-199999, >200k}
    #   disability: {0, 1} ~ {disabled, not disabled}
    def createInput(self, gender, age, race, income, disability):
        return [(gender / (self.gender_size - 1)),
                    (age / (self.age_size - 1)),
                    (race / (self.race_size - 1)),
                    (income / (self.income_size - 1)),
                    (disability / (self.disability_size - 1))]


if __name__ == '__main__':
    i = CreateSamplesInputs()
    X, y = i.get_training_data()
    to_json = [X, y]
    with open(f'{CENSUS_OUTPUT_DATA_DIR}/samples.json', 'w') as outfile:
        json.dump(to_json, outfile)


# # (X, y) = get_training_data()
# if __name__ == '__main__':
#     get_training_data()
