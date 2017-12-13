from __future__ import absolute_import
from celery import shared_task
from .models import Mail, SentHistory
from templated_email import send_templated_mail
import datetime


@shared_task
def sendmail():
    mail_list = Mail.objects.filter(is_sent=False)
    for i in mail_list:
        if i.send_date == datetime.date.today():
            left_day = (i.host.deadline - i.send_date).days
            if left_day == 0:
                left_msg = '今天'
            else:
                left_msg = '还有%s天' % left_day
            send_templated_mail(
                template_name='host',
                from_email='产品创新部运维管理系统 <huangxj@ideal.sh.cn>',
                recipient_list=[i.host.maintainer.email],
                context={
                    'left_day': left_msg,
                    'username': i.host.maintainer.name,
                    'ip': i.host.ip_address.ip_address,
                    'description': i.host.description,
                    'cpu': i.host.cpu,
                    'memory': i.host.memory,
                    'disk': i.host.storage,
                    'start_time': i.host.start_time,
                    'deadline': i.host.deadline,
                    'location': i.host.location
                },
                cc=['liuyj2016@ideal.sh.cn'],
            )
            i.is_sent = True
            i.save()
            SentHistory.objects.create(host=i.host)


@shared_task
def send_svn_apply_mail(svn, applier):
    send_templated_mail(
        template_name='svn_apply',
        from_email='产品创新部运维管理系统 <huangxj@ideal.sh.cn>',
        recipient_list=['huangxj@ideal.sh.cn', 'liuyj2016@ideal.sh.cn'],
        context={
            'applier': svn.applier,
            'proj_name_chinese': svn.proj_name_chinese,
            'proj_name_english': svn.proj_name_english,
            'pm': svn.pm,
            'tm': svn.tm,
            'dev': svn.dev,
            'test_manager': svn.test_manager,
            'test': svn.test,
            'proj_property': svn.proj_property,
            'center': svn.center
        },
        cc=[applier.email],
    )
