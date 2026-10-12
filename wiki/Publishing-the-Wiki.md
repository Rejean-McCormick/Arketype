# Publishing the Wiki to GitHub

This repository includes **GitHub Wiki-ready Markdown pages** in `wiki/`, including the `Home.md` entry point and `_Sidebar.md` navigation. The pages are in English. No remote Wiki is created or updated by the archive.

> **GitHub behavior:** A GitHub Wiki is a **separate Git repository**, typically available at `https://github.com/OWNER/REPOSITORY.wiki.git`. Pushing `wiki/` into the main repository does **not** automatically publish it as the website's Wiki.

## Manual publishing procedure

1. On the desired GitHub repository, open **Settings** and make sure Wikis are enabled where the feature is supported. Open the **Wiki** tab; create an initial Home page there if GitHub requires one before cloning.
2. Clone that repository's Wiki (replace placeholders with the real owner/repository):

   ```bash
   git clone https://github.com/OWNER/REPOSITORY.wiki.git arketype-wiki
   ```

3. Copy the contents of Arketype's `wiki/` folder into your local `arketype-wiki/` clone. Keep the page names as supplied, including `Home.md` and `_Sidebar.md`; review any existing pages before replacing them.
4. Review changes and commit **inside the Wiki clone**:

   ```bash
   cd arketype-wiki
   git status
   git add .
   git commit -m "Document Arketype library and visual archetypes"
   git push
   ```

5. Reload the GitHub Wiki to confirm page navigation and content. If your organization restricts Wiki permissions or the Wiki URL is not available, use GitHub's web interface or consult the repository settings.

## Staying in sync

Treat these source pages as the maintained documentation. GitHub does not sync them back automatically. After changing the main Arketype library, update the source Wiki pages, compare the Wiki clone with those files, and publish only after review. Do not put confidential data in public Wiki pages.

**Important:** The logo is intentionally **not embedded in the main README**. It is used in the project's visual interfaces (offline HTML catalogue and optional desktop window), where it belongs.
