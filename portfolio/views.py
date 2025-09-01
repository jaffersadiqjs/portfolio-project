from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Project, Skill, ContactMessage
from .forms import ProjectForm, ContactForm

# --- CBVs for project gallery ---
class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['skills'] = Skill.objects.all()
        return ctx


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'


# Restrict create/update/delete to staff (admin)
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProjectCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project-list')


class ProjectUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project-list')


class ProjectDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Project
    template_name = 'portfolio/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')


# --- Manual contact form (HTML form + validation) ---
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'portfolio/contact.html', {'form': form})


# --- Simple auth views (login/logout) ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('project-list')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project-list')
    return render(request, 'portfolio/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('project-list')
