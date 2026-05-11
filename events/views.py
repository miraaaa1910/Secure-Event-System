from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import AuditLog, Event, Profile
from .forms import EventForm, ProfileUpdateForm, ProfileImageForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = ProfileImageForm(instance=profile)

    return render(request, 'events/profile.html', {
        'user': request.user,
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'events/profile_update.html', {'form': form})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# 1. READ: List events (RBAC Implementation)
@login_required
def event_list(request):
    # Security: Users ONLY see events they created (Broken Object Level Authorization protection)
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/event_list.html', {'events': events})

# 2. CREATE: Register a new event
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user # Security: Tie event to the logged-in user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# 3. DETAIL: View a single event
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    return render(request, 'events/event_detail.html', {'event': event})

# 4. UPDATE: Edit an existing event
@login_required
def event_update(request, pk):
    # Security: get_object_or_404 with filter ensures user can't edit others' events
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

# 5. DELETE: Remove an event
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

class AuditLogListView(UserPassesTestMixin, ListView):
    model = AuditLog
    template_name = 'events/audit_log.html'
    context_object_name = 'logs'

    # RBAC: Only allow users where is_staff=True
    def test_func(self):
        return self.request.user.is_staff