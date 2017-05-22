# -*- coding: utf-8 -*-
from odoo import api
from  odoo import models
from  odoo import fields



class Num2Word_VN(models.Model):

    _name = 'convert.to.vn'
    @api.model
    def _convert_nn(self, val):
        if val < 20:
            return self._to_19[val]
        for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(self._tens)):
            if dval + 10 > val:
                if val % 10:
                    a = 'lăm'
                    if self._to_19[val % 10] == 'một':
                        a = 'mốt'
                    else:
                        a = self._to_19[val % 10]
                    if self._to_19[val % 10] == 'năm':
                        a = 'lăm'
                    return dcap + ' ' + a
                return dcap

    @api.model
    def _convert_nnn(self, val):
        word = ''
        (mod, rem) = (val % 100, val // 100)
        if rem > 0:
            word = self._to_19[rem] + ' trăm'
            if mod > 0:
                word = word + ' '
        if mod > 0 and mod < 10:
            if mod == 5:
                word = word != '' and word + 'lẻ năm' or word + 'năm'
            else:
                word = word != '' and word + 'lẻ ' \
                                      + self._convert_nn(mod) or word + self._convert_nn(mod)
        if mod >= 10:
            word = word + self._convert_nn(mod)
        return word

    @api.model
    def vietnam_number(self, val):
        if val < 100:
            return self._convert_nn(val)
        if val < 1000:
            return self._convert_nnn(val)
        for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(self._denom))):
            if dval > val:
                mod = 1000 ** didx
                l = val // mod
                r = val - (l * mod)

                ret = self._convert_nnn(l) + ' ' + self._denom[didx]
                if r > 0 and r <= 99:
                    ret = self._convert_nnn(l) + ' ' + self._denom[didx] + ' lẻ'
                if r > 0:
                    ret = ret + ' ' + self.vietnam_number(r)
                return ret

    @api.model
    def number_to_text(self, number):
        number = '%.2f' % number
        the_list = str(number).split('.')
        start_word = self.vietnam_number(int(the_list[0]))
        final_result = start_word
        if len(the_list) > 1 and int(the_list[1]) > 0:
            # end_word = self.vietnam_number(int(the_list[1]))
            # final_result = final_result + ' phẩy ' + end_word
            end_word=the_list[1]
            extra=''
            if len(end_word)>0:
                for digit in end_word:
                    extra+=self._to_19[int(digit)]+' '
            final_result=final_result+' phẩy ' + extra
        return final_result.upper()

    @api.model
    def to_cardinal(self, number):
        return self.number_to_text(number)

    @api.model
    def to_ordinal(self, number):
        return self.to_cardinal(number)

    _to_19 = ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu',
             'bảy', 'tám', 'chín', 'mười', 'mười một', 'mười hai',
             'mười ba', 'mười bốn', 'mười lăm', 'mười sáu', 'mười bảy',
             'mười tám', 'mười chín')
    _tens = ('hai mươi', 'ba mươi', 'bốn mươi', 'năm mươi',
            'sáu mươi', 'bảy mươi', 'tám mươi', 'chín mươi')
    _denom = ('',
             'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'trăm nghìn tỷ',
             'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion',
             'Decillion', 'Undecillion', 'Duodecillion', 'Tredecillion',
             'Quattuordecillion', 'Sexdecillion', 'Septendecillion',
             'Octodecillion', 'Novemdecillion', 'Vigintillion')