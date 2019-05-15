
![AddThemes.py](https://user-images.githubusercontent.com/8409189/57814420-e3e6aa00-7773-11e9-8731-17035c9d1bce.png)


# CmderAddThemes

Add some flare to you command prompt.
This is a simple python script for installing/adding multiple (or just one) .xml themes to your ConEmu.xml

It will also create a backup in the same directory as the ConEmu config. Previous backups do not replace each other, they just increment. If you don't want one you can use the `-s` or `--skip-backup` flag.

### Prerequisites
```
Python 3.6 or higher
```

### Basic Usage

```
python AddThemes.py [-v, --verbose] [-s, --skip-backup] [-h, --help] [themesDir] [conEmuConfigDir]
```


### Recommended Usage

1. Plonk the badboy down in your cmder config directory (cmder\config)
2. Create folder called "themes", put your .xml theme files in there
3. Run script - It will by default:

   Look for themes in `/themes`  
   and look in `../vendor/conemu-maximus5/` for the `ConEmu.xml` config file

   Example
   ```
   python Path/To/File/AddThemes.py
   ```

### Issues

* No duplication checking, if you run it multiple times with the same themes they will still be installed.

* XML formatting is subpar, the theme's xml keys start and end on the same line

* If you want to change the config dir you have to provide a theme directory, I'll fix it later. Probably. Maybe.

### Possible Improvements

* All of the above

* Maybe prettier colored printing