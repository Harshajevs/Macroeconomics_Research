# Repository release — 25 November 2026

This release combines the completed research checkpoint with the final HS455 report and the earlier report versions. It introduces a current root README, a repository index and build-product exclusions. The research source, data, results and existing provenance records are preserved; the former root README is retained at `documentation/archive/pre_report_README.md`.

The 73 files in `report/` match the delivered final report package byte-for-byte. The report is 13 pages including its cover and appendices, with 3,970 main-text words under the documented count scope. No scientific model, calculation, figure data, report wording or conclusion was changed for publication.

## Checks run from the repository copy

- `python -m unittest discover -s stage7/tests -v`: all 14 tests passed.
- Each of the nine `tests/test_*.py` programs: passed.
- `tectonic --keep-logs --keep-intermediates report.tex` from `report/`: compiled successfully.
- `python verify_report.py` from `report/`: all 213 checks passed.
- Final report package compared with the delivered version: identical.
- Project text scanned for common GitHub/OpenAI/AWS credential patterns and private-key headers: no matches.

The archived high-draw bootstrap and simulation results are included. They were not recomputed during repository publication; the full reproduction command is documented in the root README.

## Snapshot boundaries

Virtual environments, bytecode, compilation products, temporary renders, unrelated assignment/style examples, private chat-context attachments and the cancelled presentation work are excluded. Earlier checkpoint manifests remain historical records of their original packages and may refer to those private context attachments or the former root README. `PROJECT_FILES.sha256` describes this repository release instead.

Source publications retain the attribution recorded in the source register and report references. Commit authorship for this upload is K Harshavardhan; the report's existing academic team information is preserved.
