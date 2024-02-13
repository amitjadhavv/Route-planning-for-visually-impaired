In the initiative entitled "Road Scene Understanding for the Visually Impaired", our research team is meticulously advancing the development of the Sidewalk Environment Detection System for Assistive NavigaTION (hereinafter referred to as SENSATION). The primary objective of this venture is to enhance the mobility capabilities of blind or visually impaired persons (BVIPs) by ensuring safer and more efficient navigation on pedestrian pathways.
For the implementation phase, a specialized apparatus has been engineered: a chest-mounted bag equipped with an NVIDIA Jetson Nano, serving as the core computational unit. This device integrates a plethora of sensors including, but not limited to, tactile feedback mechanisms (vibration motors) for direction indication, optical sensors (webcam) for environmental data acquisition, wireless communication modules (Wi-Fi antenna) for internet connectivity, and geospatial positioning units (GPS sensors) for real-time location tracking.
Despite the promising preliminary design of the prototype, several technical challenges persist that warrant investigation.
The "Road Scene Understanding for the Visually Impaired" initiative is actively seeking student collaborators to refine the Jetson Nano-fueled SENSATION system. Through the combination of GPS systems and cutting-edge image segmentation techniques refined for sidewalk recognition, participating teams are expected to architect an application tailored to aid BVIPs in traversing urban landscapes, seamlessly guiding them from a designated starting point to a predetermined destination.
The developmental framework for this endeavor is based on the Python programming language; hence, prior experience with Python will be an advantage.
For the purposes of real-world testing and calibration, the navigation part will start at the main train station in Erlangen and end at the University Library of Erlangen-Nuremberg (Schuhstrasse 1a).
Technical milestones that must be completed in this project include:
Algorithmic generation of navigational pathways in Python, depending on defined start and endpoint parameters.
Real-time geospatial tracking to determine the immediate coordinates of the BVIP.
Optical recording of the current coordinates and subsequent algorithmic evaluation to check the orientation of the sidewalk.
Useful links for this project:
1. Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation, https://link.springer.com/chapter/10.1007/978-3-030-01234-2_49
2. How to connect an USB GPS receiver with a Linux computer?, https://gpswebshop.com/blogs/tech-support-by-os-linux/how-to-connect-an-usb-gps-receiver-with-a-linux-computer
3. Open Streetmap, https://www.openstreetmap.de/
4. GeoPy documentation, https://geopy.readthedocs.io/en/stable/
5. Efficient Localisation Using Images and OpenStreetMaps, http://www.ipb.uni-bonn.de/pdfs/zhou2021iros.pdf
6. A Practical Guide to an Open-Source Map-Matching Approach for Big GPS Data, https://link.springer.com/article/10.1007/s42979-022-01340-5
7. VALHALLA Map Matching service API reference, https://valhalla.github.io/valhalla/api/map-matching/api-reference/
8. L2MM: Learning to Map Matching with Deep Models for Low-Quality GPS Trajectory Data, https://dl.acm.org/doi/10.1145/3550486

### To install required libraries:
#### for linux:
1. sudo apt-get install imagemagic
2. pip install -r requirements.txt
3. sudo apt-get install libmagick++-dev
4. (1)sudo vim /etc/ImageMagick-6/policy.xml  and  comment the policy.xml by change from \<policy domain="path" rights="none" pattern="@*" /> to \<!--\<policy domain="path" rights="none" pattern="@*" /> -->  
    notice: there are two lines you need to comment.  
   or  
   (2)sudo mv policy.xml /etc/ImageMagick-6/policy.xml

#### for macOS:
1. brew install imagemagick
2. pip install -r requirements.txt


#### for windows:
1. install imagemagic. check <https://zulko.github.io/moviepy/install.html>
2. pip install -r requirements.txt

### To run the generate_video_walk file:
python3 generate_video_walk.py files/walking_video.mp4 edited_video.mp4

### Edited Video Link:
https://faubox.rrze.uni-erlangen.de/getlink/fi2XDxAas5pd8tdh3Dvo8V/edited_video.mp4

### link to trained weights:
https://faubox.rrze.uni-erlangen.de/getlink/fi5c3Djey6vDFuYs4AQZGi/deeplab_model.pth

### to run train.py file:
```
python3 train.py path/to/training/images path/to/training/labels path/to/validation/images path/to/validation/labels

```
### to run training_pipeline.py file:
```
python3 training_pipeline.py path/to/training/images path/to/training/labels path/to/validation/images path/to/validation/labels path/to/deeplab_model

```

### to run inference.py file:
```
python3 inference.py path/to/test/images path/to/test/ground/truth/labels path/to/model/output /path/to/deeplab_model

```
### to run convert_masks_to_grayscale.py file:
```
python3 convert_masks_to_grayscale.py /path/to/config.json /path/to/training/labels /path/to/output/training/labels path/to/validation/labels /path/to/output/validation/labels /path/to/testing/labels /path/output/testing/labels
```
