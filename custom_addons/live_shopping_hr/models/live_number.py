from odoo import models, fields, api

class NumberSeason(models.Model):
    _name = 'live.number'
    _description = 'Numero de live'
    _sql_constraints = [
        (
            'unique_name',
            'unique(name)',
            'Ce numero de live est déja enregistrer .'
        ),
    ]

    name = fields.Char(string='Name', required=True,
        readonly=True,
        copy=False,
        default=lambda self: self._get_next_live_number()
    )
