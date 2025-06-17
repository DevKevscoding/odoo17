from odoo import models, fields


class DonnerNote(models.TransientModel):
    _name = "donner.note"
    _description = "Pour donner une note"

    note = fields.Integer("Note (sur 10)")

    def donner_note(self):
        Livre = self.env['bibliotech.livre']
        livre_id = Livre.browse(self.env.context['livre_id'])
        livre_id.note = self.note
