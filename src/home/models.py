from django.db import models
import uuid
import django.utils.timezone


class Host_info(models.Model):

    host_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    modify_time = models.DateTimeField(
        verbose_name='修改时间', editable=False, auto_now=True)
    modify_people = models.CharField(
        verbose_name='修改人', editable=False, max_length=30)
    ip_address = models.OneToOneField(
        'IP_Resource',
        verbose_name='IP地址',
        on_delete=models.CASCADE)
    description = models.TextField(verbose_name='描述', blank=True)
    cpu = models.IntegerField(verbose_name='CPU(核)', blank=True, null=True)
    memory = models.IntegerField(verbose_name='内存(G)', blank=True, null=True)
    storage = models.IntegerField(verbose_name='硬盘(G)', blank=True, null=True)
    # 申请日期
    start_time = models.DateField(
        verbose_name='申请日期', max_length=20, default=django.utils.timezone.now)
    # 到期日期
    deadline = models.DateField(verbose_name='到期日期', blank=True, null=True)
    # 是否永久使用
    is_permanent = models.BooleanField(
        verbose_name='是否永久使用', default=False)
    # 用途(以后待用)
    use = models.TextField(blank=True)
    # 维护人员
    maintainer = models.CharField(verbose_name='维护人/组', max_length=30)
    # 机房
    LOCATION_CHOICES = (('理想公司测试机房', '理想公司测试机房'), ('生产机房', '生产机房'))
    location = models.CharField(
        verbose_name='所在机房', max_length=30, choices=LOCATION_CHOICES)
    # 操作系统
    OS_CHOICES = (
        ('Windows', (
            ('WindowsServer2008', 'WindowsServer2008'),
            ('Windows7', 'Windows7'),
        )
        ),
        ('Linux', (
            ('Centos6', 'Centos6'),
            ('Centos7', 'Centos7'),
            ('RedHat6', 'RedHat6'),
            ('RedHat7', 'RedHat7'),
            ('Suse', 'Suse'),
        )
        )
    )
    os = models.CharField(verbose_name='操作系统', max_length=20,
                          choices=OS_CHOICES, blank=True)

    def __str__(self):
        return '[{0}]{1}'.format(self.ip_address.ip_address,
                                 str(self.host_uuid))


class IP_Resource(models.Model):

    class Meta:
        ordering = ['bin_ip']

    ip_address = models.GenericIPAddressField(
        verbose_name='IP地址', primary_key=True, unique=True)
    # 排序用,ip转int
    bin_ip = models.BigIntegerField(editable=False)
    # 是否可用
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        '''
        保存的时候生成，用来正确ip排序
        '''
        octets = list(map(int, self.ip_address.split(".")))
        self.bin_ip = octets[0] * 256**3 + octets[1] * \
            256**2 + octets[2] * 256 + octets[3]
        super(IP_Resource, self).save(*args, **kwargs)

    def __str__(self):
        return self.ip_address
