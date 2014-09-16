#!/usr/bin/python
#########################
# Class to interface AWS metadata
#

import boto.utils
from boto import ec2

class Metadata(object):

	def __init__(self, name):
		self.name = name
		self.md = {} 
		self.mitem = {} 
		self.ms = {} 
		self.id = {}
		self.mid = {}
		self.reservations = {}

	def get_md(self):
		self.md = boto.utils.get_instance_metadata()
		
		return self.md
	
	def get_id(self):
		self.id = boto.utils.get_instance_identity()
		
		return self.id
	
	def get_mid(self):
		self.get_md()

		self.mid = self.md['instance-id']

		return self.mid

	def get_instances(self):
		region = self.get_ms('region')
		conn = ec2.connect_to_region(region)
		
		self.reservations = conn.get_all_instances()

		return self.reservations

	def get_ms(self, mitem):
		self.get_md()
	
		if mitem == 'az':
			self.ms = self.md['placement']['availability-zone']
		elif mitem == 'pmac':
			macdata = self.md['network']['interfaces']['macs'].items()[0]
			macdata = dict([macdata])
			self.ms = macdata.keys()[0]	
		elif mitem == 'pip':
			pmac = self.get_ms('pmac')
			self.ms = self.md['network']['interfaces']['macs'][pmac]['local-ipv4s'][0]
		elif mitem == 'sip':
                        pmac = self.get_ms('pmac')
                        self.ms = self.md['network']['interfaces']['macs'][pmac]['local-ipv4s'][1]
		elif mitem == 'region':
			self.get_id()
			self.ms = self.id['document']['region']
		elif mitem == 'env':
			id = self.get_mid()
			self.reservations = self.get_instances()

			instances = [i for r in self.reservations for i in r.instances]
			for instance in instances:
        			if instance.__dict__['id'] == id:
                			self.ms = instance.__dict__['tags']['env']
			
		return self.ms



