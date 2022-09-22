from .celery import app as celery_app

__all__ = ('celery_app,')

# если не заработает
# from __future__ import absolute_import, unicode_literals
# from  .celory import app as celery_app
#
# __all__ = ('celery_app,')