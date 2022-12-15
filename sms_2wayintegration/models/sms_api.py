# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.iap.tools import iap_tools
DEFAULT_ENDPOINT = 'https://iap.odoo.com'
import requests

def iap_jsonrpc(url, method='call', params=None, timeout=15):
    from odoo.http import request
    user = request.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_user_name')
    password = request.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_api_key')
    originator = request.env['ir.config_parameter'].sudo().get_param('sms_2wayintegration.msegat_user_sender')
    result=[]
    if params and params.get('messages', False):
        for p in params.get('messages'):
            url = "https://svr22.synermaxx.asia/vmobile/suysing/api/sendnow.php?username=%s&password=%s&mobilenum=%s&fullmesg=%s&originator=%s" %(
                user, password,
                p.get('number',False),
                p.get('content',False),
                originator)
            response = requests.get(url)
            if response.status_code == 200:
                result.append({'state': 'success', 'credit': 0, 'res_id': p.get('res_id', False)})
            else:
                result.append({'state': 'unregistered', 'credit': 0, 'res_id': p.get('res_id', False)})
    return result

iap_tools.iap_jsonrpc = iap_jsonrpc

