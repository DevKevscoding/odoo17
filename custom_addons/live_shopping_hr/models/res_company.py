# models/res_company.py

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    nif = fields.Char(string="NIF")
    stat = fields.Char(string="STAT")
    rcs = fields.Char(string="RCS")
