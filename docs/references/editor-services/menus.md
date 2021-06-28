# Action Menus
Menus are used to bind actions of your language, such as transformations, to a menu in the IDE. Menus are defined using the `menu` keyword under a `menus` section in an [ESV file](esv.md), and can themselves contain submenus, actions, and separators.

```esv
menu : $String $MenuOptions
  $MenuContribs
```


## Menu Contributions
A menu has zero or more `$MenuContrib`, which are: `action`, `submenu`, or `separator`.

### Actions
_Actions_ (sometimes called _builders_) are defined under a menu or submenu with syntax:

```esv
action : $String = $StrategoCall $MenuOptions
```

### Submenus
_Submenus_ allow grouping of actions in nested menus. Their syntax is:

```esv
submenu : $String $MenuOptions
  $MenuContribs
end
```

### Separators
_Separators_ allow inserting a separator in a menu list using the syntax:
```esv
separator
```


## Menu Options
The menu options specify the behavior of the menu item. The following modifiers are supported:

| Modifier       | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `(source)`     | Action is performed on the parsed AST instead of the default analyzed AST. |
| `(openeditor)` | The result should be opened in a new editor.                               |
| `(realtime)`   |                                                                            |
| `(meta)`       |                                                                            |


## Example
An example menu:

```esv
menus

  menu: "Generate"
    action: "To normal form" = to-normal-form (source)
    submenu: "To Java"
      action: "Abstract" = to-java-abstract (openeditor)
      action: "Concrete" = to-java-concrete
    end
```