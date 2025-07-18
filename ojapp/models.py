from django.db import models
from django.conf import settings

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question.question_text} -> {self.choice_text}"
    
class Problems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    examples = models.TextField()
    
    def __str__(self):
        return self.name
    

