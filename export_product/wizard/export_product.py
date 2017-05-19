# -*- coding: utf-8 -*-
from odoo import api, fields, models
import base64
import contextlib
import cStringIO
import csv
import xlwt


class ExportProduct(models.TransientModel):
    _name = "export.product.wizard"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    file_type = fields.Selection([('xls', 'xls'), ('csv', 'csv')], default='xls', required=True)
    stock_location_id = fields.Many2one('stock.location', string="Stock Location", required=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    @api.multi
    def do_export(self):
        if self.stock_location_id:
            products = self.env['product.product'].search([]).with_context({'location': self.stock_location_id.id})
            if self.file_type == 'csv':
                with contextlib.closing(cStringIO.StringIO()) as buf:
                    writer = csv.writer(buf, delimiter=";", quotechar='"')
                    writer.writerow(("product_sku", "product_name", "product_qty"))

                    for item in products:
                        writer.writerow((
                            item.default_code.encode('utf8') if item.default_code else '',
                            item.name_get()[0][1].encode('utf8') if len(item.name_get()) > 0 else '',
                            item.qty_available
                        ))

                    out = base64.encodestring(buf.getvalue())
            else:
                wb = xlwt.Workbook(encoding='utf8')
                sheet = wb.add_sheet('sheet')
                sheet.write(0, 0, "product_sku")
                sheet.write(0, 1, "product_name")
                sheet.write(0, 2, "product_qty")

                for index, item in enumerate(products):
                    sheet.write(index + 1, 0, item.default_code.encode('utf8') if item.default_code else '')
                    sheet.write(index + 1, 1, item.name_get()[0][1].encode('utf8') if len(item.name_get()) > 0 else '')
                    sheet.write(index + 1, 2,  item.qty_available)

                data = cStringIO.StringIO()
                wb.save(data)
                data.seek(0)
                out = base64.encodestring(data.read())
                data.close()

            self.write({
                'state': 'get',
                'data': out,
                'name': 'Stock_location_test.xls'
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.product.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
