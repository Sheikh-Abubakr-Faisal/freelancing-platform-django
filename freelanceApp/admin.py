from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'pfp', 'bio', 'location', 'phone', 'is_verified')
    search_fields = ('user__username', 'user__email', 'role', 'location')
    list_filter = ('role', 'is_verified')

admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)
admin.site.register(BankDetails)
admin.site.register(Project)
admin.site.register(Bid)
admin.site.register(Contract)
admin.site.register(Milestone)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Skill)
admin.site.register(UserSkill)

