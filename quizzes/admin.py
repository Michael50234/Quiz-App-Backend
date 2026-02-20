from django.contrib import admin
from .models import Tag, Quiz, Question, Choice, Submission
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Tag)
admin.site.register(Submission)