# -*- coding: utf-8 -*-
# Created by Adam from Magestore

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class Reward(models.Model):
    _name = "er.reward"
    _description = "This model will process the function of reward"

    name = fields.Char(String="Name", required=True)
    point = fields.Integer(String="Point required for perchased", required=True)
    description = fields.Text(String="Description")
    number_available = fields.Integer(String="Number Available")
    email_template = fields.Text(String="Email Template")
    remark = fields.Text(String="Remarks")
    contact_admin = fields.Many2one("res.partner", String="Contact Admin", required=True)
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
        return super(Reward, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(Reward, self).write(vals)
