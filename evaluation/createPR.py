#   =====================================================================
#   Copyright (C) 2022  Stefan Schubert, stefan.schubert@etit.tu-chemnitz.de
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   =====================================================================
# 
import numpy as np


def createPR(S, GThard, GTsoft):
    GT = GThard.astype('bool')  # ensure logical-datatype
    GTsoft = GTsoft.astype('bool')
    S[GTsoft & ~GT] = S.min()

    # init precision and recall vectors
    R = [0, ]
    P = [1, ]

    # select start and end treshold
    startV = S.max()  # start-value for treshold
    endV = S.min()  # end-value for treshold

    # iterate over different thresholds
    for i in np.linspace(startV, endV, 100):
        B = S >= i  # apply threshold

        TP = np.count_nonzero(GT & B)  # true positives
        FN = np.count_nonzero(GT & (~B))  # false negatives
        FP = np.count_nonzero((~GT) & B)  # false positives

        P.append(TP / (TP + FP))  # precision
        R.append(TP / (TP + FN))  # recall

    return P, R


##### MAIN FOR PLACE RECOGNITION #####
if __name__ == '__main__':
    from scipy.io import loadmat
    from matplotlib import pyplot as plt
    plt.ion()

    # ground truth
    GT = np.eye(288)

    # load descriptors
    D_summer = loadmat('summer.mat')['D']
    D_winter = loadmat('winter.mat')['D']

    # compute distance matrix with cosine distance
    DD = 1 - np.matmul(D_summer, D_winter.transpose())

    # compute precision recall
    P, R = createPR(DD, np.eye(288))

    # vis
    print('avgP = ', np.trapz(P, R))
    plt.plot(R, P)
    plt.draw()