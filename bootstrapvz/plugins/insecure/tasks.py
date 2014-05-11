from bootstrapvz.base import Task
from bootstrapvz.common import phases
import os
import shutil

class EnableInsecureAccess(Task):
	description = 'Enabling shell access via /dev/ttyS1'
	phase = phases.system_modification

	@classmethod
	def run(cls, info):
		# Append a line to /etc/inittab launching /bin/bash on
		# /dev/ttyS1.
		insecure_line_source = os.path.join(os.path.dirname(__file__), 'ttyS1.inittab')
		with open(os.path.join(info.root, 'etc', 'inittab'), 'a') as inittab:
			with open(insecure_line_source, 'r') as insecure_line:
				shutil.copyfileobj(insecure_line, inittab)
