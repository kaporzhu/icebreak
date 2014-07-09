# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django import forms

from .models import TimeFrame


class TimeFrameForm(forms.ModelForm):
    """
    Model form for TimeFrame
    """
    class Meta:
        model = TimeFrame
        exclude = ('shop',)

    def clean_sections(self):
        """
        Convert sections text for JSON formation string
        """
        sections = []
        for line in self.data['sections'].split('\n'):
            if line.strip():
                label, time = line.strip().split('|')
                # check time format
                try:
                    if time.count(':') == 1:
                        time = datetime.strptime(time, '%H:%M')
                    else:
                        time = datetime.strptime(time, '%H:%M:%S')
                except:
                    raise forms.ValidationError(u'时间格式不对')
                sections.append({'label': label.strip(),
                                 'time': time.strftime('%H:%M:%S')})
        return json.dumps(sections)
