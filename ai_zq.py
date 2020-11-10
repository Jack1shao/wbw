from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from pandas.core.frame import DataFrame
from sklearn.model_selection import GridSearchCV

class gu_getfromdb(object):
	"""获取本地数据"""
	#获取本地文件数据
	def get_fromfiles(self,files1):
		
		print('来自{1}类--从本地文件{0}取数--'.format(files1,self.__class__.__name__))
		
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = pd.read_csv(csv_file,index_col=0,keep_default_na=False)#指定0列为index列
		else:
			print('未找到数据，请先载入')
			return DataFrame([])
		return df
class zq_sjcl:
	def sjcl(self):
		'''数据预处理'''
		gg=gu_getfromdb()
		cp='半球'
		files1='e:/football/{}1.csv'.format(cp)
		df=gg.get_fromfiles(files1)
		ccc=df.columns.values.tolist()
		vvv=df.values.tolist()
		for row in vvv:
			if row[3] in [3,2,0]:
				row[3]=0
			else:row[3]=1

			for i in range(0,len(row)):
				if row[i] is '':
					row[i]=0
			#print(row)
		df=DataFrame(vvv,columns=ccc)		
		print(df.head())
		
		files='e:/football/{}2.csv'.format(cp.replace('/','-'))
		print(files)
		df.to_csv(files)
		return 0


from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, explained_variance_score
def main():
	gg=gu_getfromdb()
	cp='半球'
	files1='e:/football/{}2.csv'.format(cp)
	data=gg.get_fromfiles(files1)
	#data=data[data['jp']==cp]
	print(data.head())
	#print(data.columns.values)
	#['idnm' 'zd' 'kd' 'sg' 'jp' 'cp' 'c_klmx' 'c_zz' 'c_fh' '10BETbcgs'
	#print(data.shape)
	x=data.iloc[:,5:]
	y=data.iloc[:,3]
	feature=data.iloc[:,5:].columns
	#数据预处理
	x_1=pd.get_dummies(x)
	x_2=MinMaxScaler().fit_transform(x_1)
	#print(x_2)
	X_train,X_test,y_train,y_test= train_test_split(x_2,y,test_size=0.3, random_state=0)
	#print ("训练集统计描述：\n",data_train.describe().round(2))
	#print ("验证集统计描述：\n",data_test.describe().round(2))
	#print ("训练集信息：\n",data_train.iloc[:,2].value_counts())  
	#print ("验证集信息：\n",data_test.iloc[:,2].value_counts())   

	#X_train=data_train.iloc[:,5:]#  data_train.iloc[:,0:-2]     
	#X_test=data_test.iloc[:,5:] #data_train.iloc[:,0:-2]
	
	#print (feature)
	#y_train=data_train.iloc[:,3]
	#y_test=data_test.iloc[:,3]
	print(len(X_test),len(X_train))


	#数据准备完毕
	#数据预处理 
	#构建模型构建模型 随机森林
	#clf= RandomForestRegressor(n_estimators=100, max_features=sqrt(n_features),random_state=0)
	#clf.fit(X_train,y_train)
	#y_pred = clf.predict(X_test)
	#mse = mean_squared_error(y_test, y_pred)
	#evs = explained_variance_score(y_test,y_pred)
	#print(Y_test)
	#print(y_pred)
	#print(clf.feature_importances_)
	#
	'''param_test={'min_samples_split':range(200,1001,200),'n_estimators':range(20,81,10),'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
				param_test2={'max_depth':range(5,16,2),'min_samples_split':range(200,1001,200),'n_estimators':range(20,81,10),'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
				param_test1 = {'n_estimators':range(20,81,10)}
				param_test3 = {'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
				param_test4 = {'max_features':range(7,20,2)}
				#print(param_test4+param_test2)
				clf=GridSearchCV(estimator=GradientBoostingClassifier(learning_rate=0.02, n_estimators=30,max_depth=5,max_features=13, subsample=0.8, random_state=0,min_samples_leaf=1000,min_samples_leaf=60),
					param_grid = param_test, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
				clf.fit(X_train,y_train)
				print(clf.grid_scores_,clf.best_params_,clf.best_score_)'''
	#min_samples_split=200
	#max_depth=5
	#{'min_samples_leaf': 60, 'min_samples_split': 1000}
	clf=GradientBoostingClassifier(learning_rate=0.01, n_estimators=70,max_depth=5,max_features=13, subsample=0.8, random_state=0,min_samples_leaf=1000,min_samples_split=60)
	clf.fit(X_train,y_train)
	print(" Accuracy on training set: {:.3f}". format( clf.score( X_train, y_train)))
	print(" Accuracy on test set: {:.3f}". format( clf.score( X_test, y_test)))
	return 0

if __name__ == '__main__':
	#h=zqfenxi(0).creat_mxk('半球')
	#ycl=zq_sjcl().sjcl()
	main()