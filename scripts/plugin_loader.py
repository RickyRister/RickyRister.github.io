import importlib
import inspect
import glob

from plugin_base import Plugin


def loadPlugins(pluginDir: str) -> list[Plugin]:
	"""
	Loads all plugins in the given directory.

	Plugins are detected as any objects that extends from Plugin that resides in a .py file in the dir
	"""
	plugins: list[Plugin] = []

	# Instantiate all Plugin subclasses found in .py files in the plugin folder
	for filename in glob.glob(pluginDir + "/*.py"):
		if filename.endswith(".py"):
			modulename = f"{pluginDir}.{filename.removesuffix(".py")}"
			module = importlib.import_module(modulename)
			for name, cls in inspect.getmembers(module, inspect.isclass):
				if issubclass(cls, Plugin):
					print(f"Found plugin {cls} in {modulename}")
					plugins.append(cls())

	# trigger afterInit hooks
	for plugin in plugins:
		plugin.onInit()

	return plugins
