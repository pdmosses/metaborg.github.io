# Pipelines for Interactive Environments
Pipelines for interactive Environments (PIE) is the build system for Spoofax 3.
PIE consists of two parts: a Java framework, a Java runtime and the PIE Domain Specific Language (DSL).
This reference documentation is for the PIE DSL and will only provide some high level information about the framework and runtime to provide context.

PIE uses tasks to compose pipelines.
Each task has 0 or more inputs and one output.
Each task can depend on files or on other tasks.
Tasks can be marked as explicitly observed to indicate that we want the output of these tasks to stay up to date.
The PIE runtime executes tasks incrementally, which means that it only executes tasks that are no longer up to date and that are required for a task which is explicitly observed.

Tasks can be written in Java, but this involves a lot of boilerplate.
Tasks can also be written in the PIE DSL.
The PIE DSL is specifically made for PIE, so it has little boilerplate.
Tasks written in the PIE DSL are compiled to Java.


## The PIE DSL

PIE models a pipeline as tasks that call each other.
The PIE DSL calls these tasks "functions", because each task has inputs and an output.
A PIE DSL program consists of one or more files.


### File structure

```
module fully:qualified:moduleName

import fully:qualified:name:of:another:module
import org:example:multipleDefs:{func1, func2 as other, aDataTypeAsWell}
import org:example:languages:{java, cpp, sql}:spoofax:{parse, analyze, compile}

data coolDataType = foreign java org.example.MyFirstJavaClass {
    func aMethod(int) -> bool
}

func greetWorld() -> string = "Hello world!"
```

PIE DSL files contain a module statement, imports, and data and function definitions.
The module statement declares the fully qualified name of the module.
Imports are optional and import datatypes and function from other modules.
They can import multiple functions or datatypes at the same time, and they can rename elements.
Data and function definitions define functions and datatypes.


### Directory structure and module system

PIE files have the extension `.pie`.
Each PIE file forms a module.
Modules can define functions and datatypes, and can import functions and datatypes from other modules.
It is recommended to use the same name for the module as the path and filename, but this is not required.
As such, the PIE DSL does not place any restrictions on paths and file names besides the standard restrictions for Spoofax languages. 
The module system is described in [Modules](modules/).


### Types and data definitions

The PIE DSL is a statically typed language.
There are a few built-in types, such as `int` and `path`.
Built-in types use lowercase characters.
Custom datatypes can currently only be imported from Java as foreign definitions.
The types in the PIE DSL are described in [Types](types/).
The PIE DSL also supports generic datatypes.
These follow Java semantics.
The semantics of generics can be found in [Generics](generics/).


### Function definitions

Functions express task definitions.
Functions consist of a head and an implementation.

```
func $FuncHead = $FuncImpl

func greet(name: string) -> string = "Hello ${name}!"
func doSomethingDifficult() -> path = foreign org.example.DoSomethingDifficult
func callJavaStaticFunction() -> bool =
  foreign java fully.qualified.java.ClassName#staticMethodName
func createCustomType() -> CustomType =
  foreign java constructor org.example.CustomType
```

The function head describes the signature of the function: the name, the input parameter types and the output type.
All functions can be called the same way regardless of their implementation.
The function implementation describes the way a function is implemented.
A function can be implemented in PIE by providing an expression, as can be seen with `greet`
Expressions are described in [Expressions](expressions/).
A function can also be implemented in Java.
The three ways this can be done are shown in the example as well.
A complete overview of functions is given in [Functions](functions/).


### Misc information.

Java and C use the function called `main` with a certain signature as the entry point to the program.
A PIE program does not have a set entry point.
The entry point is whatever function is called from the PIE runtime.
