import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import sklearn.preprocessing as pre
from sklearn.metrics import confusion_matrix, classification_report

x_train = pd.read_csv('x_train.csv')
y_train = pd.read_csv('y_train.csv')
x_test = pd.read_csv('x_test.csv')
y_test = pd.read_csv('y_test.csv')

x_train.astype('category')
x_test.astype('category')

le = pre.LabelEncoder()
le.fit(y_train)
y_train = le.transform(y_train)
y_test = le.transform(y_test)


model = XGBClassifier(learning_rate=0.1,
                       n_estimators=100,                                                             
                       max_depth=10,               
                       min_child_weight = 50,      
                       gamma=0,                   
                       subsample=0.8,             
                       colsample_btree=0.8,       
                       objective='multi:softprob', 
                       scale_pos_weight=1,        
                       random_state=123,
                       )

model.fit(x_train,
           y_train,
          eval_set = [(x_test,y_test)],
           eval_metric = "mlogloss",
           verbose = True)

model.save_model("model.json")

y_pred = model.predict(x_train)
print('train accuracy: ',accuracy_score(y_train, y_pred))

cm = confusion_matrix(y_train, y_pred)
print(cm)

y_pred = model.predict(x_test)
print('test accuracy: ',accuracy_score(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print(cm)