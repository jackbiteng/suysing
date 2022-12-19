# -*- coding: utf-8 -*-
import json
from odoo import fields, models
from apiclient import errors
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
from odoo.addons.gd_api_auto_read.module.GoogleService import Create_Service
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveServiceConfig(models.Model):
    _name = "drive.service.config"
    _description = "Drive Service Config"

    name = fields.Char()
    folder_id = fields.Char('Source Folder ID')
    dest_folder_id = fields.Char('Archived Folder ID')
    api_name = fields.Char(default='drive', readonly=True)
    api_version = fields.Char(default='v3', readonly=True)
    connected = fields.Boolean()

    def disconnect_connection(self):
        client_config_id = self.env['drive.service.config'].search([])
        if not client_config_id:
            self.env['drive.reading.history'].create({'name': 'No Config Found'})
        client_config_id.write({'connected': False})

    def test_connection(self):
        try:
            client_config_id = self.env['drive.service.config'].search([])
            if not client_config_id:
                self.env['drive.reading.history'].create({'name': 'No Config Found'})
                raise UserError('No Drive Config Found')
            CLIENT_SECRET_FILE = get_module_resource('gd_api_auto_read', 'static/', 'client_secret.json')
            API_NAME = client_config_id.api_name
            API_VERSION = client_config_id.api_version        
            FOLDER_ID = client_config_id.folder_id
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            print(dir(service))
            #about = service.about().get().execute()
            #print(about)
            if service:
                self.connected = True
        except Exception as e:
            self.env['drive.reading.history'].create({'name': 'Exception', 'description': e, 'has_error': True})
            raise UserError(e)
            