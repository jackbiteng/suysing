# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models, _


class SendSMS(models.TransientModel):
    _inherit = 'sms.composer'

    def _prepare_mass_sms_values(self, records):
        all_bodies = self._prepare_body_values(records)
        all_recipients = self._prepare_recipient_values(records)
        blacklist_ids = self._get_blacklist_record_ids(records, all_recipients)
        optout_ids = self._get_optout_record_ids(records, all_recipients)
        done_ids = self._get_done_record_ids(records, all_recipients)

        result = {}
        for record in records:
            recipients = all_recipients[record.id]
            sanitized = recipients['sanitized']
            if sanitized and record.id in blacklist_ids:
                state = 'canceled'
                failure_type = 'sms_blacklist'
            elif sanitized and record.id in optout_ids:
                state = 'canceled'
                failure_type = 'sms_optout'
            elif sanitized and record.id in done_ids:
                state = 'canceled'
                failure_type = 'sms_duplicate'
            elif not sanitized and not recipients['number']:
                state = 'canceled'
                failure_type = 'sms_number_format' if recipients['number'] else 'sms_number_missing'
            else:
                state = 'outgoing'
                failure_type = ''

            result[record.id] = {
                'body': all_bodies[record.id],
                'partner_id': recipients['partner'].id,
                'number': sanitized if sanitized else recipients['number'],
                'state': state,
                'failure_type': failure_type,
            }
        return result