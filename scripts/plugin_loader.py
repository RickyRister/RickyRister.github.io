import glob
import inspect
import os
import sys
from importlib import util
from types import ModuleType

from plugin_base import Plugin


def loadPlugins(pluginDir: str) -> list[Plugin]:
	"""
	Loads all plugins in the given directory.

	Plugins are detected as any objects that extends from Plugin that resides in a .py file in the dir
	"""
	plugins: list[Plugin] = []

	# Instantiate all Plugin subclasses found in .py files in the plugin folder
	for path in glob.glob(pluginDir + "/*.py"):
		if path.endswith(".py"):
			module = import_from_path(os.path.basename(path), path)
			for name, cls in inspect.getmembers(module, inspect.isclass):
				if issubclass(cls, Plugin):
					print(f"Found plugin {cls} in {path}")
					plugins.append(cls())

	# trigger afterInit hooks
	for plugin in plugins:
		plugin.onInit()

	return plugins


def import_from_path(module_name, file_path) -> ModuleType:
	spec = util.spec_from_file_location(module_name, file_path)
	module = util.module_from_spec(spec)
	sys.modules[module_name] = module
	spec.loader.exec_module(module)
	return module
