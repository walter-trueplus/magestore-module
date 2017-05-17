from odoo import api
from odoo import fields
from odoo import models


class BookType(models.Model):
    _name = "library.manager.book.type"

    name = fields.Char(string='Book title', required=True)
    book_count = fields.Integer(string='Book count')
    book_available=fields.Integer(string="Available:", default=lambda self:self.book_count)
    book_author = fields.Char(string='Author')
    book_publisher = fields.Char(string='Pulisher')
    book = fields.One2many("library.manager.book", "book_type")