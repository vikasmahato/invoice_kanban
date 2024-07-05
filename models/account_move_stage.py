# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveStage(models.Model):
    _name = 'account.move.stage'
    _description = 'Account Move Stage'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)

