from django.shortcuts import render
from pathlib import Path
from api import forms, models, serializers
import os, shutil, json, requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

BASE_DIR = Path(__file__).resolve().parent.parent

CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = '415b0230b4e38407f9b0d93f866a940206869e03'

def upload_tc(request):
    if request.method == "POST":
        form = forms.TcUpload(request.POST, request.FILES)
        files = request.FILES.getlist("testcases")
        ProbId = request.POST['name']
        if form.is_valid():
            for f in files:
                file_instance = models.UploadTC(name = models.Problem.objects.get(pk = int(ProbId)), testcases=f)
                file_instance.save()
        files_list = os.listdir(os.path.join(BASE_DIR, 'media/tempTC'))
        if(os.path.isdir(os.path.join(BASE_DIR, "media", "TestCases", ProbId))):
            shutil.rmtree(os.path.join(BASE_DIR, "media", "TestCases", ProbId))
        os.mkdir(os.path.join(BASE_DIR, "media", "TestCases", ProbId))
        for f in files_list:
            shutil.move(os.path.join(BASE_DIR, "media", "tempTC", f), os.path.join(BASE_DIR, "media", "TestCases", ProbId))
    else:
        form = forms.TcUpload()
    return render(request, "upload.html", {"form": form})


@api_view(["GET", "POST"])
def getData(request):
    body = json.loads(request.body)
    if(body['type'] == "list"):
        s = set()
        for i in body['tags']:
            tagId = models.Tag.objects.get(name=i)
            c = models.Problem.objects.filter(tags=tagId.id).values_list('id', flat=True)
            for i in c:
                qs = models.Problem.objects.get(pk=i)
                s.add(qs.id)
        final_qs = models.Problem.objects.filter(id__in = s);
        res = serializers.ProblemSerializer(final_qs, many = True)
        return Response(res.data)
    else:
        probId = body["id"]
        q = models.Problem.objects.get(id = probId)
        res = serializers.ProblemSerializer(q)
        return Response(res.data)


def execute(source_file_name, language):
    source = open(source_file_name, "r")
    input_file = open("input.txt", "r")
    callback = "https://client.com/callback/"

    data = {    
        'source': source.read(),
        'lang': language,
        'time_limit': 5,
        'memory_limit': 246323,
        'input': input_file.read(),
        'callback' : callback,
        'id': "client-001"
    }
    headers = {"client-secret": CLIENT_SECRET}
    input_file.close()
    source.close()
    resp = requests.post(CODE_EVALUATION_URL, json=data, headers=headers)
    """
    This will also work:
    resp = requests.post(CODE_EVALUATION_URL, data=data, headers=headers)
    """
    dict = json.loads(resp.text)
    return dict




@api_view(['POST'])
def runCode(request, uid):
    body = json.loads(request.body)
    # tasks.runCode.delay(body, uid)
    return Response()
