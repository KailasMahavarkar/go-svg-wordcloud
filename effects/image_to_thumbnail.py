import os
import pathlib

from PIL import Image


def convert_unit(size_in_bytes, unit):
    if unit == 'KB':
        return format(float(size_in_bytes / 1024), '.2f')
    elif unit == 'MB':
        return format(float(size_in_bytes / (1024 * 1024)), '.2f')
    elif unit == 'GB':
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_file_size(file_name, size_type='KB'):
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)


# @return none | makeImage(data/gig_id/[imagefiles])
def makeImage(path, gig_id) -> None:
    """
    return: None
    Note: save image in thumbnail, preview, main quality
    """
    stem = pathlib.Path(path).stem
    file = Image.open(path)
    thumbnail = {'width': 330, 'height': 220, 'quality': 76}
    preview = {'width': 660, 'height': 440, 'quality': 80}
    image = {'width': 2120, 'height': 1360, 'quality': 95}

    thumbnailFile = file.resize((thumbnail['width'], thumbnail['height']), Image.ANTIALIAS)
    previewFile = file.resize((preview['width'], preview['height']), Image.ANTIALIAS)
    imageFile = file.resize((image['width'], image['height']), Image.ANTIALIAS)

    if not os.path.isdir('Data/{}'.format(gig_id)):
        os.mkdir('Data/{}'.format(gig_id))

    thumbnailFile.save('Data/{gig_id}/{root}Thumbnail.jpg'.format(gig_id=gig_id, root=stem), quality=thumbnail['quality'], optimize=True)
    previewFile.save('Data/{gig_id}/{root}Preview.jpg'.format(gig_id=gig_id, root=stem), quality=preview['quality'], optimize=True)
    imageFile.save('Data/{gig_id}/{root}Image.jpg'.format(gig_id=gig_id, root=stem), quality=image['quality'], optimize=True)