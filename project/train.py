'''
Add whatever you wish to be answered by the bot in the 'datamain.txt'.
'''
# If you encounter `LookupError`, it is because you need to download wordnet. To do this, uncomment lines 16 and 17 and comment these two lines again after execution.


import numpy as np 
import string
from nltk.corpus import stopwords
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer
from sklearn.pipeline import Pipeline
from nltk.stem import WordNetLemmatizer 
#import nltk
#nltk.download('wordnet')

#df = pd.read_csv('data.txt',sep='\t',error_bad_lines=False)
df = pd.read_csv('datamain.txt',sep='\t')

a = pd.Series(df.columns)

a = a.rename({0: df.columns[0],1: df.columns[1]})
#a = df.rename(columns={df.columns[0]: 'new_name'})


b = {'Questions':'Hi','Answers':'hello'}

c = {'Questions':'Hello','Answers':'hi'}

d= {'Questions':'how are you','Answers':"i'm fine. how about yourself?"}

e= {'Questions':'how are you doing','Answers':"i'm fine. how about yourself?"}

df = df._append(a,ignore_index=True)

df.columns=['Questions','Answers']

df = df._append([b,c,d,e],ignore_index=True)

df = df._append(c,ignore_index=True)

df = df._append(d,ignore_index=True)

df = df._append(d,ignore_index=True)

#clean function
lemmatizer = WordNetLemmatizer() 
def cleaner(x):
    words = (''.join([a for a in x if a not in string.punctuation])).lower().split()
    return [lemmatizer.lemmatize(word) for word in words]

print(df.isnull().sum())
#remove isnull 
df.dropna(inplace=True)

#Create pipline model
Pipe = Pipeline([
    ('bow',CountVectorizer(analyzer=cleaner)),
    ('tfidf',TfidfTransformer()),
    ('classifier',LinearSVC())
])

Pipe.fit(df['Questions'],df['Answers'])

print(Pipe.predict(["what is resistor?"])[0])
import joblib
#Train model
Pipe.fit(df['Questions'], df['Answers'])
# Save the model
joblib.dump(Pipe, 'model2.joblib')
print("Done!\nNow get back to ui.py or main.py")
