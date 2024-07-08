from django.contrib import admin
from .models import Admission, AdmissionFile,  Placement, PlacementFile, StudentProfile, Subject, ResultUpload, StudentResult, Template ,Faculty ,  Publication ,AcceptedProject, ResearchProject
from more_admin_filters import MultiSelectDropdownFilter
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
# from pyExcelerator import * 
# from django.contrib.admin.util import lookup_field
from django.utils.html import strip_tags
from django.contrib import messages
from openpyxl import Workbook
from django.db import connection
import xlsxwriter
from django.db.models import Count, Case, When, Q
from django.db import models
from django.views.generic import TemplateView
from django.urls import path, reverse
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.utils.html import format_html
from .resources import SubjectAdminResource, StudentProfileAdminResource
# from .actions import export_as_xls
# from .models import Bos,NewCoursesIntroduced, Consultants, Bookchapter, Seedmoney, Proposal, Journal, Grant,StudentsHigherEducation, AwardsAndRecognistionTeachersStudents, ListMajorMinorResearchProjects, SpecialLectureInCollege, ConferenceAttendedByTeachers, ConferenceConductedInCollege, ProfessionalDevelopmentProg, CollabrativeActivity, FundingStudentProjects, WorkshopAndSeminars, FacultyProfile
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

class AdmissionFileAdminInline(admin.TabularInline):
    model = AdmissionFile

class AdmissionAdmin(ImportExportModelAdmin, ExportActionMixin,  admin.ModelAdmin):
    list_filter = [("admission_year", MultiSelectDropdownFilter)] 
    list_display = ( 'admission_year', 'CET', 'comedk', 'management', 'diploma', 'CoB_incoming', 'CoB_outgoing', 'snq', 'total')
    inlines = (AdmissionFileAdminInline, )
    exclude = ('total',)

    def export (self, request, queryset): 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM api_admission LEFT JOIN api_placement ON api_admission.admission_year = api_placement.admission_year")
            row = cursor.fetchall()
            print(row)
            column_names = []
            cursor.execute("DESCRIBE api_admission")
            admission = cursor.fetchall()
            cursor.execute("DESCRIBE api_placement")
            placement = cursor.fetchall()
            for col in admission:
                column_names.append(col[0])
            for col in placement:
                column_names.append(col[0])
            print(column_names)
            workbook = xlsxwriter.Workbook('write_list.xlsx')
            worksheet = workbook.add_worksheet()

            for col_num, data in enumerate(column_names):
                worksheet.write(0, col_num, data)

            for row_num, row_data in enumerate(row):
                for col_num, col_data in enumerate(row_data):
                    worksheet.write(row_num+1, col_num, col_data)

            workbook.close()
            with open("write_list.xlsx", 'rb') as f:
                text = f.read()
                print(text)
                response = HttpResponse(text, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=write_list.xlsx'
                return response
            
    actions = [export]

    
    class Media:
        js = ('/media/hide_attribute.js',)

class AdmissionFileAdmin(admin.ModelAdmin):
    list_display = ('get_batch', 'name', 'file')
    list_filter = [("admission__batch", MultiSelectDropdownFilter)] 
    # list_filter = ("admission__batch", "admission__semester",)
    @admin.display(description='Batch', ordering='admission__batch')
    def get_batch(self, obj):
        return obj.admission.admission_year

# class ResultFileAdminInline(admin.TabularInline):
#     model = ResultFile

# class ResultAdmin(ImportExportModelAdmin, ExportActionMixin,  admin.ModelAdmin):
#     list_filter = [("admission_year", MultiSelectDropdownFilter), ("semester", MultiSelectDropdownFilter)] 
#     list_display = ( 'admission_year', 'semester', 'without_backlog','single_backlog','double_backlog','triple_backlog','more_than_3_backlog','dropouts')
#     # inlines = (ResultFileAdminInline, )

# class ResultFileAdmin(admin.ModelAdmin):
#     list_display = ('get_batch', 'get_semester', 'name', 'file')
#     list_filter = [("result__batch", MultiSelectDropdownFilter), ("result__semester", MultiSelectDropdownFilter)] 
#     # list_filter = ("result__batch", "result__semester",)
#     @admin.display(description='Batch', ordering='result__batch')
#     def get_batch(self, obj):
#         return obj.result.admission_year
#     @admin.display(description='Semester', ordering='result__semester')
#     def get_semester(self, obj):
#         return obj.result.semester
    
class PlacementFileAdminInline(admin.TabularInline):
    model = PlacementFile

class StudentResultInline(admin.TabularInline):
    model = StudentResult

class PlacementAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_filter = [("admission_year", MultiSelectDropdownFilter), ] 
    list_display = ( 'admission_year', 'on_campus','off_campus','internship')
    inlines = (PlacementFileAdminInline, )

class PlacementFileAdmin(admin.ModelAdmin):
    list_display = ('get_batch', 'name', 'file')
    list_filter = [("placement__batch", MultiSelectDropdownFilter)] 
    # list_filter = ("result__batch", "result__semester",)
    @admin.display(description='Batch', ordering='placement__batch')
    def get_batch(self, obj):
        return obj.placement.admission_year
  

class QuotaAggregateView(DetailView):
    template_name = "admin/quota/detail.html"
    model = StudentProfile 

    def get_context_data(self, *args, **kwargs):
        context = super(QuotaAggregateView,
             self).get_context_data(*args, **kwargs)
        print("This is context", context)
        context["category"] = "MISC"       
        queryset = super().get_queryset()
        queryset = queryset.values('admission_year').annotate(
            cet_count=Count('admission_quota', filter=Q(admission_quota='CET')),
            management_count=Count('admission_quota', filter=Q(admission_quota='MANAGEMENT')),
            comedk_count=Count('admission_quota', filter=Q(admission_quota='COMED-K')),
            snq_count=Count('admission_quota', filter=Q(admission_quota='SNQ')),
        ).order_by('admission_year')
        # convert ValuesQuerySet to QuerySet
        queryset = list(queryset)
        print("This is queryset", queryset)
        context['aggregate'] = queryset
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
            "context": context
        }

class ResultAggregateView(DetailView):
    template_name="admin/results/detail.html"
    model = StudentProfile

    def get_context_data(self, *args, **kwargs):
        students_without_f = StudentProfile.objects.exclude(result_usn__grade='F').distinct()
        counts = {}
        for student in students_without_f:
            year = student.admission_year
            if year not in counts:
                counts[year] = 0
            counts[year] += 1
        print("Total students without F", counts)
        students_with_f = StudentProfile.objects.all().order_by('-admission_year').distinct()
        counts = {}
        for student in students_with_f:
            year = student.admission_year
            if year not in counts:
                counts[year] = {
                    'zero_time': 0,
                    'one_time': 0,
                    'two_times': 0,
                    'more_than_two_times': 0,
                    'total': 0
                }
            f_count = student.result_usn.filter(grade='F').count()
            counts[year]['total'] += 1
            if f_count == 0:
                counts[year]['zero_time'] += 1
            elif f_count == 1:
                counts[year]['one_time'] += 1
            elif f_count == 2:
                counts[year]['two_times'] += 1
            else:
                counts[year]['more_than_two_times'] += 1
        print("Students with 1F, 2F and so on", counts)
        res = [] 
        context = super(ResultAggregateView,
             self).get_context_data(*args, **kwargs)
        print("This is context", context)
        context["category"] = "MISC"       
        context["xx"] = list(counts.items())
        print(context['xx'][0][1])
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
            "context": context
        }

class PlacementAggregateView(DetailView):
    template_name = "admin/placement/detail.html"
    model = StudentProfile 

    def get_context_data(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.values('admission_year').annotate(
            on_campus_count=Count('placement', filter=Q(placement='ON_CAMPUS')),
            off_campus_count=Count('placement', filter=Q(placement='OFF_CAMPUS')),
            internship_count=Count('placement', filter=Q(placement='INTERNSHIP')),
        ).order_by('admission_year')
        context = super(PlacementAggregateView,
             self).get_context_data(*args, **kwargs)
        # convert ValuesQuerySet to QuerySet
        queryset = list(queryset)
        print("This is queryset", queryset)
        context['aggregate'] = queryset
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
            "context": context
        }

@admin.register(StudentProfile)
class OrderAdmin(ImportExportModelAdmin, ExportActionMixin,  admin.ModelAdmin):
    list_display = ['usn', 'admission_year',  'admission_quota', 'quota_aggregate', 'placement_aggregate', 'result_aggregate']
    inlines = (StudentResultInline, )
    resource_class = StudentProfileAdminResource
    skip_unchanged = True
    report_skipped = True
    exclude = ('id',)
    import_id_fields = ('usn', 'admission_year', 'admission_quota', 'placement')

    def get_urls(self):
        return [
            path(
                "<pk>/quota",
                self.admin_site.admin_view(QuotaAggregateView.as_view()),
                name=f"quota_aggregate",
            ),
            path(
                "<pk>/placement",
                self.admin_site.admin_view(PlacementAggregateView.as_view()),
                name=f"placement_aggregate",
            ),
            path(
                "<pk>/result",
                self.admin_site.admin_view(ResultAggregateView.as_view()),
                name=f"result_aggregate",
            ),
            *super().get_urls(),
        ]

    def quota_aggregate(self, obj: StudentResult) -> str:
        url = reverse("admin:quota_aggregate", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')
    
    def placement_aggregate(self, obj: StudentResult) -> str:
        url = reverse("admin:placement_aggregate", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')

    def result_aggregate(self, obj: StudentResult) -> str:
        url = reverse("admin:result_aggregate", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')


class SubjectAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'code', 'credit')
    resource_class = SubjectAdminResource
    skip_unchanged = True
    report_skipped = True
    exclude = ('id',)
    import_id_fields = ('username','email','password')

class ResultUploadAdmin(admin.ModelAdmin):
    list_display = ('admission_year', 'sem', 'file', 'uploading_done', 'error')
    exclude = ('uploading_done', 'error')

class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('usn', 'sem', 'grade', 'subject_name', 'subject_code','admission_year')
    list_filter = ('usn__admission_year', 'sem', 'grade')
    # search_fields = ['usn__name', 'subject__name', 'subject__code', 'grade','usn__admission_year']

    def subject_name(self, obj):
        return obj.subject.name
    subject_name.admin_order_field = 'subject__name'  # Allows column order sorting
    subject_name.short_description = 'Subject Name'  # Renames column head
    
    def subject_code(self, obj):
        return obj.subject.code
    subject_code.admin_order_field = 'subject__code'  # Allows column order sorting
    subject_code.short_description = 'Subject Code'  # Renames column head

    def admission_year(self, obj):
        return obj.usn.admission_year
    admission_year.admin_order_field = 'usn__admission_year'  # Allows column order sorting
    admission_year.short_description = 'Admission Year'  # Renames column head

    # def subject_name(self, obj):
    #     return obj.subject.name
    
    # def subject_code(self,obj):
    #     return obj.subject.code
        
    # def admission_year(self, obj):
    #     return obj.usn.admission_year

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_form', 'gender', 'qualification','designation', 'expertise')
    search_fields = ('name','short_form','designation')

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # This will call the clean() method of the model
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)



class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors_list', 'publication_type', 'publication_year', 'link')
    list_filter = ('publication_year','publication_type')
    search_fields = ('authors__short_form','publication_year')

    def authors_list(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    authors_list.short_description = 'Authors'
    
    # def get_link(self, obj):
    #     return format_html('<a href="{}" target="_blank">Link</a>', obj.link)
    # get_link.short_description = 'Publication Link'
    
    def get_link(self, obj):
        if obj.link:
            return format_html('<a href="{}" target="_blank">Link</a>', obj.link)
        return "No link available"
    get_link.short_description = 'Publication Link'
    
    
from .models import ResearchProject, AcceptedProject

class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'funding_agency', 'agency_type', 'submission_date', 'funding_amount', 'duration', 'pi_name', 'co_pi_name', 'status')
    list_filter = ('status', 'agency_type')
    search_fields = ('project_name', 'pi_name', 'co_pi_name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == 'Accepted':
            AcceptedProject.objects.get_or_create(research_project=obj)
        else:
            AcceptedProject.objects.filter(research_project=obj).delete()

admin.site.register(ResearchProject, ResearchProjectAdmin)

@admin.register(AcceptedProject)
class AcceptedProjectAdmin(admin.ModelAdmin):
    list_display = ('research_project_project_name', 'research_project_status')
    search_fields = ('research_project__project_name',)

    def research_project_project_name(self, obj):
        return obj.research_project.project_name

    research_project_project_name.short_description = 'Project Name'

    def research_project_status(self, obj):
        return obj.research_project.status

    research_project_status.short_description = 'Status'
     
admin.site.register(Faculty,FacultyAdmin)
admin.site.register(Publication,PublicationAdmin)
# admin.site.register(Admission, AdmissionAdmin)
# admin.site.register(AdmissionFile, AdmissionFileAdmin)
admin.site.register(StudentResult, StudentResultAdmin)
admin.site.register(Template, TemplateAdmin)
# admin.site.register(ResultFile, ResultFileAdmin)
# admin.site.register(Placement, PlacementAdmin)
# admin.site.register(PlacementFile, PlacementFileAdmin)
# admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ResultUpload, ResultUploadAdmin)


