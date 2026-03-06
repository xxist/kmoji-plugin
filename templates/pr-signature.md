# KMOJI — PR & Commit Signatures

When creating pull requests or commit messages, generate a kaomoji signature using:

```bash
python "KMOJI_GENERATOR_PATH" happy 1
```

## Pull Requests

Add a kaomoji to the end of PR descriptions, before the Co-Authored-By line:

```
## Summary
- Added new feature X

## Test plan
- [x] Unit tests pass
- [x] Manual testing complete

---
⪕╭ˆ◕ᗜ◕ˆ╮⪖ 
```

## Commit Messages

Optionally include a kaomoji at the end of commit message body (not the subject line):

```
feat: add user authentication

Implemented OAuth2 flow with token refresh.
⩽╭ˆ◕ᗢ◕ˆ╮⩾
```
