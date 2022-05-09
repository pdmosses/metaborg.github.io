# Spoofax vNext

These are the release notes for the upcoming version of Spoofax.

See the corresponding [migration guide](../migrate/vnext.md) for migrating from Spoofax vPrev to Spoofax vNext.

## Changes
- Fix issues with the `implodePT` and `sdf2table` Docker substitution scripts for MacOS 64-bit
- Update Apache Commons Compress dependency to 1.21
- Update Apache Commons IO dependency to 2.11.0
- Update Guice dependencies to 4.2.3
- Update Guava dependency to 30.1
- Add Guava FailureAccess dependency, required by Guava >= 27.0


Statix
^^^^^^

* Make `ArithTest` Serializable
* Integrate the Incremental Solver in Spoofax.
* Fix issue where edges were closed twice in incremental solver when having debug log enabled.
* Deprecate the `concurrent` property in favor of the `mode` (for language projects) or `modes` (for example projects) properties.
* Allow singleton properties to be set to the same value multiple times.
* Reduce number of cascading messages (can be disabled using `runtime.statix.suppress-cascading-errors: false`).
* Show delay reasons and prevented completions on messages for unsolved constraints.
* Add `eq(term)` lambda sugar.
* Add `runtime.statix.test-log` option to show Statix test logging in the console.
* Fix bug where solver with return-on-first-error enabled would also return if the first failing constraint had a non-error message kind.

