from pyspark import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext()
spark = SparkSession(sc)
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.linalg import Vector, Vectors
import numpy as np

from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F

from pyspark.ml.clustering import LDA
from pyspark.sql.types import *
from pyspark.sql.functions import udf

from pyspark.sql.functions import col

def train(df,text, topic_num, iter_num):
    rdd_ = sc.parallelize(text)
    data = rdd_.map(lambda kv: Row(idd = int(kv[0]), Text = kv[1].split(" ")))

    docDF = spark.createDataFrame(data)
    Vector = CountVectorizer(inputCol="Text", outputCol="vectors")
    model = Vector.fit(docDF)
    result = model.transform(docDF)


    corpus = result.select("idd", "vectors").rdd.map(lambda xy: [xy[0], Vectors.sparse(xy[1].size, xy[1].indices, xy[1].values)]).cache()
    columns = ['id', 'features']
    corpus = corpus.toDF(columns)
    # corpus.printSchema()
    # corpus.show()


    # # Cluster the documents into three topics using LDA

    # from pyspark.ml.clustering import LDA

    lda = LDA(k = topic_num, maxIter = iter_num)
    ldaModel = lda.fit(corpus)

    topics = ldaModel.describeTopics(3)
    print("The topics described by their top-weighted terms:")
    topics.show()

    transformed = ldaModel.transform(corpus)
    transformed = transformed.select(col("Id").alias("_c0"),col("topicDistribution"))
    #transformed.show()
    new_df = df.join(transformed, on=['_c0'], how='left_outer')
    new_df = new_df.filter(col('ID').isin(['B-jsAw8AkiL']) == False)

    return (ldaModel, model, new_df)
