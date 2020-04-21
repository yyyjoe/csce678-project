from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.linalg import Vector, Vectors
import numpy as np

from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F

from pyspark.ml.clustering import LDA
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import re
sc = SparkContext()
spark = SparkSession(sc)

input_bucket = 's3://bucket4emr'
input_path = '/train.csv'
df = spark.read.csv(input_bucket + input_path, escape='"',sep=',',multiLine=True,header=True)
df.show()

def token(text):
    result = []
    myStopwords = ["covid","stayhome","coronavirus","home","stay"]
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            #result.append(lemmatize_stemming(token))
            if token not in myStopwords:
                result.append((token))
    return result

def preprocess(posts):

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
    train_data.append((row["ID"],' '.join(process)))


print(train_data)