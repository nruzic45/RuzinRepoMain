import pandas as pd
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from statistic import statistika,confusion_matrix_show
from data_normalize import normalize_data


x,y = normalize_data("Train-dataset.csv",include=['WELL','X_Y','DEPOSITIONAL_ENVIRONMENT'], hot_one_enc=False)
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size = 0.15,stratify=y)

df = DecisionTreeClassifier(random_state=0,criterion = 'entropy').fit(x_training_data,y_training_data)
prediction_df_training = df.predict(x_training_data)
prediction_df_test= df.predict(x_test_data)

print("Training DecisionTree: \n")
statistika(prediction_df_training,y_training_data)
confusion_matrix_show(prediction_df_training,y_training_data)
print("*********************\n")
print("Test DecisionTree: \n")
statistika(prediction_df_test,y_test_data)
confusion_matrix_show(prediction_df_test,y_test_data)

'''
SVC= SVC(kernel='poly').fit(x_training_data, y_training_data)
prediction_SVC_training = SVC.predict(x_training_data)
prediction_SVC_test= SVC.predict(x_test_data)

print("Training SVC: \n")
statistika(prediction_SVC_training,y_training_data)
confusion_matrix_show(prediction_SVC_training,y_training_data)
print("*********************\n")
print("Test SVC: \n")
statistika(prediction_SVC_test,y_test_data)
confusion_matrix_show(prediction_SVC_test,y_test_data)
'''

rf = RandomForestClassifier(n_estimators=100).fit(x_training_data,y_training_data)
prediction_rf_training = rf.predict(x_training_data)
prediction_rf_test= rf.predict(x_test_data)

print("Training RandomForest: \n")
statistika(prediction_rf_training,y_training_data)
confusion_matrix_show(prediction_rf_training,y_training_data)
print("*********************\n")
print("Test RandomForest: \n")
statistika(prediction_rf_test,y_test_data)
confusion_matrix_show(prediction_rf_test,y_test_data)

'''
lr = LogisticRegression(solver='liblinear', random_state=0).fit(x_training_data,y_training_data)
prediction_lr_training = lr.predict(x_training_data)
prediction_lr_test= lr.predict(x_test_data)

print("Training LogisticRegression: \n")
statistika(prediction_lr_training,y_training_data)
confusion_matrix_show(prediction_lr_training,y_training_data)
print("*********************\n")
print("Test LogisticRegression: \n")
statistika(prediction_lr_test,y_test_data)
confusion_matrix_show(prediction_lr_test,y_test_data)
'''

encoder=LabelEncoder()
binary_encoded_y=pd.Series(encoder.fit_transform(y))

ada = AdaBoostClassifier(DecisionTreeClassifier(max_depth=100), n_estimators=500, random_state=0).fit(x_training_data,y_training_data)
prediction_ada_training = ada.predict(x_training_data)
prediction_ada_test= ada.predict(x_test_data)

print("Training ADA: \n")
statistika(prediction_ada_training,y_training_data)
confusion_matrix_show(prediction_ada_training,y_training_data)
print("*\n")
print("Test ADA: \n")
statistika(prediction_ada_test,y_test_data)
confusion_matrix_show(prediction_ada_test,y_test_data)

clf = ExtraTreesClassifier(n_estimators=1000, random_state=0,n_jobs=-1).fit(x_training_data, y_training_data)
prediction_clf_training = clf.predict(x_training_data)
prediction_clf_test= clf.predict(x_test_data)

print("Training EXTRA: \n")
statistika(prediction_clf_training,y_training_data)
confusion_matrix_show(prediction_clf_training,y_training_data)
print("*\n")
print("Test EXTRA: \n")
statistika(prediction_clf_test,y_test_data)
confusion_matrix_show(prediction_clf_test,y_test_data)

estimator_list = [
    #('SVC',SVC),
    ('df',df),
    ('rf',rf),
    #('lr',lr),
    ('ada',ada),
    ('clf',clf)]

# Build stack model
stack_model = StackingClassifier(
    estimators=estimator_list, final_estimator=LogisticRegression()
)

# Train stacked model
stack_model.fit(x_training_data, y_training_data)

# Make predictions
y_train_pred = stack_model.predict(x_training_data)
y_test_pred = stack_model.predict(x_test_data)

# Training set model performance
stack_model_train_accuracy = accuracy_score(y_training_data, y_train_pred) # Calculate Accuracy
stack_model_train_f1 = f1_score(y_training_data, y_train_pred, average='weighted') # Calculate F1-score

# Test set model performance
stack_model_test_accuracy = accuracy_score(y_test_data, y_test_pred) # Calculate Accuracy
stack_model_test_f1 = f1_score(y_test_data, y_test_pred, average='weighted') # Calculate F1-score

print('Stack Model performance for Training set')
print('- Accuracy: %s' % stack_model_train_accuracy)
print('- F1 score: %s' % stack_model_train_f1)
print('----------------------------------')
print('Stack Model performance for Test set')
print('- Accuracy: %s' % stack_model_test_accuracy)
print('- F1 score: %s' % stack_model_test_f1)