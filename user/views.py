from django.shortcuts import render, redirect, get_object_or_404


from . models import EnterpriseUserProfile, PersonalUserProfile, user_type, MailControl

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views import View

from . forms import EnterpriseRegisterForm, PersonalRegisterForm, LoginForm, EnterpriseUserProfileUpdateForm, EnterpriseUserPasswordChangeForm ,PersonalUserProfileUpdateForm, PersonalUserPasswordChangeForm
from . tokens import account_activation_token
from title.models import Comment

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import update_session_auth_hash


# Create your views here.

def enterpriseRegister(request):

    form = EnterpriseRegisterForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        sector = form.cleaned_data.get("sector")
        bio = form.cleaned_data.get("bio")
        profile_photo = form.cleaned_data.get("profile_photo")


        
        
        newUser= User(username = username, email = email)
        newUser.is_active = False
        newUser.set_password(password)
        newUser.save()


        profile = EnterpriseUserProfile(user = newUser, sector = sector, bio = bio, profile_photo = profile_photo)
        profile.save()

        usert = None
        usert = user_type(user = newUser, is_enterprises = True)
        usert.save()

        
        token = account_activation_token.make_token(newUser)

        tokenmail = MailControl(user = newUser ,token = token)
        tokenmail.save()
        
        
        
        mail_subject = 'SentX Hesabınız - E-posta Adresinizi Doğrulayın'
        current_site = get_current_site(request)
        uid = newUser.pk
        #token = account_activation_token.make_token(newUser)
        #uid = newUser.pk
        activation_link = "{0}/user/mail_control/{1}/{2}".format(current_site, uid, token)
        #http://127.0.0.1:8000/user/mail_control/5g5-85ea27a9a9daaa48429b
        message = "Sayın {0},\nSentX Hesabınızı tamamlamak için lütfen e-posta adresinizi doğrulayın.\n{1}\n Bu bağlantı 48 saat süreyle geçerlidir.".format(newUser.username, activation_link)
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        login(request,newUser)
        #return redirect("index")
        return render(request,"mailMessages.html")


    context = {             #eğer valid değil ise bu sayfayı tekrardan döndürmem gerek.
        "form" : form
    }
    return render(request,"enterpriseRegister.html", context)


def mail_control(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)

        return render(request,"mailConfirm.html")

    else:
        return render(request,"mailInvalid.html")



def personalRegister(request):
    form = PersonalRegisterForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        sex = form.cleaned_data.get("sex")
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        age = form.cleaned_data.get("age")
        profile_photo = form.cleaned_data.get("profile_photo")
        
        newUser= User(username = username)
        newUser.set_password(password)
        newUser.save()

        profile = PersonalUserProfile(user = newUser, sex = sex, name = name, surname = surname, age = age ,profile_photo = profile_photo)
        profile.save()

        usert = None
        usert = user_type(user = newUser, is_personals = True)
        usert.save()

        login(request,newUser)
        messages.success(request,"Başarıyla Kayıt Oldunuz", extra_tags='alert alert-card alert-success')
        #bu sayfa per_register'a gidecek.
        return redirect("index")

    context = {             #eğer valid değil ise bu sayfayı tekrardan döndürmem gerek.
        "form" : form
    }
    
    return render(request,"personelRegister.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user= authenticate(username = username,password = password)

        type_obj = user_type.objects.get(user = user)
        
        


        if not user:
            messages.success(request,"Hatalı Kullanıcı Adı veya Parola Girişi")
            #raise forms.ValidationError('Hatalı Kullanıcı Adı veya ParolasıGirişi')
        

        elif type_obj.is_enterprises: #** burayı diğer (DenemeTable'dan çekerek yap.) (Kurumsal yada prsonal olduğunu belirten booleana göre) (kurumsalboolean == 1 and personalboolean==0 ise şu işlemleri yap değise diğer işlemi yap.)
            login(request,user)
            return redirect("title/ent_dashboard")

        elif type_obj.is_personals:
            login(request,user)
            return redirect("/title/per_dashboard")
        
    return render(request,"index.html",context)

def enterpriseuser_account(request):
    return render(request, "enterpriseUser.html")

def enterpriseuser_settings(request):
    sector= request.user.enterpriseuserprofile.sector
    bio = request.user.enterpriseuserprofile.bio
    profile_photo = request.user.enterpriseuserprofile.profile_photo
    initial = {'sector' : sector, 'bio' : bio ,'profile_photo' : profile_photo}
    form = EnterpriseUserProfileUpdateForm(initial=initial,instance=request.user,data=request.POST or None, files=request.FILES or None)
    
    if form.is_valid():
        user = form.save(commit=True)
        sector = form.cleaned_data.get('sector', None)
        bio = form.cleaned_data.get('bio', None)
        profile_photo = form.cleaned_data.get('profile_photo', None)

        user.enterpriseuserprofile.sector = sector
        user.enterpriseuserprofile.bio = bio
        user.enterpriseuserprofile.profile_photo = profile_photo
        user.enterpriseuserprofile.save()
    
    return render(request,"enterpriseSettings.html", context = {'form': form})

def enterprisepassword_change(request):
    form = EnterpriseUserPasswordChangeForm(user = request.user, data=request.POST or None)

    if form.is_valid():
        new_password = form.cleaned_data.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Şifre Güncellenmişitr.")

    return render(request,"enterprisepasswordChange.html", context={'form' : form})

def personaluser_account(request):
    total_comments = Comment.objects.filter(comment_author=request.user).count()

    return render(request, "personalUser.html", {'total_comments' : total_comments})

def personaluser_settings(request):
    sex = request.user.personaluserprofile.sex
    profile_photo = request.user.personaluserprofile.profile_photo
    initial = {'sex' : sex, 'profile_photo' : profile_photo}
    form = PersonalUserProfileUpdateForm(initial=initial,instance=request.user,data=request.POST or None, files=request.FILES or None)
    
    if form.is_valid():
        user = form.save(commit=True)
        sex = form.cleaned_data.get('sex', None)
        profile_photo = form.cleaned_data.get('profile_photo', None)

        user.personaluserprofile.sex = sex
        user.personaluserprofile.profile_photo = profile_photo
        user.personaluserprofile.save()
    
    return render(request,"personalSettings.html", context = {'form': form})

def personalpassword_change(request):
    form = PersonalUserPasswordChangeForm(user = request.user, data=request.POST or None)

    if form.is_valid():
        new_password = form.cleaned_data.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Şifre Güncellenmişitr.")

    return render(request,"personalpasswordChange.html", context={'form' : form})

def logoutUser(request):
    logout(request)
    return redirect("index")
