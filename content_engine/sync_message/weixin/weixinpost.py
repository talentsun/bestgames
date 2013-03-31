import logging
import os
from os.path import abspath, isabs, isdir, isfile, join
import random
import string
import sys
import mimetypes
import urllib2
import httplib
import time
import re

class weixin:
    def random_string (length):
        return ''.join (random.choice (string.letters) for ii in range (length + 1))

    def encode_multipart_data (data, files):
        boundary = random_string (30)

        def get_content_type (filename):
            return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

        def encode_field (field_name):
            return ('--' + boundary,
                    'Content-Disposition: form-data; name="%s"' % field_name,
                    '', str (data [field_name]))

        def encode_file (field_name):
            filename = files [field_name]
            return ('--' + boundary,
                    'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
                    'Content-Type: %s' % get_content_type(filename),
                    '', open (filename, 'rb').read ())

        lines = []
        for name in data:
            lines.extend (encode_field (name))
        for name in files:
            lines.extend (encode_file (name))
        lines.extend (('--%s--' % boundary, ''))
        body = '\r\n'.join (lines)

        headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
                   'content-length': str (len (body))
                    'Cookie': 'hasWarningUser=1; pgv_pvid=8543179264;'
                              ' o_cookie=406465841; ptui_loginuin=406465841; '
                              'pt2gguin=o0406465841; uin=o0406465841; '
                              'skey=@tcOcZmwn8; pgv_info=ssid=s7651662416; '
                              'ptisp=cn; cert=r3Q5L_HLpcUJUv7ooPb6vhTzhMW1yKVZ; '
                              'slave_user=gh_d8d72c671c22; '
                              'slave_sid=MDE4SURFQlp2MGg4VnRvT0p5NTdFM2FJdzY4ek44ZUw3b'
                              'XFLWTFHczFWeVVtV0k0c05iM09qTGtxVVJhXzJUNm1pT2pqckpqbGhjSGFTS0NFVkdxY29JQ2h5TWV5RWlVVTVjZHVUd1E3R3dpeWZTYlMyU3pHQUZmcUVMV2pzeXQ='}

        return body, headers

    def send_post (url, data, files):
        req = urllib2.Request (url)
        connection = httplib.HTTPConnection (req.get_host ())
        connection.request ('POST', req.get_selector (),
            encode_multipart_data (data, files))
        response = connection.getresponse ()
        logging.debug ('response = %s', response.read ())
        logging.debug ('Code: %s %s', response.status, response.reason)


    def upload_file (path, current, total):
        assert isabs (path)
        assert isfile (path)

            logging.debug ('Uploading %r to %r', path, server)
            message_template = string.Template (message or default_message)

            data = {'MAX_FILE_SIZE': '3145728',
                    'sub': '',
                    'mode': 'regist',
                    'com': message_template.safe_substitute (current = current, total = total),
                    'resto': thread,
                    'name': username or '',
                    'email': email or '',
                    'pwd': password or random_string (20),}
            files = {'upfile': path}

            send_post (server, data, files)

            logging.info ('Uploaded %r', path)
            rand_delay = random.randint (delay, delay + 5)
            logging.debug ('Sleeping for %.2f seconds------------------------------\n\n', rand_delay)
            time.sleep (rand_delay)

        return upload_file

    def upload_directory (path, upload_file):
        assert isabs (path)
        assert isdir (path)

        matching_filenames = []
        file_matcher = re.compile (r'\.(?:jpe?g|gif|png)$', re.IGNORECASE)

        for dirpath, dirnames, filenames in os.walk (path):
            for name in filenames:
                file_path = join (dirpath, name)
                logging.debug ('Testing file_path %r', file_path)
                if file_matcher.search (file_path):
                    matching_filenames.append (file_path)
                else:
                    logging.info ('Ignoring non-image file %r', path)

        total_count = len (matching_filenames)
        for index, file_path in enumerate (matching_filenames):
            upload_file (file_path, index + 1, total_count)

    def run_upload (options, paths):
        upload_file = make_upload_file (**options)

        for arg in paths:
            path = abspath (arg)
            if isdir (path):
                upload_directory (path, upload_file)
            elif isfile (path):
                upload_file (path)
            else:
                logging.error ('No such path: %r' % path)

        logging.info ('Done!')