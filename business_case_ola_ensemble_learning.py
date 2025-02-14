# -*- coding: utf-8 -*-
"""1 Business Case: OLA - Ensemble Learning

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18mUnUvz7LrTIINoxfcv5MXiuN0rdb9Tx
"""

# importing importent libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

!gdown https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/002/492/original/ola_driver_scaler.csv

# Loading the dataset

df = pd.read_csv('ola_driver_scaler.csv')

df.head(10)

df.info()

"""##**Define Problem Statement and perform Exploratory Data Analysis**"""

df.shape

df1 = df.copy()

df1.head()

df1.drop(columns=['Unnamed: 0'],inplace=True)

# conversion of categorical attributes to 'category'

#df1['Age'].astype('category')
df1['Gender'] = df1['Gender'].astype('category')
df1['City'] = df1['City'].astype('category')
df1['Education_Level'] = df1['Education_Level'].astype('category')
df1['Joining Designation'] = df1['Joining Designation'].astype('category')
df1['Grade'] = df1['Grade'].astype('category')
df1['Quarterly Rating'] = df1['Quarterly Rating'].astype('category')

# convering the DataTypes of the features which are incorrect

df1['MMM-YY'] = df1['MMM-YY'].astype('datetime64[ns]')
df1['Dateofjoining'] = df1['Dateofjoining'].astype('datetime64[ns]')
df1['LastWorkingDate'] = df1['LastWorkingDate'].astype('datetime64[ns]')

df1.describe()

df1.info()

df['Driver_ID'].duplicated()

#Missing values in our dataset

df1.isnull().sum()

"""##Univariate Analysis"""

# Count of Quarterly Rating

plt.figure(figsize=(5,4))
sns.countplot(x=df1['Quarterly Rating'],palette="Set2")
plt.title('Quarterly Rating')
plt.show()

# Ploting the age
plt.figure(figsize=(5,4))
sns.histplot(df1['Age'],bins=20,kde=True,palette='Set2')
plt.title('Age distribution')
plt.show()

# Male : 0, Female: 1
plt.figure(figsize=(5,4))
sns.countplot(x=df1['Gender'],palette='hls')
plt.title('Gender counts')
plt.show()

#Education level – 0 for 10+ ,1 for 12+ ,2 for graduate

df1['Education_Level'].value_counts()

#Education level – 0 for 10+ ,1 for 12+ ,2 for graduate
plt.figure(figsize=(5,4))
sns.countplot(x=df1['Education_Level'],palette="rocket")
plt.title('Education_Level')
plt.show()

"""##Bivariate Analysis"""

df1['MMM-YY'] = pd.to_datetime(df1['MMM-YY'])

df1.info()

df1.head()
df1.rename(columns={'MMM-YY':'Date'},inplace=True)

pd.crosstab(df1['Grade'],df1['Gender'])

#Correlations between the features

df1.corr(numeric_only=True)
sns.heatmap(df1.corr(numeric_only=True),annot=True,cmap='RdYlBu_r')
plt.show()

df1.hist(figsize=(10,10))
plt.show()

##df1.drop(columns='Driver_ID',inplace=True)

#from matplotlib import colormaps
#list(colormaps)

plt.figure(figsize=(5,4))
sns.barplot(data=df1,x='Grade',hue='Gender',palette='Paired')
plt.title('Gender Vs Grade')
plt.show()

sns.scatterplot(data=df1,x='Age', y="Income",hue="Gender",palette='rocket')
plt.show()

"""###Illustrate the insights based on EDA

1.   **Univariate Analysis**



*   It is evident that the **Quarterly Rating** is high for "**1**" and very less for the rating "**4**" the reason could be the people are leaving the company by the time they are reaching the rating "**4**".
*   From the **Gender** , it is evident that there are significantly more male drivers compared to female drivers.
* **Age** is normaly distributed it is clearly shown in the plot.


2.   **Bivariate Analysis**


*   The correlation is very less with in the features and most of the data is categorical in nature.
*   **Income** and **Joining Designation** is very well correlated.

#**Data Preprocessing**
"""

# Convering date to int64

df1['Date'] = df1['Date'].astype('int64')
df1['Dateofjoining'] = df1['Dateofjoining'].astype('int64')
df1['LastWorkingDate'] = df1['LastWorkingDate'].astype('int64')

df1.columns

# Terget encoding City feature

df1.groupby(['City'])['Income'].mean()


df1['City_encoded'] = df1['City'].map(df1.groupby(['City'])['Income'].mean())

df1.drop(columns='City',inplace=True)

df1.head()

"""###KNN Imputation"""

# importing KNNImputer

from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=2,weights="uniform")

df2 = imputer.fit_transform(df1)

df1 = pd.DataFrame(df2,columns=df1.columns)

df1.isnull().sum()

df1.head()

"""##**Feature Engineering**"""

df.head()

df['LastWorkingDate']

df1['LastWorkingDate2'] = df['LastWorkingDate']

df1.head()

#df1.drop(columns='LastWorkingDate',inplace=True)

df1.head()

#Create a column called target which tells whether the driver has left the company- driver whose last working day is present will have the value 1


#df1['target'] = df1['LastWorkingDate2'].apply(lambda x:1 if pd.notnull(x) else 0)
df1['target'] = df1['LastWorkingDate2'].notnull().astype(int)

#df1['target'].value_counts()
df1['target'].value_counts()
df1.head()

df1['target'].value_counts()

#df1.drop(columns='LastWorkingDate2',inplace=True)

df1.head()

#df1['quarter'] = df['MMM-YY'].astype('datetime64[ns]').dt.quarter

#The code calculates the difference between consecutive Quarterly Rating values for each Driver_ID and stores it in a new column rating_diff.
df1['rating_diff'] = df1.groupby('Driver_ID')['Quarterly Rating'].diff()
df1['rating_increased'] = df1['rating_diff'].apply(lambda x: 1 if x>0 else 0)
df1['rating_increased'].fillna(0, inplace=True)
df1.drop(columns=['rating_diff'],inplace=True)

df1['income_diff'] = df1.groupby('Driver_ID')['Income'].diff()
df1['income_increased'] = df1['income_diff'].apply(lambda x: 1 if x > 0 else 0)
df1['income_increased'].fillna(0, inplace=True)
df1.drop(columns='income_diff',inplace=True)

df1.head(10)

#df1.drop(columns='Date_dup',inplace=True)

df1.loc[df1['Gender']==0.5,'Gender'] = 0

df1.nunique()

df1.head()

from sklearn.preprocessing import OneHotEncoder

encode = OneHotEncoder()

df1.columns

df1['Driver_ID'] = df1['Driver_ID'].astype('int64')
df1['Age'] = df1['Age'].astype('int64')
df1['Gender'] = df1['Gender'].astype('int64')
df1['Education_Level'] = df1['Education_Level'].astype('int64')
df1['Joining Designation'] = df1['Joining Designation'].astype('int64')
df1['Grade'] = df1['Grade'].astype('int64')
df1['Quarterly Rating'] = df1['Quarterly Rating'].astype('int64')

"""###**Class Imbalance treatment**"""

df1['income_increased'].value_counts()

df1.head()

df1.drop(columns = ['LastWorkingDate','LastWorkingDate2'],inplace=True)

df1.head()

X = df1.drop(columns='target')
y = df1['target']

y.value_counts()

print(f'X shape {X.shape}\ny shape {y.shape}')

X.head()

y.value_counts()

from imblearn.over_sampling import SMOTE

smote = SMOTE()

X_res, y_res = smote.fit_resample(X,y)

print(f"X reshaped data {X_res.shape}\ny reshaped data {y_res.shape}")

"""#**Model building**"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.20,random_state=True)

"""###**Ensemble - Bagging Algorithm**"""

from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(random_state=7, max_depth=4, n_estimators=100)

from sklearn.model_selection import KFold, cross_validate

kfold = KFold(n_splits=10)
cv_acc_results = cross_validate(rf_clf,X_train,y_train,cv=kfold, scoring='accuracy',return_train_score=True)

print(f"K-Fold Accuracy Mean: \n Train: {cv_acc_results['train_score'].mean()*100:.2f} \n Validation: {cv_acc_results['test_score'].mean()*100:.2f}")
print(f"K-Fold Accuracy Std: \n Train: {cv_acc_results['train_score'].std()*100:.2f}, \n Validation: {cv_acc_results['test_score'].std()*100:.2f}")

"""It is clearly showing that the score is good for train data and validation data. And also it is showing there is low bias and low veriance

##GridSearchCV
"""

params = {
          'n_estimators' : [50,100,200],
          'max_depth' : [5,7,10],
          'max_features' : [7,8,10]
         }

# Defining parameters -

params = {
          'n_estimators' : [10,50,100,150,200],
          'max_depth' : [3,5,10],
          'criterion' : ['gini', 'entropy'],
          'bootstrap' : [True, False],
          'max_features' : [8,9,10]
         }

from sklearn.model_selection import GridSearchCV
import datetime as dt

grid = GridSearchCV(estimator = RandomForestClassifier(),
                    param_grid = params,
                    scoring = 'accuracy',
                    cv = 3,
                    n_jobs=-1
                    )

start = dt.datetime.now()
grid.fit(X_train,y_train)
end = dt.datetime.now()


print('Best params:',grid.best_params_)
print('Best params:',grid.best_score_)

time = end - start
print(time)

"""If GridSearchCV is taking too long to complete (e.g., 37 minutes), we can speed up the hyperparameter tuning process by using RandomizedSearchCV. Instead of exhaustively searching through all possible combinations, RandomizedSearchCV randomly samples a specified number of hyperparameter settings, which significantly reduces the computation time while still providing good results."""

res = grid.cv_results_

for i in range(len(res['params'])):
  print(f"Parameters: {res['params'][i]} Mean_score: {res['mean_test_score'][i]} Rank: {res['rank_test_score'][i]}")



"""###RandomizedSearchCV"""

# Defining parameters -

params = {
     "n_estimators":[10,25,50,100,150,200],
    'max_depth':[3, 5, 10, 15, 20],
    'max_leaf_nodes':[20, 40, 80]
}

from sklearn.model_selection import RandomizedSearchCV
import datetime as dt

model = RandomForestClassifier(n_jobs=-1)

clf = RandomizedSearchCV(model,param_distributions=params,cv = 3,random_state=42,scoring='accuracy')

start = dt.datetime.now()
clf.fit(X_train,y_train)
end = dt.datetime.now()

res = clf.cv_results_

for i in range(len(res['params'])):
  print(f"Parameters: {res['params'][i]} Mean_score: {res['mean_test_score'][i]} Rank: {res['rank_test_score'][i]}")

print(clf.best_estimator_)

rf = clf.best_estimator_

rf.fit(X_train,y_train)

print(f'model accuracy: {rf.score(X_test,y_test)}')

"""We can see the improvement using the **RandomForestClassifier** and the best estimators are max_depth=15, max_leaf_nodes=80, n_estimators=150,
                       n_jobs=-1, and the rank one score is **0.86451040124398** there is a great improvement in the score.



*  It picked the best of best not the best one. It is clearly evident that in the GridSearchCV the score is close to 90% but **RandomForestClassifier** gave us 86%.

#Ensemble - Boosting Algorithm

###**GradientBoostingClassifier**
"""

from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.model_selection import RandomizedSearchCV
import datetime as dt

params = {
    'n_estimators' : [50,100,150,200],
    'max_depth' : [3,5,7,10],
    'max_leaf_nodes':[20, 40, 80],
    'learning_rate' : [0.1,0.2,0.3]
}

gbc = GBC()

clf = RandomizedSearchCV(gbc,param_distributions=params,cv=3,random_state=42,verbose=1,n_jobs=-1,scoring='accuracy')

start = dt.datetime.now()

clf.fit(X_train, y_train)

end = dt.datetime.now()

res = clf.cv_results_

for i in range(len(res['params'])):
  print(f"parameters: {res['params'][i]}, mean_score: {res['mean_test_score'][i]} Rank: {res['rank_test_score'][i]}")

print(clf.best_estimator_)

gf = clf.best_estimator_

gf.fit(X_train,y_train)

print(f'model accuracy: {gf.score(X_test,y_test)}')

"""The score have shown a great growth using the **GradientBoostingClassifier** and the GradientBoostingClassifier(learning_rate=0.2, max_depth=7, max_leaf_nodes=80,
                           n_estimators=150) with the score **0.944**
"""

from sklearn.metrics import classification_report, confusion_matrix

y_pred = gf.predict(X_test)

classification_report(y_test, y_pred,output_dict=True)

print(classification_report(y_test, y_pred))

feature_importance = gf.feature_importances_

features = np.array(X.columns)

most_imp_features = features[np.argmax(feature_importance)]

print(f"The most important feature is: {most_imp_features}")

"""###XGBClassifier"""

from xgboost import XGBClassifier

params = {
    'n_estimators' : [50,100,150,200],
    'max_depth' : [3,5,7,10],
    'learning_rate' : [0.1,0.2,0.3],
    'objective' : ['binary:logistic']
}

xgb = XGBClassifier()

clf = RandomizedSearchCV(xgb,param_distributions=params,cv=3,n_jobs=-1,verbose=1,scoring='accuracy',random_state=42)

start = dt.datetime.now()
clf.fit(X_train,y_train)
end = dt.datetime.now()

print(end - start)

res = clf.cv_results_

for i in range(len(res['params'])):
  print(f"parameters {res['params'][i]} Mean_score: {res['mean_test_score'][i]} Rank: {res['rank_test_score'][i]}")

#for i in range(len(res['params'])):
#  print(f"parameters: {res['params'][i]}, mean_score: {res['mean_test_score'][i]} Rank: {res['rank_test_score'][i]}")

xf = clf.best_estimator_

xf.score(X_train,y_train)

print(f'model accuracy: {xf.score(X_test,y_test)}')

"""It is clearly great model with low bias and low veriance and the **test_score** for **XGBClassifier** with **94.90**

##**LightGBM**
"""

import lightgbm as lgb

params = {
    'n_estimators' : [50,100,150,200],
    'max_depth' : [3,5,7,10],
    'learning_rate' : [0.1,0.2,0.3]
}

lgb_model = lgb.LGBMClassifier(random_state=42,n_jobs=-1)

clf = RandomizedSearchCV(lgb_model, param_distributions=params,cv=5,random_state=42,n_jobs=-1,verbose=1,scoring='accuracy')

clf.fit(X_train, y_train)

res = clf.cv_results_

for i in range(len(res['params'])):
  print(f"Parameters {res['params'][i]} mean_score {res['mean_test_score'][i]} Rank {res['rank_test_score'][i]}")

lgb = clf.best_estimator_

lgb.score(X_train,y_train)
print(f'model accuracy: {lgb.score(X_test,y_test)}')

from sklearn.metrics import roc_curve, roc_auc_score

probability = lgb.predict_proba(X_test)

probability

probabilites = probability[:,1]

fpr, tpr, thr = roc_curve(y_test,probabilites)

# AUC
roc_auc_score(y_test,probabilites)

"""Precision Recall curve"""

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

precision, recall, thr = precision_recall_curve(y_test, probabilites)

auc(recall, precision)

"""Conclusion it is clear that the **LGBMClassifier** have a decent score with **94.9%**."""

