from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.linalg import Vector, Vectors
import numpy as np

from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F

from pyspark.ml.clustering import LDA
from pyspark.sql.types import *
from pyspark.sql.functions import udf



def train(text):
    rdd_ = sc.parallelize(l)
    # data = rdd.map(lambda x: Row(id=x[0], text=x[1]))

    data = rdd_.map(lambda (idd,words): Row(idd = idd.split(" "), words = words.split(" ")))
    docDF = spark.createDataFrame(data)
    # docDF.show()
    Vector = CountVectorizer(inputCol="words", outputCol="vectors")
    model = Vector.fit(docDF)
    result = model.transform(docDF)

    Vector_id = CountVectorizer(inputCol="idd", outputCol="vectors_id")
    model_id = Vector_id.fit(result)
    result = model_id.transform(result)
    # result.show()

    corpus = result.select("vectors_id", "vectors").rdd.map(lambda (x,y): [np.asscalar(np.where(x.toArray()==1)[0]) ,Vectors.sparse(y.size, y.indices, y.values)]).cache()
    columns = ['id', 'features']
    corpus = corpus.toDF(columns)
    # corpus.printSchema()
    # corpus.show()


    # # Cluster the documents into three topics using LDA

    # from pyspark.ml.clustering import LDA

    lda = LDA(k=10, maxIter=10)
    ldaModel = lda.fit(corpus)

    topics = ldaModel.describeTopics(3)
    print("The topics described by their top-weighted terms:")
    topics.show()

    return (ldaModel, model)

