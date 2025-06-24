"""
Contains the plugin base class and all classes required to work with plugins.

Your plugin implementation should import this module.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Context:
	"""
	This object stores the current state of the script
	"""
	pass


class Plugin(ABC):
	"""
	Your plugin should extend this class.
	Override the specific hooks that you care about.
	"""

	@property
	@abstractmethod
	def priority(self) -> int:
		"""
		Can be an integer from INT_MIN (which includes negatives) to INT_MAX.
		When multiple plugins have the same hook, plugins are run in order from highest to lowest priority value.
		If multiple plugins have the same priority, they will be run in some nondeterministic order.

		There's no structure to how the priority is decided atm.
		Just be nice I guess lol.
		Assume 0 is the default
		"""

	def onInit(self):
		"""
		Called after all plugins for this round of loading has been loaded
		"""
		...

	def onBeforeGenAllCards(self, codes: list[str]):
		"""
		Called right before the genAllCards function runs

		:param codes: The list of set codes
		"""
		...

	def onBeforeGenCardsForSet(self, codes: list[str], code: str, raw: dict[str, Any]):
		"""
		Called every time before genAllCards starts processing a single set

		:param codes: The list of set codes
		:param code: The current set code
		:param raw: The raw set json
		"""
		...

	def onBeforeGenCard(self, codes: list[str], code: str, raw: dict[str, Any], card: dict[str, Any]):
		"""
		Called before the processing of a single card from the set json

		:param codes: The list of set codes
		:param code: The current set code
		:param raw: The raw set json
		:param card: The current card that is being processed. Intended to be modified
		"""
		...

	def onAfterGenCard(self, codes: list[str], code: str, raw: dict[str, Any], card: dict[str, Any]):
		"""
		Called after the processing of a single card from the set json, before being appended to the card_input

		:param codes: The list of set codes
		:param code: The current set code
		:param raw: The raw set json
		:param card: The current card that is being processed. Intended to be modified
		"""
		...

	def onAfterGenCardsForSet(self, codes: list[str], code: str, raw: dict[str, Any], set_data: dict[str, Any]):
		"""
		Called after processing all cards from a set, before saving the set_data

		:param codes: The list of set codes
		:param code: The set code
		:param raw: The raw set json
		:param set_data: The set_data entry in the set_input json. Intended to be modified
		"""
		...

	def onAfterGenAllCards(self, codes: list[str], card_input: dict[str, Any], set_input: dict[str, Any]):
		"""
		Called after the processing from genAllCards but before the json files are printed.

		:param codes: The list of set codes
		:param card_input: The processed json, before being saved to file. Intended to be modified
		:param set_input: The processed json, before being saved to file. Intended to be modified
		"""
		...

	def onBeforeReprocessSet(self, codes: list[str], code: str, set_json: dict[str, Any]):
		"""
		Called before reprocessing the <code>-files set json

		:param codes: The list of set codes
		:param code: The set code
		:param set_json: The raw set json. Intended to be modified
		"""
		...

	def onAfterReprocessSet(self, codes: list[str], code: str, set_json: dict[str, Any]):
		"""
		Called after reprocessing the set json, before saving the set json to <code>-files/<code>.json

		:param codes: The list of set codes
		:param code: The set code
		:param set_json: The raw set json. Intended to be modified
		"""
		...

	def onAfterReprocessAllSets(self, codes: list[str]):
		"""
		Called after reprocessing all set jsons, before running the remaining html generators

		:param codes: The list of set codes
		"""
		...

	def onGenerateOtherHtml(self, codes: list[str]):
		"""
		Called after all the other processes have happened

		:param codes: The list of set codes
		"""
		...
