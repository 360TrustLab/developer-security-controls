# Operating decisions for the pull-request gate

I want the developer to know what to do next. The security requirement still
holds: the blocking marker must be removed, and the remaining risk needs an
explicit owner. The exercise changes the decision and feedback, rather than
making every result green.

## A troublesome Pull Request

The check reads real files for a nonfunctional credential marker. The dependency
and analysis findings are synthetic. Compare the noisy and focused modes, then
repair the actual file on the PR. The separate fixed fixture is useful for local
comparison but does not edit the PR.

Ask which investigation steps help decide the risk and which merely compensate
for missing guidance. File location, a repair path, and a named decision owner
belong close to the change. A real exposed credential would also need issuer-side
revocation or rotation and verification that legitimate consumers recover.

## Who owns the next step?

Platform owns operation of the workflow. Security owns policy and escalation.
Product engineering owns remediation. Leadership accepts the business risk.
These are proposed responsibilities, not approvals granted by the fixture.
Ordinary repairs should have a route that does not depend on security approving
every engineering change.

The exception fixture checks fields and expiry. It is not a production approval
system. A production record also needs exact component scope, supporting
evidence, and a renewal decision. The example expiry is November 21, 2026.
Test the expired state instead of discovering it during a release.

## Enforcement and rollout

The demo does not configure a mandatory merge rule. In production, require the
intended check from the expected reporting application and test failure paths.
Path filtering, skipped jobs, and scanner unavailability need explicit behavior.
Give the operating owner enough context to recover a legitimate blocked change
without silently weakening the requirement.

Pilot a bounded policy with the engineers doing the repairs. Review disputed
findings and compare exposure, bypasses, exception age, and repair effort before
expanding it. The deck's numerical example is hypothetical, not measured lab
results. Azure DevOps requires its own branch-policy and reporting configuration.
