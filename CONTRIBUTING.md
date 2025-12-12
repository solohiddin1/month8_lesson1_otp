# Contributing Guidelines

Thank you for your interest in contributing to this project! To maintain code quality and project stability, please follow these guidelines.

## Branching Strategy

**⚠️ IMPORTANT: Direct commits to the `main` branch are NOT allowed.**

All changes must be made through feature branches and pull requests.

### Workflow

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   
   Branch naming conventions:
   - `feature/` - for new features (e.g., `feature/add-user-profile`)
   - `bugfix/` - for bug fixes (e.g., `bugfix/fix-login-issue`)
   - `hotfix/` - for urgent production fixes
   - `docs/` - for documentation updates

2. **Make your changes** on the feature branch:
   ```bash
   # Make your code changes
   git add .
   git commit -m "Descriptive commit message"
   ```

3. **Push your branch** to the remote repository:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** (PR):
   - Go to the repository on GitHub
   - Click "Compare & pull request"
   - Provide a clear description of your changes
   - Request review from maintainers
   - Wait for approval before merging

5. **After PR is approved and merged**:
   ```bash
   # Switch back to main and update
   git checkout main
   git pull origin main
   
   # Delete your local feature branch (optional)
   git branch -d feature/your-feature-name
   ```

## Code Quality

Before submitting a PR, ensure:

- Your code follows the existing project structure
- All tests pass (if applicable)
- Your code is properly formatted
- You've tested your changes locally

## Commit Messages

Write clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Provide additional context in the body if needed

Example:
```
Add email verification for new users

- Implement OTP generation
- Send verification email
- Add verification endpoint
```

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.
