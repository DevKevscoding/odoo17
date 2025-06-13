from odoo import models, fields

class DeliveryPerson(models.Model):
    _name = 'delivery.person'
    _description = 'Delivery Person'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')