# Vendor Update

1. Fetch upstream into `.pipeline/upstream`.
2. Review license, diff, source path, and selected skill scope.
3. Copy only approved skill directories into `.pipeline/vendor`.
4. Update `SOURCE.yaml`.
5. Run `.pipeline/scripts/verify.ps1`.

Excluded skills must not appear in `.agents/skills`.
