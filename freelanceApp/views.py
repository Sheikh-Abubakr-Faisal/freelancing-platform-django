from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q 

# Create your views here.

def index(request):
    return render(request, 'index.html')

def development(request):
    return render(request, 'development.html')

def ai(request):
    return render(request, 'ai.html')

def animation(request):
    return render(request, 'animation.html')

def audio(request):
    return render(request, 'audio.html')

def cuscare(request):
    return render(request, 'cuscare.html')

def design(request):
    return render(request, 'design.html')

def marketing(request):
    return render(request, 'marketing.html')

def writing(request):
    return render(request, 'writing.html')

# ========================LOGIN===========================
def join(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username!')
            return redirect('join')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password!')
            return redirect('join')
        else:
            login(request, user)

            if hasattr(user, 'profile'):
                if user.profile.role == "freelancer":
                    return redirect('freelancer_dashboard')  
                elif user.profile.role == "client":
                    return redirect('client_dashboard')  

    # Check if user exists and password matches
        # user = authenticate(request, username=username, password=password)

        # if user is not None:
        #     login(request, user)  # Log the user in (creates session)
            
        #     # Optional: Redirect based on user role (if using a Profile model)
        #     if hasattr(user, 'profile'):
        #         if user.profile.role == 'freelancer':
        #             return redirect('freelancer_dashboard')
        #         elif user.profile.role == 'client':
        #             return redirect('client_dashboard')
        #     return redirect('home')  # Fallback
        # else:
        #     messages.error(request, 'Invalid username or password.')

    return render(request, 'join.html')

# ========================WORK AS FREELANCER===========================
def find_work(request):
    query = request.GET.get('search', '')
    projects = Project.objects.filter(status='Open')
    suggested_projects = []

    # If the user is logged in and is a freelancer
    if request.user.is_authenticated:
        if query:
            projects = projects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        else:
            freelancer_skills = UserSkill.objects.filter(User_id=request.user).values_list('skill_id__name', flat=True)
            
            if freelancer_skills:
                for skill in freelancer_skills:
                    suggested = Project.objects.filter(
                        Q(title__icontains=skill) |
                        Q(description__icontains=skill) |
                        Q(category__icontains=skill),
                        status='Open'
                    )
                    suggested_projects.extend(list(suggested))

                suggested_projects = list(set(suggested_projects))

    return render(request, 'find_work.html', {
        'projects': projects,
        'suggested_projects': suggested_projects, 
        'query': query
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, Bid
from django.contrib.auth.decorators import login_required

@login_required
def apply_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        amount = request.POST.get('amount')
        cover_letter = request.POST.get('cover_letter')

        # Check if this freelancer has already applied to this project
        if Bid.objects.filter(project_id=project, freelancer_id=request.user).exists():
            messages.warning(request, "You have already applied for this project.")
            return redirect('find_work')

        # Create the bid
        Bid.objects.create(
            project_id=project,
            freelancer_id=request.user,
            amount=amount,
            cover_letter=cover_letter,
            status="Pending"
        )

        messages.success(request, "Your proposal has been submitted successfully!")
        return redirect('find_work')

    return render(request, 'apply_project.html', {'project': project})




# ========================DETAIL ABOUT PROJECT POSTED BY CLIENT===========================
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project':project})

def freelancer_dashboard(request):
    return render(request, 'freelancer_dashboard.html')

def freelancer_profile_view(request):
    user = request.user
    profile = user.profile
    freelancer_profile = FreelancerProfile.objects.get(freelancer_id=user)

    skills = []
    if freelancer_profile.skills:
        skills = [skill.strip() for skill in freelancer_profile.skills.split(',')]

    context = {
        'user' : user,
        'profile' : profile,
        'freelancer_profile' : freelancer_profile,
        'skills' : skills,
    }
    return render(request, 'freelancer_profile_view.html', context)

def freelance_edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    freelancer_profile, created = FreelancerProfile.objects.get_or_create(freelancer_id=user, defaults={
        'hourly_rate' : 0,
    })

    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        profile.pfp = files.get('pfp', profile.pfp)
        profile.bio = data.get('bio', profile.bio)
        profile.location = data.get('location', profile.location)
        profile.phone = data.get('phone', profile.phone)
        profile.save()

        if 'pfp'  in files:
            profile.pfp = files['pfp']

        profile.save()

        freelancer_profile.hourly_rate = data.get('hourly_rate', freelancer_profile.hourly_rate)
        freelancer_profile.skills = data.get('skills', freelancer_profile.skills)
        freelancer_profile.Experience = data.get('Experience', freelancer_profile.Experience)
        freelancer_profile.job_success_score = data.get('job_success_score', freelancer_profile.job_success_score)
        # Handle certifications (multiple)
        for cert_file in request.FILES.getlist('certifications[]'):
            Certification.objects.create(freelancer=freelancer_profile, file=cert_file)

        # Optional: Handle portfolio files (if storing multiple portfolio files)
        for portfolio_file in request.FILES.getlist('portfolio'):
            PortfolioItem.objects.create(freelancer=freelancer_profile, file=portfolio_file)
            
        freelancer_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('freelancer_profile_view')
    
    context = {
        'user' : user,
        'profile' : profile,
        'freelancer_profile' : freelancer_profile
    }

    return render(request, 'freelance_edit_profile.html', context)

def freelance_projects(request):
    return render(request, 'freelance_projects.html')

def freelancer_bid(request):
    bids = Bid.objects.select_related('project_id').filter(freelancer_id=request.user).order_by('-submission_date')
    return render(request, 'freelancer_bid.html', {'bids': bids})

def freelancer_inbox(request):
    return render(request, 'freelancer_inbox.html')

def freelancer_earnings(request):
    return render(request, 'freelancer_earnings.html')

def freelancer_withdraw_funds(request):
    return render(request, 'freelancer_withdraw_funds.html')

def freelancer_bank_details(request):
    return render(request, 'freelancer_bank_details.html')

# ========================FREELANCER LOGOUT AND PERFORM LOGOUT===========================
def freelancer_logout(request):
    return render(request, 'freelancer_logout.html')
def freelancer_perform_logout(request):
    logout(request)
    return redirect('home')

def client_dashboard(request):
    return render(request, 'client_dashboard.html')

# ========================VIEW CLIENT PROFILE DETAILS===========================
def client_view_profile(request):
    user = request.user
    profile = user.profile
    client_profile = ClientProfile.objects.get(client_id=user)

    context = {
        'user' : user,
        'profile' : profile,
        'client_profile' : client_profile,
    }

    return render(request, 'client_view_profile.html', context)

# ========================EDIT CLIENT PROFILE DETAILS===========================
def client_edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    client_profile, created = ClientProfile.objects.get_or_create(client_id=user)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        profile.pfp = files.get('pfp', profile.pfp)
        profile.bio = data.get('bio', profile.bio)
        profile.location = data.get('location', profile.location)
        profile.phone = data.get('phone', profile.phone)

        if 'pfp'  in files:
            profile.pfp = files['pfp']

        profile.save()

        client_profile.company_name = data.get('company_name', client_profile.company_name)
        client_profile.company_size = data.get('company_size', client_profile.company_size)
        client_profile.hiring_history = data.get('hiring_history', client_profile.hiring_history)
        client_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('client_view_profile')
    
    context = {
        'user' : user,
        'profile' : profile,
        'client_profile' : client_profile
    }


    return render(request, 'client_edit_profile.html', context)

# ========================CLIENT POST PROJECT===========================
def client_post_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget  = request.POST.get('budget')
        deadline  = request.POST.get('deadline')
        category  = request.POST.get('category')
        status  = request.POST.get('status')

        Project.objects.create(
            client_id = request.user,
            title = title,
            description = description,
            budget = budget,
            deadline = deadline,
            category = category,
            status = status,
        )
        return redirect('client_manage_project')
    
    return render(request, 'client_post_project.html')

# ========================MANAGE PROJECT - VIEW, EDIT, DELETE===========================
def client_manage_project(request):
    user = request.user
    projects = Project.objects.filter(client_id=user).order_by('-created_at')

    context = {
        'projects' : projects
    }
    return render(request, 'client_manage_project.html', context)

# ========================VIEW PROJECT===========================
def view_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'view_project.html', {'project':project})

# ========================EDIT PROJECT===========================
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.budget = request.POST['budget']
        project.deadline = request.POST['deadline']
        project.category = request.POST['category']
        project.status = request.POST['status']
        project.save()
        return redirect('client_manage_project')
    return render(request, 'edit_project.html', {'project': project})

# ========================DELETE PROJECT===========================
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('client_manage_project')
    return render(request, 'delete_project.html', {'project':project})

def client_project_bids(request):
    return render(request, 'client_project_bids.html')

def client_inbox(request):
    return render(request, 'client_inbox.html')

def client_bank_details(request):
    return render(request, 'client_bank_details.html')

def client_payments(request):
    return render(request, 'client_payments.html')

# ========================CLIENT LOGOUT AND PERFORM LOGOUT===========================
def client_logout(request):
    return render(request, 'client_logout.html')
def client_perform_logout(request):
    logout(request)
    return redirect('home')

# ========================REGISTER===========================
def sign_up(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role = data.get('role')
        pfp = files.get('pfp')
        bio = data.get('bio')
        location = data.get('location')
        phone = data.get('phone')
        is_verified = data.get('is_verified') == 'True'

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'sign_up.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'sign_up.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registerd!")
            return render(request, 'sign_up.html')

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            # password=password,
        )

        user.set_password(password)
        user.save()

        Profile.objects.create(
            user=user,
            role=role,
            pfp=pfp,
            bio=bio,
            location=location,
            phone=phone,
            is_verified=is_verified
        )
        
        if role == 'freelancer':
            return redirect('freelancer_dashboard')  
        elif role == 'client':
            return redirect('client_dashboard')  

    return render(request, 'sign_up.html')
