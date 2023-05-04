# Spoofax vNext

These are the release notes for the upcoming version of Spoofax.

See the corresponding [migration guide](../migrate/vnext.md) for migrating from Spoofax vPrev to Spoofax vNext.

## Changes

### 32-bit binary support

- Remove `sdf2table` and `implodePT` dependencies on CoreUtils.
- Print `sdf2table` and `implodePT` output to `/tmp/sdf2table.log` and `/tmp/implodePT.log` respectively.

### Stratego 2

- Improved performance of clean build by reusing more work between compilation and analysis in the editor.
