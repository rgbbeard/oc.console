#!/usr/bin/python

import json
from typing import Union


"""The config.json file
is expected to be structured as following:

{
	"data": {
		"0" : {
			"field": "value",
			[...]
		},
		[...]
	}
}
"""
class JSONMaid:
	_data = None
	_storage: str = ""

	def __init__(self, filename: str = "config.json"):
		if ".json" in filename:
			self._storage = filename

		try:
			with open(self._storage, "r") as data:
				data = data.read()
				self._data = json.loads(data)
		except FileNotFoundError as e:
			print(f"Configuration file not found {filename}")

		if self._data is not None and not isinstance(self._data.get("data"), (dict, list, tuple)):
			self._data.set("data", dict())
			self._save()

	def __del__(self):
		self._data = None
		self._storage = ""

	def _reopen(self):
		if self._data is None:
			with open(self._storage, "r") as data:
				data = data.read()
				self._data = json.loads(data)

				if not isinstance(self._data.get("data"), (dict, list, tuple)):
					self._data.set("data", dict())

	def _save(self):
		try:
			data = json.dumps(self._data)

			storage = open(self._storage, "w")
			storage.write(data)
			storage.close()

			self._data = None
		except TypeError as te:
			print(f"Fatal error: {te}")
			exit()
		except Exception as e:
			print(f"Generic json fatal error: {e}")
			exit()

	def get_records(self):
		if self._data is None:
			self._reopen()

		return self._data.get("data")

	def records_count(self) -> int:
		if self._data is None:
			self._reopen()

		return len(self.get_records())

	def get_record(self, index: Union[int, str]) -> Union[list, dict, None]:
		try:
			return self.get_records()[str(index)]
		except KeyError:
			return None
		except Exception:
			return None

	def update_record(self, old_record: dict, new_record: dict) -> bool:
		if self._data is None:
			self._reopen()

		data = self.get_records()

		for x in range(self.records_count()):
			row = data[str(x)]

			if row == old_record:
				data[str(x)] = new_record
				self._save()
				return True

		return False

	def put_record(self, record: dict) -> bool:
		if self._data is None:
			self._reopen()
			
		can_be_added = True
	    
		for x in range(self.records_count() - 1):
			row = self.get_records()[str(x)]

			if row == record:
				can_be_added = False
				break

		if can_be_added:
			uid = self.records_count()
			uid = str(uid)

			self._data.get("data")[uid] = record
			self._save()

		return can_be_added
