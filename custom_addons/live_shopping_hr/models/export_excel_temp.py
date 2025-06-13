from odoo import models, fields

class ExportExcelTemp(models.TransientModel):
    _name = 'export.excel.temp'
    _description = 'Fichier Excel à télécharger'

    file_name = fields.Char(string="Nom du fichier")
    file_data = fields.Binary(string="Fichier", readonly=True)
