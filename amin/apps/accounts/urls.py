from django.urls import path
import apps.accounts.views as vv
app_name="accounts"

urlpatterns = [
    path("register/",vv.RegisterUserView.as_view(),name="register"),
    path("login/",vv.LoginUserView.as_view(),name="login"),
    path("logout/",vv.LogoutUserView.as_view(),name="logout"),
    path("forgot/",vv.Forgot_Pssword.as_view(),name="forgot"),
    path("verify/",vv.VerifyUser.as_view(),name="verify"),
    path("Changepass/",vv.Changepass1.as_view(),name="Changepass"),
    path("userpanel/",vv.UserPanel.as_view(),name="userpanel"),
    path("last_orders/",vv.last_orders,name="last_orders"),
    path("panel_favorite/",vv.user_panel_favorite,name="panel_favorite"),
    path("security/",vv.Security.as_view(),name="security"),
    path("delete_user/",vv.Delete_user.as_view(),name="delete_user"),
    path("verify_for_delete_user/",vv.Verify_for_delete_user.as_view(),name="verify_for_delete_user"),
    
    
]
