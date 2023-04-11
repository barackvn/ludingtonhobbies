# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderReportExcel(models.AbstractModel):
    _name = 'report.purchase_mail.purchase_order_mail_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, accounts):
        for obj in accounts:
            if obj.id and obj.id.id:
                purchase_order = self.env['purchase.order'].search([('id', '=', obj.id.id)])

                left_text = workbook.add_format({'align': 'left'})
                border_bold = workbook.add_format({'bold': True, 'bg_color': '#D0D0D0'})
                sheet = workbook.add_worksheet("Order Report Excel")

                sheet.set_column(0, 0, 30)
                sheet.set_column(0, 1, 30)
                sheet.set_column(0, 2, 30)

                sheet.write(0, 0, 'Part Number', border_bold)
                sheet.write(0, 1, 'Cost', border_bold)
                sheet.write(0, 2, 'Quantity', border_bold)

                for row, line in enumerate(purchase_order.order_line, start=1):
                    if line.product_id.default_code:
                        sheet.write(row, 0, line.product_id.default_code, left_text)
                    else:
                        sheet.write(row, 0, 'None', left_text)
                    sheet.write(row, 1, line.product_id.standard_price, left_text)
                    sheet.write(row, 2, line.product_qty, left_text)
