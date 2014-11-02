#-*- coding: utf-8 -*-
# helper.py
# Defines HelperController
#
# Copyright (C) 2013 Jakub Kadlčík
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from psutil import AccessDenied

import tracer.resources.memory as Memory
from tracer.views.helper import HelperView
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.applications import Applications


class HelperController(object):

	args = None

	def __init__(self, args):
		self.args = args

	def render(self):
		for app_name in self.args.helper:
			self.print_helper(app_name, self.args)
			if app_name != self.args.helper[-1]:
				print ""

	def print_helper(self, app_name, args):
		processes = Applications.find(app_name).instances
		if processes:
			tr = Tracer()
			package = tr.package_info(app_name)
			app = Applications.find(app_name)


			try: affected_by = tr.trace_application(app_name)
			except AccessDenied: affected_by = _("affected_by_forbidden")

			view = HelperView()
			view.assign("args", args)
			view.assign("processes", processes)
			view.assign("application", app)
			view.assign("package", package)
			view.assign("affected_by", affected_by)
			view.render()
		else:
			print _("app_not_running").format(app_name)
