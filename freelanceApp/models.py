from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=(('freelancer', 'Freelancer'), ('client', 'Client')))
    pfp = models.ImageField(upload_to='pfp/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)


class FreelancerProfile(models.Model):
    freelancer_id = models.OneToOneField(User, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.CharField(max_length=500)
    portfolio = models.TextField(blank=True)
    Experience = models.TextField(blank=True)
    certifications = models.FileField(upload_to='certificates', max_length=100)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    job_success_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class Certification(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='certifications_items')
    file = models.FileField(upload_to='certifications/')

class PortfolioItem(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='portfolio_items')
    file = models.FileField(upload_to='portfolio/')

class ClientProfile(models.Model):
    client_id = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_size = models.CharField(max_length=100)
    total_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hiring_history = models.TextField(blank=True)
    reviews_given = models.PositiveIntegerField(default=0)


class BankDetails(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    withdrawal_preferences = models.CharField(max_length=100)

class Project(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=(('Open', 'Open'), ('Closed', 'Closed')))
    created_at = models.DateTimeField(default=timezone.now)

class Bid(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cover_letter = models.TextField()
    status = models.CharField(max_length=50)
    submission_date = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_client')
    freelancer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_freelancer')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    terms = models.TextField()
    status = models.CharField(max_length=50)

class Milestone(models.Model):
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=50)

class Payment(models.Model):
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    date = models.DateField()
    method = models.CharField(max_length=50)

class Review(models.Model):
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given', null=True, blank=True)
    reviewed_User_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received', null=True, blank=True)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField()

class Message(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
