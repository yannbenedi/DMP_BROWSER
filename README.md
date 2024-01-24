<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  padding-top: 30px;
  padding-right: 30px;
  padding-bottom: 30px;
  padding-left: 30px;
}

</style>

# Features
- Browse through directory tree
- Type a shot to access directly
- Type a new shot. It'll create it using predifined folder structure
- Preview 3D folder content and PSD folder. CLick to preview picture
- PSD preview create jpg from each PSD / PSB
- Double click to open 3D file or PSD file
- Buttons for favorite folders.

# Quick start
## Browse folders
You can browse manually in the directory tree.
<img src="data/open_list.gif" width="600" class="center">
You can directly type the desired shot.
If the shot doesn't exist, it'll create the shot using predifined folder structure.
<img src="data/open_type.gif" width="600" class="center">
Click on file for image preview, or double click to open.


# Custom directories 
Link to favorite folders.

You can add your own folder in the Custom list by amending this dictionary.

<img src="data/Custom_dir.JPG" width="250" class="center">

<!-- Code -->
```python 
# CUSTOM DIRECTORY
self.dir_special = {
    "References": Path(r"C:\_YannB\_WORK\11_UNTOLD\_REF"),
    "Textures": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
}
```
<br/>


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
<br/>


# Installation

Install all depedencies using pip

```bash
  pip install -r requirements.txt
```



