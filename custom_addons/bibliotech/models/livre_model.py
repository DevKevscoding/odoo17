from odoo import fields, models, api
import qrcode
from io import BytesIO
from base64 import b64encode


class Bibliotch_Livre(models.Model):
    _name = "bibliotech.livre"
    _description = "Livre"
    _sql_constraints = [
        ('unique_livre_name', 'unique(name)',
         'Le nom de ce livre est déja utiliser .'),
        ('unique_livre_isbn', 'unique(isbn)', 'Ce ISBN est deja attribué .')
    ]

    name = fields.Char(required=True)
    annee_parution = fields.Integer(string="Annee de parution")
    auteur = fields.Char(string="Auteur", required=True)
    image = fields.Binary('Couverture')
    qr_code = fields.Binary(string="QR CODE", store=False,
                            readonly=True, compute="_compute_qrcode_image")
    etat = fields.Char('Etat', default='Disponible', readonly=True)
    isbn = fields.Char(required=True)
    edition = fields.Char(string="Edition")
    category_ids = fields.Many2many('bibliotech.category')
    resume = fields.Text("Un bref résumée")
    nbr_stock = fields.Integer(string="Nombre en stock")
    public = fields.Selection([
        ('enfant', 'Enfant'),
        ('ado', 'Ado'),
        ('adulte', 'Adulte'),
        ('tous', 'Tous publics')
    ])
    prix = fields.Monetary(string="Prix unitaire", currency_field='devise')
    devise = fields.Many2one('res.currency', string="Devise", required=True,
                             default=lambda self: self.env.company.currency_id.id)

    @api.depends("isbn")
    def _compute_qrcode_image(self):
        for o in self:
            if o.isbn:
                o.qr_code = self.generate_qrcode_image(o.isbn)
            else:
                o.qr_code = False

    def generate_qrcode_image(self, data):
        img = qrcode.make(data)
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return b64encode(buffer.getvalue()).decode('utf-8')

    def transaction_livre(self):
        if self.etat == 'Disponible':
            self.etat = 'Emprunter'
        else:
            self.etat = 'Disponible'
