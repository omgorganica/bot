from django.db import models


class ShiftUser(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShiftUser, on_delete=models.CASCADE, related_name='user_ids')
    score = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Question(models.Model):
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return str(self.text)


class Result(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE,related_name='shifts')
    user = models.ForeignKey(ShiftUser, on_delete=models.CASCADE, related_name='users')
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions')
    result = models.BooleanField()

    def __str__(self):
        return f'{self.shift},{self.question},{self.result}'
