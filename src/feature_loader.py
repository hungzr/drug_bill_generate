import numpy as np
import os
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVR, SVC
from sklearn.ensemble import RandomForestClassifier as RDF
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':
    # svr = SVR(gamma='scale', C=1e3, epsilon=0.02)
    brisque = r'D:\PycharmProjectCPU\CORE_NoRef_QualityEval\distortions\brisque'
    labels = []
    features = []
    refs = 0
    svmLabels = []
    for f in os.listdir(brisque)[1:]:
        if f.endswith('.npy') == True:
            data = np.load(os.path.join(brisque, f))
            count = []
            for idx, row in enumerate(data):
                if idx % 16 == 0:
                    refs += 1
                else:
                    features.append(row[2][0])
                    count.append(row[1])
                    svmLabels.append(int(row[0][-1:]))
                    if len(count) == 5:
                        lab = np.array(sorted(count))
                        lab = lab - np.min(lab)
                        lab = 2 * lab / np.max(lab)
                        lab = lab - 1
                        labels += list(- lab)
                        count =[]

    features = np.array(features)
    scaler = StandardScaler(0)

    X = scaler.fit_transform(features)

    labels = np.array(labels).T
    svmLabels = np.array(svmLabels).T

    C_range = 10. ** np.arange(-3, 8)
    gamma_range = 10. ** np.arange(-5, 4)

    param_grid = dict(gamma=gamma_range, C=C_range)

    # grid = GridSearchCV(SVC(), param_grid=param_grid, cv=5)
    # print("The best classifier is: ", grid.best_estimator_)
    clf = SVC(C=1000, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape='ovr', degree=3, gamma=.5, kernel='rbf',
        max_iter=-1, probability=True, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    clf.fit(X, svmLabels)
    pre = clf.predict(X[14000:])
    print(confusion_matrix(svmLabels[14000:], pre))