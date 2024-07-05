# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'account.move.invoice_kanban'

    stage_id = fields.Many2one('account.move.stage', string="Stage", default=lambda self: self._get_default_stage())

    followup_responsible_id = fields.Many2one(
        string='Accounts Receivable',
        comodel_name='res.users',
        copy=False,
        tracking=True,
        store=True,
        readonly=False,
    )

    vat = fields.Char(related='partner_id.vat', string="GSTN", readonly=False)
    place_of_supply = fields.Char(string='Place Of Supply', store=True)
    age_display = fields.Char(string='Ageing', compute='_compute_age_display', store=True)
    age_days = fields.Integer(string='Ageing in Days', compute='_compute_age_days', store=True, index=True)

    activity_state = fields.Selection([
        ('overdue', 'Next activity late'),
        ('today', 'Next activity is today'),
        ('planned', 'Next activity is planned')], string='Kanban State',
        compute='_compute_activity_state', store=True)

    @api.depends('activity_ids.date_deadline')
    def _compute_activity_state(self):
        for record in self:
            today = fields.Date.today()
            activities = self.env['mail.activity'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id)
            ])

            if not activities:
                record.activity_state = False
            else:
                min_date = min(activities.mapped('date_deadline'))
                max_date = max(activities.mapped('date_deadline'))

                if max_date < today:
                    record.activity_state = 'overdue'
                elif min_date > today:
                    record.activity_state = 'planned'
                else:
                    record.activity_state = 'today'

    @api.depends('age_days', 'invoice_date')
    def _compute_age_display(self):
        for record in self:
            if record.create_date:
                now = datetime.now()
                delta = now - record.create_date
                years = delta.days // 365
                months = (delta.days % 365) // 30
                days = (delta.days % 365) % 30

                if years > 0:
                    record.age_display = f"{years} year(s)"
                elif months > 0:
                    record.age_display = f"{months} month(s) {days} day(s)"
                else:
                    record.age_display = f"{delta.days} day(s)"
            else:
                record.age_display = False

    @api.depends('invoice_date')
    def _compute_age_days(self):
        for record in self:
            if record.create_date:
                delta = datetime.now() - record.create_date
                record.age_days = delta.days
            else:
                record.age_days = 0

    @api.model
    def _get_default_stage(self):
        stage = self.env['account.move.stage'].search([], limit=1, order='sequence')
        return stage.id if stage else False

