from odoo import models, fields


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    size_id = fields.Many2one('product.attribute.value',
                           domain=lambda self: [('attribute_id', '=', self.env.ref('mwn_sales.size_attribute').id)])
    inseam_id = fields.Many2one('product.attribute.value',
                             domain=lambda self: [('attribute_id', '=', self.env.ref('mwn_sales.size_attribute').id)])
