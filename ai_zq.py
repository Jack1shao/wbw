from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
from pandas.core.frame import DataFrame
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler,OneHotEncoder
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.cluster import AgglomerativeClustering,DBSCAN,KMeans
from sklearn.decomposition import PCA
from zqfenxi import zqfenxi
import matplotlib.pyplot as plt
import mglearn



from sklearn.externals import joblib
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
'''数据预加工'''
'''数据预处理'''	
cp='半球'	
class zq_sjcl:
	'''数据预加工'''
	
	def jg(self):
		zj=zqfenxi(0)
		zj.creat_mxk(cp)
		return 0
	def sjcl(self):
		'''数据预处理'''
		gg=gu_getfromdb()
		
		files1='e:/football/{}1.csv'.format(cp)
		df=gg.get_fromfiles(files1)

		ccc=df.columns.values.tolist()

		vvv=df.values.tolist()
		for row in vvv:
			if row[3]==2:row[3]=3

			row[3]=1 if row[3] in [0,1] else 0
	

			for i in range(0,len(row)):
				if row[i] is '':
					row[i]=0
			#print(row)
		df=DataFrame(vvv,columns=ccc)		
		#print(df.head())
		
		#files='e:/football/{}2.csv'.format(cp.replace('/','-'))
		files1='e:/football/ai2.csv'
		#print(files)
		df.to_csv(files1)
		return files1


class zq_aicl:
	#提取数据
	def getfiles(self,files1):

		#cp='半球'
		#files1='e:/football/{}2.csv'.format(cp)
		gg=gu_getfromdb()
		data=gg.get_fromfiles(files1)
		x=data.iloc[:,6:]
		y=data.iloc[:,3]
		feature=data.iloc[:,6:].columns

		return x,y,feature

	#特征工程 数据预处理
	def ai_tzgc(self,x,y,feature):
		#特征工程
		x_1=pd.get_dummies(x)
		#x_2=MinMaxScaler().fit_transform(x_1)
		x_2=StandardScaler().fit_transform(x_1)

		#print(x_2)
		#拆分训练集
		X_train,X_test,y_train,y_test= train_test_split(x_2,y,test_size=0.3, random_state=0)	
		return 	X_train,X_test,y_train,y_test,feature
	#梯度提升机参数调优
	def ai_td_tc(self,x,y,feature):
		#导入数据集
		X_train,X_test,y_train,y_test,feature=self.ai_tzgc(x,y,feature)

		param_test1 = {'n_estimators':range(20,81,10)}
		param_test2={'max_depth':range(5,16,2)}
		param_test3 = {'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
		param_test4 = {'max_features':range(7,20,2)}

		clf=GridSearchCV(estimator=GradientBoostingClassifier(learning_rate=0.01,max_depth=5,max_features=13, n_estimators=20,random_state=0),
			param_grid = param_test3, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
		clf.fit(X_train,y_train)
		#查看性能#grid_scores_
		print(clf.cv_results_,clf.best_params_,clf.best_score_)
		return 0
	#梯度提升机成模型
	def ai_td_xl(self,x,y,feature):
		#导入数据集
	
		X_train,X_test,y_train,y_test,feature=self.ai_tzgc(x,y,feature)

		clf2=GradientBoostingClassifier(learning_rate=0.03, n_estimators=60,max_depth=5,max_features=13, 
			subsample=0.8,random_state=0,min_samples_leaf=30,min_samples_split=1000)
		#clf2=GradientBoostingClassifier(learning_rate=0.01, n_estimators=20,max_depth=6,max_features=13, subsample=0.8, random_state=0,min_samples_leaf=30,min_samples_split=1000)

		clf2.fit(X_train,y_train)
		print(" Accuracy on training set: {:.3f}". format( clf2.score( X_train, y_train)))
		print(" Accuracy on test set: {:.3f}". format( clf2.score( X_test, y_test)))
		#保存模型
		dirs='e:/football/'
		fil_mx=dirs+'1_05_mx.pkl'

		joblib.dump(clf2,fil_mx)
		return 0

	#根据梯度提升机数据预测

	def ai_td_yc(self,list1):
		dirs='e:/football/'
		fil_mx=dirs+'1_05_mx.pkl'
		#提取已训练好的模型
		clk=joblib.load(fil_mx)
		#print(" Accuracy on training set: {:.3f}". format( clf2.score( X_train, y_train)))
		#print(" Accuracy on test set: {:.3f}". format( clf2.score( X_test, y_test)))
		
		#预测结果
		y=clk.predict(list1)
		print('预测结果{}'.format(y))
		return y

	def jl(self,x,y,feature):
		print(feature)
		#聚类算法
		x_1=pd.get_dummies(x)
		x_2=StandardScaler().fit_transform(x_1)
	
		#agg=AgglomerativeClustering(n_clusters=3)
		#assignment=agg.fit_predict(x_2)
		#print(assignment)
		#mglearn.discrete_scatter(x_1[:,0],x_1[:,1],assignment)
		#algorithms=[KMeans(n_clusters=2),AgglomerativeClustering(n_clusters=10),DBSCAN]
		
		#PCA 降为
		pca=PCA(n_components=2)
		x_pca=pca.fit_transform(x_2)
		print('Original shape :{}'.format(str(x_2.shape)))
		print('Reduced shape :{}'.format(str(x_pca.shape)))
		
		#dbscan=algorithms[1]
		#clusters=dbscan.fit_predict(x_2)
		#print(len(clusters),len(x_2))
		#绘制簇
		#plt.scatter(x_pca[:,0],x_2[:,1],c=clusters)
		mglearn.discrete_scatter(x_pca[:,0],x_pca[:,1],y)
		plt.legend(feature,loc='best')
		plt.gca().set_aspect("equal")
		#mglearn.plots.plot_agglomerative()
		plt.xlabel('Feature0')
		plt.ylabel('Feature1')
		plt.show()


		return 0


def main():
	zz=zq_aicl()
	zs=zq_sjcl()
	#zs.jg()
	#数据处理
	print('数据处理')
	files1=zs.sjcl()
	

	#提取数据

	files1='e:/football/ai2.csv'
	print('提取数据'+files1)
	x,y,feature=zz.getfiles(files1)
	#print(len(x),len(y))
	# 聚类
	#zz.jl(x,y,feature)
	#特征工程
	#X_train,X_test,y_train,y_test,feature=zz.ai_tzgc(x,y,feature)
	#调参
	print('调参')
	#zz.ai_td_tc(x,y,feature)
	#训练
	zz.ai_td_xl(x,y,feature)
	return 0
def test2():
	zz=zq_aicl()
	
	files1='e:/football/ai2.csv'
	x,y,feature=zz.getfiles(files1)
	X_train,X_test,y_train,y_test,feature=zz.ai_tzgc(x,y,feature)

	ln=len(X_test)
	#print(X_test)


	dirs='e:/football/'
	fil_mx=dirs+'1_05_mx.pkl'
	#提取已训练好的模型
	clk=joblib.load(fil_mx)

	for i in range(0,ln):
		jg=y_test.values[i]
		#print(X_test.values.tolist()[i])
		ycz=clk.predict([X_test[i]])
		print('结果:{} 预测:{}'.format(jg,ycz))
		if i>500:break
	
	return 0

def test1():
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
	X_train,X_test,y_train,y_test= train_test_split(x_2,y,test_size=0.35, random_state=0)
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
	param_test={'min_samples_split':range(200,1001,200),'n_estimators':range(20,81,10),'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
	param_test2={'max_depth':range(5,16,2),'min_samples_split':range(200,1001,200),'n_estimators':range(20,81,10),'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
	param_test1 = {'n_estimators':range(20,81,10)}
	param_test3 = {'min_samples_split':range(1000,2100,200), 'min_samples_leaf':range(30,71,10)}
	param_test4 = {'max_features':range(7,20,2)}
	#print(param_test4+param_test2)
	clf=GridSearchCV(estimator=GradientBoostingClassifier(learning_rate=0.07, n_estimators=30,max_depth=5,max_features=13, subsample=0.8, random_state=0),
		param_grid = param_test, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
	clf.fit(X_train,y_train)
	print(clf.cv_results_,clf.best_params_,clf.best_score_)
	#min_samples_split=200
	#max_depth=5
	#{'min_samples_leaf': 60, 'min_samples_split': 1000}
	#clf=GradientBoostingClassifier(learning_rate=0.01, n_estimators=70,max_depth=5,max_features=13, subsample=0.8, random_state=0,min_samples_leaf=1000,min_samples_split=60)
	#clf.fit(X_train,y_train)
	#print(" Accuracy on training set: {:.3f}". format( clf.score( X_train, y_train)))
	#print(" Accuracy on test set: {:.3f}". format( clf.score( X_test, y_test)))
	return 0

if __name__ == '__main__':
	#h=zqfenxi(0).creat_mxk('半球')
	#ycl=zq_sjcl().sjcl()
	#test2()
	main()
	#test2()