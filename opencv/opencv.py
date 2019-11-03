import os
import logging
import cv2
import urllib


from config import get_keyword


logger = logging.getLogger(__name__)


CASCADE_FILE = get_keyword('Cascade File')


CASCADE_FILE = os.path.join(os.path.dirname(__file__), CASCADE_FILE)
if not CASCADE_FILE:
    raise FileExistsError('{} does not exit!'.format(CASCADE_FILE))

def make_train_img(input_path, output_path):
    logger.info({
        'action': 'make_train_img',
        'input_path': input_path,
        'output_path': output_path,
        'status': 'run'
    })
    if not input_path:
        logger.error({
            'action': 'make_train_img',
            'status': 'Input path does not exist'
        })
        return

    img = cv2.imread(urllib.parse.quote(input_path))
    try:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        logger.error({
            'action': 'make_train_img',
            'input': input_path,
            'status': 'fail in cv2.cvtColor'
        })
        return
    
    cascade = cv2.CascadeClassifier(CASCADE_FILE)
    try:
        face_list = cascade.detectMultiScale(img_gray, minSize=(30, 30))
    except cv2.error:
        logger.error({
            'action': 'make_train_img',
            'input': input_path,
            'status': 'fail in detectMultiScale'
        })
        return
    
    if len(face_list) == 0:
        logger.info('No matches {}'.format(input_path))
        return
        
    x, y, w, h = face_list[0]
    img = img[y: y+h, x: x+w]
        
    cv2.imwrite(output_path, img)


def make_train_path(keyword, index):
    """ Return file name ('images/train/<keyword>/<keyword>_<index>') """
    new_images_path = 'images/train/{}'.format(keyword)
    os.makedirs(new_images_path, exist_ok=True)
    return '{0}/{1}_{2}.jpg'.format(new_images_path, keyword, index)