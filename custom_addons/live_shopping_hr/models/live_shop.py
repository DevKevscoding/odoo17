from odoo import fields,models,api
from odoo.exceptions import UserError
from collections import defaultdict
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics import renderPM
from io import BytesIO
import base64
import xlsxwriter
from datetime import datetime
import random

import logging
_logger = logging.getLogger(__name__)

from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    live_reference = fields.Char(string="Référence Produit (Live)")

class LiveShoppingBeta(models.Model):
    _name = 'live.shopping.beta'
    _description = "Live Shopping Product"
    _sql_constraints = [
        ('barcode_unique', 'unique(barcode)', 'Le code-barres doit être unique.'),
        ('reference_unique', 'unique(reference)', 'Le reference doit être unique.')
    ]
    
    name = fields.Char()
    company_id = fields.Many2one('res.company', string="Société", default=lambda self: self.env.company , required=True, readonly=True)
    date_live = fields.Datetime(string='Date du live', default=lambda self: fields.Datetime.now())
    season_id = fields.Many2one('live.season', string='Season du live', default=lambda self: self._get_last_live_id())
    live_number_id = fields.Many2one('live.number', string='N° live', default=lambda self: self._get_last_live_number_id())
    reference = fields.Char(string='Référence produit', copy=False, readonly=True)
    date_livraison = fields.Date(string='Date de livraison')
    date_paiement = fields.Date(string='Date de paiement')
    sequance = fields.Integer(string="Sequence")
    montant_jp = fields.Float('Montant JP', default=1.0)
    categ_id = fields.Many2one(string='Category', related='product_id.categ_id')
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    product_id = fields.Many2one('product.product', string='Article ', required=True)
    standard_price = fields.Float(related='product_id.standard_price', string="Prix d'achat",store="True", readonly=True)
    prix_normal = fields.Float('Prix normal (unitaire)', default=1.0)
    product_uom_qty = fields.Integer('Quantité', default=1)
    price_total = fields.Float('Prix Total', default=1.0, compute='_compute_amount_total')
    other_jp_id = fields.Text(string='2 eme JP')
    user_id = fields.Many2one('res.users', string="Commercial", related='partner_id.user_id')
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.user_id = self.partner_id.user_id
        else:
            self.user_id = False
    
    remarque = fields.Text(string='Remarque commande')
    image = fields.Binary(string="Image")
    sale_order_id = fields.Many2one('sale.order', string='Bon de Commande', readonly='True')
    purchase_order_id = fields.Many2one('purchase.order', string='Bon de Demande de Prix', readonly=True)
    facture_order_id = fields.Many2one('account.move', string='Facturation', domain=[('move_type', '=', 'out_invoice')], readonly=True)
    variant_value_ids = fields.Many2many(
        comodel_name="product.template.attribute.value",
        string="Valeur de la Variante",
        compute="_compute_variant_values",
        store=True
    )
    status = fields.Selection([
        ('AR', 'A Récupérer'),
        ('dispo', 'Disponible')
    ], string='Disponibilité')
    status_aar = fields.Selection([
        ('non_ok', 'NON OK'),
        ('ok', 'OK')
    ], string='AAR')
    surplus = fields.Selection([
        ('surplus_ar', 'Vente en Live'),
        ('surplus_dispo', 'Vente Surplus')
    ], string='Origine vente', default="surplus_ar")
    etat_jp = fields.Selection([
        ('done', 'Confirmé'),
	('en attente', 'En attente'),
        ('cancel', 'Désistement')
    ], string='Etat JP', default="en attente")
    etat_mp = fields.Selection([
        ('mp_sent', 'MP Envoyé'),
        ('mp_not_sent', 'MP Pas Envoyé')
    ], string='Etat MP', default="mp_not_sent")
    etat_paiement = fields.Selection([
        ('not_paid', 'Non Payé'),
        ('paye', 'Tout Payé'),
        ('accompte', 'Acompte')
    ], string='Etat paiement', defaut="not_paid")
    etat_colis = fields.Selection(string="Etat colis (Boutique)", selection=[
        ("recup","Récuperer"),
        ("livre","Livré"),
        ("return","Retourné"),
    ])
    etat_livraison = fields.Selection(string="Etat de livraison", selection=[
        ("livre","Fait"),
        ("report","Reporté")
    ])
    
    @api.onchange('etat_colis')
    def _onchange_livraison(self):
        for record in self:
            if record.etat_colis == "livre":
                if record.etat_colis == "livre":
                    record.etat_livraison = "livre"
                elif record.etat_colis == "return":
                    record.etat_livraison = "report"
                    
    @api.onchange('etat_jp')
    def _onchange_desistement(self):
        for record in self:
            if record.etat_jp == "cancel":
                record.etat_livraison = ""
                record.etat_colis = ""
                record.etat_paiement = ""
                
    @api.onchange('etat_paiement')
    def onchange_etat_paiement(self):
        for record in self:
            if record.etat_paiement != "":
                record.etat_jp = "en attente"
    
    
    contacts = fields.Char(string="Contacts", related='partner_id.phone')
    adresse_livraison = fields.Char(string='Adresse de Livraison', related='partner_id.street')
    accompte_recu = fields.Float(string='Acompte recu')
    ref_envoie = fields.Char(string='Reference renvoie')
    reste_paye = fields.Float(string='')
    total_recue = fields.Float(string='Total recu')
    frais_livraison = fields.Float(string='Frais de livraison')
    frais_diver = fields.Float(string="Frais divers")
    remarque_paiement = fields.Text(string='Remarque paiement')
    remarque_livraison = fields.Text(string='Remarque livraison')
    date_envoie = fields.Date(string="Date d'envoie")
    remarque_envoie = fields.Text(string='Remarque envoie')
    date_receipt = fields.Date(string='Date de reception')
    envoie_colis = fields.Selection([
        ('send', 'Article Envoyé'),
        ('not_send', 'Article Non Envoyé')
    ],string='Envoi Article', default='not_send')
    rec_colis = fields.Selection([
        ('arived', 'Article Arrivé'),
        ('not_arrived', 'Article Non Arrivé')
    ],string='Reception Article', default='not_arrived')
    colisage = fields.Selection([
        ('not_colis', 'Non Emballé'),
        ('not_done', 'Emballé Non Étiqueté'),
        ('done', 'Emballé Étiqueté Prêt à Livrer'),
    ],string='Colisage', default='not_colis')
    pay_livraison = fields.Selection([
        ('tana', 'TANA'),
        ('pro', 'PRO'),
        ('fr', 'FR')
    ], string='Lieu de livraison')
    entrepot = fields.Selection([
        ('casa', 'Ampandrana'),
        ('hk', 'Alasora')
    ],string='Entrepot/Stockage')
    delivery_person_id = fields.Many2one('delivery.person', string='Livreur')
    rapport_commande = fields.Selection([
        ('done', 'Clôturée'),
        ('not_done_livre', 'En Cours de Traitement'),
        ('not_done_recup', 'A Suivre de Près')
    ],string='Rapport de commande')
    remarque_generale = fields.Text(string='Remarque generale')
    margin = fields.Float(string='Margin', compute='_compute_margin', store=True)
    marge = fields.Float(string="Marge", compute='_compute_marge', store=True)
    reste_payer = fields.Float(string='Reste à Payer', compute='_compute_reste_a_payer', store=True)
    barcode = fields.Char('Code-barres EAN-13', readonly=True)  # Creation du code barre a partir de la reference et autre
    barcode_img = fields.Binary(string="Code barre", readonly=True)
    imprimer = fields.Char(default="0")
    
    # Les methodes et les actions automatiques
    
    @api.model
    def _get_next_name(self):
        last_record = self.search([], order='id desc', limit=1)
        last_number = 0

        if last_record and last_record.name and last_record.name.startswith('N-'):
            try:
                last_number = int(last_record.name.split('-')[1])
            except (ValueError, IndexError):
                last_number = 0

        return f'N-{last_number + 1}'
    
    @api.depends('product_uom_qty', 'prix_normal')
    def _compute_amount_total(self):
        for rec in self:
            rec.price_total = rec.product_uom_qty * rec.prix_normal
    
    @api.depends('reference')
    def _compute_display_name(self):
        for record in self:
            if record.reference:
                record.display_name = record.reference
        
    def _calculate_ean13_checksum(self,value12):
        assert len(value12) == 12 and value12.isdigit(), "Le code doit contenir 12 chiffres"
        total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(value12))
        return str((10 - total % 10) % 10)

        
    @api.model
    def create(self, vals):
        # === GÉNÉRATION DE LA RÉFÉRENCE LIVE ===
        if not vals.get('reference') and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            live_code = product.code_ref or f"PROD{product.id}"  # Champ personnalisé ou fallback
            prefix = f"{live_code.upper()}-"
            seq = self.env['ir.sequence'].next_by_code('live.shopping.reference') or '001'
            vals['reference'] = f"{prefix}{seq}"

        # === GÉNÉRATION DU CODE-BARRES UNIQUE ===
        if not vals.get('barcode'):
            for _ in range(100):
                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(11)])
                base_code = f"9{random_digits}"  # Commence par 9 + 11 chiffres
                checksum = self._calculate_ean13_checksum(base_code)
                full_code = base_code + checksum

                # Vérifier unicité
                existing = self.env['live.shopping.beta'].search([('barcode', '=', full_code)], limit=1)
                if not existing:
                    vals['barcode'] = full_code

                    # Générer l'image PNG
                    barcode = createBarcodeDrawing('EAN13', value=full_code, barHeight=40, barWidth=1.0)
                    png_data = renderPM.drawToString(barcode, fmt='PNG')
                    vals['barcode_img'] = base64.b64encode(png_data)
                    break
            else:
                raise UserError("Impossible de générer un code-barres unique après 100 essais.")

        return super().create(vals)
    
    @api.depends('montant_jp', 'standard_price')
    def _compute_marge(self):
        for record in self:
            if record.montant_jp and record.standard_price:
                record.marge = record.montant_jp - record.standard_price
            else:
                record.marge = 0.0

    @api.depends('montant_jp', 'total_recue')
    def _compute_reste_a_payer(self):
        for record in self:
            montant_jp = record.montant_jp or 0.0
            total_recue = record.total_recue or 0.0
            record.reste_payer = montant_jp - total_recue
            
    def calculate_ean13_checksum(self,value12):
        assert len(value12) == 12 and value12.isdigit(), "Le code doit contenir 12 chiffres"
        total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(value12))
        return str((10 - total % 10) % 10)

    def _compute_barcode(self):
        for record in self:
            if record.barcode and record.barcode_img:  # Si déjà généré, ne rien faire
                continue

            unique = False
            max_tries = 100  # Sécurité anti-boucle infinie

            while not unique and max_tries > 0:
                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(11)])
                base_code = f"9{random_digits}"  # 12 chiffres
                checksum = self.calculate_ean13_checksum(base_code)
                full_code = base_code + checksum  # 13 chiffres

                # Vérifier unicité dans les produits
                exists = self.env['product.template'].search([('barcode', '=', full_code)], limit=1)
                if not exists:
                    unique = True
                    record.barcode = full_code

                    # Générer l'image PNG du code-barres
                    barcode = createBarcodeDrawing('EAN13', value=full_code, barHeight=40, barWidth=1.0)
                    png_data = renderPM.drawToString(barcode, fmt='PNG')
                    record.barcode_img = base64.b64encode(png_data)
                else:
                    max_tries -= 1

            if not unique:
                raise UserError("Impossible de générer un code-barres unique après plusieurs tentatives.")

            
    @api.model
    def _get_last_live_id(self):
        last_live = self.env['live.season'].search([], order='id desc', limit=1)
        return last_live.id if last_live else False
    @api.model
    def _get_last_live_number_id(self):
        last_live_number = self.env['live.number'].search([], order='id desc', limit=1)
        return last_live_number.id if last_live_number else False


    @api.depends('product_id', 'product_id.list_price', 'product_id.standard_price')
    def _compute_margin(self):
        for line in self:
            if line.product_id:
                line.margin = line.product_id.list_price - line.product_id.standard_price
            else:
                line.margin = 0.0

    @api.onchange('product_id')
    def onchange_saller_id(self):
        if self.product_id:
            self.montant_jp = self.montant_jp
        else:
            self.montant_jp = False

    @api.model
    def action_create_devis(self):
        # Vérifier si 'active_ids' existe dans le contexte et n'est pas vide
        active_ids = self.env.context.get('active_ids', [])
        
        if not active_ids:
            raise UserError("Aucune ligne sélectionnée.")

        # Filtrer les lignes de shopping en fonction des 'active_ids'
        selected_lines = self.browse(active_ids)

        for line in selected_lines:
            # Créer le devis pour chaque client
            sale_order = self.env['sale.order'].create({
                'partner_id': line.partner_id.id,
                'date_order': fields.Datetime.now(),
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_total': line.montant_jp,  # Utiliser montant_jp pour le prix unitaire
                    'name': line.product_id.name,
                    'tax_id': [(6, 0, line.product_id.taxes_id.ids)],
                })],
            })

        return True
    def write(self, vals):
        _logger.info("Updating LiveShoppingBeta %s with values: %s", self.ids, vals)
        return super(LiveShoppingBeta, self).write(vals)
        
    @api.depends("product_id")
    def _compute_variant_values(self):
        for record in self:
            if record.product_id:
                record.variant_value_ids = record.product_id.product_template_variant_value_ids
            else:
                record.variant_value_ids = False
                
    def action_create_invoice_direct(self):
        AccountMove = self.env['account.move']

        if not self:
            raise UserError("Aucune ligne sélectionnée.")

        partners = self.mapped('partner_id')
        if len(partners) != 1:
            raise UserError("Toutes les lignes doivent appartenir au même client pour générer une seule facture.")

        partner = partners[0]
        invoice_lines = []

        for line in self:
            if not line.product_id:
                raise UserError(f"Produit manquant pour la ligne {line.reference}.")

            product = line.product_id

            # Compte de revenu
            income_account = product.categ_id.property_account_income_categ_id
            if not income_account:
                raise UserError(f"Aucun compte de revenu défini pour la catégorie du produit {product.name}.")
            
            ref = f"[{line.reference}] " if line.reference else ""

            invoice_lines.append((0, 0, {
                'product_id': product.id,
                'name': f"{ref} {product.name}",
                'quantity': line.product_uom_qty,
                'price_unit': line.prix_normal,
                'tax_ids': [(6, 0, product.taxes_id.ids)],
                'account_id': income_account.id,
            }))

        invoice = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_origin': ', '.join(self.mapped('product_id.name')),
            'live_reference': ', '.join(self.mapped('reference')),
            'user_id': partner.user_id.id,
            'invoice_line_ids': invoice_lines
        })

        self.write({'facture_order_id': invoice.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Créée',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }
 
    def action_create_purchase_order(self):
        """ Regroupe les lignes par fournisseur et génère une demande de prix (RFQ) """
        purchase_orders = {}

        orders_by_supplier = defaultdict(list)
        for line in self:
            if line.product_id.seller_ids:
                supplier = line.product_id.seller_ids[0].partner_id
                if supplier:
                    orders_by_supplier[supplier].append(line)

        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']

        for supplier, lines in orders_by_supplier.items():
            order_vals = {
                'partner_id': supplier.id, 
                'state': 'draft' 
            }
            order = PurchaseOrder.create(order_vals)

            for line in lines:
                supplier_info = line.product_id.seller_ids.filtered(lambda s: s.partner_id == supplier)
                price_total = supplier_info[0].price if supplier_info else line.product_id.standard_price 

                order_line_vals = {
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'price_total': price_total,  # Utilisation du prix fournisseur
                    'date_planned': fields.Date.today(),
                }
                PurchaseOrderLine.create(order_line_vals)

                line.purchase_order_id = order.id

            purchase_orders[supplier.id] = order

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [o.id for o in purchase_orders.values()])],
            'target': 'current',
        }

    def action_create_sale_order(self):
        sale_orders = {}

        orders_by_client = defaultdict(list)
        for line in self:
            orders_by_client[line.partner_id].append(line)

        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        for client, lines in orders_by_client.items():
            order_vals = {
                'partner_id': client.id,
                'order_line': []
            }
            order = SaleOrder.create(order_vals)

            for line in lines:
                order_line_vals = {
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_total': line.montant_jp,
                }
                SaleOrderLine.create(order_line_vals)
                
                line.sale_order_id = order.id
            sale_orders[client.id] = order

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [o.id for o in sale_orders.values()])],
            'target': 'current',
        }
    
    @api.model
    def _get_last_live_id(self):
        last_live = self.env['live.season'].search([], order='id desc', limit=1)
        return last_live.id if last_live else False
    
    @api.model
    def _get_last_live_number_id(self):
        last_live_number = self.env['live.number'].search([], order='id desc', limit=1)
        return last_live_number.id if last_live_number else False
    
    def action_print_barcode_labels(self):
        return self.env.ref('live_shopping_hr.barcode_label_report_action').report_action(self)
    
    def action_export_excel(self):
        # Création du fichier Excel en mémoire
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Clients')

        headers = ['VARIANT', 'ARTICLE', 'REFERENCE', 'PRIX', 'ID', 'CODE BARRE', 'IMPRIMER']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        row = 1
        for rec in self:
            # ✅ Récupération des variantes (ex: "Couleur: Rouge, Taille: XL")
            variant_values = ', '.join([
                f"{v.name}"
                for v in rec.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id')
            ])

            worksheet.write(row, 0, variant_values or '')
            worksheet.write(row, 1, rec.product_id.name or '')
            worksheet.write(row, 2, rec.reference or '')
            worksheet.write(row, 3, rec.prix_normal or '')
            worksheet.write(row, 4, rec.id or '')
            worksheet.write(row, 5, rec.barcode or '')
            worksheet.write(row, 6, rec.imprimer or '')
            row += 1

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read())

        file_name = f"live_export_{datetime.today().strftime('%Y-%m-%d')}.xlsx"

        export_temp = self.env['export.excel.temp'].create({
            'file_name': file_name,
            'file_data': file_data,
        })

        return {
            'name': 'Exportation des données',
            'type': 'ir.actions.act_window',
            'res_model': 'export.excel.temp',
            'view_mode': 'form',
            'res_id': export_temp.id,
            'target': 'new',
        }