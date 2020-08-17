from sklearn import datasets

print('test ai')

iris = datasets.load_iris() # 导入数据集
X = iris.data # 获得其特征向量
y = iris.target # 获得样本label
print(iris)
print(len(X))
print(len(y))
