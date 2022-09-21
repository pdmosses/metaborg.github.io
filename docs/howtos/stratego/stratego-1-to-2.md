# Migrating from Stratego 1 to Stratego 2

??? tip "Stratego 2 is somewhat unstable"
    Stratego 2 is quite new and has a lot of exciting new things going for it. But it _is_ therefore also more unstable, with errors popping up somewhat regularly. Your project build may break or your code may behave in unexpected ways. Of course you can [file bug reports](https://github.com/metaborg/stratego/issues).

Stratego 2 is the new version of Stratego that provides access to the incremental compiler and gradual type system that were developed for Stratego. Stratego 2 is accessible separately because it is organised quite differently from Stratego 1 and it provides a clear distinction and documentable upgrade path. This is that documented upgrade path. This How-To will guide you through the changes you need to make in your Spoofax project in order to use Stratego 2.

1. Make sure you run the development version of Spoofax. This step will become obsolete in the future but currently Stratego 2 development is moving quickly and fixing bugs every week. 
2. In your `metaborg.yaml` file:
    1. Add a compile dependency (`dependencies.compile`) on `org.metaborg:stratego.lang:${metaborgVersion}` (the Stratego 2 language)
    2. Add a source dependency on `org.metaborg:strategolib:${metaborgVersion}` (the Stratego 2 version of strategolib, the standard library)
    3. Remove from `language.stratego.args` the `-la` and `stratego-lib` lines (2 lines, leave the other `-la`)
    4. Remove `language.stratego.build` if there, it is now ignored, all compilation will be incremental
    5. Remove `language.stratego.format` if there, it is now ignored, the compilation is always to jar. _If the format option you remove is `ctree`_, also search your `.esv` files for a line `provider : target/metaborg/stratego.ctree`, likely in `editor/Main.esv`, and remove it. 
3. Rename all `.str` files in your project that are not in `src-gen` to `.str2`. Generated Stratego files in `src-gen` should already have a `.str2` version next to the `.str` version of the file.
4. Remove any imports to `libstratego-lib` or `libstrategolib` in those renamed files.
5. Add the `strategolib` import to all your `.str2` files outside of `src-gen`.
6. Add `target/replicate/str2libs` as a class directory on your Eclipse build path. Do so by right-clicking on the project, then go to `Build Path > Configure Build Path...`, select the Libraries tab, use the `Add Class Folder...` button on the right. 

??? info "Stratego versions"
    The version numbers of Stratego are a little strange, Stratego and Stratego/XT used to number up to 0.17, then did not receive any more numbered releases even though small bugfixes and changes were released through Spoofax 1 and 2. In the current documentation we now consider this post-0.17 Stratego in Spoofax to be Stratego 1. This is not necessarily a statement of stability and matureness of the language but more to distinguish it from the new Stratego 2 project.

## Imports in Stratego 2

At this point your project may be buildable again, but perhaps you are still getting errors about unresolved strategies or constructors. Stratego 2 has a stricter import policy than Stratego 1. If you use a strategy, rule or constructor, you must either define that strategy/rule/constructor in the module or import a module that defines it. Imports are no longer transitive for name resolution. 
