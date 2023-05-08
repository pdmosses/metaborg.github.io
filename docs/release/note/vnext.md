# Spoofax vNext

These are the release notes for the upcoming version of Spoofax.

See the corresponding [migration guide](../migrate/vnext.md) for migrating from Spoofax vPrev to Spoofax vNext.

## Added

### Statix

- Add new primitives for term index handling
  - `SG_index_more_ast`: Add indices to terms without index
  - `SG_get_max_ast_index`: retrieve largest index in AST
  - `SG_reindex_ast`: Give all nodes a fresh index. Also returns map of old index to new index.

## Changes

The following dependencies were updated:
- `com.google.guava:guava`: 26.0 -> 31.1
- `com.google.guava:failureaccess`: -> 1.0.1. Added because guava needs it.

## Fixes

### 32-bit binary support

- Remove `sdf2table` and `implodePT` dependencies on CoreUtils.
- Print `sdf2table` and `implodePT` output to `/tmp/sdf2table.log` and `/tmp/implodePT.log` respectively.

### Stratego

- Lowered memory usage by interning fewer strings.

### Stratego 2

- Improved performance of clean build by reusing more work between compilation and analysis in the editor.
- Removed support for importing RTree and Stratego 1 files from Stratego 2.

### Statix

- Fix bug where failing AST property constraints would emit messages if there was a custom message in the causation chain.
