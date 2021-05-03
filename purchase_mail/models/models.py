# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def action_rfq_send(self):
        res = super(PurchaseOrderInherit, self).action_rfq_send()

        report = self.env.ref('purchase_mail.report_purchase_order_mail').render_qweb_pdf(self.id)
        attachment_values = \
            {
                'name': 'Order Report' + '.pdf',
                'type': 'binary',
                'datas': base64.b64encode(report[0]),
                'store_fname': 'Order Report' + '.pdf',
                'res_model': 'purchase.order',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            }
        attachment = self.env['ir.attachment'].create(attachment_values)

        mail = self.env.ref('purchase.email_template_edi_purchase')
        mail.attachment_ids = attachment

        mail = self.env.ref('purchase.email_template_edi_purchase_done')
        mail.attachment_ids = attachment

        report = self.env.ref('purchase_mail.report_purchase_order_mail_xlsx').render(self)
        attachment_values = \
            {
                'name': 'Order Report' + '.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(report[0]),
                'store_fname': 'Order Report' + '.xlsx',
                'res_model': 'purchase.order',
                'res_id': self.id,
                'mimetype': 'application/csv',
            }
        attachment = self.env['ir.attachment'].create(attachment_values)

        mail = self.env.ref('purchase.email_template_edi_purchase')
        mail.attachment_ids += attachment

        mail = self.env.ref('purchase.email_template_edi_purchase_done')
        mail.attachment_ids += attachment

        return res
