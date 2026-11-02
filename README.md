# CuriousTogether project page and release

This folder is the complete GitHub upload for **CuriousTogether: Implications of Curiosity and Cultural Grounding in Multi-Agent LLM Interactions**.

It contains:

- a static, responsive project page at `index.html`;
- the paper under `assets/`;
- cleaned code under `code/`;
- curated data and result summaries under `data/`;
- a downloadable code/data archive generated from those release folders.

The website is intentionally non-anonymous. The code and data subfolders omit author identities, emails, affiliations, local machine paths, cluster accounts, and original Git history.

## Publish under the LIT EECS site

All links are relative, so the folder can be placed directly inside the repository that serves `lit.eecs.umich.edu`.

1. Rename this folder to the desired public path, for example `curioustogether`.
2. Copy the folder into the root of the LIT GitHub Pages repository.
3. Commit and push it to the branch used by GitHub Pages.
4. Visit `https://lit.eecs.umich.edu/curioustogether/`.

Do not add a `CNAME` file inside this subfolder; the parent Pages repository already owns the custom domain.

For a standalone GitHub repository, enable Pages from the repository root. Its default URL will be the organization’s GitHub Pages project URL unless the LIT domain maintainers map a custom path.

## Local preview

From this directory:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Stop the server with `Ctrl-C`.

## Validate code and data

Use Python 3.10 or newer:

```bash
python3 -m unittest discover -s code/tests -v
python3 code/scripts/check_anonymity.py code
python3 code/scripts/check_anonymity.py data
```

The paper and website contain author information by design and are outside the anonymous scanner’s scope.
