from django.contrib import admin

from .models import Organization,Profile, Project, PIA, Thread, Risk, RiesgoInherente,Results


class RiskAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('risk', 'thread', 'confImpact','integImpact','disImpact', 'noRepImpact')
    list_filter = ('risk','thread')
    fieldsets = (
        (None, {'fields': ('risk', 'thread')}),
        ('Domain Impacts', {'fields': ('confImpact','integImpact','disImpact', 'noRepImpact')}),
    )
    search_fields = ('risk',)
    ordering = ('risk',)
    filter_horizontal = ()

admin.site.register(Organization)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(PIA)
admin.site.register(Thread)
admin.site.register(Risk, RiskAdmin)
admin.site.register(RiesgoInherente)
admin.site.register(Results)