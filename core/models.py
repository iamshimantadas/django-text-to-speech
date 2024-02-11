from django.db import models

class TextToSpeech(models.Model):
    input_text = models.TextField()
    lang = models.CharField(max_length=10)
    audio_path = models.FileField(upload_to="media/")
    datetime = models.DateTimeField()
    loc = models.CharField(max_length=10)

    def __str__(self):
        return self.input_text
