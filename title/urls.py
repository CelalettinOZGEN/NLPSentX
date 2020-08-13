from django.contrib import admin
from django.urls import path
from . import views

app_name = "title"

urlpatterns = [
    path('ent_dashboard/', views.enterpriseDashboard, name="ent_dashboard"),
    path('per_dashboard/', views.personalDashboard, name="per_dashboard"),

    path('addtitle/', views.addTitle, name="addtitle"),
    path('hst_title/', views.titleHistory, name="hst_title"),

    path('titles/', views.titles, name="titles"),

    path('report/<int:id>', views.reportTitle, name="report"),
    path('update/<int:id>', views.updateTitle, name="update"),
    path('delete/<int:id>', views.deleteTitle, name="delete"),
    path('pdf_download/<int:id>', views.DownloadPDF.as_view(), name="pdf_download"),
    
    path('<int:id>', views.detail, name="detail"),
    path('titles/<int:id>', views.detailcomment, name="detailcomment"),

    path('addcomment/<int:id>',views.addComment,name = "addcomment"),
    path('hst_comment/', views.commentHistory, name="hst_comment"),

    path('upload/',views.upload,name = "upload"),
]


