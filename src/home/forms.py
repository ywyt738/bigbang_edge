from django import forms
from .models import Svn
from easy_select2 import Select2Multiple
from authtools.models import User
from crispy_forms.layout import Layout, Field, Submit, Button
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse_lazy


class SvnForm(forms.ModelForm):
    pm = forms.ModelMultipleChoiceField(
        label='项目经理',
        queryset=User.objects.all(),
        widget=Select2Multiple(select2attrs={'width': '100%'}))
    tm = forms.ModelMultipleChoiceField(
        label='技术经理',
        queryset=User.objects.all(),
        widget=Select2Multiple(select2attrs={'width': '100%'}))
    dev = forms.ModelMultipleChoiceField(
        label='开发人员',
        queryset=User.objects.all(),
        widget=Select2Multiple(select2attrs={'width': '100%'}))
    test_manager = forms.ModelMultipleChoiceField(
        label='测试经理',
        queryset=User.objects.all(),
        widget=Select2Multiple(select2attrs={'width': '100%'}))
    test = forms.ModelMultipleChoiceField(
        label='测试人员',
        queryset=User.objects.all(),
        widget=Select2Multiple(select2attrs={'width': '100%'}),
        required=False,
        )

    class Meta:
        model = Svn
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SvnForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse_lazy('svn')
        self.helper.layout = Layout(
            Field('proj_name_chinese', wrapper_class="col-md-6"),
            Field('proj_name_english', wrapper_class="col-md-6"),
            Field('pm', wrapper_class="col-md-6"),
            Field('tm', wrapper_class="col-md-6"),
            Field('dev', wrapper_class="col-md-12"),
            Field('test_manager', wrapper_class="col-md-6"),
            Field('test', wrapper_class="col-md-6"),
            Field('proj_property', wrapper_class="col-md-12"),
            Field('center', wrapper_class="col-md-12"),
            FormActions(
                Submit('submit', '提交'),
                Button('cancle', '取消'),
                css_class="col-md-12"
            )
        )
