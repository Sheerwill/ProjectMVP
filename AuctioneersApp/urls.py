from django.urls import path, include
from .views import (CustomLoginView, staff_home_view, signup, CustomPasswordResetView,
                    newdefaulter, search_defaulter, search_for_defaulter, edit_defaulter,
                    delete_defaulter, send_reminder_emails, chatbot)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('staff-home/', staff_home_view, name='staff_home'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('signup/', signup, name='signup'),  
    path('accounts/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'), 
    path('newdefaulter/', newdefaulter, name='newdefaulter'),
    path('searchdefaulter/', search_defaulter, name='searchdefaulter'),
    path('search_for_defaulter/', search_for_defaulter, name='search_for_defaulter'),
    path('edit_defaulter/<int:defaulter_id>/', edit_defaulter, name='edit_defaulter'),
    path('delete_defaulter/<int:defaulter_id>/', delete_defaulter, name='delete_defaulter'),
    path('email_defaulters/', send_reminder_emails, name='send_reminder_emails'),    
    path('chatbot/', chatbot, name='chatbot'),
]