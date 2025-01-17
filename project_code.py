# -*- coding: utf-8 -*-
"""project code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aHg8xYqWZqqxqarYv1vSv6bGZjO_KHv8
"""

import pandas as pd
import numpy as np
data = pd.read_csv("weatherAUS.csv")
data

import seaborn as sns
sns.heatmap(data.isnull(), cbar=False, cmap='PuBu')

data.dropna(inplace = True)

data.reset_index(inplace = True,drop = True)

data.shape

#data.groupby("RainTomorrow").count().iloc[1,0]

12427/(12427+43993)

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
tmp = data.select_dtypes(include=numerics)
tmp["RainTomorrow"]= data["RainTomorrow"]

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.pairplot(tmp, vars = tmp.columns[:4],hue="RainTomorrow")
plt.show()

sns.pairplot(tmp, vars = tmp.columns[4:8],hue="RainTomorrow")
plt.show()

sns.pairplot(tmp, vars = tmp.columns[8:12],hue="RainTomorrow")
plt.show()

sns.pairplot(tmp, vars = tmp.columns[12:16],hue="RainTomorrow")
plt.show()

sns.pairplot(tmp, vars = tmp.columns[16:17],hue="RainTomorrow")
plt.show()

data['Month'] = pd.to_datetime(data['Date']).dt.month

# We check the target distribution across our new feature
sns.countplot(x = 'Month', hue =  'RainTomorrow', orient = 'h', data = data)

plt.figure(figsize=(20, 10))
sns.countplot(y = 'Location', hue =  'RainTomorrow', orient = 'h', data = data)

sns.countplot(x = 'WindGustDir', hue =  'RainTomorrow', orient = 'h', data = data)

sns.countplot(x = 'RainToday', hue =  'RainTomorrow', orient = 'h', data = data)

# replace the string labels with 0 and 1 numbers:
data['RainToday'].replace({'No':0,'Yes':1},inplace = True)
data['RainTomorrow'].replace({'No':0,'Yes':1},inplace = True)

# encode categorical values
categorical = ['WindGustDir','WindDir9am','WindDir3pm','Location']
data = pd.get_dummies(data,columns = categorical,drop_first=True)

data.shape

data

data.select_dtypes(include=numerics).describe()

"""# NN"""

data.columns

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x = data.drop(labels = ['RainTomorrow','Date',"RISK_MM"],axis = 1)
y = data['RainTomorrow']
x = sc.fit_transform(x)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.4,random_state = 40)
x_test,x_validation,y_test,y_validation = train_test_split(x_test,y_test,test_size = 0.5,random_state = 40)

import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense

classifier = Sequential()

classifier.add(Dense(units = 30,kernel_initializer='uniform',activation = 'relu',input_dim = 88))
classifier.add(Dense(units = 30,kernel_initializer='uniform',activation = 'relu'))
classifier.add(Dense(units = 30,kernel_initializer='uniform',activation = 'relu'))
classifier.add(Dense(units = 1,activation='sigmoid',kernel_initializer='uniform'))

from keras.utils import plot_model
 plot_model(classifier, show_shapes=True, to_file='model.png')

print(classifier.summary())

classifier.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])

classifier.fit(x_train,y_train,epochs = 100,batch_size=10)

y_pred = classifier.predict_classes(x_test)
y_train_pred = classifier.predict_classes(x_train)
y_validation_pred = classifier.predict_classes(x_validation)

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
print('Training Accuracy ---->',accuracy_score(y_train,y_train_pred))
print('Testing Accuracy  ---->',accuracy_score(y_test,y_pred))
print('Validation Accuracy  ---->',accuracy_score(y_validation,y_validation_pred))

print(classification_report(y_train,y_train_pred))

print(confusion_matrix(y_train,y_train_pred))

print(classification_report(y_test,y_pred))

print(confusion_matrix(y_test,y_pred))

"""# DT"""

import sklearn.tree as st

model = st.DecisionTreeClassifier(max_depth=8)

model

model.fit(x_train, y_train)

y_pred_test = model.predict(x_test)
y_validation_test = model.predict(x_validation)
y_train_pred_dt = model.predict(x_train)

fi = model.feature_importances_

names = data.columns

fi[np.argsort(-fi)]

names[np.argsort(-fi)]

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
print(classification_report(y_train,y_train_pred_dt))

print(confusion_matrix(y_train,y_train_pred_dt))

print(classification_report(y_test,y_pred_test))

print(confusion_matrix(y_validation,y_validation_test))

"""# LR"""

from sklearn.linear_model import LogisticRegression as LR
lr = LR(C=3000,random_state=123)
lr.fit(x_train,y_train)
y_pred = lr.predict(x_test)
print(u"Confusion matrix",confusion_matrix(y_true=y_test,y_pred=y_pred))
lr.coef_

lr

y_test_pred_lr = lr.predict(x_test)
y_validation_pred_lr = lr.predict(x_validation)
print(classification_report(y_train,y_train_pred))
print(confusion_matrix(y_train,y_train))

print(classification_report(y_test,y_test_pred_lr))
print(confusion_matrix(y_test,y_test_pred_lr))

"""# Random forest"""

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators= 100, random_state=42)

rf.fit(x_train, y_train)

y_pred_test = rf.predict(x_test)
y_validation_test = rf.predict(x_validation)
y_train_pred_dt = rf.predict(x_train)


print(classification_report(y_train,y_train_pred_dt.round()))




print(classification_report(y_test,y_pred_test.round()))

