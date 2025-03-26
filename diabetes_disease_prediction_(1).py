# -*- coding: utf-8 -*-
"""Diabetes_Disease_Prediction (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19_kAndD1U82vjryJOkhy3ZAoWVyqPyHc

#**What is Diabetes?**
**Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces. Learning how to use Machine Learning can help us predict Diabetes. Let’s get started!**
#**About this project**
**The objective of this project is to classify whether someone has diabetes or not.
Dataset consists of several Medical Variables(Independent) and one Outcome Variable(Dependent)
The independent variables in this data set are :-'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age'
The outcome variable value is either 1 or 0 indicating whether a person has diabetes(1) or not(0).**
#**About the Dataset**
Pregnancies :- Number of times a woman has been pregnant
Glucose :- Plasma Glucose concentration of 2 hours in an oral glucose tolerance test
BloodPressure :- Diastollic Blood Pressure (mm hg)
SkinThickness :- Triceps skin fold thickness(mm)
Insulin :- 2 hour serum insulin(mu U/ml)
BMI :- Body Mass Index ((weight in kg/height in m)^2)
Age :- Age(years)
DiabetesPedigreeFunction :-scores likelihood of diabetes based on family history)
Outcome :- 0(doesn't have diabetes) or 1 (has diabetes)
"""

## 1. Import Required Libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt #to plot charts
import seaborn as sns #used for data visualization
import warnings #avoid warning flash
warnings.filterwarnings('ignore')
plt.style.use('ggplot')
from google.colab import drive
drive.mount('/content/drive')
import time

## Loading the dataset
file_path = '/content/drive/My Drive/Diabetes.csv'
df = pd.read_csv(file_path)

"""#**Exploratory Data Analysis**"""

## First Few observations of the dataset
df.head(10)

## Shape of the dataset
df.shape

## Columns
df.columns

## data type analysis
#plt.figure(figsize=(5,5))
#sns.set(font_scale=2)
sns.countplot(y=df.dtypes ,data=df)
plt.xlabel("count of each data type")
plt.ylabel("data types")
plt.show()

## Data Types
df.dtypes

## Structure of the dataset
df.info()

## Summary Statistics
df.describe() #helps us to understand how data has been spread across the table.
# count :- the number of NoN-empty rows in a feature.
# mean :- mean value of that feature.
# std :- Standard Deviation Value of that feature.
# min :- minimum value of that feature.
# max :- maximum value of that feature.
# 25%, 50%, and 75% are the percentile/quartile of each features.

"""**CONCLUSION :- We observe that min value of some columns is 0 which cannot be possible medically.Hence in the data cleaning process we'll have to replace them with median/mean value depending on the distribution. Also in the max column we can see insulin levels as high as 846! We have to treat outliers**

#**Data Cleaning**
**Dropping duplicate values
Checking NULL values
Checking for 0 value and replacing it :- It isn't medically possible for some data record to have 0 value such as Blood Pressure or Glucose levels. Hence we replace them with the mean value of that particular column.**
"""

#dropping duplicate values - checking if there are any duplicate rows and dropping if any
df=df.drop_duplicates()

## null count analysis
import missingno as msno
p=msno.bar(df)

#check for missing values, count them and print the sum for every column
df.isnull().sum() #conclusion :- there are no null values in this dataset

#checking for 0 values in 5 columns , Age & DiabetesPedigreeFunction do not have have minimum 0 value so no need to replace , also no. of pregnancies as 0 is possible as observed in df.describe
print(df[df['BloodPressure']==0].shape[0])
print(df[df['Glucose']==0].shape[0])
print(df[df['SkinThickness']==0].shape[0])
print(df[df['Insulin']==0].shape[0])
print(df[df['BMI']==0].shape[0])

"""#**Some of the columns have a skewed distribution, so the mean is more affected by outliers than the median. Glucose and Blood Pressure have normal distributions hence we replace 0 values in those columns by mean value. SkinThickness, Insulin,BMI have skewed distributions hence median is a better choice as it is less affected by outliers.** **bold text**"""

#replacing 0 values with median of that column
df['Glucose']=df['Glucose'].replace(0,df['Glucose'].mean())#normal distribution
df['BloodPressure']=df['BloodPressure'].replace(0,df['BloodPressure'].mean())#normal distribution
df['SkinThickness']=df['SkinThickness'].replace(0,df['SkinThickness'].median())#skewed distribution
df['Insulin']=df['Insulin'].replace(0,df['Insulin'].median())#skewed distribution
df['BMI']=df['BMI'].replace(0,df['BMI'].median())#skewed distribution

"""#**Data Visualization**
**Count Plot :- to see if the dataset is balanced or not
Histograms :- to see if data is normally distributed or skewed
Box Plot :- to analyse the distribution and see the outliers
Scatter plots :- to understand relationship between any two variables
Pair plot :- to create scatter plot between all the variables**
"""

## Bar Chart for Outcome Variable
sns.countplot(x = "Outcome", data = df)
plt.title("Count Plot for Outcome Variable")
plt.show()

"""#**Conclusion :- We observe that number of people who do not have diabetes is far more than people who do which indicates that our data is imbalanced.**"""

#histogram for each  feature
df.hist(bins=10,figsize=(10,10))
plt.show()

"""#**Conclusion :- We observe that only glucose and Blood Pressure are normally distributed rest others are skewed and have outliers**"""

plt.figure(figsize=(16,12))
sns.set_style(style='whitegrid')
plt.subplot(3,3,1)
sns.boxplot(x='Glucose',data=df)
plt.subplot(3,3,2)
sns.boxplot(x='BloodPressure',data=df)
plt.subplot(3,3,3)
sns.boxplot(x='Insulin',data=df)
plt.subplot(3,3,4)
sns.boxplot(x='BMI',data=df)
plt.subplot(3,3,5)
sns.boxplot(x='Age',data=df)
plt.subplot(3,3,6)
sns.boxplot(x='SkinThickness',data=df)
plt.subplot(3,3,7)
sns.boxplot(x='Pregnancies',data=df)
plt.subplot(3,3,8)
sns.boxplot(x='DiabetesPedigreeFunction',data=df)

"""#**Outliers are unusual values in your dataset, and they can distort statistical analyses and violate their assumptions. Hence it is of utmost importance to deal with them. In this case removing outliers can cause data loss so we have to deal with it using various scaling and transformation techniques**"""

from pandas.plotting import scatter_matrix
scatter_matrix(df,figsize=(20,20));
# we can come to various conclusion looking at these plots for example  if you observe 5th plot in pregnancies with insulin, you can conclude that women with higher number of pregnancies have lower insulin

"""#**5. Feature Selection**
#**Pearson's Correlation Coefficient : Helps you find out the relationship between two quantities. It gives you the measure of the strength of association between two variables. The value of Pearson's Correlation Coefficient can be between -1 to +1. 1 means that they are highly correlated and 0 means no correlation. A heat map is a two-dimensional representation of information with the help of colors. Heat maps can help the user visualize simple or complex information.**
"""

corrmat=df.corr()
sns.heatmap(corrmat, annot=True)

"""#**Handling Outliers**
**1 — What is an Outlier?**
**An outlier is a data point in a data set that is distant from all other observations.**
**2 — How can we Identify an outlier?**
**Using Box plots**
**Using Scatter plot**
**Using Z score**
**I've used Box Plots above in data visualization step to detect outliers.**
**3 — How am I treating the outliers ?**
**Quantile Transformer :- This method transforms the features to follow a uniform or a normal distribution. Therefore, for a given feature, this transformation tends to spread out the most frequent values. It also reduces the impact of (marginal) outliers: this is therefore a robust preprocessing scheme.**
"""

from sklearn.preprocessing import QuantileTransformer
x=df
quantile  = QuantileTransformer()
X = quantile.fit_transform(x)
df_new=quantile.transform(X)
df_new=pd.DataFrame(X)
df_new.columns =['Pregnancies', 'Glucose','SkinThickness','BMI','Age',"BloodPressure", "Insulin", "DiabetesPedigreeFunction", "Outcome"]
df_new.head()

plt.figure(figsize=(16,12))
sns.set_style(style='whitegrid')
plt.subplot(3,3,1)
sns.boxplot(x=df_new['Glucose'],data=df_new)
plt.subplot(3,3,2)
sns.boxplot(x=df_new['BMI'],data=df_new)
plt.subplot(3,3,3)
sns.boxplot(x=df_new['Pregnancies'],data=df_new)
plt.subplot(3,3,4)
sns.boxplot(x=df_new['Age'],data=df_new)
plt.subplot(3,3,5)
sns.boxplot(x=df_new['SkinThickness'],data=df_new)
plt.subplot(3,3,6)
sns.boxplot(x=df_new['BloodPressure'],data=df_new)
plt.subplot(3,3,7)
sns.boxplot(x=df_new['Insulin'],data=df_new)
plt.subplot(3,3,8)
sns.boxplot(x=df_new['DiabetesPedigreeFunction'],data=df_new)

"""#**5. Split the Data Frame into X and y**"""

target_name='Outcome'
y= df_new[target_name]#given predictions - training data
X=df_new.drop(target_name,axis=1)#dropping the Outcome column and keeping all other columns as X

X.head() # contains only independent features

"""#**7. TRAIN TEST SPLIT**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=0)#splitting data in 80% train, 20%test
X_train.shape,y_train.shape
X_test.shape,y_test.shape

"""#**9.1 K Nearest Neighbours :-**
KNN algorithm, is a non-parametric algorithm that classifies data points based on their proximity and association to other available data.
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import GridSearchCV

#List Hyperparameters to tune
knn= KNeighborsClassifier()
n_neighbors = list(range(15,25))
p=[1,2]
weights = ['uniform', 'distance']
metric = ['euclidean', 'manhattan', 'minkowski']

#convert to dictionary
hyperparameters = dict(n_neighbors=n_neighbors, p=p,weights=weights,metric=metric)

#Making model
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=knn, param_grid=hyperparameters, n_jobs=-1, cv=cv, scoring='f1',error_score=0)

best_model = grid_search.fit(X_train,y_train)

#Best Hyperparameters Value
print('Best leaf_size:', best_model.best_estimator_.get_params()['leaf_size'])
print('Best p:', best_model.best_estimator_.get_params()['p'])
print('Best n_neighbors:', best_model.best_estimator_.get_params()['n_neighbors'])

#Predict testing set
knn_pred = best_model.predict(X_test)
Knn_score = accuracy_score(y_test, knn_pred)

print("Classification Report is:\n",classification_report(y_test,knn_pred))
print("\n F1:\n",f1_score(y_test,knn_pred))
print("\n Precision score is:\n",precision_score(y_test,knn_pred))
print("\n Recall score is:\n",recall_score(y_test,knn_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,knn_pred))

"""#**9.2 Naive Bayes :-**
Naive Bayes is classification approach that adopts the principle of class conditional independence from the Bayes Theorem. This means that the presence of one feature does not impact the presence of another in the probability of a given outcome, and each predictor has an equal effect on that result
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

param_grid_nb = {
    'var_smoothing': np.logspace(0,-2, num=100)
}
naive = GridSearchCV(estimator=GaussianNB(), param_grid=param_grid_nb, verbose=1, cv=10, n_jobs=-1)
best_model= naive.fit(X_train, y_train)
nb_pred=best_model.predict(X_test)
naive_score= accuracy_score(y_test,nb_pred)
print("Classification Report is:\n",classification_report(y_test,nb_pred))
print("\n F1:\n",f1_score(y_test,nb_pred))
print("\n Precision score is:\n",precision_score(y_test,nb_pred))
print("\n Recall score is:\n",recall_score(y_test,nb_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,nb_pred))

"""#**9.3 Support Vector Machine :-**
It is typically leveraged for classification problems, constructing a hyperplane where the distance between two classes of data points is at its maximum. This hyperplane is known as the decision boundary, separating the classes of data points (e.g., has diabetes vs doesn't have diabetes ) on either side of the plane.
"""

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
svm = SVC()
kernel = ['poly', 'rbf', 'sigmoid']
C = [50, 10, 1.0, 0.1, 0.01]
gamma = ['scale']
# define grid search
grid = dict(kernel=kernel,C=C,gamma=gamma)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=svm, param_grid=grid, n_jobs=-1, cv=cv, scoring='f1',error_score=0)
grid_result = grid_search.fit(X, y)
svm_pred=grid_result.predict(X_test)
svm_score= accuracy_score(y_test,svm_pred)
print("Classification Report is:\n",classification_report(y_test,svm_pred))
print("\n F1:\n",f1_score(y_test,svm_pred))
print("\n Precision score is:\n",precision_score(y_test,svm_pred))
print("\n Recall score is:\n",recall_score(y_test,svm_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,svm_pred))

"""#**9.4 Decision Tree**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import GridSearchCV
dt = DecisionTreeClassifier(random_state=42)
# Create the parameter grid based on the results of random search
params = {
    'max_depth': [5, 10, 20,25],
    'min_samples_leaf': [10, 20, 50, 100,120],
    'criterion': ["gini", "entropy"]
}
DT = GridSearchCV(estimator=dt,
                           param_grid=params,
                           cv=4, n_jobs=-1, verbose=1, scoring = "accuracy")
best_model=DT.fit(X_train, y_train)
dt_pred=best_model.predict(X_test)
dt_score= accuracy_score(y_test,dt_pred)
print("Classification Report is:\n",classification_report(y_test,dt_pred))
print("\n F1:\n",f1_score(y_test,dt_pred))
print("\n Precision score is:\n",precision_score(y_test,dt_pred))
print("\n Recall score is:\n",recall_score(y_test,dt_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,dt_pred))

"""#**9.5 Random Forest :-**
The "forest" references a collection of uncorrelated decision trees, which are then merged together to reduce variance and create more accurate data predictions
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
# define models and parameters
RF = RandomForestClassifier()
n_estimators = [1800]
max_features = ['sqrt', 'log2']
# define grid search
grid = dict(n_estimators=n_estimators,max_features=max_features)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=RF, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
best_model = grid_search.fit(X_train, y_train)
rf_pred=best_model.predict(X_test)
RF_score= accuracy_score(y_test,rf_pred)
print("Classification Report is:\n",classification_report(y_test,rf_pred))
print("\n F1:\n",f1_score(y_test,rf_pred))
print("\n Precision score is:\n",precision_score(y_test,rf_pred))
print("\n Recall score is:\n",recall_score(y_test,rf_pred))
print("\n Confusion Matrix:\n")
sns.heatmap(confusion_matrix(y_test,rf_pred))

"""#**9.6 Logistic Regression:-**
Logistical regression is selected when the dependent variable is categorical, meaning they have binary outputs, such as "true" and "false" or "yes" and "no."

Logistic regression does not really have any critical hyperparameters to tune. Sometimes, you can see useful differences in performance or convergence with different solvers (solver).Regularization (penalty) can sometimes be helpful.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score,accuracy_score
reg = LogisticRegression()
reg.fit(X_train,y_train)
lr_pred=reg.predict(X_test)
print("Classification Report is:\n",classification_report(y_test,lr_pred))
print("\n F1:\n",f1_score(y_test,lr_pred))
print("\n Precision score is:\n",precision_score(y_test,lr_pred))
print("\n Recall score is:\n",recall_score(y_test,lr_pred))
print("\n Confusion Matrix:\n")
reg_score=accuracy_score(y_test,lr_pred)
sns.heatmap(confusion_matrix(y_test,lr_pred))

"""#**Comparing Models to choose the best One**"""

model_comp = pd.DataFrame({'Model': ['Logistic Regression','Random Forest',
                    'K-Nearest Neighbour','Support Vector Machine','Naive Bayes Classifier'], 'Accuracy': [reg_score*100,
                    RF_score*100,Knn_score*100,svm_score*100, naive_score*100]})
model_comp

from sklearn.metrics import roc_auc_score
final_metrics={'Accuracy': accuracy_score(y_test,svm_pred), # Changed X_test to y_test
                   'Precision': precision_score(y_test,svm_pred), # Changed Y_test to y_test
                   'Recall': recall_score(y_test,svm_pred), # Changed Y_test to y_test
                   'F1': f1_score(y_test,svm_pred), # Changed Y_test to y_test
                   'AUC': roc_auc_score(y_test, svm_pred)} # Changed Y_test to y_test


metrics=pd.DataFrame(final_metrics,index=[0])

metrics.T.plot.bar(title='Final metric evaluation',legend=False);

## Lets save our model using pickle
import pickle as pkl
pkl.dump(svm,open("diabetes_model.p","wb"))

diabetes_model=pkl.load(open("diabetes_model.p","rb"))

# -*- coding: utf-8 -*-
"""
Created on Tue March  26 10:09:17 2025

@author: enock bereka
"""

import pickle as pkl
import streamlit as st
from streamlit_option_menu import option_menu

# loading the saved models
diabetes_model= pkl.load(open("diabetes_model.p","rb"))
# sidebar navi bar

with st.sidebar:
    selected = option_menu("Disease Menu",

                           ["Diabetes Diseases",
                            "Breast Diseases",
                            "Heart Diseases",
                            "Parkinsons Diseases"],

                           icons= ['bandaid','person-standing-dress','postcard-heart','headset-vr'],
                           default_index = 0)

# Diabetses prediction page
if (selected == "Diabetes Diseases"):
    #page title
    st.title("DIABETES DISEASE PREDICTION")

    # Getting the input data from the user
    # Columns for input fileds

    col1,col2,col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose level')
    with col3:
        BloodPressure = st.text_input('Blood pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness Value')
    with col2:
        Insulin = st.text_input('Insulin level')
    with col3:
        BMI = st.text_input('BMI Value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
    with col2:
        Age = st.text_input('Age of the Person')

    # code for prediction
    diabetes_prediction = ''

    #creating button for prediction
    if st.button('Diagnose'):
        diabetes_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if(diabetes_prediction[0]==1):
            diabetes_prediction = 'DIABETIC'
        else:
            diabetes_prediction = "NOT DIABETIC"

    st.success(diabetes_prediction)