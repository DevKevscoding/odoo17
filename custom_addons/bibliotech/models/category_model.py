from odoo import fields, api, models


class Bibliotech_category(models.Model):
    _name = "bibliotech.category"
    _description = "Categorie livre"
    _sql_constraints = [
        ('unique_category_name', 'unique(name)',
         'Ce nom de categorie est déja enregistrer.'),
    ]

    name = fields.Char(string="Nom de la categorie", required=True)
    description = fields.Text(string="Description")
