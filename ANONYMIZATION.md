# Code and data anonymization record

The public project page names the authors and institutions. The `code/` and `data/` release content was separately cleaned so it can be reviewed without local machine or contributor identifiers.

Removed from code and data:

- author names, emails, affiliations, acknowledgments, and funding text;
- absolute home, scratch, GPFS, NFS, and cache paths;
- scheduler accounts, logs, and machine-specific launch files;
- original repository history and remotes;
- annotator names and free-form annotator metadata;
- caches, compiled Python files, model weights, and adapters.

Included:

- task adapters and the shared multi-agent interaction protocol;
- synthetic schema examples;
- public model identifiers and task names;
- aggregate paper results and statistical summaries;
- tests and an automated path/identity scanner.

Large generated-output directories from the working tree are not included because they exceed normal GitHub limits and contain legacy caches and paths. They should be released separately after licensing and privacy review.
