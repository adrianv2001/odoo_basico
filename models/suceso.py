
from odoo import models, fields, api


class suceso(models.Model):
     _name = 'odoo_basico.suceso'#nombre del modelo, debe coincidir con el nombre del archivo y de la clase
     _description = 'Módulo 2 de Odoo, Agrupamientos y Filtros'

     name = fields.Char(required=True, size=20, string="Suceso")
     descripcion = fields.Text(string="A Descripción do Suceso")  # string é a etiqueta do campo
     #campo selection debe llevar dos valores; el que va a la bbdd y el que sale por pantalla,
     #si no se ponen los dos da error
     nivel = fields.Selection([('Baixo', 'Baixo'), ('Medio', 'Medio'), ('Alto', 'Alto')], string='Nivel')
     data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
