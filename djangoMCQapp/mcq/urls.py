from django.urls import path
# from django.conf.urls import include
from . import views
urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls'))
    path('question/<int:question_id>',
         views.QuestionView.as_view(), name='question'),
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('catalog', views.Catalog.as_view(), name='catalog'),
    path('submit_answer/<int:question_id>', views.SubmitAnswer.as_view(),
         name='submit_answer'),
    path('result/<int:question_set>', views.ResultView.as_view(), name='result'),
# TODO: / = /catalog if logged in, /login if not
]
