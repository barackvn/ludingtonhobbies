# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date, timedelta
import calendar


class ProductReplenishValues(models.Model):
    _name = 'product.replenish.values'

    x_studio_special_order = fields.Boolean(string='Special Order')
    x_studio_so_name = fields.Char(string='SO Name')
    x_studio_so_phone = fields.Char(string='SO Phone')


class ProductReplenishInherit(models.TransientModel):
    _inherit = 'product.replenish'

    x_studio_special_order = fields.Boolean(string='Special Order')
    x_studio_so_name = fields.Char(string='SO Name')
    x_studio_so_phone = fields.Char(string='SO Phone')

    def launch_replenishment(self):
        values = {
                    'x_studio_special_order': self.x_studio_special_order,
                    'x_studio_so_name': self.x_studio_so_name,
                    'x_studio_so_phone': self.x_studio_so_phone,
                 }
        self.env['product.replenish.values'].create(values)
        return super(ProductReplenishInherit, self).launch_replenishment()


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def create(self, values):
        product_replenish = self.env['product.replenish.values'].search([])
        if product_replenish:
            if product_replenish.x_studio_special_order:
                values['X_studio_special_order'] = product_replenish.x_studio_special_order
            if product_replenish.x_studio_so_name:
                values['X_studio_so_name'] = product_replenish.x_studio_so_name
            if product_replenish.x_studio_so_phone:
                values['X_studio_so_phone'] = product_replenish.x_studio_so_phone
            product_replenish.unlink()

        return super(PurchaseOrderLineInherit, self).create(values)

    def write(self, values):
        product_replenish = self.env['product.replenish.values'].search([])
        if product_replenish:
            if product_replenish.x_studio_special_order:
                values['X_studio_special_order'] = product_replenish.x_studio_special_order
            if product_replenish.x_studio_so_name:
                values['X_studio_so_name'] = product_replenish.x_studio_so_name
            if product_replenish.x_studio_so_phone:
                values['X_studio_so_phone'] = product_replenish.x_studio_so_phone
            product_replenish.unlink()

        return super(PurchaseOrderLineInherit, self).write(values)

