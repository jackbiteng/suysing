# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import werkzeug
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
            params_json = {
                "username": user,
                "password": password,
                "mobilenum": p.get('number',False),
                "originator": originator,
                "fullmesg": p.get('content',False)
            }
            url = "https://svr22.synermaxx.asia/vmobile/suysing/api/sendnow.php?"+werkzeug.urls.url_encode(params_json)
            response = requests.get(url)
            if not response.text.split('|')[0].endswith('NACK'):
                result.append({'state': 'success', 'credit': 0, 'res_id': p.get('res_id', False)})
            else:
                result.append({'state': 'unregistered', 'credit': 0, 'res_id': p.get('res_id', False)})
    return result

iap_tools.iap_jsonrpc = iap_jsonrpc

