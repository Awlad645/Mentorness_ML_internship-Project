

from google.colab import drive
drive.mount('/content/drive')

"""# IMPORTING PACKAGES"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn import feature_selection
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

import warnings
warnings.filterwarnings("ignore")




df=pd.read_csv(r"/content/drive/MyDrive/Prediction for Credit Card Approval/train_data.csv")
df1=pd.read_csv(r"/content/drive/MyDrive/Prediction for Credit Card Approval/test_data.csv")

"""# READING THE DATA"""

train_original=df.copy()
test_original=df1.copy()

df.head(10)

df.shape

df1.shape

#GET SOME STATISTICS

df.describe()

df.info()

#COUNT THE EMPTY VALUES IN EACH COLUMNS

df.isnull().sum()

"""Test Dataset info"""

df1.info()

#COUNT THE EMPTY VALUES IN EACH COLUMNS

df1.isnull().sum()

"""# EXPLORING AND PREPARING THE DATA"""

data=[df,df1]
for dataset in data:
    #FILTER CATEGORICAL VARIABLES
    categorical_columns=[x for x in dataset.dtypes.index if dataset.dtypes[x]=='object']
    #EXCLUDE ID COLS AND SOURCE:
    categorical_columns =[x for x in categorical_columns if x not in['ID']]


    #PRINT FREQUENCY OF CATEGORIES
for col in categorical_columns:
    print('\nFrequency of categories for variable %s'%col)
    print(df[col].value_counts())

pd.crosstab(df['Gender'], df['Is high risk'], margins=True)

#DEPENDENDANTS

plt.figure(figsize=(6,6))
labels=['0','1','2','3+']
explode=(0.05,0,0,0)
size=[345,102,101,51]
plt.pie(size,explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
plt.axis('equal')
plt.show()

pd.crosstab(df['Dwelling'], df['Is high risk'], margins=True)

#pd.crosstab(df.Dependents,df.Loan_Status,margins=True)

pd.crosstab(df['Has a property'], df['Is high risk'], margins=True)

#SELF EMPLOYED

sns.countplot(df['Employment status'])

#pd.crosstab(df.Self_Employed, df.Loan_Status, margins=True)

#EDUCATION

sns.countplot(df['Education level'])

#PROPERTY AREA


#sns.countplot(df.Property_Area)

temp1=df['Has a car'].value_counts(ascending=True)
temp2=df.pivot_table(values='Is high risk',index=['Has a car'],aggfunc= lambda x: x.map({'Y':1,'N':0}).mean())
print('Frequency Table for Credit History:')
print(temp1)
print('\n probability of getting loan for each credit history class:')
print(temp2)

temp3=pd.crosstab(df['Family member count'],df['Is high risk'])
temp3.plot(kind='bar',stacked=True, color=['red','blue'],grid=False)

df.apply(lambda x: sum(x.isnull()),axis=0)

"""# CORRELATION BETWEEN ALL THE NUMERICAL VARIABLES

"""

# HEATMAP REPRESENTATION OF THE CORRELATION

matrix=df.corr()
f,ax=plt.subplots(figsize=(9,6))
sns.heatmap(matrix,vmax=.8,square=True,cmap="BuPu")

#COUNT THE EMPTY VALUES IN EACH COLUMNS

df.isnull().sum()

"""# Checking correlation with class data"""

pd.crosstab(df['Employment status'], df['Is high risk'], margins=True)

pd.crosstab(df['Education level'], df['Is high risk'], margins=True)

pd.crosstab(df['Dwelling'], df['Is high risk'], margins=True)

pd.crosstab(df['Marital status'], df['Is high risk'], margins=True)

pd.crosstab(df['Dwelling'], df['Is high risk'], margins=True)

"""# Categorical Variable Mapping for Feature Engineering"""



#CONVERTING STRING VALUES(CATEGORICAL VALUES) TO INTEGER
df.Gender=df.Gender.map({"F":0,"M":1})
df['Marital status'] = df['Marital status'].map({"Single / not married":0, "Married":1, "Civil marriage":2, "Widow":3, "Separated":4})
df['Has a car']=df['Has a car'].map({"N":0,"Y":1})
df['Has a property']=df['Has a property'].map({"N":0,"Y":1})
df['Employment status']=df['Employment status'].map({"Commercial associate":0,"Pensioner":1,"State servant":2,"Student":3,"Working":4})
df['Education level']=df['Education level'].map({"Academic degree":0,"Higher education":1,"Incomplete higher":2,"Lower secondary":3,"Secondary / secondary special":4})
df['Dwelling']=df['Dwelling'].map({"Co-op apartment":0,"House / apartment":1,"Municipal apartment":2,"Office apartment":3,"Rented apartment":4,"With parents":5})

df1.Gender=df1.Gender.map({"F":0,"M":1})
df1['Marital status'] = df1['Marital status'].map({"Single / not married":0, "Married":1, "Civil marriage":2, "Widow":3, "Separated":4})
df1['Has a car']=df1['Has a car'].map({"N":0,"Y":1})
df1['Has a property']=df1['Has a property'].map({"N":0,"Y":1})
df1['Employment status']=df1['Employment status'].map({"Commercial associate":0,"Pensioner":1,"State servant":2,"Student":3,"Working":4})
df1['Education level']=df1['Education level'].map({"Academic degree":0,"Higher education":1,"Incomplete higher":2,"Lower secondary":3,"Secondary / secondary special":4})
df1['Dwelling']=df1['Dwelling'].map({"Co-op apartment":0,"House / apartment":1,"Municipal apartment":2,"Office apartment":3,"Rented apartment":4,"With parents":5})

df.head()



"""# Drop Column

"""

df.drop(columns=['ID'], inplace=True)
df.drop(columns=['Job title'], inplace=True)

df1.drop(columns=['ID'], inplace=True)
df1.drop(columns=['Job title'], inplace=True)

df1.isnull().sum()

df.isnull().sum()

"""# Check feature types"""

df1.dtypes

#LOOK AT THE DATA TYPES

df.dtypes

"""#  Model devlopment & evaluation



"""

#LETS PREPARE THE DATA FOR FEEDING IN TO THE MODELS
#SAVE THE TARGET VARIABLE IN SEPARATE

x=df.drop("Is high risk",1)
y=df['Is high risk']

xtest=df1.drop("Is high risk",1)
ytest=df1['Is high risk']



x=pd.get_dummies(x)
df=pd.get_dummies(df)

"""Random forest Normal"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate Random Forest Classifier
rfc = RandomForestClassifier()

# Fit the classifier on the training data
rfc.fit(x, y)

# Make predictions on the test data
pred_rfc = rfc.predict(xtest)

# Calculate accuracy
acc_rfc = accuracy_score(ytest, pred_rfc) * 100
print("Accuracy:", acc_rfc)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_rfc)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_rfc)
print("Classification Report:")
print(report)

"""Gradiant Boosting Normal"""

#USE GRADIENT BOOSTING CLASSIFIER

from sklearn.ensemble import GradientBoostingClassifier
gbk=GradientBoostingClassifier()
gbk.fit(x,y)
pred_gbc=gbk.predict(xtest)
acc_gbc=accuracy_score(ytest,pred_gbc)*100
acc_gbc

from sklearn.metrics import confusion_matrix
cm= confusion_matrix(ytest, pred_gbc)

cm

from sklearn.metrics import classification_report

# Generate classification report
report = classification_report(ytest, pred_gbc)

# Print the classification report
print(report)

"""KNeighborsClassifier"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate KNN Classifier
knn_classifier = KNeighborsClassifier()

# Fit the classifier on the training data
knn_classifier.fit(x, y)

# Make predictions on the test data
pred_knn = knn_classifier.predict(xtest)

# Calculate accuracy
acc_knn = accuracy_score(ytest, pred_knn) * 100
print("Accuracy:", acc_knn)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_knn)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_knn)
print("Classification Report:")
print(report)

"""Decision tree"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate Decision Tree Classifier
dt_classifier = DecisionTreeClassifier()

# Fit the classifier on the training data
dt_classifier.fit(x, y)

# Make predictions on the test data
pred_dt = dt_classifier.predict(xtest)

# Calculate accuracy
acc_dt = accuracy_score(ytest, pred_dt) * 100
print("Accuracy:", acc_dt)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_dt)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_dt)
print("Classification Report:")
print(report)

"""Oversampling"""

from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate SMOTE
smote = SMOTE()

# Oversample the minority class
x_resampled, y_resampled = smote.fit_resample(x, y)

# Instantiate Decision Tree Classifier
dt_classifier = DecisionTreeClassifier()

# Fit the classifier on the resampled data
dt_classifier.fit(x_resampled, y_resampled)

# Make predictions on the test data
pred_dt = dt_classifier.predict(xtest)

# Calculate accuracy
acc_dt = accuracy_score(ytest, pred_dt) * 100
print("Accuracy:", acc_dt)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_dt)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_dt)
print("Classification Report:")
print(report)

"""Oversampling with random forest"""

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate SMOTE
smote = SMOTE()

# Oversample the minority class
x_resampled, y_resampled = smote.fit_resample(x, y)

# Instantiate Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Fit the classifier on the resampled data
rf_classifier.fit(x_resampled, y_resampled)

# Make predictions on the test data
pred_rf = rf_classifier.predict(xtest)

# Calculate accuracy
acc_rf = accuracy_score(ytest, pred_rf) * 100
print("Accuracy:", acc_rf)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_rf)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_rf)
print("Classification Report:")
print(report)

"""Decision tree"""

from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate SMOTE
smote = SMOTE()

# Oversample the minority class
x_resampled, y_resampled = smote.fit_resample(x, y)

# Instantiate Decision Tree Classifier
dt_classifier = DecisionTreeClassifier()

# Fit the classifier on the resampled data
dt_classifier.fit(x_resampled, y_resampled)

# Make predictions on the test data
pred_dt = dt_classifier.predict(xtest)

# Calculate accuracy
acc_dt = accuracy_score(ytest, pred_dt) * 100
print("Accuracy:", acc_dt)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_dt)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_dt)
print("Classification Report:")
print(report)

"""KNN"""

from imblearn.over_sampling import SMOTE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Instantiate SMOTE
smote = SMOTE()

# Oversample the minority class
x_resampled, y_resampled = smote.fit_resample(x, y)

# Instantiate KNN Classifier
knn_classifier = KNeighborsClassifier()

# Fit the classifier on the resampled data
knn_classifier.fit(x_resampled, y_resampled)

# Make predictions on the test data
pred_knn = knn_classifier.predict(xtest)

# Calculate accuracy
acc_knn = accuracy_score(ytest, pred_knn) * 100
print("Accuracy:", acc_knn)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_knn)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_knn)
print("Classification Report:")
print(report)

import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Calculate class weights
class_weights = len(y) / (2 * np.bincount(y))

# Instantiate XGBoost Classifier with class weights
xgb_classifier = xgb.XGBClassifier(scale_pos_weight=class_weights[1])

# Fit the classifier on the training data
xgb_classifier.fit(x, y)

# Make predictions on the test data
pred_xgb = xgb_classifier.predict(xtest)

# Calculate accuracy
acc_xgb = accuracy_score(ytest, pred_xgb) * 100
print("Accuracy:", acc_xgb)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_xgb)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_xgb)
print("Classification Report:")
print(report)

from collections import Counter

# Count the occurrences of each class


# Print the class counts


# Instantiate Random Forest Classifier with class weights
rf_classifier = RandomForestClassifier(class_weight={0: class_counts[0], 1: class_counts[1]})

# Fit the classifier on the training data
rf_classifier.fit(x, y)

# Make predictions on the test data
pred_rf = rf_classifier.predict(xtest)

# Calculate accuracy
acc_rf = accuracy_score(ytest, pred_rf) * 100
print("Accuracy:", acc_rf)

# Generate confusion matrix
cm = confusion_matrix(ytest, pred_rf)
print("Confusion Matrix:")
print(cm)

# Generate classification report
report = classification_report(ytest, pred_rf)
print("Classification Report:")
print(report)
