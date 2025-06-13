from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    code_ref = fields.Char(string="Code Live", help="Code utilisé pour générer les références en live.")