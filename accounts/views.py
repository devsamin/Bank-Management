from django.shortcuts import render
from accounts.forms import UserRegisterForms
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views import View
from accounts.forms import UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import CustomChangePassForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# from django.contrib.auth.forms import 

def send_transaction_email(user, subject, template):
    message = render_to_string(template, {
        'user' : user,
    })
    to_email = user.email
    send_email = EmailMultiAlternatives(subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class UserRegisterViews(FormView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForms
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    

class UserLoginview(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

# class Userlogoutview(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('home')

def UserLogoutview(request):
    logout(request)
    return redirect('home')

class BankaccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        # print(request.user)
        form = UserUpdateForm(instance = request.user)
        # print("samin")
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request):
        form = UserUpdateForm(request.POST, instance = request.user)
        if form.is_valid():
            # print(form)
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form' : form})
    
# class ChangePasswordviews(LoginRequiredMixin, PasswordChangeView):
#     # form_class =  PasswordChangeForm
#     template_name = 'accounts/password_change.html'
#     success_url = reverse_lazy('home')
#     success_message = "User password updated successfully."

def passwordchangeviews(request):
    if request.method == 'POST':
        form = CustomChangePassForm(request.user, request.POST)
        if form.is_valid():
            print(form.cleaned_data['old_password'])

            form.save()
            messages.success(request, 'User password update successfully')
            send_transaction_email(request.user, "Password Change", 'accounts/password_change_email.html')

            update_session_auth_hash(request, request.user)
    else:
        form = CustomChangePassForm(request.user)
    return render(request, 'accounts/password_change.html',{'form' : form})
