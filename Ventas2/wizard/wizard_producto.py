from odoo import api, exceptions, fields, models

class CrearProducto(models.TransientModel):
    _name = 'ventas2.crear.producto'
    _description = 'Crea un producto con Wizard'

    nombre_producto = fields.Char('Nombre del Producto', required=True)


    #@api.multi
    def button_send(self):
        self.ensure_one()
        reg_nuevo = self.env['product.template'].create({'name': self.nombre_producto})

        return True #Añadir esto es una buena práctica