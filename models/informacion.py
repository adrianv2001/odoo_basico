# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class informacion(models.Model):
     _name = 'odoo_basico.informacion'
     _description = 'Módulo 2 de Odoo, Agrupamientos y Filtros'
     _sql_constraints = [('nombreUnico','unique(name)','No se puede repetir el nombre')]

     name = fields.Char(string='Titulo')
     descripcion = fields.Text(string='Descripcion')
     alto = fields.Integer(string='Alto en cm')
     largo = fields.Integer(string='largo en cm')
     ancho = fields.Integer(string='ancho en cm')
     peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)
     volume = fields.Float(compute="_volume", store=True)
     densidad = fields.Integer(compute="_densidad",store=True)
     literal = fields.Char(store = False)
     autorizado = fields.Boolean(string="¿Autorizado?", default=True)
     sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Otros','Outros')],string="Sexo")

     @api.depends('alto','largo','ancho')
     def _volume(self):
          for registro in self:
               registro.volume = float(registro.alto)*float(registro.largo)*float(registro.ancho)

     @api.depends('volume', 'peso')
     def _densidad(self):
          for registro in self:
               if registro.volume !=0:
                    registro.densidad =100 * (float(registro.peso)/ float(registro.volume))
               else:
                    registro.densidad=0

     @api.onchange('alto')
     def _avisoAlto(self):
          for rexistro in self:
               if rexistro.alto > 7:
                    rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto
               else:
                    rexistro.literal = "f"

     @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
     def _constrain_peso(self):
          for rexistro in self:
               if rexistro.peso < 1 or rexistro.peso > 4:
                    raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)
