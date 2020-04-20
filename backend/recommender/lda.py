from pyspark import SparkContext, sql
from pyspark.mllib.linalg import DenseVector
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer, CountVectorizerModel
from pyspark.ml.linalg import Vector, Vectors
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as F
from pyspark.ml.clustering import LDA, LocalLDAModel
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import re
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import os
import json
import nltk
from . import user_account
# nltk.download('wordnet')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sc = SparkContext()
spark = SparkSession(sc)

class LDA_APP(object):
    def __init__(self):
        self.NUM_TOPICS=3

        db_path = "/home/hadoop/csce678-project/LDA/db.csv"

        df = pd.read_csv(db_path,lineterminator='\n')
        self.db = spark.createDataFrame(df)

        ldaModel_path = "/home/hadoop/csce678-project/LDA/lda_model"
        self.ldaModel = LocalLDAModel.load(ldaModel_path)

        model_path = "/home/hadoop/csce678-project/LDA/token"
        self.model = CountVectorizerModel.load(model_path)

    def lemmatize_stemming(self,text):
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    def token(self,text):
        result = []
        myStopwords = ["quarantine","corona","covid","stayhome","coronavirus","home","stay"]
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                #result.append(lemmatize_stemming(token))
                if token not in myStopwords:
                    result.append((token))
        return result

    def preprocess(self,posts):
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

    def get_recommendation(self,user_id):
        print("process: ",user_id)
        text = self.get_text(user_id)
        probability_v = self.get_topic_vector(text)
        app_json = self.get_similarity(probability_v,10)

        return app_json

    def get_text(self,user_id):
        post_num = 10
        text = user_account.get_user_post(user_id,post_num)
        return text

    def get_topic_vector(self,text):
        # text -> [[ID,Document]]
        text[0][1] = " ".join(self.token(self.preprocess(text[0][1])))

        rdd_ = sc.parallelize(text)
        data = rdd_.map(lambda kv: Row(idd = kv[0], Text = kv[1].split(" ")))
        docDF = spark.createDataFrame(data)
        result = self.model.transform(docDF)


        corpus = result.select("idd", "vectors").rdd.map(lambda xy: [xy[0], Vectors.sparse(xy[1].size, xy[1].indices, xy[1].values)]).cache()
        columns = ['id', 'features']
        corpus = corpus.toDF(columns)
        transformed = self.ldaModel.transform(corpus)
        vector = transformed.select('topicDistribution').collect()[0][0]

        return vector
    
    def get_similarity(self,vector,k):
        # input vector is the probability distribution of each topic
        nums_of_posts=np.zeros(self.NUM_TOPICS,dtype=float)
        topic_id = np.arange(self.NUM_TOPICS)
        percentage = np.zeros(self.NUM_TOPICS,dtype=float)
        columns = ["ID","topicDistribution","Img_URL","Text","Date","Likes"]
        df = self.db.rdd.map(lambda row:((   row["ID"],
                                                float(np.fromstring(row["topicDistribution"][1:-1], dtype=np.float, sep=',').dot(vector)),
                                                row["Img_URL"],
                                                row["Text"],
                                                row["Date"],
                                                row["Likes"],
                                                ))).toDF(columns)
        topk = df.orderBy('topicDistribution',ascending=False).take(k)

        data ={}
        data["num_topics"] = self.NUM_TOPICS
        data["topics"] = {}
        data["posts"] = []
        data["topics"]["labels"] = list(topic_id)
        data["topics"]["data"] = list(vector)

        for row in topk:
            data["posts"].append({'userID':row[0],
                                  'imgURL':row[2],
                                  'text':row[3],
                                  'date':row[4],
                                  'like':row[5],
                                 })

        app_json = json.dumps(str(data))

        return app_json