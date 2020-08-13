from django import forms
from django.contrib.auth.models import User
import re
from . models import EnterpriseUserProfile, PersonalUserProfile


class EnterpriseRegisterForm(forms.Form):
    username = forms.CharField(max_length=30, label="Kurum Adı")
    email = forms.EmailField(label = "Mail Adresi")
    sector = forms.ChoiceField(required=True, choices=EnterpriseUserProfile.SECTOR)
    bio = forms.CharField(max_length=1000, label ='Hakkımızda', widget = forms.Textarea)
    profile_photo = forms.ImageField(label="Profil Fotoğrafı")
    password = forms.CharField(max_length=20, label="Parola", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label= "Parola Doğrulama", widget = forms.PasswordInput)

    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if  ".com" in email: #.com.tr olacak
            return email

        elif ".edu.tr" in email:
            return email
        
        elif ".org" in email:
            return email
        
        elif ".org.tr" in email:
            return email
        
        elif ".bel.tr" in email:
            return email
        raise forms.ValidationError("Malesef gönderilen e-posta alan adınız geçersiz. E-postanızın alan adı sistemde bulunmamaktadır.")

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")

        #en son metin kontrolü gelecek.

        if len(bio) < 30:
            raise forms.ValidationError("En Az 30 Karakter Olmalıdır.")

    def clean(self): #clean methodu şifrelrin aynı olup olmadığını göstermek ve
        username = self.cleaned_data.get("username") #submit edilmeden önce görülecek demektir.
        email = self.cleaned_data.get("email")
        sector = self.cleaned_data.get("sector")
        bio = self.cleaned_data.get("bio")
        profile_photo = self.cleaned_data.get("profile_photo")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmedi.")
        
        elif len(password) < 8:
            raise forms.ValidationError("Parolanız 8 karakterden küçük olmamalıdır.")

        elif re.search('[0-9]', password) is None:
             raise forms.ValidationError("Parolanızda en az bir sayı olduğundan emin olun.")
        
        elif re.search('[A-Z]', password) is None:
            raise forms.ValidationError("Parolanızda en az bir büyük harf olduğundan emin olun.")

        elif User.objects.filter(username = username).exists():
            raise forms.ValidationError("Girmiş olduğnuz kurum adı sistemde mevcuttur.")
        
        
        #elif User.objects.filter(email = email).exists():
            #raise forms.ValidationError("Bu mail adresi sistemde kayıtlıdır.")


        values = {          #yukarıdkai değerleri bir sonraki sayfada aktarabilmem için değerleri sözlük içerisnde oluşturmam gerekiyor.
            "username" : username,
            "email" : email,
            "sector" : sector,
            "bio" : bio,
            "profile_photo" : profile_photo,
            "password" : password,
        }

        return values

class EnterpriseUserProfileUpdateForm(forms.ModelForm):
    sector = forms.ChoiceField(required=True, choices=EnterpriseUserProfile.SECTOR)
    bio = forms.CharField(required=False,max_length=1000, label ='Hakkımızda', widget = forms.Textarea)
    profile_photo = forms.ImageField(required=False,label="Profil Fotoğrafı")

    
    class Meta:
        model = User
        fields = ['username','sector', 'bio' ,'profile_photo']

class EnterpriseUserPasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(required=True,max_length=20, label="Mevcut Parolanız", widget = forms.PasswordInput)
    new_password = forms.CharField(required=True,max_length=20, label="Yeni Parolanız", widget = forms.PasswordInput)
    new_confirm_password = forms.CharField(required=True,max_length=20, label="Yeni Parola Doğrulama", widget = forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user #içerideki değeri dışarıda kullanmak için
        super(EnterpriseUserPasswordChangeForm, self).__init__(*args,**kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_confirm_password = self.cleaned_data.get('new_confirm_password')

        if new_password and new_confirm_password and new_password != new_confirm_password:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        elif len(new_password) < 8:
            raise forms.ValidationError("8'den Küçük Karakter Bulunmaktadır.")

        elif re.search('[0-9]', new_password) is None:
             raise forms.ValidationError("Parolanızda bir sayı olduğundan emin olun")
        
        elif re.search('[A-Z]', new_password) is None:
            raise forms.ValidationError("Parolanızda büyük harf olduğuna dikkat edin.")
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
             raise forms.ValidationError("Lütfen Mevcut Şifrenizi Doğru Giriniz")
        
        return old_password

class PersonalRegisterForm(forms.Form):
    username= forms.CharField(max_length=30, label="Kullanıcı Adı")
    name = forms.CharField(max_length=30, label="İsim")
    surname = forms.CharField(max_length=25, label="Soyisim")
    sex = forms.ChoiceField(required=True, choices=PersonalUserProfile.SEX, label="Cinsiyet")
    age = forms.IntegerField(min_value=18, max_value=120, label="Yaşınız")
    profile_photo = forms.ImageField(required=False,label="Profil Fotoğrafı")
    password = forms.CharField(max_length=30, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=30, label="Parola Doğrulama", widget=forms.PasswordInput)

    #validation e-mail
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Bu mail adresi sistemde kayıtlıdır.")
        return email

    def clean(self): #clean methodu şifrelrin aynı olup olmadığını göstermek ve
        username = self.cleaned_data.get("username") #submit edilmeden önce görülecek demektir.
        sex = self.cleaned_data.get("sex")
        name = self.cleaned_data.get("name")
        surname = self.cleaned_data.get("surname") 
        age = self.cleaned_data.get("age")
        profile_photo = self.cleaned_data.get("profile_photo")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")


        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmedi")

        elif len(password) < 8:
            raise forms.ValidationError("Parolanız 8 karakterden küçük olmamalıdır.")

        elif re.search('[0-9]', password) is None:
             raise forms.ValidationError("Parolanızda en az bir sayı olduğundan emin olun.")
        
        elif re.search('[A-Z]', password) is None:
            raise forms.ValidationError("Parolanızda en az bir büyük harf olduğundan emin olun.")

        elif User.objects.filter(username = username).exists():
            raise forms.ValidationError("Bu kullanıcı adı sistemde mevcuttur.")


        values = {          #yukarıdkai değerleri bir sonraki sayfada aktarabilmem için değerleri sözlük içerisnde oluşturmam gerekiyor.
            "username" : username,
            "sex" : sex,
            "name" : name,
            "surname" : surname,
            "profile_photo" : profile_photo,
            "age" : age,
            "password" : password,

            
        }

        return values



class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)


class PersonalUserProfileUpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(required=True, choices=PersonalUserProfile.SEX, label="Cinsiyet")
    profile_photo = forms.ImageField(required=False,label="Profil Fotoğrafı")
    class Meta:
        model = User
        fields = ['username','sex', 'profile_photo']

class PersonalUserPasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(required=True,max_length=20, label="Mevcut Parolanız", widget = forms.PasswordInput)
    new_password = forms.CharField(required=True,max_length=20, label="Yeni Parolanız", widget = forms.PasswordInput)
    new_confirm_password = forms.CharField(required=True,max_length=20, label="Yeni Parola Doğrulama", widget = forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user #içerideki değeri dışarıda kullanmak için
        super(PersonalUserPasswordChangeForm, self).__init__(*args,**kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_confirm_password = self.cleaned_data.get('new_confirm_password')

        if new_password and new_confirm_password and new_password != new_confirm_password:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        elif len(new_password) < 8:
            raise forms.ValidationError("8'den Küçük Karakter Bulunmaktadır.")

        elif re.search('[0-9]', new_password) is None:
             raise forms.ValidationError("Parolanızda bir sayı olduğundan emin olun")
        
        elif re.search('[A-Z]', new_password) is None:
            raise forms.ValidationError("Parolanızda büyük harf olduğuna dikkat edin.")
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
             raise forms.ValidationError("Lütfen Mevcut Şifrenizi Doğru Giriniz")
        
        return old_password