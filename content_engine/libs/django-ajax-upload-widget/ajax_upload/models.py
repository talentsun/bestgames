from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import os
import time

def get_media_upload_dir(instance,filename):
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #if os.path.exists(settings.MEDIA_ROOT + today):
    #    pass
    #else:
    #    os.makedirs(settings.MEDIA_ROOT + today)

    upload_dir = "%s/%s" % ('bestgames/upload_images/' + today, filename)
    #print "Upload dir set to: %s" % upload_dir
    return upload_dir

class UploadedFile(models.Model):
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    file = models.FileField( upload_to=get_media_upload_dir)

    class Meta:
        ordering = ('id',)
        verbose_name = _('uploaded file')
        verbose_name_plural = _('uploaded files')

    def __unicode__(self):
        return unicode(self.file)

    def delete(self, *args, **kwargs):
        super(UploadedFile, self).delete(*args, **kwargs)
        if self.file:
            self.file.delete()
    delete.alters_data = True
