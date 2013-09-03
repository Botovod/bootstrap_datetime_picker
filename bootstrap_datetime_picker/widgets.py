# coding: utf-8
from __future__ import unicode_literals
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.utils import formats, datetime_safe
from django.utils.encoding import force_text
from datetime import datetime
import re

dateFormatConversion = {
    'P' : '%p',
    'ss' : '%S',
    'mm' : '%M',
    'hh' : '%H',
    'HH' :  '%I',
    'dd' : '%d',
    'MM' : '%m',
    'yy' : '%y',
    'yyyy' : '%Y',
}


class BootstrapDateTimePicker(TextInput):
    def __init__(self, attrs=None, disable_date=False, disable_time=False,  date_format=None, time_format=None, language='ru', ):
        super(BootstrapDateTimePicker, self).__init__(attrs=attrs)
        pattern = re.compile(r'\b(' + '|'.join(dateFormatConversion.keys()) + r')\b')
        self.format = ''
        if date_format and time_format and disable_date is False and disable_time is False:
            self.format = "{0} {1}".format(date_format, time_format)
        elif date_format and disable_time is True:
            self.format = date_format
        elif time_format and disable_date is True:
            self.format = time_format
        self.html_format = self.format
        self.format = pattern.sub(lambda x: dateFormatConversion[x.group()], self.format)
        self.params = "language: '{lang}'".format(lang=language)
        if disable_date:
            self.params += ", pickDate: false"
        if disable_time:
            self.params += ", pickTime: false"

    def _format_value(self, value):
        # import ipdb; ipdb.set_trace()
        if self.is_localized:
            return formats.localize_input(value)
        elif hasattr(value, 'strftime'):
            value = datetime_safe.new_datetime(value)
            return value.strftime(self.format)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        value = force_text(self._format_value(value))
        template = '''
        <div id="id_{name}" class="input-append date">
           <input class="datetimepicker" data-format="{format}" name="{name}" value="{value}" type="text">
            <span class="add-on">
                <i data-time-icon="icon-time" data-date-icon="icon-calendar">
                </i>
            </span>
        </div>
        '''.format(format=self.html_format, name=name, value=value)
        script = '''
        <script type="text/javascript">
          $(function() {
            $('#id_''' + name + ''' ').datetimepicker({
            ''' + self.params + '''
            });
          });
        </script>
        '''
        return mark_safe(template+script)