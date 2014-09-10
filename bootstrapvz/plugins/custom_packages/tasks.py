from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import packages

from glob import iglob

import os


class AddCustomPackages(Task):
	description = 'Adding custom debs matching /tmp/packages/*.deb'
	phase = phases.package_installation
	successors = [packages.InstallPackages]

	@classmethod
	def run(cls, info):
		for pkg in ['curl', 'ethtool', 'kpartx', 'parted', 'rsync', 'uuid-runtime']:
			info.packages.add(pkg)

		for pkg in iglob('/tmp/packages/*.deb'):
			# For all packages that we'll be installing locally, also ensure we're not trying to
			# install them other ways, e.g. via apt-get from our public apt repository.

			# Parse out the package name from the deb filename (the format is standard and
			# underscore-delimited).
			pkg_name = os.path.basename(pkg).split('_')[0]

                        # Next, remove it from the list of packages to install before re-queuing it for a
			# local install.
			#
			# Do this with slice assignment to ensure we remove all occurrences
			# that might have been added to the list. info.packages.add() enforces something
			# reasonable by default, but info.packages.add_local() doesn't.
			#
			# Elements of info.packages.install will have a name attribute if they're added via
			# add(), but not if added via add_local(). Really. Therefore we need to use hasattr in
			# order to placate Python.
			info.packages.install[:] = (p for p in info.packages.install
			                            if not (hasattr(p, 'name') and p.name == pkg_name))

			# Last, add this package to the list of local installs.
			info.packages.add_local(pkg)
