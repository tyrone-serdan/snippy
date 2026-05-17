from pathlib import Path
from platformdirs import user_documents_dir
import json

SNIPPETS_DIR = Path(user_documents_dir()) / "snippy-snippets"

def load_snippets():
	SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
	snippets = []

	for file in SNIPPETS_DIR.glob("*.json"):
		try:
			with open(file, "r", encoding="utf-8") as f:
				snippet = json.load(f)

				snippets.append(snippet)

		except Exception as e:
			print(f"Failed to load {file}: {e}")

	return snippets

def save_snippet(snippet: dict):
	title = snippet.get("title", "untitled")

	filepath = SNIPPETS_DIR / f"{title}.json"

	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(snippet, f, indent=2)

def delete_snippet(title: str):
	filepath = SNIPPETS_DIR / f"{title}.json"
	filepath.unlink(missing_ok=False)
