from odoo import models, fields, api
from odoo.osv.expression import OR
from odoo.exceptions import UserError

class LiveSearchWizard(models.TransientModel):
    _name = 'live.search.wizard'
    _description = 'Assistant de recherche de lives'

    category_id = fields.Many2one('product.category', string="Catégorie")
    attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Valeurs de variantes")
    live_ids = fields.Many2many('live.shopping.beta', string="Lives trouvés")

    def action_search_lives(self):
        domain = []

        if self.category_id:
            domain.append(('categ_id', '=', self.category_id.id))

        if self.attribute_value_ids:
            # Si tu veux faire un filtre "variant_value_ids.name ilike valeur"
            # Par exemple, sur le premier élément des valeurs sélectionnées (ou concaténer)
            # Ici on prend le premier pour l'exemple
            valeur_cherchee = self.attribute_value_ids[0].name
            domain.append(('variant_value_ids.name', 'ilike', valeur_cherchee))

        lives = self.env['live.shopping.beta'].search(domain)

        self.live_ids = [(6, 0, lives.ids)]

        if not lives:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Résultat vide',
                    'message': 'Aucun live ne correspond aux critères.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        else:
            return {
            'name': 'Lives trouvés',
            'type': 'ir.actions.act_window',
            'res_model': 'live.shopping.beta',
            'view_mode': 'kanban',
            'views': [(self.env.ref('live_shopping_hr.live_shopping_view_kanban').id, 'kanban')],
            'domain': [('id', 'in', lives.ids)],
            'target': 'current',
        }






