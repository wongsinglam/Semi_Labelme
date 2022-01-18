import json
from mmdet.apis import init_detector, inference_detector
import os
import numpy as np
from imantics import Mask
import mmcv
import torch


# Configs
class_names = ['shoulder', 'elbow', 'ur10', 'person']
config_file = '/home/shenglin/Projects/new_detect/mmdetection/work_dirs/faster_robot/faster_robot.py'
checkpoint_file = '/home/shenglin/Projects/new_detect/mmdetection/hpc_epoch_12.pth'
detect_type = "bbox"
model = init_detector(config_file, checkpoint_file, device='cuda:0')

def annotat(dirs):
    for dir in dirs:
        for imgfile in os.listdir(dir):
            if "json" in imgfile:
                continue

            Image_Annot = dict({
                "version": "0.1.0",
                "flags": {},
                "shapes":[],
                "imagePath": None,
                "imageData": None,
                "imageHeight": None,
                "imageWidth": None}
            )


            img_fullName = os.path.join(dir, imgfile)
            result = inference_detector(model, img_fullName)
            if isinstance(result, tuple):
                bbox_result, segm_result = result
                if isinstance(segm_result, tuple):
                    segm_result = segm_result[0]  # ms rcnn
            else:
                bbox_result, segm_result = result, None

            bboxes = np.vstack(bbox_result)
            det_labels = [
                np.full(bbox.shape[0], i, dtype=np.int32)
                for i, bbox in enumerate(bbox_result)
            ]
            det_labels = np.concatenate(det_labels)

            # draw segmentation masks
            segms = None
            if segm_result is not None and len(det_labels) > 0:  # non empty
                segms = mmcv.concat_list(segm_result)
                if isinstance(segms[0], torch.Tensor):
                    segms = torch.stack(segms, dim=0).detach().cpu().numpy()
                else:
                    segms = np.stack(segms, axis=0)

            score_thr = 0.3
            if score_thr > 0:
                assert bboxes.shape[1] == 5
                scores = bboxes[:, -1]
                inds = scores > score_thr
                bboxes = bboxes[inds, :]
                det_labels = det_labels[inds]
                if segms is not None:
                    segms = segms[inds, ...]  
            
            for i, (bbox, det_label) in enumerate(zip(bboxes, det_labels)):
                
                Annot = dict({
                    "label": None, 
                    "points": [],
                    "group_id": None,
                    "shape_type": None, 
                    "flags": {}
                })

                Annot['label'] = class_names[det_label]
                if detect_type == "bbox":
                    Annot['points'] = [[bbox[0].tolist(), bbox[1].tolist()], [bbox[2].tolist(), bbox[3].tolist()]]
                    Annot['shape_type'] = "rectangle"
                else:
                    mask = segms[i].astype(bool)
                    polygons = Mask(mask).polygons()
                    Annot['points'] = [[poly.tolist()] for poly in polygons.points[0]] 
                    Annot['shape_type'] = "polygon"
                Annot['group_id'] = None
                if not Annot['points']:
                # skip point-empty shape
                    continue
                Image_Annot['shapes'].append(Annot)
            Image_Annot['imagePath'] = imgfile
            img = mmcv.imread(img_fullName)
            Image_Annot['imageHeight'] = img.shape[0]
            Image_Annot['imageWidth'] = img.shape[1]
            print(Image_Annot['imagePath'])
            json_str = json.dumps(Image_Annot, indent=4)
            with open(dir+'{}.json'.format(imgfile.split('.')[0]), 'w') as json_file:
                json_file.write(json_str)



if __name__ == "__main__":

    # images folders
    list1 = '/home/shenglin/newdata/1/'
    list2 = '/home/shenglin/newdata/2/'
    list3 = '/home/shenglin/newdata/3/'
    list4 = '/home/shenglin/newdata/4/'

    dirs = [list1, list2, list3, list4]    
    annotat(dirs)
        