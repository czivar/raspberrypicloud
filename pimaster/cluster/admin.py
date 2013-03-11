from django.contrib import admin
from cluster.models import *

admin.site.register(Rack)
admin.site.register(VM)
admin.site.register(Node)
admin.site.register(Template)
admin.site.register(NodePerformanceData)
