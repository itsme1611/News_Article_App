import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings


def read_articles(request):

    """
        News article API, integrated news.org 
    """

    page = request.GET.get('page', 1)
    search = request.POST.get('search', None)
    
    if search is None or search=="top":
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us",1,settings.NEWS_API_KEY
        )
    else:
        # get the search query request
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search,"publishedAt",page,settings.NEWS_API_KEY
        )
    r = requests.get(url=url)

    data = r.json()
    
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    # seprating the necessary data
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": "" if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    # send the news feed to template in context
    return render(request, 'index.html', context=context)



def refreshcontent(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&NEWS_API_KEY={}".format(
        #     "Technology","popularity",page,settings.NEWS_API_KEY
        # )
        if search is None or search=="top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",page,settings.NEWS_API_KEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search,"publishedAt",page,settings.NEWS_API_KEY
            )
        print("url:",url)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success":False})
        data = data["articles"]
        context = {
            "success": True,
            "data": [],
            "search": search
        }
        for i in data:
            context["data"].append({
                "title": i["title"],
                "description":  "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": "" if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"]
            })

        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success":False})