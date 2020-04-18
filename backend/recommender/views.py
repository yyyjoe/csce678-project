from django.shortcuts import render
from .lda import LDA_APP
LDA = LDA_APP.LDA()

# Create your views here.
def index(request):

    my_dict = {"insert_content": "Hello iam from first app"}
    return render(request,"recommender/index.html",context=my_dict)

def post_recommender(request):

    user_id = request.GET['user_id']
    data = LDA.get_recommendation(user_id)

    return HttpResponse(data)