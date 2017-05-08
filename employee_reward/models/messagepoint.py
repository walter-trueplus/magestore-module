# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class Messagepoint(models.Model):
    _name = "er.messagepoint"
    _description = "setup point to each message type"

    name = fields.Char(string="Message Type", required=True, translate=True)
    point = fields.Integer(string="Points", default = 0)
    active = fields.Boolean('Active', default=True)

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Photo", attachment=True,
        help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
        help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")


    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(Messagepoint, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(Messagepoint, self).write(vals)
