# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import models, fields,_, api
from odoo.exceptions import UserError
import random
import string
import datetime
import logging
_logger = logging.getLogger(__name__)


def _default_unique_key(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


class RestAPI(models.Model):
	_name = "rest.api"
	_description = "RESTful Web Services"

	def _default_unique_key(self, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	@api.model
	def _check_permissions(self, model_name, context=None):
		response = {'success':True, 'message':'OK','permisssions':{}}
		model_exists = self.env['ir.model'].sudo().search([('model','=',model_name)])
		if not model_exists:
			response['success'] = False
			response['message'] = f"Model({model_name}) doen`t exists !!!"
		elif self.availabilty == "all":
			response['success']= True
			response['message'] = f"Allowed all Models Permission: {self.availabilty}"
			response['model_id'] = model_exists.id
			response['permisssions'].update({'read':True,'write':True,'delete':True,'create':True})
		elif (
			resource_allowed := self.env['rest.api.resources']
			.sudo()
			.search([('api_id', '=', self.id), ('model_id', '=', model_exists.id)])
		):
			response['success'] = True
			response[
				'message'
			] = f"Allowed {model_exists.name} Models Permission: {self.availabilty}"
			response['model_id'] = model_exists.id
			response['permisssions'].update({'read': resource_allowed.read_ok, 'write': resource_allowed.write_ok, 'delete': resource_allowed.unlink_ok, 'create': resource_allowed.create_ok})
		else:
			response['success'] = False
			response[
				'message'
			] = f"Sorry,you don`t have enough permission to access this Model({model_name}). Please consult with your Administrator."
		return response

	@api.model
	def _validate(self, api_key, context=None):
		context = context or {}
		response = {'success':False, 'message':'Unknown Error !!!'}
		if not api_key:
			response['responseCode'] = 0
			response['message'] = 'Invalid/Missing Api Key !!!'
			return response
		try:
			if Obj_exists := self.sudo().search([('api_key', '=', api_key)]):
				response['success'] = True
				response['responseCode'] = 2
				response['message'] = 'Login successfully.'
				response['confObj'] = Obj_exists
			else:
				response['responseCode'] = 1
				response['message'] = "API Key is invalid !!!"
		except Exception as e:
			response['responseCode'] = 3
			response['message'] = "Login Failed: %r"%e.message or e.name
		return response

	name = fields.Char('Name', required=1)
	description = fields.Text('Extra Information', help="Quick description of the key", translate=True)
	# api_key = fields.Char(string='API Secret key', default=_default_unique_key(32), required=1)
	api_key = fields.Char(string='API Secret key')
	active = fields.Boolean(default=True)
	resource_ids = fields.One2many('rest.api.resources','api_id', string='Choose Resources')
	availabilty = fields.Selection([
        ('all', 'All Resources'),
        ('specific', 'Specific Resources')], 'Available for', default='all',
        help="Choose resources to be available for this key.", required=1)

	def generate_secret_key(self):
		self.api_key = _default_unique_key(32)

	# @api.one
	def copy(self, default=None):
		raise UserError(_("You can't duplicate this Configuration."))

	# @api.multi
	def unlink(self):
		raise UserError(_('You cannot delete this Configuration, but you can disable/In-active it.'))
