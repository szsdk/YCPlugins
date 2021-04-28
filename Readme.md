# YesCommander Plugins

This is the package consists of several `Commander`s used for [`YesCommander`](https://github.com/szsdk/YesCommander)

## Calculator (`yc_calculator`)

## Color converter (`yc_color_converter`)

## Covid information (`yc_covid`)

## Currency converter (`yc_currency`)

## Googler (`yc_googler`)
### Dependency
[Googler](https://github.com/jarun/googler)

## Search (`yc_search`)
```python
google = SearchSoldier("https://www.google.com/search?q=%s", "Google", score=10)
google.marker = " "
```

## TeXDoc (`yc_texdoc`)

Search documentations of texlive.

The leading keyword, `td`, is mandatory.
Example keywords: `td ctex`

### Dependency
[rapidfuzz](https://github.com/maxbachmann/RapidFuzz)

## Fuzzy searching json file (`yc_json`)
A json file converted from TLDR project, `tldr.json` is in the folder `cheat_sheet`.

```python
JsonCmdCommander(config_folder / "YCPlugins" / "cheat_sheet" / "tldr.json", num_candidates=20)
```

### Dependency
[rapidfuzz](https://github.com/maxbachmann/RapidFuzz)
