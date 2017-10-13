# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import re
import boto
from boto.exception import S3ResponseError
from boto.s3.connection import OrdinaryCallingFormat
import os
import xml
import tempfile

from pkg_resources import Requirement, resource_stream
from anthem.lyrics.loaders import load_csv_stream


req = Requirement.parse('sensefly-odoo')


class S3Uri(object):

    _url_re = re.compile("^s3:///*([^/]*)/?(.*)", re.IGNORECASE | re.UNICODE)

    def __init__(self, uri):
        match = self._url_re.match(uri)
        if not match:
            raise ValueError("%s: is not a valid S3 URI" % (uri,))
        self._bucket, self._item = match.groups()

    def bucket(self):
        return self._bucket

    def item(self):
        return self._item


def _parse_s3_error(s3error):
    msg = s3error.reason
    # S3 error message is a XML message...
    doc = xml.dom.minidom.parseString(s3error.body)
    msg_node = doc.getElementsByTagName('Message')
    if msg_node:
        msg = '%s: %s' % (msg, msg_node[0].childNodes[0].data)
    return msg


def _get_s3_bucket(name=None):
    """Connect to S3 and return the bucket

    The following environment variables can be set:
    * ``AWS_ACCESS_KEY_ID``
    * ``AWS_SECRET_ACCESS_KEY``
    * ``AWS_REGION``
    * ``AWS_BUCKETNAME``

    If a name is provided, we'll read this bucket, otherwise, the bucket
    from the environment variable ``AWS_BUCKETNAME`` will be read.

    """
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region_name = os.environ.get('AWS_REGION')
    if name:
        bucket_name = name
    else:
        bucket_name = os.environ.get('AWS_BUCKETNAME')
    if not (access_key and secret_key and bucket_name and region_name):
        msg = ('If you want to read from the %s S3 bucket, the following '
               'environment variables must be set:\n'
               '* AWS_ACCESS_KEY_ID\n'
               '* AWS_SECRET_ACCESS_KEY\n'
               '* AWS_REGION\n'
               '* AWS_BUCKETNAME\n'
               ) % (bucket_name, )

        raise Exception(msg)

    try:
        # seems only connect_to_region works
        # we can't use boto.connect_s3 due to
        # S3ResponseError: 301 Moved Permanently
        conn = boto.s3.connect_to_region(
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            calling_format=OrdinaryCallingFormat())

    except S3ResponseError as error:
        # log verbose error from s3, return short message for user
        raise Exception(_parse_s3_error(error))

    bucket = conn.lookup(bucket_name)
    if not bucket:
        bucket = conn.create_bucket(bucket_name)
    return bucket


def get_content(req, path):
    if path.startswith('s3://'):
        # Use local file if USE_S3 env var is false
        # USE_S3 env var must be set
        if 'USE_S3' not in os.environ:
            msg = ('It must be explicit if S3 must be used or not.'
                   ' Please define USE_S3 environment variable.')
            raise Exception(msg)
        if not os.environ.get('USE_S3'):
            # replace s3://bucket_name/ by data/ to use local file
            path = '/'.join(['data'] + path[5:].split('/')[1:])

    if path.startswith('s3://'):
        s3uri = S3Uri(path)
        bucket = _get_s3_bucket(name=s3uri.bucket())
        filekey = bucket.get_key(s3uri.item())
        if not filekey:
            raise Exception(
                "file '%s' is missing on object storage", path
            )
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.write(filekey.get_contents_as_string())
        tmp_file.seek(0)
        content = tmp_file
    else:
        content = resource_stream(req, path)
    return content


def load_csv(ctx, path, model, delimiter=','):
    content = get_content(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter)
