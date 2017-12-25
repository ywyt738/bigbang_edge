from django.contrib import admin
from .models import Host_info, IP_Resource, Mail, SentHistory, Svn
from django.db.models import Q
from easy_select2 import Select2
from django import forms
import datetime


class HostInfoForm(forms.ModelForm):

    class Meta:
        model = Host_info
        widgets = {
            'ip_address': Select2(),
            'maintainer': Select2(),
        }
        fields = '__all__'


class Host_infoAdmin(admin.ModelAdmin):
    form = HostInfoForm
    search_fields = ('ip_address__ip_address', 'maintainer__name', 'description')
    list_filter = ('cpu', 'memory', 'storage', 'maintainer',
                   'os', 'location', 'is_permanent')
    list_display = ('ip_address',
                    'description',
                    'maintainer',
                    'deadline',
                    'location',
                    'cpu',
                    'memory',
                    'storage')
    date_hierarchy = 'deadline'
    ordering = ('ip_address__bin_ip', )
    radio_fields = {"location": admin.HORIZONTAL}
    actions = None

    def save_model(self, request, obj, form, change):
        """
        重写新增和修改时保存动作。
        新增：
            新增时候将被分配ip的available改成False
        修改：
            修改的时候查看ip_address的是否在修改的字段内，
            如果修改字段中包含ip_address，则将源ip的available改成True
        """
        if change:
            if 'ip_address' in form.changed_data:
                sip = IP_Resource.objects.get(
                    ip_address=form.initial['ip_address'])
                sip.available = True
                sip.save()
                obj.ip_address.available = False
                obj.ip_address.save()
            if obj.is_permanent:
                obj.deadline = None
        else:
            obj.ip_address.available = False
            obj.ip_address.save()
        super(Host_infoAdmin, self).save_model(request, obj, form, change)
        # 发送邮件生成
        if change:  # 修改到期信息
            if obj.is_permanent:
                Mail.objects.filter(host=obj).delete()
            elif 'deadline' in form.changed_data:
                Mail.objects.filter(host=obj).delete()
                Mail.objects.create(host=obj, send_date=obj.deadline)
                Mail.objects.create(
                    host=obj,
                    send_date=obj.deadline - datetime.timedelta(days=3))
                Mail.objects.create(
                    host=obj,
                    send_date=obj.deadline - datetime.timedelta(days=7))
        else:  # 新增主机
            if not obj.is_permanent:
                Mail.objects.create(host=obj, send_date=obj.deadline)
                Mail.objects.create(
                    host=obj,
                    send_date=obj.deadline - datetime.timedelta(days=3))
                Mail.objects.create(
                    host=obj,
                    send_date=obj.deadline - datetime.timedelta(days=7))

    def delete_model(self, request, obj):
        obj.ip_address.available = True
        obj.ip_address.save()
        super(Host_infoAdmin, self).delete_model(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ip_address':
            if request.resolver_match.args:
                uuid = request.resolver_match.args[0]
                kwargs["queryset"] = IP_Resource.objects.filter(
                    Q(host_info__host_uuid=uuid) | Q(available=True))
            else:
                kwargs["queryset"] = IP_Resource.objects.filter(available=True)
        return super(Host_infoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


def ip_use(obj):
    if obj.host_info:
        return obj.host_info.description
    else:
        return ''


ip_use.short_description = '用途'
admin.site.register(Host_info, Host_infoAdmin)


class IP_ResourceAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    list_display = ('ip_address', 'available', ip_use)
    ordering = ('bin_ip', )


admin.site.register(IP_Resource, IP_ResourceAdmin)


class MailAdmin(admin.ModelAdmin):
    list_display = ('host', 'send_date', 'is_sent')


admin.site.register(Mail, MailAdmin)


class SentHistoryAdmin(admin.ModelAdmin):
    list_display = ('host', 'sent_date')


admin.site.register(SentHistory, SentHistoryAdmin)


class SvnAdmin(admin.ModelAdmin):
    list_display = ('proj_name_chinese', 'proj_name_english', 'proj_property', 'apply_time', 'pm',
                    'tm', 'dev', 'test_manager', 'test')


admin.site.register(Svn, SvnAdmin)
