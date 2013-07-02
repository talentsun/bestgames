import uuid

from django import forms

from .models import UploadedFile

import time, random


class UploadedFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ('file',)

    def clean_file(self):
        data = self.cleaned_data['file']
        # Change the name of the file to something unguessable
        # Construct the new name as <unique-hex>-<original>.<ext>
        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        mimetype = data.name.split('.')[-1]
        name = random.randint(10000, 20000) + '.' + mimetype
        data.name = u'%s-%s' % (today, name)
        return data
