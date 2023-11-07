

from odoo import models, fields, api
from datetime import timedelta
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "estate.property"
    _description = "my first model for state property"
    _order = "id desc"
    _sql_constraints = [('positive_expected_price',
                         'CHECK(expected_price >= 0)',
                         'The expected price must be positive'),
                        ('positive_property_rooms',
                         'CHECK(bedrooms >= 0 AND living_area >= 0 AND garden_area >= 0 AND facades >= 0)',
                         'negative values are not accepted')
                        ]

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available Form', copy=False,
                                    default=lambda self: fields.Datetime.today()+timedelta(days=90))
    expected_price = fields.Float('Expected Price"', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'),
                                                     ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    STATES = [('new', 'New'), ('offer Received', 'Offer Received'), ('offer Accepted', 'Offer Accepted'),
              ('sold', 'Sold'), ('canceled', 'Canceled')]
    state = fields.Selection(required=True, copy=False,
                             selection=STATES, default=STATES[0][0])

    # property_ids = fields.One2many('estate.property','property_type_id','Properties')
    property_type_id = fields.Many2one('estate.property.type', String="Property Type", required=True)

    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    # env.user get current user
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tags_ids = fields.Many2many('estate.property.tag', String="Property Tags")

    # property_id = fields.Many2one('estate.property', required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offers')
    # ondelete='cascade'

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.offer_ids.price, 0.9 * record.expected_price,
                             precision_rounding=0.1) < 0:
                raise ValidationError('Offer price lower than 90% of the expected price is not accepted')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def sold_property(self):
        for record in self:
            record.state = record.STATES[3][0]
        return True

    def cancel_property(self):
        for record in self:
            record.state = record.STATES[4][0]
        return True
