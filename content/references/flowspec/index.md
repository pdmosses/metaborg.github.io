---
title: "FlowSpec"
---
# FlowSpec — Data Flow

Programs that are syntactically well-formed are not necessarily valid programs. Programming languages typically impose additional context-sensitive requirements on programs that cannot be captured in a syntax definition. Languages use data and control flow to check certain extra properties that fall outside of names and type systems. The FlowSpec ‘Flow Analysis Specification Language’ supports the specification of rules to define the static control flow of a language, and data flow analysis over that control flow. FlowSpec supports flow-sensitive intra-procedural data flow analysis.

<!--[:material-message-question: How-tos](../../howtos/){ .md-button }-->
[:material-file-cog: Reference](../../references/flowspec/index.md){ .md-button }
[:material-source-branch: Sources](#sources){ .md-button }


## Control Flow Graphs

Control-flow represents the execution order of a program. Depending on the input given to the program, or other things the program may observe of its execution environment (e.g. network communication, or a source of noise used to generate pseudo-random numbers), a program may execute a different trace of instructions. Since in general programs may not terminate at all, and humans are not very adapt at reasoning about possible infinities, we use a finite representation of possibly infinite program traces using control-flow graphs.

Control-flow graphs are similarly finite as program text and are usually very similar, giving rise to a visual representation of the program. Loops in the program are represented as cycles in the control-flow graph, conditional code is represented by a split in control-flow which is merged again automatically after the conditional code.

## Data Flow Analysis over Control Flow Graphs

Data-flow analysis propagates information either forward or backward along the control-flow graph. This can be information that approximates the data that is handled by the program, or the way in which the program interacts with memory, or something else altogether.

Examples of data-flow analysis include constant analysis which checks when variables that are used in the program are guaranteed to have the same value regardless of the execution circumstances of the program, or live variables analysis which identifies if values in variables are actually observable by the program.



## Sources
The sources of FlowSpec can be found at:

- [metaborg/flowspec :material-source-branch: flowspec.lang](https://github.com/metaborg/flowspec/tree/master/flowspec.lang): FlowSpec language specification
