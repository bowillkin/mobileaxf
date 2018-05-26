from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from users import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.register(r'^ordergood', views.OrderGoodsModelEdit)

urlpatterns = [
    url('^foodtypes/(\d+)/', views.foodtypes),
    url('^fenlei/(\d+)/(\d+)/(\d+)/', views.fenlei),
    url('^home/', views.home),
    url('^addnum/', views.addnum),
    url('^subnum/', views.subnum),
    url('^change/', views.change),
    url('^selectall/', views.selectall),
    url('^caltotal/', views.caltotal),
    url('^take_order/', views.take_order),
    url('^alipay/(\d+)/', views.alipay),
    url('^wait_send/', views.wait_send),
    url('^wait_pay', views.wait_pay),
    # url('^dj_regist/', views.djregist),
    # url('^dj_login/', views.djlogin),
    # url('^dj_logout/', views.djlogout),
    url('^regist/', views.regist),
    url('^login', views.login),
    url('^logout', views.logout),
    url('^cart/', views.cart),
    url('^mine/', views.mine)
]

# urlpatterns += router.urls