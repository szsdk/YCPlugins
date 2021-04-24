## Generate `tldr.json` from [tldr](https://github.com/tldr-pages/tldr)

```
cd tldr
git checkout master
git pull
cd ..
./tldr2json tldr/pages --output tldr.json
```
