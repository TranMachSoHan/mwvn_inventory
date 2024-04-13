from odoo import api, models, fields, _
from odoo.exceptions import UserError


class MrpBomLinesWizard(models.TransientModel):
    _name = "mrp.bom.lines.wizard"

    bom_id = fields.Many2one('mrp.bom', string='Đơn Hàng')
    product_tmpl_id = fields.Many2one('product.template')
    exclude_product_id = fields.Many2one('product.product')
    product_id = fields.Many2one('product.product', string='Sản Phẩm',
                                 domain="['&', ('product_tmpl_id', '=', product_tmpl_id), ('id', '!=', exclude_product_id)]")
    # size_attributes = fields.Many2many('product.attribute.value', 'size_attribute_wizard_rel', 'wizard_id', 'attribute_id',
    #                                    string="Size", 
    #                                    domain=lambda self: [('attribute_id', '=', self.env.ref('mwn_sales.size_attribute').id)])
    # inseam_attributes = fields.Many2many('product.attribute.value', 'inseam_attribute_wizard_rel', 'wizard_id', 'attribute_id',
    #                                      string="Inseam",
    #                                      domain=lambda self: [('attribute_id', '=', self.env.ref('mwn_sales.inseam_attribute').id)])
    wizard_line_ids = fields.One2many('mrp.bom.lines.wizard.line', 'wizard_id')

    def button_confirm(self):
        self.ensure_one()
        bom_line_vals = self._generate_bom_line_vals()
        self.bom_id.update({'bom_line_ids': bom_line_vals})

    def _generate_bom_line_vals(self):
        bom_line_vals = []
        if self.wizard_line_ids:
            bom_line_vals = [(2, line.id) for line in self.bom_id.bom_line_ids.filtered(
                    lambda line: line.product_id.id == self.product_id.id)]
            for line in self.wizard_line_ids:
                if line.qty > 0:
                    bom_line_vals.append((0, 0, {
                        'product_id': self.product_id.id,
                        'product_qty': line.qty,
                        'size_id': line.size_id.id,
                        'inseam_id': line.inseam_id.id
                    }))
        return bom_line_vals
    
    def _prepare_product_sale_order_line(self, size_id, inseam_id):
        return {
            'bom_id': self.bom_id.id,
            'product_id': self.product_id.id,
            'product_qty': 1.0,
            'size_id': size_id,
            'inseam_id': inseam_id
        }

    def action_update_wizard_lines(self):
        if not self.product_id:
            raise UserError("Hãy nhập sản phẩm")
        
        size_attributes = self.env['product.attribute.value'].search([('attribute_id', '=', self.env.ref('mwn_sales.size_attribute').id)])
        inseam_attributes = self.env['product.attribute.value'].search([('attribute_id', '=', self.env.ref('mwn_sales.inseam_attribute').id)])
        bom_line_ids = {(line.inseam_id, line.size_id): line.product_qty
            for line in self.bom_id.bom_line_ids.filtered(
                lambda line: line.product_id.id == self.product_id.id)}

        wizard_lines = [(5, 0, 0)] + [
            (0, 0, {
                'inseam_id': inseam_id.id,
                'size_id': size_id.id,
                'qty': bom_line_ids.get((inseam_id, size_id), 0),
            })
            for inseam_id in inseam_attributes
            for size_id in size_attributes
        ]

        self.update({
            'wizard_line_ids': wizard_lines
        })
        action = self.env['ir.actions.act_window']._for_xml_id('mwn_sales.mrp_bom_lines_wizard_action')
        action['views'] = [(False, 'form')]
        action['res_id'] = self.id
        return action
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.update({
            'wizard_line_ids': [(5, 0, 0)]
        })

        

class MrpLinesWizard(models.TransientModel):
    _name = "mrp.bom.lines.wizard.line"

    wizard_id = fields.Many2one('mrp.bom.lines.wizard')
    size_id = fields.Many2one('product.attribute.value', readonly=True)
    inseam_id = fields.Many2one('product.attribute.value', readonly=True)
    qty = fields.Float()
