# Project Configuration

This page describes the configuration options in a `metaborg.yaml` file of a
Spoofax project (i.e., a project that _uses_ a Spoofax language definition).

## `runtime`

### `statix`

All options under the `runtime.statix` options configure the behavior of the
[Statix](../../statix) solver in this project. The available options are:

| Option                      | Values       | Default | Description                                                                                                                          |
| :-------------------------- | :----------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------- |
| `test-log`                  | `true|false` | `false` | When set to `true`, executing an [`stxtest`](../../statix/tests) will emit detailed logging in the Eclipse Console.                  |
| `suppress-cascading-errors` | `true|false` | `true`  | When set to `true`, the solver will not emit messages for constraints that could not be solved due to other constraints failing.     |
| `message-trace-length`      | An integer   | `0`     | The number of constraints in the causation trace to print below the error message. `-1` prints the full trace.                       |
| `message-term-depth`        | An integer   | `3`     | The depth in which terms are printed inside an error message. For deeper terms, and ellipsis is printed. `-1` prints infinite terms. |

In addition, there is a `modes` parameter, which manages the solver modes in
this project. This parameter contains subnodes consisting of a language name as
key, and either `traditional` (default), `concurrent` of `incremental` as value.
This setting overrides the default solver mode set by the language definition.

The Statix segment of an configuration file can look as follows.
```yaml
runtime:
  statix:
    test-log: true
    suppress-cascading-errors: true
    message-trace-length: 4
    message-term-depth: -1
    modes:
      MyLang: concurrent
```
