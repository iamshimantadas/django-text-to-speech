from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
from core.models import TextToSpeech
from datetime import datetime
from ipware import get_client_ip
import os
import hashlib


def Home(request):
    if request.method == "POST":
        data = request.POST
        print(data)

        text = data.get("text")
        lang = data.get("lang")

        myobj = gTTS(text=text, lang=f"{lang}", slow=False)


        if not os.path.exists("media"):
            os.makedirs("media")
            
        filename = hashlib.md5(text.encode()).hexdigest() + ".mp3"
        while os.path.exists(os.path.join("media", filename)):
            filename = hashlib.md5(os.urandom(32)).hexdigest() + ".mp3"

        file_path = os.path.join("media", filename)
        myobj.save(file_path)
            
        
        try:
            obj = TextToSpeech.objects.create(
                input_text=text,
                lang=lang,
                audio_path=file_path,
                loc=get_client_ip(request),
                datetime=datetime.now(),
            )
            obj.save()
        except Exception as e:
            print(e)
            return HttpResponse("error occured")
        
        domain = request.build_absolute_uri('/')
        print(domain)
        file_path = domain+'/'+file_path
        return HttpResponse(f"<a href='{file_path}' download>click here to download</a>")
    else:
        language_list = {
            "af": "Afrikaans",
            "ar": "Arabic",
            "bn": "Bengali",
            "bs": "Bosnian",
            "ca": "Catalan",
            "cs": "Czech",
            "cy": "Welsh",
            "da": "Danish",
            "de": "German",
            "el": "Greek",
            "en": "English",
            "eo": "Esperanto",
            "es": "Spanish",
            "et": "Estonian",
            "fi": "Finnish",
            "fr": "French",
            "gu": "Gujarati",
            "hi": "Hindi",
            "hr": "Croatian",
            "hu": "Hungarian",
            "hy": "Armenian",
            "id": "Indonesian",
            "is": "Icelandic",
            "it": "Italian",
            "ja": "Japanese",
            "jw": "Javanese",
            "km": "Khmer",
            "kn": "Kannada",
            "ko": "Korean",
            "la": "Latin",
            "lv": "Latvian",
            "mk": "Macedonian",
            "ml": "Malayalam",
            "mr": "Marathi",
            "my": "Myanmar (Burmese)",
            "ne": "Nepali",
            "nl": "Dutch",
            "no": "Norwegian",
            "pl": "Polish",
            "pt": "Portuguese",
            "ro": "Romanian",
            "ru": "Russian",
            "si": "Sinhala",
            "sk": "Slovak",
            "sq": "Albanian",
            "sr": "Serbian",
            "su": "Sundanese",
            "sv": "Swedish",
            "sw": "Swahili",
            "ta": "Tamil",
            "te": "Telugu",
            "th": "Thai",
            "tl": "Filipino",
            "tr": "Turkish",
            "uk": "Ukrainian",
            "ur": "Urdu",
            "vi": "Vietnamese",
            "zh-CN": "Chinese",
        }

    context = {"language_list": language_list}

    return render(request, "home.html", context)
