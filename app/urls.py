from django.urls import path
from app.views.home import home
from app.views.signup import signup
from app.views.configuration import configuration
from app.views.user import user_profile, inactive_user
from app.views.session import exit_session, delete_session
from app.views.files import FileList, \
                            upload_csv_file, \
                            set_key_words_events_file, \
                            set_key_words_devices_file, \
                            delete_file
from app.views.data_analytics import data_analytics
from app.views.chart import chart


urlpatterns = [
    path('', home, name='home'),

    path('signup', signup, name='signup'),

    path('settings', configuration, name='settings'),

    path('profile', user_profile, name='user_profile'),

    path('profile/delete_account/<username>/', inactive_user, name='inactive_user'),

    path('files', FileList.as_view(), name='file_list'),

    path('files/upload', upload_csv_file, name='upload_file'),

    path('files/key_words_events_file', set_key_words_events_file, name='key_words_events_file'),

    path('files/key_words_devices_file', set_key_words_devices_file, name='key_words_devices_file'),

    path('files/<int:pk>', delete_file, name='delete_file'),

    path('data_analytics', data_analytics, name='data analytics'),

    path('chart', chart, name='chart'),

    path('exit', exit_session, name='exit'),

    path('exit/delete', delete_session, name='delete_session'),

]
