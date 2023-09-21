from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# pytube will help us to get the title and the audio file of the video - package
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from decouple import config
import openai
from .models import SavedSummary

# Create your views here.

AAI_KEY = config('AAI_KEY')
GPT_KEY = config('GPT_KEY')

@login_required
def index(request):
    return render(request, 'index.html')


# used to get the title of the video 
def get_title(link):
    yt = YouTube(link)
    title = yt.title
    return title


# to extract the audio file of the video
# we will download the audio file for aai to generate the transcript - will be saved in the media folder
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(file)
    audio_file = base + '.mp3'
    os.rename(file, audio_file)
    return audio_file


# used to get the transcript of the video
def get_transcript(link):
    # we will genarate the transcript of the video from the audio file of the video
    audio_file = download_audio(link)
    aai.settings.api_key = AAI_KEY

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcript.text



# to convert the transcript to summaries using the openai 
def generate_summary(transcription):
    openai.api_key = GPT_KEY

    # we pass prompt to the api in the following manner
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    # modifying the response according to our needs
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )

    generated_content = response.choices[0].text.strip()

    return generated_content



@csrf_exempt
def genarate_summary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            link = data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data provided!'}, status=400)
        
        # getting the title of the video
        title = get_title(link)

        # getting the transcript of the video
        transcription = get_transcript(link)
        if not transcription:
            return JsonResponse({'error': 'Failed to get transcription!'}, status=500)
        
        # generating the summary using openai
        content = genarate_summary(transcription)
        if not content:
            return JsonResponse({'error': 'Failed to generate summary!!'}, status=500)
        
        # saving the generated summary of the video
        new_summary = SavedSummary.objects.create(
            user=request.user,
            yt_title=title,
            yt_link=link, 
            generated_content=content
        )
        new_summary.save()
        
        return JsonResponse({'content': content})
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    


# user login logic
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')



# user signup logic 
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatPassword']

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            
            except:
                error_message = "Error while creating your account!"
                return render(request, 'signup.html', {'error_message': error_message})
            
        else:
            error_message = 'Password donot match!'
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')



# user logout logic
def user_logout(request):
    logout(request)
    return redirect("/")
