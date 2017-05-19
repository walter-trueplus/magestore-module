from odoo import fields,models,api

class Student(models.Model):
    _name = 'library.manager.student'
    name=fields.Char(string='Student name')
    student_id=fields.Char(string='Student id')
    student_borrow=fields.One2many('library.manager.book','book_borrow')

