# -*- coding: utf-8 -*-
# Created by Adam from Magestore

import logging

from odoo import api, fields, models
from odoo import tools, http, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.http import request
import time
from datetime import datetime


_logger = logging.getLogger(__name__)

class MessageManagement(models.Model):
    _name = "er.message"
    # _inherit = ['mail.thread', 'mail.alias.mixin']
    _inherit = 'mail.thread'
    # _mail_post_access = 'read'
    _description = "Manage message"

    # name will be calculated base on message_type title and the partner name (Ex: Thank you to Adam, Magestore)
    name = fields.Char(store=True)
    department_id = fields.Many2one("hr.department", String="Department")

    #receiver: get partners. Filter by the user id
    # receiver = fields.Many2many("res.partner", String="To", required=True, domain="['&',('user_ids.id', '!=', 0), ('user_ids.id', '!=',uid)]")
    receiver = fields.Many2many("hr.employee", relation="er_message_receiver_hr_employee_rel", String="To",
                                required=True, domain="['&',('user_id.id', '!=', 0), ('user_id.id', '!=',uid)]")
    receiver_title = fields.Text(compute="_get_receiver_title", store=True)

    #receiver_count: calculate the number of receiver who receive the message
    receiver_count = fields.Integer(compute="_get_receiver_count", store=True)
    receiver_num = fields.Integer(compute="_get_receiver_num", store=True)
    # single_receiver: use to display the avatar of receiver if there is only one receiver

    single_receiver = fields.Many2one("hr.employee", compute="_get_single_receiver")

    message_type = fields.Many2one("er.messagepoint", String="Message Type", requied=True)
    message_point = fields.Integer(compute="_get_message_point")

    #message_title: will be display in the message form (Ex: Thank you * 2)
    message_title = fields.Char(computer="_get_message_title", store=True)

    like_number = fields.Integer(String="Likes", compute="_get_like_number", store=True)
    member_liked = fields.Text()
    member_liked_ids = fields.Many2many("hr.employee", relation="er_message_like_hr_employee_rel",
                                        String="Member Liked")
    member_liked_title = fields.Text(String="Member Like Title", compute="_get_member_liked_title", store=True)
    is_liked = fields.Integer(String="Is Liked", compute="_check_member_like")
    comment_id = fields.Many2one(String="Comments")
    quality_id = fields.Many2many("er.quality", String="Quality")
    quality_title = fields.Text(String="Quality Title", compute="_get_quality_title", store=True)
    message = fields.Text(String="Message")

    sender = fields.Many2one("hr.employee", String="From", required=True, default=lambda self: self.env.user.employee_ids[0])
    active = fields.Boolean('Active', default=True)

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Photo", store=True)
    image_medium = fields.Binary("Medium-sized photo", store=True)
    image_small = fields.Binary("Small-sized photo", store=True)

    sender_image = fields.Html(String="Sender Image", compute="_get_sender_image_url", store=True)
    receiver_image = fields.Html(String="Receiver Image", compute="_get_receiver_image_url", store=True)

    balance_point = fields.Integer(compute="_get_user_balance_point", store=True)
    sending_point = fields.Integer('Sending Point', compute="_get_sending_point", default='0', store=True)
    remaining_point = fields.Integer('Remaining Point', compute="_get_remaining_point", store=True)

    created_time = fields.Char(compute="_get_created_time")
    comment_count = fields.Integer(default=0, string='Number of comment', compute='_compute_comment_quantity')
    # test = fields.Html(default='<img src="/web/image?model=hr.employee&amp;field=image_medium&amp;id=1"/>')

    # @api.model
    # def _default_image(self):
    #     image_path = get_module_resource('employee-reward', 'static/src/img', 'default_image.png')
    #     return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    @api.depends("sender")
    def _get_sender_image_url(self):
        for message in self:
            message.sender_image = '<img src="/web/image?model=hr.employee&amp;field=image_medium&amp;id=' + str(message.sender.id) + '" width="64" height="64"/>'

    @api.depends("receiver", "department_id")
    def _get_receiver_image_url(self):
        for message in self:
            if message.receiver_count == 0:
                message.receiver_image = False
            else:
                if message.receiver_count == 1 & len(message.receiver) == 1:
                    for rc in message.receiver:
                        message.receiver_image = '<img src="/web/image?model=hr.employee&amp;field=image_medium&amp;id=%d" " width="64" height="64"/>' % rc.id
                else:
                    message.receiver_image = '<img src="employee-reward/static/src/img/default_image.png" width="64" height="64" class="oe_kanban_avatar pull-left"/>'

    # store the id of current record and will be used to hidden the right column in xml file: views/message.xml

    @api.multi
    def toggle_active(self):
        for record in self:
            if record.active:
                # Subtract point from receivers
                for message in self:
                    self._update_point_to_receiver(message, False)
            else:
                # Subtract point from receivers
                for message in self:
                    self._update_point_to_receiver(message, True)
            record.active = not record.active

    #
    # walter
    #
    @api.multi
    def _compute_comment_quantity(self):
        for record in self:
            internal_message = self.env['mail.message'].search([('res_id', '=', record.id)])
            record.comment_count = len(internal_message)

    @api.depends("department_id", "receiver")
    def _get_single_receiver(self):
        for message in self:
            if message.receiver_count == 1 & len(message.receiver) == 1:
                for rc in message.receiver:
                    message.single_receiver = self.env['hr.employee'].search([('id', '=', rc.id)])

    @api.depends("message_type")
    def _get_message_point(self):
        for message in self:
            message.message_point = message.message_type.point

    @api.model
    def _get_created_time(self):
        for message in self:
            if message.create_date:
                # format date time
                fm = "%Y-%m-%d %H:%M:%S"

                # convert the create_date to format above
                create_date = datetime.strptime(message.create_date, fm)

                # Get the current time
                today = datetime.now()

                #Subtract the current time and create_date: 3 days, 21:11:00
                subtract = today - create_date
                _days = subtract.days

                if _days > 1 and _days < 30:
                    message.created_time = "%d days ago" % _days
                elif _days == 1:
                    message.created_time = "%d day ago" % _days
                elif _days > 30:
                    message.created_time = create_date
                else:
                    _time = str(subtract).split(":")
                    _hours = int(_time[0])
                    _minutes = int(_time[1])
                    if _hours == 1:
                        message.created_time = "%d hour ago" % _hours
                    elif _hours > 1:
                        message.created_time = "%d hours ago" % _hours
                    else:
                        if _minutes >= 1:
                            message.created_time = "%d minutes ago" % _minutes
                        else:
                            message.created_time = "Just now"


    @api.depends("message_type")
    def _get_user_balance_point(self):
        self.balance_point = self.sender.usr_balance_point
        # for item in self:

    @api.depends("message_type", "receiver", "department_id")
    def _get_message_title(self):
        if self.message_type.name:
            self.message_title = self.message_type.name
            if len(self.receiver) > 0:
                self.message_title = str(self.message_title) + " x " + str(self.receiver_count)

    @api.depends("message_type", "receiver", "department_id")
    def _get_sending_point(self):
        self.sending_point = self.message_type.point * self.receiver_count

    @api.depends("message_type", "receiver", "department_id")
    def _get_remaining_point(self):
        self.remaining_point = self.balance_point - (self.message_type.point * self.receiver_count)

        if self.remaining_point < 0:
            self.remaining_point = self.balance_point
            self.sending_point = 0

    @api.multi
    def report_to_admin(self):
        self.toggle_active()

        # Start code to reload kanban view after click on button report to admin
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('employee-reward', 'er_user_message_wall_kanban')
        view_id = model_obj.browse(data_id).res_id
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': _('Locker'),
            'res_model': 'er.message',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }

    @api.multi
    def remove_message_by_admin(self):
        self.toggle_active()

        # Start code to reload kanban view after click on button report to admin
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('employee-reward', 'manage_wall_message_tree')
        view_id = model_obj.browse(data_id).res_id
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': _('Locker'),
            'res_model': 'er.message',
            'view_type': 'tree',
            'view_mode': 'tree',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }

    @api.depends("department_id", "receiver")
    def _get_receiver_title(self):
        if len(self.receiver) > 0:
            self.receiver_title = ''
            if self.department_id:
                if self.receiver_title != False:
                    self.receiver_title = self.department_id.name + ", " + self.receiver_title
                else:
                    self.receiver_title = self.department_id.name + ", "
            for rc in self.receiver:
                if self.receiver_title != False:
                    self.receiver_title = self.receiver_title + rc.name + ", "
            self.receiver_title = self.receiver_title.rstrip(", ")

    @api.model
    def _get_receiver_list(self):
        employee_ids = []
        if self.department_id.id:
            member_ids = self.env['hr.department'].search([('id', '=', self.department_id.id)]).member_ids
            for member in member_ids:
                if member.user_id.id > 0:
                    if member.id != self.env.user.employee_ids[0].id:
                        if member.id not in employee_ids:
                            employee_ids.append(member.id)
        if self.receiver:
            for receiver in self.receiver:
                if receiver.id not in employee_ids:
                    employee_ids.append(receiver.id)
        return employee_ids

    @api.depends("department_id", "receiver")
    def _get_receiver_count(self):
        self.receiver_count = 0
        employee_ids = self._get_receiver_list()
        self.receiver_count = len(employee_ids)

    @api.depends("receiver")
    def _get_receiver_num(self):
        self.receiver_num = len(self.receiver)

    @api.onchange('message_type', 'receiver', 'department_id')
    def _onchange_message_type_receiver(self):
        # if not self.alias_id:
        if self.message_type:
            self.name = self.message_type.name
            if self.receiver_count > 0:
                self.name += " to "
                for r in self.receiver:
                    self.name += r.name + ", "
                # self.name = self.name[:-1]
                self.name = self.name.rstrip(", ")

        if self.message_type.name:
            self.message_title = self.message_type.name
            if self.receiver_count > 0:
                self.message_title = str(self.message_title) + " x " + str(self.receiver_count)

        self.image = self.message_type.image
        self.image_medium = self.message_type.image_medium
        self.image_small = self.message_type.image_small

        self.sending_point = self.message_type.point * self.receiver_count
        self.remaining_point = self.balance_point - (self.message_type.point * self.receiver_count)

        if self.remaining_point < 0:
            self.remaining_point = self.balance_point
            self.sending_point = 0
            # self.message_type = {}
            return {
                'warning': {
                    'title': "Insufficient points",
                    'message': "This message will be sent with no points.",
                }
            }

    @api.multi
    def _update_point_to_receiver(self, message, is_add=True):
        member_ids = message._get_receiver_list()
        members = self.env['hr.employee'].search([('id', 'in', member_ids)])

        if message.sending_point:
            receive_point = message.sending_point / len(members)
            for member in members:
                if is_add:
                    point = member.usr_receive_point + receive_point
                    point_all_time = member.usr_point_all_time + receive_point  # Walter adding point all time
                else:
                    point = member.usr_receive_point - receive_point
                    point_all_time = member.usr_point_all_time - receive_point  # Walter adding point all time
                member.write({
                    'usr_receive_point': point,
                    'usr_point_all_time': point_all_time,  # Walter adding point all time
                })

    @api.multi
    def _update_point_to_sender(self, message):
        if message.sending_point > 0:
            sending_point = message.sender.usr_sent_point + message.sending_point
            message.sender.write({
                'usr_balance_point': message.remaining_point,
                'usr_sent_point': sending_point
            })

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        res = super(MessageManagement, self).create(vals)
        for r in res:
            # member_ids = r._get_receiver_list()
            # members = self.env['hr.employee'].search([('id', 'in', member_ids)])
            #
            # if r.sending_point:
            #     receive_point = r.sending_point / len(members)
            #     for member in members:
            #         point = member.usr_receive_point + receive_point
            #         point_all_time = member.usr_point_all_time + receive_point      # Walter adding point all time
            #         member.write({
            #             'usr_receive_point': point,
            #             'usr_point_all_time': point_all_time,                       # Walter adding point all time
            #         })
            # sending_point = r.sender.usr_sent_point + r.sending_point
            # r.sender.write({
            #     'usr_balance_point': r.remaining_point,
            #     'usr_sent_point': sending_point
            # })
            # Add point to receivers
            self._update_point_to_receiver(r, True)
            # Send notification to receivers
            r.send_notification_to_receiver()

            # subtract point from the sender
            self._update_point_to_sender(r)


            # Get the subtypes without model
            subtypes = self.env['mail.message.subtype'].search(
                [('res_model', '=', False)])

            # add the receiver into the follower. When the customer write a comment, they will get the notification.
            partner_ids = r._get_partner_receiver()
            r.message_subscribe(partner_ids, subtype_ids=subtypes.ids)
            r.message_subscribe([r.sender.user_id.partner_id.id], subtype_ids=subtypes.ids)
        return res

        # return super(MessageManagement, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(MessageManagement, self).write(vals)

    @api.multi
    def like_action(self):
        member_ids = []
        for message in self:
            if message.member_liked_ids:
                for r in self.member_liked_ids:
                    member_ids.append(r.id)
            if self.env.user.employee_ids[0].id != message.sender.id:
                member_ids.append(self.env.user.employee_ids[0].id)
                self.send_like_notification_to_receiver(self.env.user.employee_ids[0])

            members = self.env['hr.employee'].search([('id', 'in', member_ids)])
            self.member_liked_ids = members

    @api.depends("member_liked_ids")
    def _get_like_number(self):
        for message in self:
            if message.member_liked_ids:
                message.like_number = len(message.member_liked_ids)

    @api.depends("member_liked_ids")
    def _get_member_liked_title(self):
        for message in self:
            if message.member_liked_ids:
                for member in message.member_liked_ids:
                    if message.member_liked_title:
                        message.member_liked_title = message.member_liked_title + member.name + ", "
                    else:
                        message.member_liked_title = member.name
                message.member_liked_title.rstrip(", ")

    @api.model
    def _check_member_like(self):
        for message in self:
            if message.sender.id == message.env.user.employee_ids[0].id:
                message.is_liked = 1
            else:
                if message.member_liked_ids:
                    for member in message.member_liked_ids:
                        if (self.env.user.employee_ids[0].id == member.id):
                            message.is_liked = 1
                        else:
                            message.is_liked = 0
                else:
                    message.is_liked = 0

    # Send notification to the receiver when they receive a message
    @api.multi
    def send_notification_to_receiver(self):
        subject = "%s give you a %s message" % (self.sender.name, self.message_type.name)
        body = self.message
        partner_ids = self._get_partner_receiver()
        message_type = 'notification'
        subtype = 'mail.mt_comment'

        post_vars = {
            'subject': subject,
            'body': body,
            'partner_ids': partner_ids,
            'message_type': message_type,
            'subtype': subtype,
            'record_name': self.name
        }
        # Send notification to the receiver
        self.env['mail.thread'].message_post(**post_vars)

    # Send notification to the receiver when they receive a message
    @api.multi
    def send_like_notification_to_receiver(self, member):
        subject = "%s like the message that you received" % (member.name)
        body = "%s like dthe message that you received" % (member.name)
        partner_ids = self._get_partner_receiver()
        message_type = 'notification'
        subtype = 'mail.mt_comment'

        post_vars = {
            'subject': subject,
            'body': body,
            'partner_ids': partner_ids,
            'message_type': message_type,
            'subtype': subtype
        }
        # Send notification to the receiver
        self.env['mailmail.thread'].message_post(**post_vars)

    # get list partner from the receiver
    @api.model
    def _get_partner_receiver(self, ):
        employee_ids = self._get_receiver_list()
        receivers = self.env['hr.employee'].search([('id', 'in', employee_ids)])
        recipients = []
        for receiver in receivers:
            recipients.append(receiver.user_id.partner_id.id)
        return recipients

    # Send notification to the administrator when a message is reported
    # @api.model
    # def send_notification_to_admin(self):
    #     subject = "%s give you a %s message" % (self.sender.name, self.message_type.name)
    #     body = "The message %s has been reported. Please check it" %(self.name)
    #     partner_ids = self._get_administrator_account()
    #     message_type = 'notification'
    #     subtype = 'mail.mt_comment'
    #
    #     post_vars = {
    #         'subject': subject,
    #         'body': body,
    #         'partner_ids': partner_ids,
    #         'message_type': message_type,
    #         'subtype': subtype
    #     }
    #     self.env['mail.thread'].message_post(**post_vars)
    #
    # @api.model
    # def _get_administrator_account(self):

