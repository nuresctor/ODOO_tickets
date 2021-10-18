from odoo import fields, models, api
from datetime import datetime, date, time, timedelta

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





