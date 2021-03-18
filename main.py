import pickle
import pandas as pd

datos = {'age': [40,56,34], 'duration': [342,55,3], 'campaña':['dos','juan','pedro']}

df = pd.DataFrame.from_dict(datos)

print(df)

clf_file = open('clf.p', 'rb')
test_file = open('X_new_test.p', 'rb')
clf = pickle.load(clf_file)
test = pickle.load(test_file)
print(test)
# close the file
result = clf.predict(test)
print("prediccion",result)