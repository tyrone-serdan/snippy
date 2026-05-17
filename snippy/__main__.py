from textual.app import App, ComposeResult
from textual.widgets import Header, ListView, ListItem, TextArea, Static, Button, Input
from textual.containers import Horizontal, Vertical
from snippy.services import storage
from snippy.services import clipboard
from snippy.services import utils

class Snippy(App):
	CSS = """
	#sidebar {
		width: 25%;
		border: solid $primary;
	}

	#content {
		width: 75%;
		border: solid $primary;
	}

	#button-bar {
		dock: bottom;
		height: 3;
		padding: 0 1;
		align: center middle;
	}

	#button-bar Button {
		background: transparent;
		border: none;
		color: $text-muted;
		margin: 0 1;
	}

	#button-bar Button:hover {
		color: $text;
		text-style: bold;
	}

	#button-bar Button:focus {
		text-style: underline;
	}

	#snippet-form {
		dock: bottom;
		height: auto;
		padding: 0 1;
		border-top: solid $primary;
	}

	#snippet-list {
		height: 1fr;
	}
	"""

	def __init__(self):
		super().__init__()
		self.snippets = storage.load_snippets()

	def compose(self) -> ComposeResult:
		yield Header()
		with Horizontal():
			with Vertical(id="sidebar"):
				yield ListView(
					*[ListItem(Static(s["title"])) for s in self.snippets],
					id="snippet-list"
				)
				with Vertical(id="snippet-form"):
					yield Input(placeholder="Snippet name...", id="name-input")
					yield Input(placeholder="Language...", id="lang-input")
			yield TextArea(id="content", tab_behavior="indent", show_line_numbers=True)
		with Horizontal(id="button-bar"):
			yield Button("Copy", id="copy-btn")
			yield Button("Create", id="create-btn")
			yield Button("Delete", id="delete-btn")
			yield Button("Save", id="save-btn")

	def on_list_view_selected(self, event: ListView.Selected) -> None:
		idx = event.list_view.children.index(event.item)
		snippet = self.snippets[idx]

		nameinput = self.query_one("#name-input", Input)
		langinput = self.query_one("#lang-input", Input)
		textarea = self.query_one("#content", TextArea)

		nameinput.value = snippet["title"]
		langinput.value = snippet["language"]
		textarea.text = snippet["content"]

		if langinput.value in textarea.available_languages or utils.language_from_shorthand(langinput.value) in textarea.available_languages:
			textarea.language = langinput.value
		else:
			textarea.language = ""

	def on_button_pressed(self, event: Button.Pressed) -> None:
		button = event.button.id

		match button:
			case "copy-btn":
				self._copy_snippet()
			case "create-btn":
				self._create_snippet()
			case "delete-btn":
				self._delete_snippet()
			case "save-btn":
				self._save_snippet()

	def _copy_snippet(self) -> None:
		textarea = self.query_one("#content", TextArea).text
		clipboard.copy(textarea)

	def _create_snippet(self) -> None:
		nameinput = self.query_one("#name-input", Input)
		langinput = self.query_one("#lang-input", Input)
		textarea = self.query_one("#content", TextArea)

		nameinput.value = ""
		langinput.value = ""
		textarea.text = ""

	def _delete_snippet(self) -> None:
		nameinput = self.query_one("#name-input", Input).value

		storage.delete_snippet(nameinput)
		self._refresh_snippet_list()

	def _save_snippet(self) -> None:
		nameinput = self.query_one("#name-input", Input).value
		langinput = self.query_one("#lang-input", Input).value
		textarea = self.query_one("#content", TextArea).text

		snippet = {"title": nameinput, "language": langinput, "content": textarea}

		storage.save_snippet(snippet)
		self._refresh_snippet_list()

	def _refresh_snippet_list(self) -> None:
		self.snippets = storage.load_snippets()
		list_view = self.query_one("#snippet-list", ListView)

		list_view.clear()
		list_view.extend(ListItem(Static(s["title"])) for s in self.snippets)


def main():
	Snippy().run()


if __name__ == "__main__":
	main()
