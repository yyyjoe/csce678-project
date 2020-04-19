from pyspark import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext()
spark = SparkSession(sc)
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer, CountVectorizerModel
from pyspark.ml.linalg import Vector, Vectors
import numpy as np

from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F

from pyspark.ml.clustering import LDA, LocalLDAModel
from pyspark.sql.types import *
from pyspark.sql.functions import udf



ldaModel_path = "lda_model"
ldaModel = LocalLDAModel.load(ldaModel_path)
model_path = "token"
model = CountVectorizerModel.load(model_path)


l_test=[(1,"I fucking hate covid-19")]

def test(text, ldaModel, model):
    rdd_ = sc.parallelize(text)
    data = rdd_.map(lambda kv: Row(idd = kv[0], Text = kv[1].split(" ")))
    docDF = spark.createDataFrame(data)
    result = model.transform(docDF)


    corpus = result.select("idd", "vectors").rdd.map(lambda xy: [xy[0], Vectors.sparse(xy[1].size, xy[1].indices, xy[1].values)]).cache()
    columns = ['id', 'features']
    corpus = corpus.toDF(columns)

    transformed = ldaModel.transform(corpus)
    transformed.show()

#     ldaModel.transform(corpus).show()

test(l_test, ldaModel, model)
