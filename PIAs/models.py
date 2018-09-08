from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import PermissionDenied

import uuid

User = get_user_model()

class Organization(models.Model):
    orgName  = models.CharField('Client Name',max_length=40)
    orgCode  = models.CharField('Client Code', max_length=8)
    def __str__(self):
        return self.orgName

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.email

class Project(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title        = models.CharField(max_length=254)
    organization = models.ForeignKey(Organization, on_delete=None, null=True)
    date_created = models.DateTimeField(default=timezone.now) #TODO: auto_now_add=True
    last_edited  = models.DateTimeField(default=timezone.now) #TODO: auto_now=True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', args=[str(self.pk)])

    def deny_if_not_owner(self, user):
        if self.organization != Profile.objects.get(user=user).organization:
            raise PermissionDenied
        return self.organization

class CL1(models.Model):
    interesados     = models.CharField(max_length=254)
    responsable     = models.CharField(max_length=254)
    encargado       = models.CharField(max_length=254)
    tercerasPartes  = models.CharField(max_length=254)
    cesionesDatos   = models.CharField(max_length=254)
    flujosDatos     = models.CharField(max_length=254)
    prodGenerados   = models.CharField(max_length=254)
    procSolCons     = models.CharField(max_length=254)
    procEjDer       = models.CharField(max_length=254)
    idOblig         = models.CharField(max_length=254)
    transNoEU       = models.CharField(max_length=254)

class PIA(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name         = models.CharField(max_length=254)
    project      = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    cl1          = models.ForeignKey(CL1,on_delete=None, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)  # TODO: auto_now_add=True
    last_edited  = models.DateTimeField(default=timezone.now)  # TODO: auto_now=True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pia', args=[str(self.project.id),str(self.id)])

    def deny_if_not_owner(self, user):
        if self.project.organization != Profile.objects.get(user=user).organization:
            raise PermissionDenied
        return self.project.organization


class Thread(models.Model):
    thread  = models.CharField(max_length=255)
    def __str__(self):
        return self.thread

class Risk(models.Model):
    IMPACT = (
            (1, 'Negligible (1)'),
            (2, 'Limited (2)'),
            (3, 'Significant (3)'),
            (4, 'Maximum (4)')
            )
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    risk        = models.CharField(max_length=255)
    thread      = models.ForeignKey(Thread, on_delete=None, null=True)
    confImpact   = models.IntegerField()
    integImpact  = models.IntegerField()
    disImpact    = models.IntegerField()
    noRepImpact    = models.IntegerField()

    def __str__(self):
        return self.risk

class RiesgoInherente(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PIA             = models.ForeignKey(PIA, on_delete=models.CASCADE,null=True)
    risk            = models.ForeignKey(Risk, on_delete=None,null=True)
    probability     = models.IntegerField(null=True, validators=[
                                                        MaxValueValidator(100),
                                                        MinValueValidator(1)
                                                    ],
                                          verbose_name=('Probability (1-100)'))
    confModImpact   = models.IntegerField()
    integModImpact  = models.IntegerField()
    disModImpact    = models.IntegerField()
    noRepInhRisk    = models.IntegerField()
    def __str__(self):
        return self.PIA.name

    def deny_if_not_owner(self, user):
        if self.PIA.project.organization != Profile.objects.get(user=user).organization:
            raise PermissionDenied
        return self.PIA.project.organization

class Results(models.Model):
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PIA              = models.ForeignKey(PIA, on_delete=models.CASCADE, null=True)
    tsv              = models.FileField(upload_to='TSV_FILES/')
    date             = models.DateTimeField(default=timezone.now)

class LastAccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        request.user.last_login = timezone.now()
        request.user.save(update_fields=['last_login'])
        return super(LastAccessMixin, self).dispatch(request, *args, **kwargs)

class LastEditMixin(object):
    def dispatch(self, request, *args, **kwargs):
        p = PIA.objects.get(id=self.kwargs['pia_pk'])
        p.last_edited = timezone.now()
        p.save(update_fields=['last_edited'])
        return super(LastEditMixin, self).dispatch(request, *args, **kwargs)