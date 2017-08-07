# -*- coding: utf-8 -*-
import numbers

import re

from odoo.osv.query import Query

from odoo.osv import expression

from odoo import api

from odoo import models
from .. import ace


class CustomSearch(models.Model):
    _name = 'search.custom'
    _field_no_accent = []

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # convert input to no accent
        for x in domain:
            if type(x) is list:
                if x[0].encode('utf8') in self._field_no_accent:
                    if not isinstance(x[2], numbers.Number):
                        x[2] = ace.normalize(x[2])
                        print x
        records = self.search(domain or [], offset=offset, limit=limit, order=order)
        if not records:
            return []

        if fields and fields == ['id']:
            # shortcut read if we only want the ids
            return [{'id': record.id} for record in records]

        # read() ignores active_test, but it would forward it to any downstream search call
        # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
        # was presumably only meant for the main search().
        # TODO: Move this to read() directly?
        if 'active_test' in self._context:
            context = dict(self._context)
            del context['active_test']
            records = records.with_context(context)

        result = records.read(fields)
        if len(result) <= 1:
            return result

        # reorder read
        index = {vals['id']: vals for vals in result}
        return [index[record.id] for record in records if record.id in index]

        # TODO: ameliorer avec NULL

    @api.model
    def _where_calc(self, domain, active_test=True):
        """Computes the WHERE clause needed to implement an OpenERP domain.
        :param domain: the domain to compute
        :type domain: list
        :param active_test: whether the default filtering of records with ``active``
                            field set to ``False`` should be applied.
        :return: the query expressing the given domain as provided in domain
        :rtype: osv.query.Query
        """
        # if the object has a field named 'active', filter out all inactive
        # records unless they were explicitely asked for
        if 'active' in self._fields and active_test and self._context.get('active_test', True):
            # the item[0] trick below works for domain items and '&'/'|'/'!'
            # operators too
            if not any(item[0] == 'active' for item in domain):
                domain = [('active', '=', 1)] + domain

        if domain:
            e = expression.expression(domain, self)
            tables = e.get_tables()
            where_clause, where_params = e.to_sql()

            w = where_clause.encode('utf-8')
            columns = re.findall(r'"\w+"."\w+"::text', w)
            distinct_columns = list(set(columns))

            for column in distinct_columns:
                print column
                temp = column.split('.')[1]
                field = temp[1:len(temp) - 7]
                print type(field)
                print field
                print self._field_no_accent
                print field in self._field_no_accent
                if field in self._field_no_accent:
                    kq = re.sub(r'' + re.escape(column), 'vn_unaccent(' + column + ')', where_clause)
                    where_clause = kq
            print where_clause
            where_clause = [where_clause] if where_clause else []

        else:
            where_clause, where_params, tables = [], [], ['"%s"' % self._table]

        return Query(tables, where_clause, where_params)
