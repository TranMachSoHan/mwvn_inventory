from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    default_code = fields.Char(index=True,compute=False,inverse=False,store=True,required=True)
    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    default_code = fields.Char(index=True)


    @api.model
    def process_after_save(self,vals,data_obj):
        if 'attribute_value_ids' in vals:
            ptal_pool = self.env['product.template.attribute.line'].sudo().with_context(update_product_template_attribute_values=False)
            ptav_pool = self.env['product.template.attribute.value'].sudo()
            tmp_line_obj = False
            tmp_lines = False
            tmp_ptav_ids = []
            tmp_value = data_obj.product_tmpl_id.id
            for child_val in data_obj.attribute_value_ids:
                tmp_lines = ptal_pool.search([('product_tmpl_id','=',tmp_value),
                                              ('attribute_id','=',child_val.attribute_id.id)], limit=1)
                if tmp_lines:
                    tmp_line_obj = tmp_lines[0]
                    if child_val.id not in tmp_line_obj.value_ids.ids:
                        tmp_line_obj.write({'value_ids':[(4,child_val.id)]})
                else:
                    tmp_line_obj = ptal_pool.create({'product_tmpl_id':tmp_value,
                                      'attribute_id':child_val.attribute_id.id,
                                      'value_ids':[(6,0,[child_val.id])]})
                
                
                tmp_lines = ptav_pool.search([('product_tmpl_id','=',tmp_value),
                                              ('attribute_line_id','=',tmp_line_obj.id),
                                              ('product_attribute_value_id','=',child_val.id)],limit=1)
                if tmp_lines:
                    tmp_ptav_ids.append(tmp_lines[0].id)
                else:
                    tmp_line_obj = ptav_pool.create({'product_tmpl_id': tmp_value,
                                      'attribute_line_id': tmp_line_obj.id,
                                      'product_attribute_value_id': child_val.id
                                      })
                    tmp_ptav_ids.append(tmp_line_obj.id)
            
            super(ProductProduct,data_obj).write({'product_template_attribute_value_ids':[(6,0,tmp_ptav_ids)]})
            data_obj.with_context(vks_import_ex_thread=False)._compute_combination_indices()
    
    @api.model
    def make_variant_code_auto(self,new_obj):
        d_default_code = new_obj.product_tmpl_id.default_code
        if len(new_obj.product_variant_ids)>1:
            # Todo : Change id to color
            variant_lines = new_obj.product_template_variant_value_ids.filtered(
                lambda line: line.display_type == 'color')
            color_name = variant_lines and variant_lines[0].name or ''
            d_default_code = '%s-%s' % (d_default_code,color_name)
        
        return d_default_code
    
    @api.model
    def create(self,vals):
        new_obj = super(ProductProduct,self).create(vals)
        self.process_after_save(vals=vals,data_obj=new_obj)
        if not new_obj.default_code:
            d_default_code = self.make_variant_code_auto(new_obj=new_obj)
            new_obj.write({'default_code':d_default_code})
        return new_obj
    