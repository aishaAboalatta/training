from datetime import *

from odoo import models, fields, api



class property_offers(models.Model):
    _name = 'estate.property.offer'
    _description = ''
    _order = "price desc"
    _sql_constraints = [('positive_price',
                         'CHECK(price >= 0)',
                         'The offer price must be positive'),
                        ('positive_validity',
                         'CHECK(validity >= 0)',
                         'Validity must be positive')
                        ]

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)

    # offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offers')
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7, string='validity(days)')
    date_deadline = fields.Date(string='deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
                # subtracting two dates results TimeDelta object

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.create_date:
            self.validity = (self.date_deadline - fields.Date.to_date(self.create_date)).days

    @api.onchange('validity')
    def _onchange_validity(self):
        if self.create_date:
            self.date_deadline = self.create_date + timedelta(days=self.validity)

    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer Accepted'
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True