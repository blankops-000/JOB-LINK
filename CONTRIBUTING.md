# Contributing to JobLink

## Gitflow Workflow

### Branch Structure
- `master` - Production-ready code
- `dev` - Integration branch for features
- `feature/*` - New features (branch from dev)
- `hotfix/*` - Critical fixes (branch from master)

### Workflow Steps

1. **Feature Development**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   # Make changes
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Target: `dev` branch
   - Require 1 reviewer approval
   - All CI checks must pass

3. **Release Process**
   ```bash
   git checkout master
   git merge dev
   git tag v1.0.0
   git push origin master --tags
   ```

## Code Standards
- Use meaningful commit messages
- Write tests for new features
- Follow existing code style
- Update documentation as needed