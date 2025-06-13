from odoo import models, fields

class DeliverySeason(models.Model):
    _name = 'live.season'
    _description = 'Season de live'
    _sql_constraints = [
        (
            'unique_name',
            'unique(name)',
            'Cette season est déja enregistrer .'
        ),
    ]

    name = fields.Char(string='Name', required=True)
