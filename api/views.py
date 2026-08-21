from django.views.generic import TemplateView
from .models import User  

from textblob import TextBlob
from nrclex import NRCLex
import nltk
nltk.data.path.append(os.path.join(settings.BASE_DIR, "nltk_data"))


class UserFormView(TemplateView):
    template_name = 'index.html'

    def detect_emotions(self, text):
        # ... your emotion detection code (same as before)
        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        emotion = NRCLex(text)
        emotion_scores = emotion.raw_emotion_scores
        dominant_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else None

        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "dominant_emotion": dominant_emotion,
            "emotion_scores": emotion_scores,
        }

    def post(self, request, *args, **kwargs):
        sentence = request.POST.get('sentence', '')
        emotions = self.detect_emotions(sentence)

        # Save to database
        user_entry = User.objects.create(
            sentence=sentence,
            polarity=emotions['polarity'],
            subjectivity=emotions['subjectivity'],
            dominant_emotion=emotions['dominant_emotion'],
            emotion_scores=emotions['emotion_scores']
        )

        context = self.get_context_data(sentence=sentence, emotions=emotions, saved=user_entry)
        return self.render_to_response(context)


from django.views.generic import ListView
from .models import User

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'  # create this template
    context_object_name = 'users'     # accessible in the template as 'users'
