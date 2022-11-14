# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    msegat_user_name = fields.Char("Synermaxx User Name")
    msegat_api_key = fields.Char("Synermaxx Password")
    msegat_user_sender = fields.Char("Synermaxx Originator")

    @api.model
    def get_values(self):
        res = super(ResConfig, self).get_values()
        res.update(
            msegat_user_name=self.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_user_name'),
            msegat_api_key=self.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_api_key'),
            msegat_user_sender=self.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_user_sender')
        )
        return res

    def set_values(self):
        super(ResConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sms_2wayintegration.msegat_user_name', self.msegat_user_name)
        self.env['ir.config_parameter'].sudo().set_param('sms_2wayintegration.msegat_api_key', self.msegat_api_key)
        self.env['ir.config_parameter'].sudo().set_param('sms_2wayintegration.msegat_user_sender', self.msegat_user_sender)
