# herdr-plugins

Plugins for [Herdr](https://herdr.dev), one per folder.

## pane-equalize

![Three uneven columns snap to equal widths, then three uneven stacked panes snap to equal heights](pane-equalize/demo.gif)

Gives the panes in the current tab equal space. Panes side by side share it equally; a nested group split the other way counts as one pane among them and is equalized on its own. Needs `python3`.

```sh
herdr plugin install filipecsweb/herdr-plugins/pane-equalize
```

Bind it to a key in Herdr's `config.toml`:

```toml
[[keys.command]]
key = "prefix+="
type = "plugin_action"
command = "filipecsweb.pane-equalize.equalize"
```
