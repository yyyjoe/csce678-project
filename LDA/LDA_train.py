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



def train(docDF, topic_num, iter_num):
    Vector = CountVectorizer(inputCol="Text", outputCol="vectors")
    model = Vector.fit(docDF)
    result = model.transform(docDF)


    corpus = result.select("_c0", "vectors").rdd.map(lambda xy: [xy[0], Vectors.sparse(xy[1].size, xy[1].indices, xy[1].values)]).cache()
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

    return (ldaModel, model)
