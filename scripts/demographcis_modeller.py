from sklearn.kernel_approximation import RBFSampler
import random
import numpy as np

# with open('../data/census_data/pipeline_output/tract_to_demographics.json', 'r') as f:
#     tr_demo = json.load(f)

# sample_size = 1000
# num_tracts = 3
# num_dim = 2
# tensor = np.zeros((num_tracts, sample_size, num_dim))
# for tract in tr_demo:
#     # need to calculate all the probabilities based on tract pop
#     # add one to every population smooth for the possibility that there is 0 probability of some demo existing 
#     # go through and create the sample matrix
#     for i in range(sample_size):
#         r = random.random()
#         if r < male_percent:
#             tensor[tract][i][0] = 0  # In this sample, index 0, gender = 0 to rep male

#             # scale each feature...
#             # disability
#             if r < no_disabilty_percent * male_percent:
#                 tensor[tract][i][1] = 0
#                 if
             
#             elif no_disabilty_percent * male_percent < r < one_disabilty_percent * male_percent:
#                 tensor[tract][i][1] = 1

#             else:
#                 tensor[tract][i][1] = 2
#         else:
#             tensor[tract][i][0] = 1


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
