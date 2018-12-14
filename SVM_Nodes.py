# Support Vector Machine Classification (Node Flooding)

# Part A - Data Preparation

# Import the necessary libraries
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

# Set the working directory (set to directory containing the dataset)
os.chdir('C:\\Users\Brad\Desktop\Briefcase\Personal\GeorgiaTechMasters\CS7641_MachineLearning\Homework\Homework1')

# Import the dataset and collect some high-level information on it
dataset = pd.read_csv('NodeFlooding.csv')
print ("Dataset Length = ", len(dataset))
print ("Dataset Shape = ", dataset.shape)
print (dataset.head())

# Break up the dataset into X and Y components
X = dataset.iloc[:, [19, 1, 2, 4, 6, 7, 16, 17, 18, 20]].values
Y = dataset.iloc[:, 21].values
print(X[:10, :])
print(Y[:10])

# Encode the categorical data
# Encode the Independent variables
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()
X_Headers = np.array(['NodeStatus_B', 'NodeStatus_NB', 'NodeStatus_PNB',
                      'UtilBandwRate', 'PacketDropRate', 'AvgDelay_perSec',
                      'PctLostByteRate', 'PacketRecRate', '10RunAvgDropRate',
                      '10RunAvgBandwUse', '10RunDelay', 'FloodStatus'])
print(X_Headers)
print(X[:10, :])

# Encode the dependent variable
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)
Y_Results = np.array(['0=Block', '1=NB-No_Block', '2=NB-Wait', '3=No_Block'])
print(Y_Results)
print(Y[:10])

# Split the dataset into the Training set and Test set (25% test)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.25,
                                                    random_state = 0)

# Part B - Run SVM model on the training data

# Determine the accuracy over a variety of SVM kernel options via the
# Training set
accuracy = []
kernels = ['linear', 'poly', 'rbf']
for kernel in kernels:
    if kernel == 'linear':
        classifier = SVC(kernel = kernel, random_state = 0)
        scores = cross_val_score(classifier, X_train, y_train, cv=10)
        accuracy.append(np.mean(scores))
    else:
        for i in range(2, 3, 1):
            classifier = SVC(kernel = kernel, degree = i, random_state = 0)
            scores = cross_val_score(classifier, X_train, y_train, cv=10)
            accuracy.append(np.mean(scores))
kern_options = ['Linear', 'Poly-2', 'RBF-2']
plt.plot(kern_options, accuracy)
plt.xlabel('Kernal Options')
plt.ylabel('Accuracy')
plt.title('Accuracy by Kernel Option')
plt.grid(True)
plt.show()
# Maximum accuracy at the 2nd degree polynomial option

# Part C - Make predictions on the test data based on training model chosen

# Redo SVM classifier with the Poly 2nd degree kernel
classifier = SVC(kernel = 'poly', degree = 2, random_state = 0)
scores = cross_val_score(classifier, X_train, y_train, cv=10)
print('Mean = ', np.mean(scores))
# Based on cross-validation, should predict with 77.2% accuracy

# Make predictions on the test data and calculate the Confusion Matrix
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(Y_Results)
print(cm)
print('Accuracy = ', accuracy_score(y_test, y_pred))
# Based on the test data, model predicts with 78.8% accuracy
# Misclassifies several between "NB-No Block" and "NB-Wait"
# Misclassifies a few between Block and No Block

# Part D - Determine model performance over several training/test splits

# Measure model accuracy over a variety of test set sizes
train = []
test = []
splits = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
for split in splits:
    # Split the dataset into the Training set and Test set varying test set size
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 1 - split,
                                                        random_state = 0)
    # Use classifier parameters that have been pre-determined
    classifier = SVC(kernel = 'linear', random_state = 0)
    classifier.fit(X_train, y_train)
    train.append(1 - classifier.score(X_train, y_train))
    test.append(1 - classifier.score(X_test, y_test))

# Graph results
plt.plot(splits, train, color='blue', label='Training Set')
plt.plot(splits, test, color='orange', label='Test Set')
plt.legend()
plt.xlabel('Training Size Pct')
plt.axes()
plt.ylabel('Error Rate')
plt.title('Error Rate vs Training Size')
plt.grid(b = True, which = 'both')
plt.show()
# Training error rate degrades with test error rate as training size declines.
# Test error rate degrades faster than training error rate with decreasing training size
