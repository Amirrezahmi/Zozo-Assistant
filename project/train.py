'''
Add whatever you wish to be answered by the bot in the 'datamain.txt'.
'''
import numpy as np 
import string
from nltk.corpus import stopwords
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer
from sklearn.pipeline import Pipeline

#df = pd.read_csv('data.txt',sep='\t',error_bad_lines=False)
df = pd.read_csv('datamain.txt',sep='\t')

a = pd.Series(df.columns)

a = a.rename({0: df.columns[0],1: df.columns[1]})
#a = df.rename(columns={df.columns[0]: 'new_name'})


b = {'Questions':'Hi','Answers':'hello'}

c = {'Questions':'Hello','Answers':'hi'}

d= {'Questions':'how are you','Answers':"i'm fine. how about yourself?"}

e= {'Questions':'how are you doing','Answers':"i'm fine. how about yourself?"}

df = df.append(a,ignore_index=True)

df.columns=['Questions','Answers']

df = df.append([b,c,d,e],ignore_index=True)

df = df.append(c,ignore_index=True)

df = df.append(d,ignore_index=True)

df = df.append(d,ignore_index=True)

#clean function
def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

print(df.isnull().sum())
#remove isnull 
df.dropna(inplace=True)

#Create pipline model
Pipe = Pipeline([
    ('bow',CountVectorizer(analyzer=cleaner)),
    ('tfidf',TfidfTransformer()),
    ('classifier',DecisionTreeClassifier())
])

Pipe.fit(df['Questions'],df['Answers'])

print(Pipe.predict(["what is resistor?"])[0])
import joblib
#Train model
Pipe.fit(df['Questions'], df['Answers'])
# Save the model
joblib.dump(Pipe, 'model2.joblib')