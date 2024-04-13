from odoo import models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def action_open_wizard_generate_sale_order_line_product_attributes(self):
        self.ensure_one()
        return {
            'name': 'Tạo đơn hàng',
            'view_mode': 'form',
            'view_id': self.env.ref(
                'mwn_sales.mrp_bom_lines_wizard_view_form').id,
            'view_type': 'form',
            'res_model': 'mrp.bom.lines.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_bom_id': self.id,
                'default_exclude_product_id': self.product_id.id,
                'default_product_tmpl_id': self.product_tmpl_id.id
            }
        }
