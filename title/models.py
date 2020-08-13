from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Title(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name = "Başlığı Oluşturan")
    title_name = models.CharField(max_length=30, verbose_name="Başlığın Adı")
    title_bound = models.IntegerField(verbose_name="Yorum Sınırı")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.title_name
    
    class Meta:
        ordering = ['-created_date']

    def get_comment_count(self):
        comment_size = self.comment.count()
        if comment_size > 0 :
            return comment_size
        return "0"

class Comment(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name = "Başlık", related_name="comment")
    comment_author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name= "Yorum Yapan")
    comment_content = models.CharField(max_length=200, verbose_name="Yapılan Yorum")
    sentiment = models.CharField(max_length=20, verbose_name="Duygu Analizi")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Yorum Yapma Tarihi")

    class Meta:
        ordering = ['-comment_date']

class SentimentTotalSystem(models.Model):
    title = models.OneToOneField(Title,on_delete=models.CASCADE, null = True, blank=False, verbose_name= 'Title')
    positive_count = models.IntegerField(verbose_name='Total Positive')
    negative_count = models.IntegerField(verbose_name= 'Total Negative')
    notr_count = models.IntegerField(verbose_name= 'Total Notr')