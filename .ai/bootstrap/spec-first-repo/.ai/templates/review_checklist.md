# Review Checklist

## Spec alignment
- [ ] Behavior matches spec exactly
- [ ] Any spec changes were made explicitly (not implicit drift)

## Correctness
- [ ] Handles edge cases
- [ ] Error handling is explicit and reasonable
- [ ] No silent failures

## Tests
- [ ] New behavior has tests
- [ ] Tests are deterministic
- [ ] Tests cover acceptance criteria

## Maintainability
- [ ] Code is simple and readable
- [ ] Functions/classes have clear responsibilities
- [ ] Naming is clear and consistent

## Security
- [ ] Security considerations in the spec were reviewed
- [ ] Unclear security impact was surfaced explicitly as a blocker
- [ ] No unsafe eval/exec
- [ ] Auth/authz changes are correct and least-privilege aware
- [ ] Secrets are not exposed in code, logs, or config changes
- [ ] File operations are safe (path traversal considered)
- [ ] Network and external service changes are constrained and intentional
- [ ] Dependency changes do not introduce obvious avoidable risk
- [ ] External input validated/sanitized where needed

## Tooling / quality
- [ ] Lint passes
- [ ] CI passes
