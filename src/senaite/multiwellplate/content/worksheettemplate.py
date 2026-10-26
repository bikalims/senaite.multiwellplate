# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.MULTIWELLPLATE.
#
# SENAITE.MULTIWELLPLATE is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2026 by it's authors.
# Some rights reserved, see README and LICENSE.

from plone.supermodel import model
from senaite.core.content.worksheettemplate import IWorksheetTemplateSchema
from zope.schema import getFieldsInOrder

from senaite.multiwellplate import messageFactory as _
from senaite.multiwellplate.schema import MultiWellPlateConfigSchema


MULTIWELLPLATE_FIELDS = [
    name for name, field in getFieldsInOrder(MultiWellPlateConfigSchema)
]


class IMultiWellPlateWorksheetTemplateSchema(
        IWorksheetTemplateSchema, MultiWellPlateConfigSchema):
    """Worksheet template schema selected only by the installed site's FTI.

    Never modify IWorksheetTemplateSchema: it is shared by every Plone site
    in the process, including sites without the add-on's browser layer.
    """

    model.fieldset(
        "multiwellplate",
        label=_(u"label_fieldset_multiwellplate", default=u"MultiWell Plate"),
        fields=MULTIWELLPLATE_FIELDS,
    )
