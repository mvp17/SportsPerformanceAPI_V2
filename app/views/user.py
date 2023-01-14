from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# "Deleting" user account
def inactive_user(request, username):
    user = User.objects.get(username=username)
    # It is recommended to set this flag to False instead of deleting accounts;
    # that way, if your applications have any foreign keys to users, the foreign keys won't break.
    user.is_active = False
    user.save()
    return redirect('/')


def user_profile(request):
    return render(request, 'registration/user_profile.html')
