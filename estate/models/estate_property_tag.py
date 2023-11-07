from odoo import models, fields

class property_Tags(models.Model):

    _name = 'estate.property.tag'
    _description = ''
    _order = "name"
    _sql_constraints = [('unique_tag_name', 'UNIQUE (name)', 'This tag name already exist')]

    name = fields.Char(required=True)
    Color = fields.Integer()


