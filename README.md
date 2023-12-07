### To install required libraries:
for linux:
1. sudo apt-get install imagemagic
2. pip install -r requirements.txt
3. sudo apt-get install libmagick++-dev
4. (1)sudo vim /etc/ImageMagick-6/policy.xml  and  comment the policy.xml by change from \<policy domain="path" rights="none" pattern="@*" /> to \<!--\<policy domain="path" rights="none" pattern="@*" /> -->  
    notice: there are two lines you need to comment.  
   or  
   (2)sudo mv policy.xml /etc/ImageMagick-6/policy.xml

for macOS:
1. brew install imagemagick
2. pip install -r requirements.txt


for windows:
1. install imagemagic. check <https://zulko.github.io/moviepy/install.html>
2. pip install -r requirements.txt

### To run the generate_video_walk file:
python3 generate_video_walk.py files/walking_video.mp4 edited_video.mp4
