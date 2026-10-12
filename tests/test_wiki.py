"""Documentation / branding regression checks, standard library only."""
from __future__ import annotations
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / 'wiki'


class WikiDocumentationTests(unittest.TestCase):
    def test_wiki_entry_points_exist(self):
        for name in ('Home', '_Sidebar', 'Getting-Started', 'Architecture',
                     'Visual-Grammar', 'Archetype-Catalog', 'Use-Case-Profiles',
                     'Composition-Recipes', 'Publishing-the-Wiki',
                     'Security-and-Boundaries'):
            with self.subTest(name=name):
                self.assertTrue((WIKI / f'{name}.md').is_file())
        self.assertGreaterEqual(len(list(WIKI.glob('*.md'))), 17)

    def test_internal_wiki_links_resolve(self):
        links = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
        for page in WIKI.glob('*.md'):
            for link in links.findall(page.read_text(encoding='utf-8')):
                if link.startswith(('https://', 'http://', 'mailto:', '#')):
                    continue
                destination = link.split('#', 1)[0]
                with self.subTest(page=page.name, link=link):
                    self.assertTrue((WIKI / (destination if destination.endswith('.md') else destination + '.md')).is_file())

    def test_catalogues_cover_live_json_keys(self):
        text = (WIKI / 'Archetype-Catalog.md').read_text(encoding='utf-8')
        index = json.loads((ROOT / 'catalogue.json').read_text(encoding='utf-8'))
        self.assertEqual(len(index['archetypes']), 19)
        for entry in index['archetypes']:
            self.assertIn('`' + entry['slug'] + '`', text)
        profiles = json.loads((ROOT / 'inventaires/profils-usage.json').read_text(encoding='utf-8'))['profiles']
        ptext = (WIKI / 'Use-Case-Profiles.md').read_text(encoding='utf-8')
        self.assertEqual(len(profiles), 5)
        for profile in profiles:
            self.assertIn(profile['assemblage_reference'], ptext)
        recipes = list((ROOT / 'assemblages').glob('*.json'))
        rtext = (WIKI / 'Composition-Recipes.md').read_text(encoding='utf-8')
        self.assertEqual(len(recipes), 14)
        for recipe in recipes:
            self.assertIn('`' + recipe.stem + '`', rtext)

    def test_readme_english_and_logo_not_embedded(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('A visual archetype library', text)
        self.assertIn('GitHub Wiki publishing', text)
        self.assertNotRegex(text, r'!\[[^\]]*\]\([^)]*\)')
        self.assertNotIn('<img', text.lower())
        self.assertNotIn('<svg', text.lower())

    def test_logo_is_available_in_both_visual_interfaces(self):
        svg = ROOT / 'assets/logo-k.svg'
        png = ROOT / 'assets/logo-k-ui.png'
        self.assertTrue(svg.is_file())
        self.assertTrue(png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
        self.assertIn('logo-k-ui.png', (ROOT / 'Lancer_Arketype.pyw').read_text(encoding='utf-8'))
        self.assertIn('logo-k.svg', (ROOT / 'catalogue/index.html').read_text(encoding='utf-8'))

    def test_wiki_github_repository_separation_documented(self):
        guide = (WIKI / 'Publishing-the-Wiki.md').read_text(encoding='utf-8')
        self.assertIn('separate Git repository', guide)
        self.assertIn('REPOSITORY.wiki.git', guide)
        self.assertIn('No remote Wiki is created or updated', guide)


if __name__ == '__main__':
    unittest.main()
