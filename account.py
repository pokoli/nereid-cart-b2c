# -*- coding: UTF-8 -*-
'''
    nereid_cart.account

    User Account

    :copyright: (c) 2010-2011 by Openlabs Technologies & Consulting (P) LTD
    :license: GPLv3, see LICENSE for more details
'''
from werkzeug.exceptions import NotFound
from nereid import render_template, login_required, request
from nereid.backend import ModelPagination

from trytond.model import ModelSQL

class Account(ModelSQL, ModelPagination):
    """When the account page is displayed it may be required to display a lot of
        information. and this depends from site to site. So rather than 
        rewriting the render page everytime it is optimal to have a context 
        being rebuilt by subclassing.

        This basic context builder builds sales, invoices and shipments, 
        (only last 5) of the customer.

        To add more items to the context, subclass the method and call super 
        to get the result of this method and then add your content to it.
    """
    _name = 'nereid.website'
    
    def __init__(self):
        super(Account, self).__init__()
        self.per_page = 9

    def account_context(self):
        "First get existing context and then add"
        sale_obj = self.pool.get('sale.sale')
        invoice_obj = self.pool.get('account.invoice')
        shipment_obj = self.pool.get('stock.shipment.out')

        sales_ids = sale_obj.search(
            [
            ('party', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft')
            ],
            limit=5)
        sales = sale_obj.browse(sales_ids)

        invoice_ids = invoice_obj.search(
            [
            ('party', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft'),
            ],
            limit=5)
        invoices = invoice_obj.browse(invoice_ids)

        shipment_ids = shipment_obj.search(
            [
            ('customer', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft'),
            ],
            limit=5)
        shipments = shipment_obj.browse(shipment_ids)

        context = super(Website, self).account_context()
        context.update({
            'sales': sales,
            'invoices': invoices,
            'shipments': shipments,
            })
        return context

    @login_required
    def sales(self, page=1):
        'All sales'
        sale_obj = self.pool.get('sale.sale')
        sales_ids = sale_obj.paginate(
            [
            ('party', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft')
            ], page, self.per_page)
        sales = sale_obj.browse(sales_ids)
        return render_template('sales.jinja', sales=sales)

    @login_required
    def sale(self, sale):
        'Individual Sale Order'
        sale_obj = self.pool.get('sale.sale')
        sales_ids = sale_obj.search(
            [
            ('party', '=', request.nereid_user.party.id),
            ('id', '=', sale), ('state', '!=', 'draft')
            ])
        if not sales_ids:
            return NotFound()
        sale = sale_obj.browse(sales_ids[0])
        return render_template('sale.jinja', sale=sale)

    @login_required
    def invoices(self, page=1):
        'List of Invoices'
        invoice_obj = self.pool.get('account.invoice')
        invoice_ids = invoice_obj.paginate(
            [
            ('party', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft')
            ], page, self.per_page)
        invoices = invoice_obj.browse(invoice_ids)
        return render_template('invoices.jinja', invoices=invoices)

    @login_required
    def invoice(self, invoice):
        'individual Invoice'
        invoice_obj = self.pool.get('account.invoice')
        invoice_ids = invoice_obj.search(
            [
            ('party', '=', request.nereid_user.party.id),
            ('id', '=', invoice),
            ('state', '!=', 'draft')
            ])
        if not invoice_ids:
            return NotFound()
        invoice = invoice_obj.browse(invoice_ids[0])
        return render_template('invoice.jinja', invoice=invoice)

    @login_required
    def shipments(self, page=1):
        'List of Shipments'
        shipment_obj = self.pool.get('stock.shipment.out')
        shipment_ids = shipment_obj.paginate(
            [
            ('customer', '=', request.nereid_user.party.id),
            ('state', '!=', 'draft'),
            ], page, self.per_page)
        shipments = shipment_obj.browse(shipment_ids)
        return render_template('shipments.jinja', shipments=shipments)

    @login_required
    def shipment(self, shipment):
        'Shipment'
        shipment_obj = self.pool.get('stock.shipment.out')
        shipment_ids = shipment_obj.search(
            [
            ('customer', '=', request.nereid_user.party.id),
            ('id', '=', shipment),
            ('state', '!=', 'draft'),
            ])
        if not shipment_ids:
            return NotFound()
        shipment = shipment_obj.browse(shipment_ids[0])
        return render_template('shipment.jinja', shipment=shipment)

Account()