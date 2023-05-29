from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db.models import Q
from users.models import Detail, Personnell, Projett, Service

from .forms import CommentaireForm, PersonnelForm, ProjetForm, RegisterForm, LoginForm, ServiceForm
from django.shortcuts import render
from .models import Commentaire, Contact, Equipe
from .forms import ContactForm

def home(request):
    return render(request, 'users/home.html')

def mespersonnels(request):
    personnells= Personnell.objects.all()
    context={'personnells':personnells}
    return render( request,'agence/mespersonnels.html ',context )

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')




@login_required


def addservice(request):
    if request.method == "POST" :
        form = ServiceForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_detail', service_id=form.instance.id)
    else :
        form = ServiceForm() #créer formulaire vide
    return render(request,'agence/majService.html',{'form':form})

def addpersonnel(request):
    if request.method == "POST" :
        form = PersonnelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('personnel_detail', personnel_id=form.instance.id)
    else :
        form = ServiceForm() #créer formulaire vide
    return render(request,'agence/personnel.html',{'form':form})

def addprojet(request):
    if request.method == "POST":
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.user_id = request.user.id  # Set user_id to the current user's ID

            # Set created_by_admin based on the user's role
            if request.user.is_staff:  # Admin user
                projet.created_by_admin = True
            else:  # Regular user
                projet.created_by_admin = False

            projet.save()
            return redirect('projet_detail', projet_id=projet.id)
    else:
        equipe_list = Equipe.objects.all()
        form = ProjetForm()
    
    context = {'form': form, 'equipe_list': equipe_list}
    return render(request, 'agence/projet.html', context)

def addcomment(request):
    if request.method == "POST":
        form = CommentaireForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user =request.user
            comment.save()
            return redirect('addcomment')
    else:
        form = CommentaireForm()

    projetts = Projett.objects.all()
    comments = Commentaire.objects.all()

    context = {'form': form, 'projetts': projetts, 'comments': comments}
    return render(request, 'agence/comment.html', context)

def addcontact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contact_detail', contact_id=form.instance.id)
    else:
        service_list = Service.objects.all()
        form = ContactForm()
        context = {'form': form, 'service_list': service_list}
        return render(request, 'agence/contact.html', context)


    
def index(request):
    projetts = Projett.objects.all()
    personnells = Personnell.objects.all()
    contact= Contact.objects.all()
    services = Service.objects.all()
    equipes = Equipe.objects.all()
    comments = Commentaire.objects.all()
    service_list = Service.objects.all()
    context = {'projetts': projetts,'personnells':personnells,'services': services, 'equipes': equipes, 'comments': comments,'service_list':service_list}
    return render(request, 'users/home.html', context)



def c_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    projets = Projett.objects.filter(detail__service=service)
    context = {'service': service, 'projets': projets}
    return render(request, 'agence/service_detail.html', context)

def equipe(request):
    personnel = Personnell.objects.all()
    context = {'personnel': personnel}
    return render(request, 'agence/equipe.html', context)

def service_detail(request, service_id):
    service = Service.objects.get(id=service_id)
    template = loader.get_template('users/home.html')
    return render(request, 'users/home.html', {'service': service})

def personnel_detail(request, personnel_id):
    personnel = Personnell.objects.get(id=personnel_id)
    template = loader.get_template('agence/personnel_detail.html')
    return render(request, 'agence/personnel_detail.html', {'personnel': personnel})

def contact_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    template = loader.get_template('agence/contact_detail.html')
    return render(request, 'agence/contact_detail.html', {'contact': contact})


def projet_detail(request, projet_id):
    projet = Projett.objects.get(id=projet_id)
    template = loader.get_template('agence/projet_detail.html')
    return render(request, 'agence/projet_detail.html', {'projet': projet})



def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contact_list.html', {'contacts': contacts})
    

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})