# -*- coding: utf-8 -*-
# from odoo import http


# class LiveShoppingHr(http.Controller):
#     @http.route('/live_shopping_hr/live_shopping_hr', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/live_shopping_hr/live_shopping_hr/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('live_shopping_hr.listing', {
#             'root': '/live_shopping_hr/live_shopping_hr',
#             'objects': http.request.env['live_shopping_hr.live_shopping_hr'].search([]),
#         })

#     @http.route('/live_shopping_hr/live_shopping_hr/objects/<model("live_shopping_hr.live_shopping_hr"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('live_shopping_hr.object', {
#             'object': obj
#         })

