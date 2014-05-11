from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import packages

from glob import iglob


class AddCustomPackages(Task):
	description = 'Adding custom debs matching /tmp/packages/*.deb'
	phase = phases.package_installation
	successors = [packages.InstallPackages]

	@classmethod
	def run(cls, info):
		for pkg in ['curl', 'ethtool', 'kpartx', 'parted', 'rsync', 'uuid-runtime']:
			info.packages.add(pkg)

		for pkg in iglob('/tmp/packages/*.deb'):
			info.packages.add_local(pkg)
