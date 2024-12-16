from django.shortcuts import render
from accounts.forms import UserRegisterForms
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views import View
from accounts.forms import UserUpdateForm

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