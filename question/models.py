from django.db import models

# Create your models here.


class Tag(models.Model):
    word = models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(self.word)


class Owner(models.Model):
    reputation = models.IntegerField()
    user_type = models.CharField(max_length=255)
    profile_image= models.URLField()
    display_name= models.CharField(max_length=255)
    link= models.URLField()
    
    def __str__(self):
        return(self.display_name)


class Question(models.Model):
    is_answered=models.CharField(max_length=255)
    view_count= models.IntegerField()
    closed_date= models.DateField(blank=True,null=True)
    answer_count= models.IntegerField()
    score= models.IntegerField()
    last_activity_date= models.DateField()
    creation_date= models.DateField()
    question_id = models.PositiveIntegerField()
    link= models.URLField()
    closed_reason= models.CharField(max_length=255,blank=True,null=True)
    title= models.CharField(max_length=255)
    display_name= models.CharField(max_length=255)
    search_term= models.CharField(max_length=255,blank=True,null=True)

    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(self.title)
