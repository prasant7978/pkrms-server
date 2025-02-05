from django.contrib import admin
from api.models.user import User, ApprovalRequest
from api.models.province import Province
from api.models.balai import Balai
from api.models.kabupaten import Kabupaten
from api.models.link import Link
from api.models.role import Role
# Register your models here.
admin.site.register(User)
admin.site.register(ApprovalRequest)
admin.site.register(Province)
admin.site.register(Balai)
admin.site.register(Kabupaten)
admin.site.register(Link)
admin.site.register(Role)