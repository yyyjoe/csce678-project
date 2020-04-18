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
# nltk.download('wordnet', "/Users/jeff/nltk_data")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NUM_TOPICS=10

class LDA_APP(object):
    def __init__(self):
        nltk.download('wordnet')
        # LAD_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/lda_model.pkl")
        # self.lda_model_tfidf = models.LdaModel.load(LAD_DIR)

        # DIC_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/dictionary_model.dict")
        # self.dictionary = corpora.Dictionary.load(DIC_DIR)

        self.stemmer = PorterStemmer()
        self.NUM_TOPICS=10
        
        #DIC_DIR = os.path.join(BASE_DIR,"Good2Know/LDA_models/dataframe.csv")
        DIC_DIR = "/Users/jeff/Desktop/output.csv"
        self.db = pd.read_csv(DIC_DIR)

        #################
        self.NUM_TOPICS=10
        self.ldaModel = ??
        self.model = ??
    # # Define stemmer and Process
    def lemmatize_stemming(self,text):
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    # def preprocess(self,text):
    #     result = []
    #     for token in gensim.utils.simple_preprocess(text):
    #         if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
    #             result.append(self.lemmatize_stemming(token))
    #     return result

    def preprocess(self,posts):

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

        text = self.get_text(user_id)
        probability_v = self.get_topic_vector(text)
        app_json = self.get_similarity(probability_v)

        return app_json

    def get_text(self,user_id):
        post_num = 10
        text = user_account.get_user_post(user_id,post_num)
        
    def get_topic_vector(self,text):
        # text -> [[ID,Document]]
        text[0][1] = self.preprocess(text[0][1])
        rdd_test = sc.parallelize(text)
        data_test = rdd_test.map(lambda (idd,words): Row(idd = idd.split(" "), words = words.split(" ")))
        docDF_test = spark.createDataFrame(data_test)
        result_test = self.model.transform(docDF_test)

        Vector_id = CountVectorizer(inputCol="idd", outputCol="vectors_id")
        model_id_test = Vector_id.fit(result_test)
        result_test = model_id_test.transform(result_test)

        corpus_test = result_test.select("vectors_id", "vectors").rdd.map(lambda (x,y): [np.asscalar(np.where(x.toArray()==1)[0]) ,Vectors.sparse(y.size, y.indices, y.values)]).cache()
        columns = ['id', 'features']
        corpus_test = corpus_test.toDF(columns)

        transformed = self.ldaModel.transform(corpus_test)
        vector = transformed.select('topicDistribution').collect()[0][0]

        return vector

    def get_similarity(self,vector,k):
        # input vector is the probability distribution of each topic
        nums_of_posts=np.zeros(self.NUM_TOPICS,dtype=float)
        topic_id = np.arange(self.NUM_TOPICS)
        percentage = np.zeros(self.NUM_TOPICS,dtype=float)

        columns = ["ID","topic_distribution","Img_URL","Text","Date","Likes"]
        df = self.db.rdd.map(lambda row:((   row["ID"],
                                                float(row["topic_distribution"].dot(vector)),
                                                row["Img_URL"],
                                                row["Text"],
                                                row["Date"],
                                                row["Likes"],
                                                ))).toDF(columns)

        topk = df.orderBy('topic_distribution',ascending=False).take(k)

        data ={}
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
