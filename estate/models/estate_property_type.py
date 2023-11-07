from odoo import models, fields


class property_Types(models.Model):

    _name = 'estate.property.type'
    _description = ''
    _order = "sequence, name"

    name = fields.Char(required=True)
    # property_type_id = fields.Many2one('estate.property.type', String="Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', 'Properties')

    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")
