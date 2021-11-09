# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
     _name = 'odoo_basico.informacion'
     _description = 'Módulo 2 de Odoo, Agrupamientos y Filtros'

     autorizado = fields.Boolean(string="¿Autorizado?", default=True)
     name = fields.Char(string='Titulo')
     descripcion = fields.Text(string='Descripcion')
     alto = fields.Integer(string='Alto en cm')

