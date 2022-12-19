# -*- coding: utf-8 -*-
from odoo import fields, models, tools, _

class GoogleDriveReadingHistory(models.Model):
    _name = "drive.reading.history"
    _description = "Drive Reading History"

    name = fields.Char()
    description = fields.Text()
    has_error = fields.Boolean('Error')