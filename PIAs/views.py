from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from filetransfers.api import serve_file, public_download_url
from django.views.static import serve

from PIAs.forms import NewPIAForm
from PIAs.fusioncharts import FusionCharts
from PIAs.models import Profile, RiesgoInherente, Results, Risk, Project, PIA, LastAccessMixin, LastEditMixin, Organization
from PIAs.scripts.writer import TSV
from shared.decorators import active_only

import os
User = get_user_model()

@method_decorator(active_only, name='dispatch')
class ProjectsView(LastAccessMixin,ListView):
    model = Project
    template_name = 'projects.html'

    def get_queryset(self):
        return self.model.objects.filter(organization=Profile.objects.get(user=self.request.user).organization)

@method_decorator(active_only, name='dispatch')
class ProjectView(DetailView):
    model = Project
    template_name = 'project.html'

@method_decorator(active_only, name='dispatch')
class PIAsView(DetailView):
    model = Project
    template_name = 'project.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deny_if_not_owner(request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pias']  = PIA.objects.filter(project=self.get_object())
        return context

@method_decorator(active_only, name='dispatch')
class PIAView(TemplateView):
    template_name = 'pia1.html'
    pia = Profile.objects.get

    def get(self, request, *args, **kwargs):
        self.object = PIA.objects.get(id=self.kwargs['pk'])
        if self.object.project.organization != Profile.objects.get(user=self.request.user).organization:
            self.object.deny_if_not_owner(request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['riesgosinh'] = RiesgoInherente.objects.filter(PIA=self.kwargs['pk'])
        context['pia']        = PIA.objects.get(id=self.kwargs['pk'])
        return context

@method_decorator(active_only, name='dispatch')
class createPIAView(CreateView):
    model = PIA
    fields = ['name',]
    template_name = 'pia_form.html'

    def dispatch(self, *args, **kwargs):
        """
        Overridden so we can make sure the instance exists
        before going any further.
        """
        self.project = get_object_or_404(Project, id=kwargs['project_pk'])
        self.p_id = self.project.id
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.project = self.project
        return super().form_valid(form)

@method_decorator(active_only, name='dispatch')
class createProjectView(CreateView):

    model = Project
    fields = ['title',]
    template_name = 'project_form.html'


    def dispatch(self, *args, **kwargs):
        """
        Overridden so we can make sure the instance exists
        before going any further.
        """
        self.organization = get_object_or_404(Organization, orgName=Profile.objects.get(user=self.request.user).organization)
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.organization = self.organization
        return super().form_valid(form)

@method_decorator(active_only, name='dispatch')
class PIAsDetailedView(TemplateView):
    template_name = 'pia.html'
    prof = Profile.objects.get
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user).organization
        return context

@method_decorator(active_only, name='dispatch')
class createRIView(CreateView):
    model = RiesgoInherente
    fields = ['risk','probability']
    template_name = 'risk_form.html'

    def get(self, request, *args, **kwargs):
        self.object = PIA.objects.get(id=self.kwargs['pk'])
        if self.object.project.organization != Profile.objects.get(user=self.request.user).organization:
            self.object.deny_if_not_owner(request.user)
        self.object.last_edited = timezone.now()
        self.object.save(update_fields=['last_edited'])
        return super().get(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.pia = get_object_or_404(PIA, id=kwargs['pk'])
        self.pia_id = self.pia.id
        self.project = get_object_or_404(Project, id=kwargs['project_pk'])
        self.p_id = self.project.id
        return super().dispatch(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.PIA = self.pia
        form.instance.confModImpact  = Risk.objects.get(id=form.instance.risk.id).confImpact
        form.instance.integModImpact = Risk.objects.get(id=form.instance.risk.id).integImpact
        form.instance.disModImpact   = Risk.objects.get(id=form.instance.risk.id).disImpact
        form.instance.noRepInhRisk   = Risk.objects.get(id=form.instance.risk.id).noRepImpact

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("pia", kwargs={'pk': self.pia_id,'project_pk':self.p_id})

@method_decorator(active_only, name='dispatch')
class updateRIView(LastEditMixin,UpdateView):
    model = RiesgoInherente
    fields = ['risk','probability','confModImpact','integModImpact','disModImpact','noRepInhRisk']
    template_name = 'editrisk_form.html'

    def dispatch(self, *args, **kwargs):
        self.pia = get_object_or_404(PIA, id=kwargs['pia_pk'])
        self.pia_id = self.pia.id
        self.project = get_object_or_404(Project, id=kwargs['project_pk'])
        self.p_id = self.project.id
        return super().dispatch(*args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse("pia", kwargs={'pk': self.pia_id, 'project_pk': self.p_id})

#@method_decorator(active_only, name='dispatch')
def deleteRIView(request, **kwargs):
    model = RiesgoInherente
    instance = get_object_or_404(RiesgoInherente, id=kwargs['pk'])
    instance.deny_if_not_owner(request.user)
    instance.delete()
    return redirect("pia", pk = kwargs['pia_pk'], project_pk = kwargs['project_pk'])

#@method_decorator(active_only, name='dispatch')
def download(request, **kwargs):#id
    object = PIA.objects.get(id=kwargs['pk'])
    if object.project.organization != Profile.objects.get(user=request.user).organization:
        object.deny_if_not_owner(request.user)

    RI = []
    ri  = RiesgoInherente.objects.filter(PIA=kwargs['pk'])

    if ri:
        for r in ri:
            RI.append({'Family':"essential",'Thread':str(r.risk.thread), 'likely':r.probability,
                        'A': r.disModImpact/100, 'I':r.integModImpact/100, 'C': r.confModImpact/100,
                        'Auth':r.noRepInhRisk/100})

        tsv = TSV(kwargs['pk']).file(RI)

        result_obj,created = Results.objects.update_or_create(PIA = PIA.objects.get(id=kwargs['pk']),
                                                              defaults={'tsv': tsv})

    return serve_file(request, result_obj.tsv, save_as="tsv_pia"+result_obj.date.strftime('%m/%d/%Y-%H%M%S'))

def download_catalog(request, **kwargs):
    filepath = 'TSV_FILES/ext_threats_pia_en.xml'
    fsock = open(filepath, 'r',encoding='utf-8')
    response = HttpResponse(fsock, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename=ext_threats_pia_en.xml"
    return response

class NewPIAView(FormView):
    template_name = 'pia_form.html'
    form_class = NewPIAForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        p = get_object_or_404(id=self.kwargs.get('project_pk'))
        return super().form_valid(form)

class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
     template = get_template('report.html')
     context = {
         "pia": PIA.objects.get(id=kwargs['pk']),
         'riesgosinh' : RiesgoInherente.objects.filter(PIA=self.kwargs['pk']),
         "customer_name": "John Cooper",
         "amount": 1399.99,
         "today": "Today",
     }

     html = template.render(context)
     pdf = render_to_pdf('report.html', context)
     if pdf:
         response = HttpResponse(pdf, content_type='application/pdf')
         filename = "PIA_%s.pdf" % ("12341231")
         content = "inline; filename='%s'" % (filename)
         download = request.GET.get("download")
         if download:
             content = "attachment; filename='%s'" % (filename)
         response['Content-Disposition'] = content
         return response
     return HttpResponse("Not found")

class GeneratePdf2(View):

    def get(self, request, *args, **kwargs):

        ri = RiesgoInherente.objects.filter(PIA=self.kwargs['pk'])
        datas = []
        rows = []
        for r in ri:
            datas.append({
                "rowid": str(r.risk),
                "columnid": "confidentiality",
                "value": r.confModImpact,
                "tllabel": str(r.risk),
                })
            datas.append({
                "rowid": str(r.risk),
                "columnid": "integrity",
                "value": r.integModImpact,
                "tllabel": str(r.risk),
                })
            datas.append({
                "rowid": str(r.risk),
                "columnid": "availability",
                "value": r.disModImpact,
                "tllabel": str(r.risk),
            })
            datas.append({
                "rowid": str(r.risk),
                "columnid": "authenticity",
                "value": r.noRepInhRisk,
                "tllabel": str(r.risk),
            })
            rows.append({
                "id": str(r.risk),
                "label": str(r.risk)
                })

        draw_data = {
                   "chart": {
                       "caption": "Privacy Risk Impact",
                       "subcaption": "By Security Domain",
                       "xAxisName": "Security Domain",
                       "yAxisName": "Privacy Risk",
                       "showplotborder": "1",
                       "showValues": "1",
                       "xAxisLabelsOnTop": "1",
                       "plottooltext": "<div id='nameDiv' style='font-size: 12px; border-bottom: 1px dashed #666666; font-weight:bold; padding-bottom: 3px; margin-bottom: 5px; display: inline-block; color: #888888;' >$rowLabel :</div>{br}Rating : <b>$dataValue</b>{br}$columnLabel : <b>$tlLabel</b>{br}<b>$trLabel</b>",
                       "baseFontColor": "#333333",
                       "baseFont": "Helvetica Neue,Arial",
                       "toolTipBorderRadius": "2",
                       "toolTipPadding": "5",
                       "theme": "fusion"
                   },
            "rows": {
                "row": [
                    {
                        "id": "SGS5",
                        "label": "Samsung Galaxy S5"
                    },
                    {
                        "id": "HTC1M8",
                        "label": "HTC One (M8)"
                    },
                    {
                        "id": "IPHONES5",
                        "label": "Apple iPhone 5S"
                    },
                    {
                        "id": "LUMIA",
                        "label": "Nokia Lumia 1520"
                    }
                ]
            },
            "columns": {
                "column": [
                    {
                        "id": "processor",
                        "label": "Processor"
                    },
                    {
                        "id": "screen",
                        "label": "Screen Size"
                    },
                    {
                        "id": "price",
                        "label": "Price"
                    },
                    {
                        "id": "backup",
                        "label": "Battery Backup"
                    },
                    {
                        "id": "cam",
                        "label": "Camera"
                    }
                ]
            },
                   "dataset": [
                       {
                           "data": []
                       }
                   ],
                   "colorrange": {
                       "gradient": "100",
                       "minvalue": "0",
                       "code": "E24B1A",
                       "startlabel": "Poor",
                       "endlabel": "Good",
                       "color": [
                           {
                               "code": "E24B1A",
                               "minvalue": "1",
                               "maxvalue": "5",
                               "label": "Bad"
                           },
                           {
                               "code": "F6BC33",
                               "minvalue": "5",
                               "maxvalue": "8.5",
                               "label": "Average"
                           },
                           {
                               "code": "6DA81E",
                               "minvalue": "8.5",
                               "maxvalue": "10",
                               "label": "Good"
                           }
                       ]
                   }
               }
        draw_data2 = {
    "chart": {
        "caption": "Privacy Risk Impact",
        "subcaption": "By Security Domain",
        "xAxisName": "Security Domain",
        "yAxisName": "Privacy Risk",
        "showplotborder": "1",
        "xAxisLabelsOnTop": "1",
        "plottooltext": "<div id='nameDiv' style='font-size: 12px; border-bottom: 1px dashed #666666; font-weight:bold; padding-bottom: 3px; margin-bottom: 5px; display: inline-block; color: #888888;' >$rowLabel :</div>{br}Rating : <b>$dataValue</b>{br}$columnLabel : <b>$tlLabel</b>{br}<b>$trLabel</b>",
        "baseFontColor": "#333333",
        "baseFont": "Helvetica Neue,Arial",
        "captionFontSize": "14",
        "subcaptionFontSize": "14",
        "subcaptionFontBold": "0",
        "showBorder": "0",
        "bgColor": "#ffffff",
        "showShadow": "0",
        "canvasBgColor": "#ffffff",
        "canvasBorderAlpha": "0",
        "legendBgAlpha": "0",
        "legendBorderAlpha": "0",
        "legendShadow": "0",
        "legendItemFontSize": "10",
        "legendItemFontColor": "#666666",
        "toolTipColor": "#ffffff",
        "toolTipBorderThickness": "0",
        "toolTipBgColor": "#000000",
        "toolTipBgAlpha": "80",
        "toolTipBorderRadius": "2",
        "toolTipPadding": "5"
    },
    "rows": {
        "row": [

        ]
    },
    "columns": {
        "column": [
            {
                "id": "confidentiality",
                "label": "Confidentiality"
            },
            {
                "id": "integrity",
                "label": "Integrity"
            },
            {
                "id": "availability",
                "label": "Availability"
            },
            {
                "id": "authenticity",
                "label": "Authenticity"
            }
        ]
    },
    "dataset": [
        {
            "data": [

            ]
        }
    ],
    "colorrange": {
        "gradient": "80",
        "minvalue": "0",
        "code": "6DA81E",
        "startlabel": "Negligible",
        "endlabel": "Maximum",
        "color": [
            {
                "code": "CC0000",
                "minvalue": "75",
                "maxvalue": "100",
                "label": "Maximum"
            },
            {
                "code": "FF8000",
                "minvalue": "40",
                "maxvalue": "75",
                "label": "Significant"
            },
            {
                "code": "F6BC33",
                "minvalue": "0",
                "maxvalue": "40",
                "label": "Limited"
            }
        ]
    }
}

        [draw_data2["rows"]["row"].append(r) for r in rows]
        [draw_data2["dataset"][0]["data"].insert(0,d) for d in datas]

        # Create an object for the column2d chart using the FusionCharts class constructor
        scatter = FusionCharts("heatmap","ex1", "1000", "400", "chart-1", "json", str(draw_data2)
                               )
        context = {
            "pia": PIA.objects.get(id=kwargs['pk']),
            'riesgosinh': RiesgoInherente.objects.filter(PIA=self.kwargs['pk']),
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
            'output': scatter.render(),
        }
        # returning complete JavaScript and HTML code,
        # which is used to generate chart in the browsers.
        return render(request, 'fusion.html', context)
