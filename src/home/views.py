from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from home.models import Host_info, IP_Resource, Svn
from django.contrib import messages
from django.contrib.admin import widgets
from django import forms
from django.forms import Select
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.db.models import Q
import json

from home.forms import SvnForm
from authtools.models import User
from .tasks import send_svn_apply_mail

@login_required()
def index(request):
    list = [
        (1001, 'Lorem ', 'ipsum ', 'dolor ', 'sit'),
        (1002, 'amet ', 'consectetur ', 'adipiscing ', 'elit'),
        (1003, 'Integer ', 'nec ', 'odio ', 'Praesent'),
        (1003, 'libero ', 'Sed ', 'cursus ', 'ante'),
        (1004, 'dapibus ', 'diam ', 'Sed ', 'nisi'),
        (1005, 'Nulla ', 'quis ', 'sem ', 'at'),
        (1006, 'nibh ', 'elementum ', 'imperdiet ', 'Duis'),
        (1007, 'sagittis ', 'ipsum ', 'Praesent ', 'mauris'),
        (1008, 'Fusce ', 'nec ', 'tellus ', 'sed'),
        (1009, 'augue ', 'semper ', 'porta ', 'Mauris'),
        (1010, 'massa ', 'Vestibulum ', 'lacinia ', 'arcu'),
        (1011, 'eget ', 'nulla ', 'Class ', 'aptent'),
        (1012, 'taciti ', 'sociosqu ', 'ad ', 'litora'),
        (1013, 'torquent ', 'per ', 'conubia ', 'nostra'),
        (1014, 'per ', 'inceptos ', 'himenaeos ', 'Curabitur'),
        (1015, 'sodales ', 'ligula ', 'in ', 'libero')
    ]
    list1 = {'1': 1, '2': 2, '3': 3, '4': 4}
    return render(request, 'home/index.html', {'list': list, 'list1': list1})


def hostsJson(request):
    draw = int(request.GET.get('draw'))
    start = int(request.GET.get('start'))
    length = int(request.GET.get('length'))
    keyword = request.GET.get('search[value]')
    order_col = request.GET.get('order[0][column]')
    order_type = request.GET.get('order[0][dir]')
    if order_type == "asc":
        # 获取排序字段名，并且根据排序方法拼出排序字段
        order_para = request.GET.get('columns[%s][name]' % order_col)
    else:
        order_para = "-" + request.GET.get('columns[%s][name]' % order_col)

    # 关键字
    if keyword == "":
        keyword_result = Host_info.objects.all()
    else:
        keyword_result = Host_info.objects.filter(
            Q(ip_address__ip_address__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(os__icontains=keyword) |
            Q(maintainer__icontains=keyword)
        )
    # 总共条目数量
    recordstotal = Host_info.objects.all().count()
    # 过滤后的条目数量
    recordsfiltered = keyword_result.count()
    # 排序
    order_result = keyword_result.order_by(order_para)
    # 分页
    if length == -1:
        paginator_result = order_result
    else:
        paginator_result = order_result[start:(start + length)]
    # 序列化排序后的结果
    serialize_result = serializers.serialize("json", paginator_result)
    # 反序列化，为重组返回json用
    result = json.loads(serialize_result)
    # 组合返回json
    data_before_serialize = {"draw": draw, "recordsTotal": recordstotal,
                             "recordsFiltered": recordsfiltered, "data": result}
    data = json.dumps(data_before_serialize)
    return HttpResponse(data, content_type='application/json')


@login_required()
def hosts(request):
    """
    虚拟机资源
    """
    return render(request, 'home/hosts.html')


class datewidget(forms.Form):
    """
    (未使用)以django admin的时间插件构建时间插件给页面使用
    """
    timewidget = forms.DateTimeField(
        required=True, label='时间', widget=widgets.AdminDateWidget)


class Oswidget(forms.ModelForm):
    """
    构建操作系统下拉框插件
    """
    class Meta:
        model = Host_info
        fields = ['os']
        widgets = {
            'os': Select(attrs={'class': 'form-control'}),
        }


@login_required()
def host_detail(request, host_id, **kw):
    """
    虚拟机详情、编辑
    """
    if kw == {}:
        status = "detail"
    elif kw["status"] == 'change':
        status = "change"
    else:
        return HttpResponseNotFound()
    host_detail = get_object_or_404(Host_info, host_uuid=host_id)
    osc = Oswidget()
    return render(request, 'home/detail.html', {'host_detail': host_detail, 'osc': osc, 'status': status})


@login_required()
def new_add(request):
    osc = Oswidget()
    if request.method == 'GET':
        return render(request, 'home/add.html', {'osc': osc})
    else:
        ip_address = request.POST.get('ip_address')
        description = request.POST.get('description')
        cpu = request.POST.get('cpu')
        memory = request.POST.get('memory')
        storage = request.POST.get('storage')
        start_time = request.POST.get('start_time').replace("/","-")
        end_time = request.POST.get('end_time').replace("/","-")
        use = request.POST.get('use')
        maintainer = request.POST.get('maintainer')
        os = request.POST.get('os')
        modify_people = request.user
        Host_info.objects.create(
            ip_address=ip_address,
            description=description,
            cpu=cpu,
            memory=memory,
            storage=storage,
            start_time=start_time,
            end_time=end_time,
            use=use,
            maintainer=maintainer,
            os=os,
            modify_people=modify_people,
        )
        return HttpResponseRedirect("/hosts/")


@login_required()
def ip_resources(request):
    # if request.path == "/ip_resources/":
    return render(request, 'home/ip_resources.html', {'tab': 'ip_resources'})
    # elif request.path == "/ip_resources/add_network/":
    #     if request.method == 'GET':
    #         return render(request, 'home/ip_resources.html.j2', {'tab': 'add_network'})
    #     else:
    #         import IPy
    #         network = request.POST.get('network')
    #         netmask = request.POST.get('netmask')
    #         ip_list = IPy.IP(network + netmask)
    #         for i in ip_list:
    #             if i == ip_list.net() or i == ip_list.broadcast():
    #                 pass
    #             else:
    #                 try:
    #                     IP_Resource.objects.create(ip_address=i.strNormal(0) , available='available')
    #                 except Exception as e:
    #                     print(e)
    #                     return  render(request, 'home/ip_resources.html.j2', {'tab': 'add_network', 'add_success': 'fail'})
    #         return render(request, 'home/ip_resources.html.j2', {'tab': 'add_network', 'add_success': 'success'})


def ipJson(request):
    draw = int(request.GET.get('draw'))
    start = int(request.GET.get('start'))
    length = int(request.GET.get('length'))
    keyword = request.GET.get('search[value]')
    order_col = request.GET.get('order[0][column]')
    order_type = request.GET.get('order[0][dir]')
    if order_type == "asc":
        # 获取排序字段名，并且根据排序方法拼出排序字段
        order_para = request.GET.get('columns[%s][name]' % order_col)
    else:
        order_para = "-" + request.GET.get('columns[%s][name]' % order_col)

    # 关键字
    if keyword == "":
        keyword_result = IP_Resource.objects.all()
    else:
        A_DICT = {'在用': False, '空闲': True}
        if keyword in A_DICT:
            a_keyword = A_DICT[keyword]
            keyword_result = IP_Resource.objects.filter(
                Q(ip_address__icontains=keyword) |
                Q(available=a_keyword) |
                Q(host_info__description__icontains=keyword)
            )
        else:
            keyword_result = IP_Resource.objects.filter(
                Q(ip_address__icontains=keyword) |
                Q(host_info__description__icontains=keyword)
            )
    # 总共条目数量
    recordstotal = IP_Resource.objects.all().count()
    # 过滤后的条目数量
    recordsfiltered = keyword_result.count()
    # 排序
    order_result = keyword_result.order_by(order_para)
    # 分页
    if length == -1:
        paginator_result = order_result
    else:
        paginator_result = order_result[start:(start + length)]
    # 序列化排序后的结果
    # serialize_result = serializers.serialize("json", paginator_result.value(
    #     'ip_address', 'bin_ip', 'available', 'host_info__description'))
    serialize_result = paginator_result.values(
        'ip_address', 'bin_ip', 'available', 'host_info__description')
    # 反序列化，为重组返回json用
    result = json.dumps(list(serialize_result), ensure_ascii=False)
    # 组合返回json
    data_before_serialize = {"draw": draw, "recordsTotal": recordstotal,
                             "recordsFiltered": recordsfiltered, "data": json.loads(result)}
    data = json.dumps(data_before_serialize)
    return HttpResponse(data, content_type='application/json')


@login_required()
def svn_apply(request):
    # form = SvnForm
    if request.method == 'GET':
        return render(request, 'home/svn_apply.html')
    elif request.method == 'POST':
        proj_name_chinese = request.POST['proj_name_chinese']
        proj_name_english = request.POST['proj_name_english']
        center = request.POST['center']
        pm = [User.objects.get(id=x).name for x in request.POST.getlist('pm')]
        tm = [User.objects.get(id=x).name for x in request.POST.getlist('tm')]
        dev = [User.objects.get(id=x).name for x in request.POST.getlist('dev')]
        test_manager = [User.objects.get(id=x).name for x in request.POST.getlist('test_manager')]
        test = [User.objects.get(id=x).name for x in request.POST.getlist('test')]
        proj_property = request.POST['proj_property']
        svn = Svn.objects.create(
            applier=request.user.name,
            proj_name_chinese=proj_name_chinese,
            proj_name_english=proj_name_english,
            proj_property=proj_property,
            center=center,
            pm=','.join(pm),
            tm=','.join(tm),
            dev=','.join(dev),
            test_manager=','.join(test_manager),
            test=','.join(test),
        )
        send_svn_apply_mail.delay(svn, request.user)
        messages.success(request, """<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
  <strong>完成！</strong> 申请SVN成功，请等待实施人员开库。""")
        return render(request, 'home/svn_apply.html')


def svn_project_check(request):
    d = {}
    proj_name_english = request.GET.get('proj_name_english')
    proj_name_chinese = request.GET.get('proj_name_chinese')
    if proj_name_chinese:
        chinese = Svn.objects.filter(proj_name_chinese=proj_name_chinese)
        if chinese.exists():
            d["valid"] = False
        else:
            d["valid"] = True
        return JsonResponse(d)
    elif proj_name_english:
        english = Svn.objects.filter(proj_name_english=proj_name_english)
        if english.exists():
            d["valid"] = False
        else:
            d["valid"] = True
        return JsonResponse(d)
    else:
        return JsonResponse({"valid": 'null'})


def account(request):
    term = request.GET.get('term')
    page = request.GET.get('page') or 1
    page = int(page)
    users = User.objects.filter(email__icontains=term).values(
        'id', 'name', 'email')
    total_count = users.count()
    filter_users = users[page * 10 - 10:page * 10]
    s_users = json.dumps(list(filter_users), ensure_ascii=False)
    d = {"total_count": total_count, "results": json.loads(s_users)}
    return JsonResponse(d)


def svn_list(request):
    projects = Svn.objects.all()
    center1 = projects.filter(center='开发交付一中心')
    center2 = projects.filter(center='开发交付二中心')
    center3 = projects.filter(center='技术创新中心')
    center4 = projects.filter(center='支撑拓展中心')
    context = {'projects': projects,
               'center1': center1, 'center2': center2, 'center3': center3,
               'center4': center4}
    return render(request, 'home/svn_list.html', context)
