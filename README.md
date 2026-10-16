# CRH06: Security Controls Developers Won't Fight

A runnable PR feedback exercise with a real file-pattern check and **synthetic**
dependency/static-analysis findings. There is no live credential, real vulnerable
package, CVE claim, or third-party security scanner.

## Demo 1: experience the broken gate

```sh
python3 -m unittest discover -s tests -v
python3 lab.py --mode before --enforce
```

The second command deliberately exits 1: all three fixture findings block.
For a GitHub run, dispatch **Synthetic PR security feedback**, `mode=before`.
Open its file/line annotations. Discuss missing prioritization and ownership.

## Demo 2: redesign the same change

```sh
python3 lab.py --mode after --enforce
python3 lab.py --mode after --fixed --enforce
```

The first remains red: the literal marker still needs removal. The second passes
while retaining one warning and one owned, approved, expiring dependency exception.
The repaired file resolves a secret ARN reference instead of storing a literal.
No report prints the marker itself. A real exposed credential would need rotation.

`exceptions.json` expires on November 21, 2026, after the conference. Expiry is
validated on every run. To rehearse later, explicitly create a new approved expiry;
do not disable expiry checking. Use `--date 2026-11-19` only for an openly labeled
historical replay, never as a way to bypass a real policy decision.

## Stage the pull request

The prepared `demo/broken-gate` branch introduces the nonfunctional marker into
`app/service.py`. Open a draft PR from that branch. The PR workflow scans that
actual changed file and emits an error at its file/line. Main keeps that file clean.
Run the workflow in `before` mode on the demo branch to show the noisy gate.
Switch to `after` mode to show prioritization while the marker still blocks.
The prepared `demo/repaired-gate` branch removes the marker from the same file.
Apply that fix to the draft PR to show a green rerun with the exception retained.

For local verification of the current application file, run:
`python3 lab.py --mode after --source app/service.py --enforce`.
`--fixed` selects the separate fixture used for offline screenshots and unit tests;
it does not claim to repair a PR. Replacing the marker in the PR's actual source
is what changes that PR's policy result.

## Reset

The default fixtures stay unchanged by all commands. Rerun with `before`, then
`after`, then `after --fixed`. Close demo PRs only when no longer needed. Test
exception expiry with `--date 2026-11-22` and show the dependency blocks again.

See [SOURCES.md](SOURCES.md) for source documentation and model limits.

## Local screenshot viewer

Run `python3 viewer.py --port 8765`, then open http://127.0.0.1:8765.
The browser shows actual local lab output with its scope clearly labeled.
It is not an AWS Console or GitHub screenshot. Stop with Ctrl+C.

## Replay the published draft PR

The live PR is https://github.com/360TrustLab/developer-security-controls/pull/1.
It remains a draft. Its main branch is clean. The broken branch keeps a small
health endpoint change alongside the synthetic marker so the repaired PR still
has a meaningful application change to review.

From a fresh authenticated clone, repair the PR without merging it:

```sh
git fetch origin
git switch demo/broken-gate
git restore --source origin/demo/repaired-gate -- app/service.py
git add app/service.py
git commit -m "Demo: use a runtime secret reference"
git push origin HEAD
```

To restage the conference's intentionally failing starting state, restore the
same file from `origin/demo/reset-fixture`, commit and push. Do not force-push or
merge the draft PR. The local workspace Git snapshots were prepared independently
of the published Git history; use a fresh clone for this remote replay.
