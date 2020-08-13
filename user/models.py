from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class MailControl(models.Model):
    token = models.CharField(max_length=100, verbose_name="Hesap aktifleştirme")
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token_date = models.DateTimeField(auto_now_add=True, verbose_name="Token Oluşturma Tarihi")

class EnterpriseUserProfile(models.Model):
    SECTOR = ((None, 'Sektör Seçiniz'), ('belediye', 'BELEDİYE'), ('eğitim', 'EĞİTİM'), ('eğlence', 'EĞLENCE'), ('girişim', 'GİRİŞİM'), ('hizmet', 'HİZMET'), ('sağlık', 'SAĞLIK'), ('sanayi', 'SANAYİ'), ('sivil toplum örgütü', 'SİVİL TOPLUM ÖRGÜTÜ'), ('teknoloji', 'TEKNOLOJİ'))
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, verbose_name='Hakkımızda', blank=False, null=True)
    profile_photo = models.ImageField(upload_to="user_profile" ,blank = True, verbose_name='Profil Fotoğrafı')
    sector = models.CharField(choices=SECTOR, blank=False, null=True, max_length=20, verbose_name='Sektör')
    email_confirmation = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Kurumsal Kullanici Profili'


class PersonalUserProfile(models.Model):
    SEX = ((None, 'Cinsiyet Seçiniz'), ('diğer', 'DİĞER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN'))
    user = models.OneToOneField(User,on_delete=models.CASCADE, null = True, blank=False, verbose_name= 'User')
    name = models.CharField(max_length=50, verbose_name="Ad")
    surname = models.CharField(max_length=25, verbose_name="Soyad")
    profile_photo = models.ImageField(upload_to="user_profile" ,blank = True, verbose_name='Profil Fotoğrafı')
    age = models.IntegerField(verbose_name="Yaş")
    sex = models.CharField(choices=SEX, blank=False, null=True, max_length=6, verbose_name='Cinsiyet')

    class Meta:
        verbose_name_plural = 'Bireysel Kullanici Profili'
    
    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/images/default.jpg"

class PersonalAwardSystem(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null = True, blank=False, verbose_name= 'User')
    total_comment = models.IntegerField(verbose_name='Total Comment')
    is_gold = models.BooleanField(default=False)
    is_silver = models.BooleanField(default=False)
    is_bronze = models.BooleanField(default=False)
    positive_count = models.IntegerField(verbose_name='Total Positive')
    negative_count = models.IntegerField(verbose_name= 'Total Negative')
    notr_count = models.IntegerField(verbose_name= 'Total Notr')

class user_type(models.Model):
    is_enterprises = models.BooleanField(default=False)
    is_personals = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        if self.is_enterprises == True:
            return User.username(self.user) + " - is_enterprises"
        else:
            return User.username(self.user) + " - is_personals" 