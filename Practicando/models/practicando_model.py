from odoo import fields, models

class Practicando(models.Model):

    _name = 'practicando.model'
    _description = 'Siguiendo los tickets'

    texto_prueba = fields.Text('Texto de prueba')
    name = fields.Char('Nombre')
    date= fields.Date('Fecha')


