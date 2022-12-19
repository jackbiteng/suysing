# -*- coding: utf-8 -*-
from apiclient import http
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.gd_api_auto_read.module.GoogleService import Create_Service


SCOPES = ['https://www.googleapis.com/auth/drive']

class CrmLead(models.Model):
    _inherit = "crm.lead"

    drive_filename = fields.Char('Filename')
    drive_file_id = fields.Char('File ID')

    def _cron_auto_read_files(self):
        client_config_id = self.env['drive.service.config'].search([])
        if not client_config_id:
            self.env['drive.reading.history'].create({'name': 'No Config Found'})
            raise UserError('No Drive Config Found')
        
        if not client_config_id.connected:
            self.env['drive.reading.history'].create({'name': 'Please check connection'})
            raise UserError('Please check connection')
        CLIENT_SECRET_FILE = "custom/gd_api_auto_read/data/client_secret.json"
        API_NAME = client_config_id.api_name
        API_VERSION = client_config_id.api_version        
        FOLDER_ID = client_config_id.folder_id
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        query = f"parents = '{FOLDER_ID}' and mimeType='text/csv'"
        response = service.files().list(q=query,pageSize=10).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')
        while nextPageToken:
            response = service.files().list(q=query, pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        for file in files:
            self.process_file(service, file)
            
            
    def generate_error_log(self, e, file):
        self.env['drive.reading.history'].create({
            'name': f"Exception in '{file.get('name')}'", 'description': e, 'has_error': True})

    def generate_complete_log(self, file):
        self.env['drive.reading.history'].create({
            'name': f"'{file.get('name')}' reading complete", 
            'description': f"'{file.get('name')}' reading successfully"})

    def process_file(self, service, file):
        try:
            print('Processing the file...')
            fileContent = service.files().get_media(fileId=file.get('id')).execute().decode()
            headers = fileContent.split('\n')[0]
            datas = fileContent.split('\n')[1]
            headersArray = headers.split(',')
            dataArray = datas.split(',')
            dataArray.insert(3, "")
            formattedContent = []
            for colIndex in range(0, len(headersArray)):
                valueDict = {}
                key = self.get_valid_format_string(headersArray[colIndex])
                valueDict[key] = self.get_valid_format_string(dataArray[colIndex])
                formattedContent.append(valueDict)
            self.create_lead_record(formattedContent, service, file)
        except Exception as e:
            print(e)
            self.generate_error_log(e, file)

    def create_lead_record(self, formattedContent, service, file):
        print('Generating new record...')
        for leadRecord in formattedContent:
            crmVals = {
                'drive_filename': file.get('name'),
                'drive_file_id': file.get('id'),
                'email_from': self.get_valid_format_string(leadRecord.get('Email Address')),
                'mobile': self.get_valid_format_string(leadRecord.get('Mobile Number')),
                'x_studio_existing_suy_sing_customer': self.get_valid_format_string(leadRecord.get('Do you have an existing account with Suy Sing?')),
                'x_studio_what_is_your_customer_code_1': self.get_valid_format_string(leadRecord.get('For Existing Customers')),
                'name': self.get_valid_format_string(leadRecord.get(' First Name')),
                'x_studio_purpose_of_inquiry_1': self.get_valid_format_string(leadRecord.get('Purpose of inquiry')),
                'x_studio_last_name': self.get_valid_format_string(leadRecord.get('Last Name')),
                'x_studio_facebook_name_1': self.get_valid_format_string(leadRecord.get('Facebook Name')),
                'phone': self.get_valid_format_string(leadRecord.get('Landline Number')),
                'x_studio_do_you_have_existing_store_or_business': self.get_valid_format_string(leadRecord.get('Do you have an existing store or business?')),
                'x_studio_how_many_years_in_the_business_1': self.get_valid_format_string(leadRecord.get('How many years in the business?')),
                'x_studio_storebusiness_format': self.get_valid_format_string(leadRecord.get('Store/Business Format')),
                'x_studio_storedelivery_location_1': self.get_valid_format_string(leadRecord.get('Delivery location')),
                'x_studio_province_1': self.get_valid_format_string(leadRecord.get('Province')),
                'x_studio_where_did_you_hear_about_us': self.get_valid_format_string(leadRecord.get('Where did you hear about us?')),
            }
            if not crmVals['name']:
                crmVals.update({'name': self.get_valid_format_string(leadRecord.get('Purpose of inquiry'))})

            if not crmVals['name']:
                self.env['drive.reading.history'].create({
                    'name': "Data Format Error", 
                    'description': f"{file.get('name')}' does not contains First Name and Purpose of inquiry", 
                    'has_error': True})
            else:
                crm_id = self.env['crm.lead'].create(crmVals)
                if crm_id:
                    self.generate_complete_log(file)
                    self.move_to_archived(service, file)

    def get_valid_format_string(self, content):
        if not content:
            return False
        strContent = content
        if strContent.startswith("'"):
            strContent = strContent[1:]
        if strContent.startswith('"'):
            strContent = strContent[1:]
        if strContent.endswith("'"):
            strContent = strContent[:-1]
        if strContent.endswith('"'):
            strContent = strContent[:-1]
        if strContent == 'None':
            return False
        elif len(strContent) == 0:
            return False
        else:
            return strContent

    def move_to_archived(self, service, file):
        print('Archiving the file...')
        client_config_id = self.env['drive.service.config'].search([])
        service.files().update(
            fileId=file.get('id'),
            addParents=client_config_id.dest_folder_id,
            removeParents=client_config_id.folder_id
        ).execute()

