# Wiki-crawler
This file finds the path from N random wiki pages to the Philosophy page

## To run
```
python wiki_path_finder.py.py
```

## Notes:

If any of the following were the first link in the main article body, I skipped over it so that I had working links:
* Anchor tags that linked to an element within the current page i.e. `<a href="#section-1">`
* Red links (to dead pages) i.e. a link that led to https://en.wikipedia.org/wiki/New_Shiloh_Baptist_Church

Discarded paths that led to pages with the following problem:
* Pages that entered a never ending loop, such as `/Internal_migration` and  `/Human_migration`
* Pages with no viable links such as https://en.wikipedia.org/wiki/Association_for_Theatre_in_Higher_Education
