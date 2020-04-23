from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer, CountVectorizerModel
from pyspark.ml.linalg import Vector, Vectors
import numpy as np
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F
from pyspark.ml.clustering import LDA, LocalLDAModel
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import re
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
from pyspark.sql.functions import udf
from LDA_train import *
from pyspark.sql.functions import split
from pyspark.sql.types import IntegerType
import pandas as pd

def ascii_ignore(x):
    return x.encode('ascii', 'ignore').decode('ascii')

ascii_udf = udf(ascii_ignore)

nltk.download('wordnet')

input_bucket = 's3://bucket4emr'
input_path = '/train.csv'
df = spark.read.csv(input_bucket + input_path, escape='"',sep=',',multiLine=True,header=True)

#df = df.withColumn("Text", ascii_udf('Text')).select(['_c0','Text']).withColumn("Text", split("Text", "\s+")).withColumn("_c0", df["_c0"].cast(IntegerType()))

#df.show()

#train_data = df


def token(text):
    result = []
    myStopwords = ["quarantine","corona","covid","stayhome","coronavirus","home","stay"]
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            #result.append(lemmatize_stemming(token))
            if token not in myStopwords:
                result.append((token))
    return result


def preprocess(posts):
        posts = str(posts)
        emoji_pattern = re.compile( u"(["                     # .* removed
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"(\\n)"
                                u"(#|@)"
                                "])", flags= re.UNICODE)
        posts = re.sub(r'[^a-zA-Z]+', ' ', posts, re.ASCII)
        posts = emoji_pattern.sub(u'', posts)

        return posts


train_data =[]
for row in df.rdd.collect():
    text = str(row["Text"])
    process = token(preprocess(text))
    train_data.append((row["_c0"],' '.join(process)))


topic_num=3
iter_num=2000

ldaModel, model, new_df = train(df,train_data,topic_num,iter_num)


topics = ldaModel.topicsMatrix()
vocabArray = model.vocabulary

new_df.toPandas().to_csv("db.csv")
ldaModel.write().overwrite().save("/home/hadoop/csce678-project/LDA/lda_model")
model.write().overwrite().save("/home/hadoop/csce678-project/LDA/token")

wordNumbers = 10  # number of words per topic

des = ldaModel.describeTopics(maxTermsPerTopic = wordNumbers)
topicIndices = des.select('termIndices').rdd

def topic_render(topic):  # specify vector id of words to actual words
    terms = topic[0]
    result = []
    for i in range(wordNumbers):
        term = vocabArray[terms[i]]
        result.append(term)
    return result

topics_final = topicIndices.map(lambda topic: topic_render(topic)).collect()

for topic in range(len(topics_final)):
    print ("Topic" + str(topic) + ":")
    for term in topics_final[topic]:
        print (term)
    print ('\n')
    

