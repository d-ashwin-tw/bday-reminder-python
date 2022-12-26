from django.urls import path
from apps.auth_manager import views


urlpatterns = [
    # login
    path("login/", views.Login.as_view()),  # sign in
    # path("logout/", views.Logout.as_view()),  # sign in

    # Add new developer
    path("developer/add/", views.AddDeveloper.as_view()),
    path("developer/deactivate/", views.DeactivateDeveloper.as_view()),
    path("developer/list/", views.ListDeveloper.as_view()),
    path("developer/update/<str:developer_id>/",
         views.UpdateDeveloper.as_view()),

    path("developer/list/test/", views.ListDeveloperTest.as_view()),
    path("send/verify/link/", views.SendVerifyLinkToDeveloper.as_view()),
    path("verify/<str:token>/", views.VerifyDetailTokenView.as_view()),

]
