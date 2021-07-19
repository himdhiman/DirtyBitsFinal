from asyncio.windows_events import NULL
from celery import shared_task
from api import models, serializers
from rest_framework.response import Response
import os
from pathlib import Path
from api.models import Problem, Submission
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json, requests, base64
from django.core import serializers as djSerializer

BASE_DIR = Path(__file__).resolve().parent.parent


channel_layer = get_channel_layer()

post_url = "http://18.233.92.170:2358/submissions/?base64_encoded=false&wait=true"


def encode_base64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

@shared_task
def runCode(body, uid):
    response = serializers.SubmissionSerializer(data = body)
    if(response.is_valid()):
        inst = response.save()

        if(inst.input_Given != ""):
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'inp' : inst.input_Given, 'problemId' : inst.problemId}
            post_data = {
                "source_code" : data["code"],
                "language_id" : 53,
                "stdin" : data["inp"]
            }
        
        else:
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'problemId' : inst.problemId}

        probId = data['problemId']
        totaltc = Problem.objects.get(id = probId).total_Tc

        isInputGiven = False

        if('inp' in data.keys() and data['inp'] != None):
            isInputGiven = True

        submission_string = ""
        tc_passed = ""
        error_string = ""
        out_gen = ""

        if(isInputGiven == False):
            count = 0
            for i in range(1, totaltc+1):
                inpPath = os.path.join(BASE_DIR, "media", 'TestCases', str(probId), 'input'+str(i)+'.txt')
                with open(inpPath) as f1:
                    input_data = f1.read();
                input_data = input_data.strip()
                post_data = {
                    "source_code" : data["code"],
                    "language_id" : 53,
                    "stdin" : input_data
                }
                response = requests.post(post_url, encode_base64(post_data))
                print(response.json())
                # print(base64.b64decode(response.json()["compile_output"]))

                submission_string = submission_string + response.json()["status"]["description"] + " ,"
                if response.json()["stdout"] != None:
                    out_data = response.json()["stdout"]
                    with open(os.path.join(BASE_DIR, "media", 'TestCases', str(probId), 'output'+str(i)+'.txt')) as f1:
                        data1 = f1.read()
                        data2 = out_data
                        if data1.strip() == data2.strip():
                            count += 1
                            async_to_sync(channel_layer.group_send)("user_"+uid, {'type': 'sendStatus', 'text' : f"1/{i}/{totaltc}"})
                        else:
                            async_to_sync(channel_layer.group_send)("user_"+uid, {'type': 'sendStatus', 'text' : f"0/{i}/{totaltc}"})
                else:
                    error_string = response.json()["stderr"]
                    async_to_sync(channel_layer.group_send)("user_"+uid, {'type': 'sendStatus', 'text' : response.json()["stderr"]})
        
            Submission.objects.filter(pk = data['id']).update(error = error_string, status = submission_string, test_Cases_Passed = count, total_Test_Cases = totaltc)


        else:
            response = requests.post(post_url, post_data)
            error_string = response.json()["stderr"]
            out_gen = response.json()["stdout"]
            submission_string = response.json()["status"]["description"]
            Submission.objects.filter(pk = data['id']).update(output_Generated = out_gen, status = submission_string)

        response = models.Submission.objects.filter(id = inst.id)
        async_to_sync(channel_layer.group_send)("user_"+uid, {'type': 'sendResult', 'text' : djSerializer.serialize('json', response)})
