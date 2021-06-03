# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import pytz
from odoo.exceptions import ValidationError


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    def open_special_order_mail(self):
        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        time_now = pytz.utc.localize(datetime.now()).astimezone(user_timezone)

        if time_now.hour:
            purchase_order_lines = self.env['purchase.order.line'].search([('x_studio_special_order', '=', True), ('x_studio_closed', '=', False)]).sorted(key=lambda obj: obj.x_studio_so_name)

            special_orders_list = []

            for order in purchase_order_lines:
                order_info = \
                    {
                        'part': order.order_id.name,
                        'purchase_order': order.order_id.origin,
                        'vendor': order.order_id.partner_id.name,
                        'order_date': order.order_id.date_order,

                        'x_studio_special_order': order.x_studio_special_order,
                        'x_studio_so_name': order.x_studio_so_name,
                        'x_studio_so_phone': order.x_studio_so_phone,
                    }
                special_orders_list.append(order_info)

            special_orders_dictionary = {'special_orders_list': special_orders_list}

            template_id = self.env.ref('open_special_orders.mail_open_special_orders_template').id
            self.env['mail.template'].browse(template_id).with_context(special_orders_dictionary).send_mail(self.id, force_send=True)
