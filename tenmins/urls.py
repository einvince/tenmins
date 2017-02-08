
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from main.views import index, detail, comment, index_login, index_register, vote, profile, modify_profile,detail_vote,mycollection

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^index/', index, name="index"),
    url(r'^detail/(?P<id>\d+)/$', detail, name="detail"),
    url(r'^detail/vote/(?P<id>\d+)$', detail_vote, name='detail_vote'),
    url(r'^comment/(?P<id>\d+)/$', comment, name="comment"),
    url(r'^login/$', index_login, name="login"),
    url(r'^register/$', index_register, name="register"),
    url(r'^logout/', logout, {'next_page': '/index'}, name="logout"),
    url(r'^vote/(?P<id>\d+)/$', vote, name="vote"),
    url(r'^profile/$', profile, name='profile'),
    url(r'^modify_profile/$', modify_profile, name='modify_profile'),
    url(r'^mycollection/$', mycollection, name='mycollection'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
