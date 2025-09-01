from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    contact_view, login_view, logout_view
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # Admin (staff) CRUD with ModelForm
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

    # Contact + Auth
    path('contact/', contact_view, name='contact'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
