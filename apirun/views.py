from django.shortcuts import *
from django.http import *
from django.core.paginator import Paginator
from django.core import serializers
from apiclient.discovery import build
import googleapiclient
from datetime import datetime
import threading
from django.apps import apps

API_KEYS=["AIzaSyAuTIE9X4f-gqKns4H3HGaMtf4r_AfhH3A","AIzaSyB3pucSsGKPRr4wSjj4-kN9vF1i3gHJf4E","AIzaSyA-3-2Jla42RP5CSBI7E31nfPWN81jA1MY","AIzaSyCaJJ5z6TPcljmRAPyPG34Drc_bDVRnjd0"]

# Thread To Fetch Data From YouTube Api After every 10 sec
def fetchVideo(api_key=API_KEYS[0]):
    threading.Timer(10.0, fetchVideo).start()
    try:
        youtube = build('youtube','v3',developerKey=api_key)
        req = youtube.search().list(q='nick jonas',part='snippet',type='video')
        context = req.execute()

        video_list = context["items"]

        for video_obj in video_list:
            title = video_obj["snippet"]["title"]
            description = video_obj["snippet"]["description"]
            thumbnail_url = video_obj["snippet"]["thumbnails"]["default"]["url"]

            datetime_string = video_obj["snippet"]["publishedAt"]
            str1 = datetime_string.split("-")[0]
            datetime_string = datetime_string.replace("T"," ")
            datetime_string = datetime_string.replace("Z","")
            datetime_string = datetime_string.replace(str1,str1[2:])
            publishedAt = datetime.strptime(datetime_string, '%y-%m-%d %H:%M:%S')

            Video = apps.get_model('apirun', 'Video')
            # store the data in database if the data not exists there
            if len(Video.objects.filter(title=title,description=description,thumbnail_url=thumbnail_url))==0:
                video = Video(title=title,description=description,thumbnail_url=thumbnail_url,publishedAt=publishedAt)
                video.save()

    # change the api key when qouta get exhausted
    except googleapiclient.errors.HttpError:
        api_keys = API_KEYS[:]
        api_keys.remove(api_key)
        if(len(api_keys)):
            fetchVideo(api_key[0])
            return

# view api which gives all the stored video data 
# in a paginated response 
def viewvideo(request):
    page_number = request.GET.get('page')
    if(page_number is None):
        page_number=1
    else:
        page_number=int(page_number)

    Video = apps.get_model('apirun', 'Video')
    video_list = Video.objects.all().order_by('-publishedAt')

    paginator = Paginator(video_list,10) # Show 10 videos per page.
    
    if(page_number<=paginator.num_pages):
        page_obj = paginator.get_page(page_number)
        videos_per_page = serializers.serialize('json', page_obj.object_list)
        return HttpResponse(videos_per_page, content_type="text/json-comment-filtered")
    else:
        page_obj = paginator.get_page(1)
        videos_per_page = serializers.serialize('json', page_obj.object_list)
        return HttpResponse(videos_per_page, content_type="text/json-comment-filtered")


# search Api which gives stored video data 
# according to search query q
def search(request):
    q = request.GET["q"]
    query_substr = q.split(" ")

    Video = apps.get_model('apirun', 'Video')

    all_videos = set()
    for substr in query_substr:
        if not (len(substr)==0):
            all_videos_title = Video.objects.filter(title__icontains=substr)
            all_videos_description = Video.objects.filter(description__icontains=substr)
            substr=substr.lower()
            all_videos_title2 = Video.objects.filter(title__icontains=substr)
            all_videos_description2 = Video.objects.filter(description__icontains=substr)

            if all_videos_title:
                for video in all_videos_title:
                    all_videos.add(video)
            if all_videos_description:
                for video in all_videos_description:
                    all_videos.add(video)
            if all_videos_description2:
                for video in all_videos_description2:
                    all_videos.add(video)
            if all_videos_title2:
                for video in all_videos_title2:
                    all_videos.add(video)
    all_videos_list = serializers.serialize('json', all_videos)
    return HttpResponse(all_videos_list, content_type="text/json-comment-filtered")


# to view search results 
# on the webpage use search bar
def searchmain(request):
    return render(request,'apirun/search.html')

# show search results on the web page
def searchview(request):
    q = request.GET["q"]
    query_substr = q.split(" ")

    Video = apps.get_model('apirun', 'Video')

    all_videos = set()

    for substr in query_substr:
        if not (len(substr)==0):
            all_videos_title = Video.objects.filter(title__icontains=substr)
            all_videos_description = Video.objects.filter(description__icontains=substr)
            substr=substr.lower()
            all_videos_title2 = Video.objects.filter(title__icontains=substr)
            all_videos_description2 = Video.objects.filter(description__icontains=substr)

            if all_videos_title:
                for video in all_videos_title:
                    all_videos.add(video)
            if all_videos_description:
                for video in all_videos_description:
                    all_videos.add(video)
            if all_videos_description2:
                for video in all_videos_description2:
                    all_videos.add(video)
            if all_videos_title2:
                for video in all_videos_title2:
                    all_videos.add(video)
    context={
        "all_videos":all_videos
    }
    return render(request,'apirun/searchresults.html',context)

# show all the videos stored in database 
# allows filter option to view filtered data (via title)
def index(request):
    page_number = request.GET.get('page')
    if(page_number is None):
        page_number=1
    else:
        page_number=int(page_number)

    Video = apps.get_model('apirun', 'Video')
    video_list = Video.objects.all().order_by('-publishedAt')
    return render(request,'apirun/index.html',{"video_list":video_list})


# perform filtering for the dashboard
def filteraction(request):
    keyword = request.GET["keyword"]
    Video = apps.get_model('apirun', 'Video')
    video_list = Video.objects.filter(title__icontains=keyword).order_by('-publishedAt')

    video_obj_list=[]

    for video in video_list:
        video_obj={}
        video_obj["title"]=video.title
        video_obj["description"]=video.description
        video_obj["publishedAt"]=video.publishedAt
        video_obj["thumbnail_url"]=video.thumbnail_url
        video_obj_list.append(video_obj)

    context={
        "video_list":video_obj_list
    }
    return JsonResponse(context)