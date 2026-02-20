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
- [ ] No unsafe eval/exec
- [ ] File operations are safe (path traversal considered)
- [ ] External input validated/sanitized where needed

## Tooling / quality
- [ ] Lint passes
- [ ] CI passes