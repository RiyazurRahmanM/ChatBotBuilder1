from django.shortcuts import render
import os
import openai
from dotenv import load_dotenv
from django.db import models
from .models import Messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

load_dotenv()

openai_api_key = "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"
openai.api_key = openai_api_key

@xframe_options_exempt
def chatbot_view(request):
    messages = Messages.objects.filter(chatbot_name=request.GET.get('cname'))
    loop=1
    input_messages = []

    if openai_api_key is not None and request.method != "POST":
        for message in messages:

            system_message = message.system_message
            if loop==0:
                input_message = message.input_message
                output_message = message.output_message
                input_messages.append(
                    {"role":"user","content":f"{input_message}"}
                    )
                input_messages.append(
                    {'role':"assistant","content":f"{output_message}"},
                )
            if loop == 1:
                input_messages.append(
                    {"role":"system","content":f"{system_message}"}
                    )
                initial_message= message.initial_message
                system_message = message.system_message
                loop = 0

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = input_messages,
            temperature = 0,
            max_tokens = 100,
        )
        print(input_messages)
        return render(request,'chatbot.html',{'messages':messages})
    
    loop = 1
    if openai_api_key is not None and request.method == "POST":
        for message in messages:

            system_message = message.system_message
            if loop==0:
                input_message = message.input_message
                output_message = message.output_message
                input_messages.append(
                    {"role":"user","content":f"{input_message}"}
                    )
                input_messages.append(
                    {'role':"assistant","content":f"{output_message}"},
                )
            if loop == 1:
                input_messages.append(
                    {"role":"system","content":f"{system_message}"}
                    )
                initial_message= message.initial_message
                system_message = message.system_message
                loop = 0

        user_prompt = request.POST.get('user_prompt','')
        input_messages.append({"role":"user","content":f"{user_prompt}"})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = input_messages,
            temperature = 0,
            max_tokens = 100,
        )
        print(input_messages)
        message = Messages(chatbot_name=request.GET.get('cname'), initial_message=f"{initial_message}", system_message=f"{system_message}", input_message=f"{user_prompt}",output_message=response["choices"][0]["message"]["content"])
        message.save()
        messages = Messages.objects.filter(chatbot_name=request.GET.get('cname'))
        return render(request,'chatbot.html',{'messages':messages})
    

    return render(request,'chatbot.html',{'messages':messages})
def home_view(request):
     
    #Database Section:
    message = Messages()
    message.system_message = str(request.session.get('niche'))
    message.initial_message = str(request.session.get('imess'))
    message.chatbot_name = str(request.session.get('cname'))
    message.save()
    #Converstion Section:
    cname = str(request.session.get('cname'))
    return render(request,'home.html',{'cname': cname })
    


def create_view(request):
    return render(request,'create.html')
    
def myform_view(request):
    if request.method == "POST":
        request.session['cname'] = request.POST.get('cname')
        request.session['imess'] = request.POST.get('imess')
        request.session['nomess'] = request.POST.get('nomess')
        niche = request.POST.get('niche')
        dfeed = request.POST.get('dfeed')
        niche += "Additional Data related to niche: =>"
        niche += dfeed
        niche += " If the user is asking irrelevent questions that are not relate to the niche of chatbot. you just have to reply => "
        nomess = request.POST.get('nomess')
        niche += nomess
        request.session['niche'] =  niche 
        return HttpResponseRedirect(reverse('dfeed_view'))
    return render(request, 'myform.html')



