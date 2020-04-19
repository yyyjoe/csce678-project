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

train_data = []
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
count=0
for row in df.rdd.collect():
    t = (row["ID"],preprocess(str(row["Text"])))
    train_data.append(t)









