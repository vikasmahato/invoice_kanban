# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceKanban(http.Controller):
#     @http.route('/invoice_kanban/invoice_kanban', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_kanban/invoice_kanban/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_kanban.listing', {
#             'root': '/invoice_kanban/invoice_kanban',
#             'objects': http.request.env['invoice_kanban.invoice_kanban'].search([]),
#         })

#     @http.route('/invoice_kanban/invoice_kanban/objects/<model("invoice_kanban.invoice_kanban"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_kanban.object', {
#             'object': obj
#         })

