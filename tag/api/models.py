# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
