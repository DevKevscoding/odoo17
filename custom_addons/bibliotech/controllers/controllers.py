# -*- coding: utf-8 -*-
# from odoo import http


# class Bibliotech(http.Controller):
#     @http.route('/bibliotech/bibliotech', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bibliotech/bibliotech/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bibliotech.listing', {
#             'root': '/bibliotech/bibliotech',
#             'objects': http.request.env['bibliotech.bibliotech'].search([]),
#         })

#     @http.route('/bibliotech/bibliotech/objects/<model("bibliotech.bibliotech"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bibliotech.object', {
#             'object': obj
#         })

