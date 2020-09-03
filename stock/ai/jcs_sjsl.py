from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
 
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
print(len(df))
 
train, test = df[df['is_train']==True], df[df['is_train']==False]
 
features = df.columns[:4]
#print(train[features].values.tolist())
#print(test.loc[2])#[4.9,3,1.4,0.2]
#模型
clf = RandomForestClassifier(n_estimators=100,n_jobs=2)
y, _ = pd.factorize(train['species'])
#print(pd.factorize(train['species']))
#y2,_pd.factorize(test['species'])
#训练
clf.fit(train[features], y)

aa=clf.predict([[6.5, 3.0, 5.2, 2.0]])
print(aa)
 
preds = iris.target_names[clf.predict(test[features])]
#print(preds)
y2=pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])

print(clf.score(train[features],y))
#print(clf.score(preds,y2))

importances = clf.feature_importances_
print(importances)
indices = np.argsort(importances)[::-1]
for f in range(train[features].shape[1]):
    #print("%2d) %-*s %f" % (f + 1, 30, features[indices[f]], features[indices[f]]))
    print(f+1,features[indices[f]], features[indices[f]])


