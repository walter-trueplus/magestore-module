# -*- coding: utf-8 -*-

import json
import odoo.http as http
from odoo.http import request
from odoo.addons.web.controllers.main import CSVExport


class ExcelExportView(CSVExport):
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
            self.from_data(columns_headers, rows),
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % self.filename(model)),
                ('Content-Type', self.content_type)
            ],
            cookies={'fileToken': token}
        )

# class CSVExport(ExportFormat, http.Controller):
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
#         return base + '.vcf'
#
#     def from_data(self, fields, rows):
#         fp = StringIO()
#         writer = csv.writer(fp, delimiter=":", quotechar='"')
#         for data in rows:
#             lst_data2 = []
#             lst_data2.append(data)
#             for lst_data in lst_data2:
#                 writer.writerow(("BEGIN", "VCARD"))
#                 writer.writerow(("VERSION", "3.0"))
#                 writer.writerow(("N",lst_data[0] if lst_data else ''))
#                 writer.writerow(("FN",lst_data[0] if lst_data else ''))
#                 writer.writerow(("TEL;TYPE=CELL",lst_data[1] if lst_data else ''))
#                 writer.writerow(("TEL;TYPE=WORK", lst_data[2] if lst_data else ''))
#                 writer.writerow(("EMAIL;TYPE=WORK",lst_data[3] if lst_data else ''))
#                 writer.writerow(
#                     ("ORG;CHARSET=UTF-8", lst_data[5] if lst_data else ''))
#                 writer.writerow(("TITLE",lst_data[6] if lst_data else ''))
#                 writer.writerow(("END", "VCARD"))
# writer.writerow([name.encode('utf-8') for name in fields])
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
#                 Spreadsheet apps tend to detect formulas on leading =, + and -
                # if type(d) is str and d.startswith(('=', '-', '+')):
                #     d = "'" + d
                #
                # row.append(d)
            # writer.writerow(row)
        #
        # fp.seek(0)
        # data = fp.read()
        # fp.close()
        # return data
class CSVExport(ExportFormat, http.Controller):

    @http.route('/web/export/csv', type='http', auth="user")
    @serialize_exception
    def index(self, data, token):
        return self.base(data, token)

    @property
    def content_type(self):
        return 'text/csv;charset=utf8'

    def filename(self, base):
        return base + '.vcf'

    def from_data(self, fields, rows):
        fp = StringIO()
        writer = csv.writer(fp, delimiter=":", quotechar='"')
        for data in rows:
            lst_data2 = []
            lst_data2.append(data)
            for lst_data in lst_data2:
                writer.writerow(("BEGIN", "VCARD"))
                writer.writerow(("VERSION", "3.0"))
                writer.writerow(("N",lst_data[0] if lst_data else ''))
                writer.writerow(("FN",lst_data[0] if lst_data else ''))
                writer.writerow(("TEL;TYPE=CELL",lst_data[1] if lst_data else ''))
                writer.writerow(("TEL;TYPE=WORK", lst_data[2] if lst_data else ''))
                writer.writerow(("EMAIL;TYPE=WORK",lst_data[3] if lst_data else ''))
                writer.writerow(
                    ("ORG;CHARSET=UTF-8", lst_data[5] if lst_data else ''))
                writer.writerow(("TITLE",lst_data[6] if lst_data else ''))
                writer.writerow(("END", "VCARD"))
writer.writerow([name.encode('utf-8') for name in fields])

        for data in rows:
            row = []
            for d in data:
                if isinstance(d, unicode):
                    try:
                        d = d.encode('utf-8')
                    except UnicodeError:
                        pass
                if d is False: d = None

                Spreadsheet apps tend to detect formulas on leading =, + and -
                if type(d) is str and d.startswith(('=', '-', '+')):
                    d = "'" + d

                row.append(d)
            writer.writerow(row)

        fp.seek(0)
        data = fp.read()
        fp.close()
        return data