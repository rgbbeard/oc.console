#!/usr/bin/python

import importlib.util as util


class OCDepsManager:
	__class_name: str = None

	def __init__(self):
		pass

	@staticmethod
	def module_from_path(path: str):
		spec = OCDepsManager.create_spec(path)
		module = util.module_from_spec(spec)
		spec.loader.exec_module(module)
		return module

	@staticmethod
	def create_spec(path: str):
		return util.spec_from_file_location("c", path)
