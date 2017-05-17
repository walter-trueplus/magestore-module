 # -*- coding: utf-8 -*-
# Copyright 2016 Henry Zhou (http://www.maxodoo.com)
# Copyright 2016 Rodney (http://clearcorp.cr/)
# Copyright 2012 Agile Business Group
# Copyright 2012 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import odoo.http as http
from odoo.http import request
from odoo.addons.web.controllers.main import ExcelExport


class ExcelExportView(ExcelExport):
    def __getattribute__(self, name):
        if name == 'fmt':
            raise AttributeError()
        return super(ExcelExportView, self).__getattribute__(name)

    @http.route('/web/export/xls_view', type='http', auth='user')
    def export_xls_view(self, data, token):
        data = json.loads(data)
        model = data.get('model', [])
        columns_headers = data.get('headers', [])
        rows = data.get('rows', [])

        return request.make_response(
            self.from_data_exp(columns_headers, rows),
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % self.filename(model)),
                ('Content-Type', self.content_type)
            ],
            cookies={'fileToken': token}
        )
# class VCARDExport(ExportFormat, http.Controller):
#
#     @http.route('/web/export/csv', type='http', auth="user")
#     @serialize_exception
#     def index(self, data, token):
#         return self.base(data, token)
#
#     @property
#     def content_type(self):
#         return 'text/csv;charset=utf8'
#
#     def filename(self, base):
#         return base + '.csv'
#
#     def from_data_exp(self, fields, rows):
#         fp = StringIO()
#         writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
#
#         writer.writerow([name.encode('utf-8') for name in fields])
#
#         for data in rows:
#             row = []
#             for d in data:
#                 if isinstance(d, unicode):
#                     try:
#                         d = d.encode('utf-8')
#                     except UnicodeError:
#                         pass
#                 if d is False: d = None
#
#                 # Spreadsheet apps tend to detect formulas on leading =, + and -
#                 if type(d) is str and d.startswith(('=', '-', '+')):
#                     d = "'" + d
#
#                 row.append(d)
#             writer.writerow(row)
#
#         fp.seek(0)
#         data = fp.read()
#         fp.close()
#         return data