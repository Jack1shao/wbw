from sklearn import datasets
import pandas as pd
import mglearn
import matplotlib.pyplot as plt
print('test ai')

iris_dataset = datasets.load_iris() # 导入数据集
X = iris_dataset.data # 获得其特征向量
y = iris_dataset.target # 获得样本label
#print(iris_dataset['data'], iris_dataset['target'])


from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split( iris_dataset['data'], iris_dataset['target'], random_state= 0)

print(" X_train shape: {}".format( X_train.shape)) 
print(" y_train shape: {}".format( y_train.shape))

# 利用 X_train 中的 数据 创建 DataFrame 
# 利用 iris_dataset.feature_names 中的 字符串 对 数据 列 进行 标记 
iris_dataframe = pd.DataFrame( X_train, columns= iris_dataset.feature_names) 
# 利用 DataFrame 创建 散点图 矩阵， 按 y_train 着色 
grr = pd.plotting.scatter_matrix( iris_dataframe, c= y_train, figsize=( 15, 15), marker='o', hist_kwds={'bins': 20}, s= 60, alpha=.8, cmap= mglearn.cm3)
plt.show()
print('hel')