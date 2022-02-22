# -*- coding: utf-8 -*-
import locale

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import os
import pytz
from . import Utilidades


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo 2 de Odoo, Agrupamientos y Filtros'
    _sql_constraints = [('nombreUnico', 'unique(name)', 'No se puede repetir el nombre')]

    name = fields.Char(string='Titulo')
    descripcion = fields.Text(string='Descripcion')
    alto = fields.Integer(string='Alto en cm')
    largo = fields.Integer(string='largo en cm')
    ancho = fields.Integer(string='ancho en cm')
    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)
    volume = fields.Float(compute="_volume", store=True)
    densidad = fields.Integer(compute="_densidad", store=True)
    literal = fields.Char(store=False)
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string="Sexo")
    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    hora_utc = fields.Char(compute="_hora_utc", string="Hora UTC", size=15, store=True)
    hora_timezone_usuario = fields.Char(compute="_hora_timezone_usuario", string="Hora Timezone do Usuario", size=15,
                                        store=True)
    hora_actual = fields.Char(compute="_hora_actual", string="Hora Actual", size=15, store=True)
    #mes_castelan = fields.Char(compute="_mes_castelan", size=15, string="Mes castelán", store=True)
    #mes_galego = fields.Char(compute="_mes_galego", size=15, string="Mes galego", store=True)

    @api.depends('alto', 'largo', 'ancho')
    def _volume(self):
        for registro in self:
            registro.volume = float(registro.alto) * float(registro.largo) * float(registro.ancho)

    @api.depends('volume', 'peso')
    def _densidad(self):
        for registro in self:
            if registro.volume != 0:
                registro.densidad = 100 * (float(registro.peso) / float(registro.volume))
            else:
                registro.densidad = 0

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

    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            # Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            # Importamos tamén a libreria os mediante import os
            raise Warning(
                'Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))

        # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,
                                                        data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(
            self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(
            usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self:  # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    def actualiza_hora_actual_UTC(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende _hora_actual
        for rexistro in self:
            rexistro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")
        # Grava a hora en UTC, se quixesemos poderiamos usar a función  _convirte_data_hora_de_utc_a_timezone_do_usuario

    @api.depends('data_hora')
    def _hora_actual(self):
        for rexistro in self:
            rexistro.actualiza_hora_actual_UTC()

        # Esta función será chamada dende a función actualiza_hora_timezone_usuario_dende_boton_e_apidepends e
        #  dende pedido.py (Cando insertamos os valores do template self.env.user.tz non ten o timezone do usuario por iso se carga coa hora UTC,
        #  o botón en pedido.py é para actualizar todos os rexistros masivamente dende outro modelo)

    def actualiza_hora_timezone_usuario(self, obxeto_rexistro):
        obxeto_rexistro.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(
            obxeto_rexistro.data_hora).strftime(
            "%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario

    def actualiza_hora_timezone_usuario_dende_boton_e_apidepends(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende @api.depends _hora_timezone_usuario
        self.actualiza_hora_timezone_usuario(
            self)  # leva self como parametro por que actualiza_hora_timezone_usuario ten 2 parametros
        # porque usamos tamén actualiza_hora_timezone_usuario dende outro modelo (pedido.py) e lle pasamos como parámetro o obxeto_rexistro

    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    def actualizadorHoraTimezone(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion'].actualiza_hora_timezone_usuario(rexistro)

    #@api.depends('data_hora')
    # def _mes_castelan(self):
    #     # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
    #     # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
    #     # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
    #     # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
    #     locale.setlocale(locale.LC_TIME, Utilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))
    #     for rexistro in self:
    #         rexistro.mes_castelan = rexistro.data.strftime("%B")  # strftime https://strftime.org/
    #
    # @api.depends('data_hora')
    # def _mes_galego(self):
    #     # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
    #     # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
    #     # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
    #     # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
    #     locale.setlocale(locale.LC_TIME, Utilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
    #     for rexistro in self:
    #         rexistro.mes_galego = rexistro.data.strftime("%B")
    #     locale.setlocale(locale.LC_TIME, Utilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    def envio_email(self):
        meu_usuario = self.env.user
        # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'adrianodoo2022@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Importante!',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,
                                                        data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(
            self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(
            usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz