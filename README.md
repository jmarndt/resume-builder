# Résumé Builder
This utility lets you create your résumé data in a simple, plain text markdown document, and Python will take care of generating a PDF that's nicely formatted for you. This way, you don't have to worry about messing up page styling and formatting while trying to focus on the actual information. The markdown document is not traditionally formatted, but should be easy enough to follow the structure. Simply replace the details in the provided sample with your own! Be sure to retain the structure or the script will break.

# Installation
You will need two dependencies for this to run properly:
- [fpdf2](https://pypi.org/project/fpdf2/)
```
pip install fpdf2
```

- [markdown-to-json](https://pypi.org/project/markdown-to-json/)
```
pip install markdown-to-json
```

# Running
Simply run `python3 build_resume.py` - by default it will search the for `resume.md` in this folder, but you can optionally provide the filename as well. For example `python3 build_resume.py my_second_resume.md`.

To see what the output will look like check out the `example_résumé` PDF. The fonts, styling, etc are what I use, but you can always change this up! The default fonts (`Cabin`) are provided and located in the fonts directory.