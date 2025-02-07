from django.contrib import admin
from api.models.User import User, ApprovalRequest
from api.models.Province import Province
from api.models.Balai import Balai
from api.models.Kabupaten import Kabupaten
from api.models.Link import Link
from api.models.Role import Role
# Register your models here.
admin.site.register(User)
admin.site.register(ApprovalRequest)
admin.site.register(Province)
admin.site.register(Balai)
admin.site.register(Kabupaten)
admin.site.register(Link)
admin.site.register(Role)