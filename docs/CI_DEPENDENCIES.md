# CI dependency record

GitHub Actions references were resolved through the GitHub connector on September 24, 2026 and pinned to the returned commit objects:

- actions/checkout v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`
  Source: https://api.github.com/repos/actions/checkout/git/ref/tags/v7.0.1
- actions/setup-python v7.0.0: `5fda3b95a4ea91299a34e894583c3862153e4b97`
  Source: https://api.github.com/repos/actions/setup-python/git/ref/tags/v7.0.0

The workflow uses GitHub-hosted ubuntu-latest with read-only contents permission and Python 3.10, 3.12 and 3.13 jobs. It does not install runtime dependencies. The hosted workflow was not triggered or validated in this build; inspect its actual results after publication. The local runtime/tested interpreter is reported separately in VALIDATION.md. A pinned action is not proof of secure source code or an independent supply-chain audit.
