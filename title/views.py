from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.http import HttpResponseForbidden
from . forms import TitleForm
from . models import Title, Comment, SentimentTotalSystem
from user.models import EnterpriseUserProfile, PersonalAwardSystem

from django.contrib import messages

from django.contrib.auth.models import User

#entiment analysis
from sentiment.Sentiment import tokens_to_string, tokenizer, pad_sequences, max_tokens
from tensorflow.python.keras.models import load_model

#calculations
from django.db.models import F,Count,Sum,Aggregate

#paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#texteditor
import turkishnlp
from turkishnlp import detector

#graphs and reports pdf
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

#decarators
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required(login_url = "index")
def titles(request):
    titles= Title.objects.all()

    paginator = Paginator(titles,9)
    page = request.GET.get('page')
    titles = paginator.get_page(page)

    return render(request,"yorumlar.html",{"titles": titles})

@login_required(login_url = "index")
def enterpriseDashboard(request):
    titles = Title.objects.all().filter(author = request.user)

    

    paginator = Paginator(titles,9)
    page = request.GET.get('page')
    titles = paginator.get_page(page)

    return render(request,"enterpriseDashboard.html", {"titles": titles})

@login_required(login_url = "index")
def personalDashboard(request):
    titles= Title.objects.all()

    paginator = Paginator(titles,9)
    page = request.GET.get('page')
    titles = paginator.get_page(page)

    return render(request,"personalDashboard.html", {"titles": titles})

@login_required(login_url = "index")
def addTitle(request):
    form = TitleForm(request.POST or None)

    if form.is_valid():
        title = form.save(commit=False)

        title.author = request.user
        title.save()
        messages.success(request,'Başlığınız Başarıyla Oluşturuldu', extra_tags='alert alert-success')
        return redirect("title:addtitle")
    return render(request,"addTitle.html",{"form": form})

@login_required(login_url = "index")
def titleHistory(request):
    titles = Title.objects.filter(author = request.user)

    total_title = titles.all().count()

    
    paginator = Paginator(titles,10)
    page = request.GET.get('page')
    titles = paginator.get_page(page)
    

    context = {
        "titles" : titles,
        "total_title" : total_title,
    }
    return render(request,"titlehistory.html", context)

@login_required(login_url = "index")
def reportTitle(request,id):
    title = get_object_or_404(Title, id = id)

    if request.user != title.author:
        return HttpResponseForbidden()

    comments = title.comment.all() #titles fonksiyonunun hepsini getir.
    total_comment = title.comment.all().count()
    positive = title.comment.filter(sentiment = 'Pozitif').count()
    negative = title.comment.filter(sentiment = 'Negatif').count()
    notr = title.comment.filter(sentiment = 'Nötr').count()

    paginator = Paginator(comments,10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    
    return render(request,"report.html",{"title": title, "total_comment": total_comment,"comments": comments, "positive":positive, "negative":negative, "notr":notr,}) 

#PDF İşlemleri
def render_to_pdf(template_src, contex_dict={}):
    template = get_template(template_src)
    html = template.render(contex_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("iso-8859-9")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None

class DownloadPDF(View):
    def get( self, request, id):
        title = get_object_or_404(Title, id = id)
        
        if request.user != title.author:
            return HttpResponseForbidden()

        comments = title.comment.all()
        total_comment = title.comment.all().count()
        positive = title.comment.filter(sentiment = 'Pozitif').count()
        negative = title.comment.filter(sentiment = 'Negatif').count()
        notr = title.comment.filter(sentiment = 'Nötr').count()
        context={
            "title" : title,
            "comments" : comments,
            "total_comment" : total_comment,
            "positive" : positive,
            "negative" : negative,
            "notr" : notr
        }
        pdf = render_to_pdf('pdf_template.html',context)

        response= HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content_Diposition'] = content
        return response

@login_required(login_url = "index")      
def updateTitle(request,id):
    title = get_object_or_404(Title, id = id) 
    form = TitleForm(request.POST or None, request.FILES or None, instance= title) 
    if form.is_valid():
        title = form.save(commit=False)

        title.author = request.user
        title.save()

        messages.success(request,"Başlığınız Başarıyla Güncellendi ve Yeni Başlık Adıyla Yayınlandı", extra_tags='alert alert-card alert-success')
        return redirect("title:ent_dashboard")

    return render(request,"update.html" ,{"form": form})

@login_required(login_url = "index")
def deleteTitle(request,id):
    title = get_object_or_404(Title, id = id)

    title.delete()

    messages.success(request,"Başlığınız Başarıyla Silindi", extra_tags='alert alert-card alert-success')

    return redirect("title:hst_title")

@login_required(login_url = "index")
def upload(request):
    return render(request,"upload.html")

@login_required(login_url = "index")
def detail(request,id):
    title = get_object_or_404(Title, id = id)

    total_comment = title.comment.all().count()
    deneme = title.title_bound

    comments = title.comment.all() #tüm yorumları buraya çek.

    return render(request,"detail.html", {"title" : title, "total_comment" : total_comment,"comments" : comments, "deneme":deneme})

@login_required(login_url = "index")
def detailcomment(request,id):
    title = get_object_or_404(Title, id = id)

    total_comment = title.comment.all().count()
    comment_control = title.comment.filter(comment_author = request.user).count()
    deneme = title.title_bound
    

    if total_comment == deneme:
        comments = title.comment.all()
        return render(request,"detail.html", {"title" : title,"comments" : comments,"total_comment" : total_comment,"deneme":deneme})
    
    return render(request,"addComment.html",{"title" : title,"total_comment" : total_comment, "comment_control":comment_control, "deneme":deneme})

@login_required(login_url = "index")
def addComment(request,id):
    title = get_object_or_404(Title, id=id)

    comment_control = title.comment.filter(comment_author = request.user).count()

    obj = detector.TurkishNLP()
    #obj.download()
    obj.create_word_set() #veri setini oluşturmak için kullanıyoruz.

    if request.method == "POST":
        comment_content = obj.list_words(request.POST.get("comment_content"))
        comment_author = request.user #sonra bu author'u yorumu yapan kişiye at

        if comment_control == 0:

            control = obj.is_turkish(comment_content) #türkçe yazım doğruluğu oranını kontrol etmek için.

            if control > 0.10:

                model = load_model("model.h5")

                corrected_words = obj.auto_correct(comment_content) #H2. Burada "list_words" metodunun yaptığı string olarak gelen texti regex yardımıyla kelimelerine ayırmaktır.
                corrected_string = " ".join(corrected_words) #H3. Kelimeleri birleştirmek için Python'ın "join" metodu kullanılabilir. 

                texts = [corrected_string]

                tokens = tokenizer.texts_to_sequences(texts)
                tokens_pad = pad_sequences(tokens, maxlen=max_tokens)

                sentiment = model.predict(tokens_pad)

                if (sentiment>=0.85):
                    sentiment = "Pozitif"
                    messages.success(request,"Pozitif")
                elif (0.40 <= sentiment < 0.85):
                    sentiment = "Nötr"
                    messages.success(request,"Nötr")
                else:
                    sentiment = "Negatif"
                    messages.success(request,"Negatif")

                newComment = Comment(comment_author = comment_author, comment_content = corrected_string, sentiment = sentiment )

                newComment.title = title

                newComment.save()

                total_comments = Comment.objects.filter(comment_author = comment_author).count()
                positive_count = Comment.objects.filter(comment_author = comment_author, sentiment = "Pozitif").count()
                negative_count = Comment.objects.filter(comment_author = comment_author, sentiment = "Negatif").count()
                notr_count = Comment.objects.filter(comment_author = comment_author, sentiment = "Nötr").count()

                positive_count_title = Comment.objects.filter(title = title, sentiment = "Pozitif").count()
                negative_count_title = Comment.objects.filter(title = title, sentiment = "Negatif").count()
                notr_count_title = Comment.objects.filter(title = title, sentiment = "Nötr").count()

                if SentimentTotalSystem.objects.filter(title = title).exists():
                    for y in SentimentTotalSystem.objects.filter(title = title):
                        y.positive_count = positive_count_title
                        y.negative_count = negative_count_title
                        y.notr_count = notr_count_title

                        y.save()
                else:
                    new_sentiment_total = SentimentTotalSystem(title =  title, positive_count= positive_count_title, negative_count = negative_count_title, notr_count = notr_count_title)
                    
                    new_sentiment_total.save()
                    
                if PersonalAwardSystem.objects.filter(user = comment_author).exists():
                    for x in PersonalAwardSystem.objects.filter(user = comment_author):
                        x.total_comment = total_comments
                        x.positive_count = positive_count
                        x.negative_count = negative_count
                        x.notr_count = notr_count

                        if x.total_comment>=5:
                            x.is_gold = True
                            x.is_silver = False
                            x.is_bronze = False
                        elif x.total_comment>=3:
                            x.is_gold = False
                            x.is_silver = True
                            x.is_bronze = False
                        elif x.total_comment>=1:
                            x.is_gold = False
                            x.is_silver = False
                            x.is_bronze = True
                        
                        x.save()
                else:
                    new_total = PersonalAwardSystem(user = comment_author, total_comment = total_comments, positive_count = positive_count, negative_count = negative_count, notr_count = notr_count)
                    
                    if total_comments>=5:
                        new_total.is_gold = True
                        new_total.is_silver = False
                        new_total.is_bronze = False
                    elif total_comments>=3:
                        new_total.is_gold = False
                        new_total.is_silver = True
                        new_total.is_bronze = False
                    elif total_comments>=1:
                        new_total.is_gold = False
                        new_total.is_silver = False
                        new_total.is_bronze = True
                    
                    new_total.save()


            else:
                messages.success(request,"Yorumunuz Yazım Hatalarından Dolayı Göderilemedi. Lütfen Yorumunuzu Tekrar Belirtiniz!")
        else:
            messages.success(request,"Yorum Bulunmaktadır Yorum Yapamazsınız")
    return redirect("/title/titles/" + str(id))

@login_required(login_url = "index")
def commentHistory(request):
    comments = Comment.objects.filter(comment_author = request.user)

    personal_comment_size = comments.count()

    paginator = Paginator(comments,10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    
    return render(request, "personalcomment.html",  {"comments": comments,"personal_comment_size":personal_comment_size})
