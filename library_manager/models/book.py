from odoo import models, fields, api


class Book(models.Model):
    _name = "library.manager.book"

    book_type = fields.Many2one("library.manager.book.type", string="book type:")
    book_borrow=fields.Many2one("library.manager.student",string="Student borrow")

    @api.model
    def create(self, vals):
        return_value = super(Book, self).create(vals)
        res = self.env['library.manager.book.type'].search([('id', '=', vals["book_type"])])
        res.book_count += 1
        res.book_available += 1
        return return_value

    @api.multi
    def write(self, vals):
        old_value = {}
        new_value = {}
        old_book_list = self.env['library.manager.book']
        if vals.has_key('book_type'):
            # get old value before edit
            for record in self:
                book_id = record.id
                book = old_book_list.search([('id', '=', book_id)])
                old_value[book_id] = book.book_type.id
            # edit record
            return_value = super(Book, self).write(vals)
            # get new value after edit
            new_book_list = self.env['library.manager.book']
            for record in self:
                book_id = record.id
                book = new_book_list.search([('id', '=', book_id)])
                new_value[book_id] = book.book_type.id
            # update book type count:
            book_type_list = self.env['library.manager.book.type']
            for record in self:
                book_id = record.id
                # update book type:
                old_book_type = book_type_list.search([('id', '=', old_value[book_id])])
                old_book_type.book_count -= 1
                old_book_type.book_available -= 1
                new_book_type = book_type_list.search([('id', '=', new_value[book_id])])
                new_book_type.book_count += 1
                old_book_type.book_available += 1
            return return_value
        else:
            return super(Book, self).write(vals)

    @api.multi
    def unlink(self):
        book_type_list = self.env['library.manager.book.type'].search([])
        for book in self:
            book_type_id = book.book_type.id
            book_type = book_type_list.search([('id', '=', book_type_id)])
            book_type.book_count -= 1
            book_type.book_available -= 1
        return_value = super(Book, self).unlink()
        return return_value
