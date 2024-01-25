
# Features
- Browse through directory tree
- Type a shot to access directly
- Type a new shot. It'll create it using predifined folder structure
- Preview 3D folder content and PSD folder. CLick to preview picture
- PSD preview create jpg from each PSD / PSB
- Double click to open 3D file or PSD file
- Buttons for favorite folders.



<img src="data/GUI.JPG" width="600" >


# Quick start
## Browse folders
You can browse manually in the directory tree.
You can directly type the desired shot.
If the shot doesn't exist, it'll create the shot using predifined folder structure.
Click on file for image preview, or double click to open.

<img src="data/open_list.gif" width="600" >

<img src="data/open_type.gif" width="600" >


# Custom directories 
Link to favorite folders.

You can add your own folder in the Custom list by amending this dictionary.

<img src="data/Custom_dir.JPG" width="250" >

<!-- Code -->
```python 
# CUSTOM DIRECTORY
self.dir_special = {
    "References": Path(r"C:\_YannB\_WORK\11_UNTOLD\_REF"),
    "Textures": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
}
```


Edit your template for new shot.
<!-- Code -->
```python 
    def create_template_folder(self):
        """
        Template for new shot
        """
        self.shot_dir.joinpath("3D/scenes").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/data").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/textures").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/assets").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/imagePlane").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("PSD").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("REF").mkdir(parents=True, exist_ok=True)
```

# Installation

Install all depedencies using pip

```bash
  pip install -r requirements.txt
```



