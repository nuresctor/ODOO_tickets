from odoo import fields, models, api
from datetime import datetime, date, time, timedelta
from openerp.exceptions import except_orm

class Ventas2(models.Model):

    _inherit = 'sale.order'
    _description = 'Siguiendo los tickets'

    referencia_pedido = fields.Char('Referencia del pedido',

        required=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        #self es una lista
       for record in self:
           record.referencia_pedido='Añada referencia'

    def button_cambio_fecha(self):
        for rec in self:
            rec.validity_date=datetime.now()+timedelta(days=2)

    def button_ventana_emergente_OPTIMO(self):
        #import pdb;
        #pdb.set_trace()
        for rec in self:
            res = {
                #accion de abrir un modelo en una nueva ventana con el tipo de vista x
                'type': 'ir.actions.act_window',
                'view_mode': 'form', #por defecto tree,form sin espacios
                #'view_type': 'tree',
                'res_model': 'product.template',
                'target': 'new',
                #'res_id': '',
                #'view_id': '',
                'domain': False,
            }
            return res
