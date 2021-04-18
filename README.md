# suruiha
Workspace oluşturmak için:
```
mkdir -p ~/bosphorusuav/src
cd ~/bosphorusuav
catkin_make
source devel/setup.bash
cd ~/bosphorusuav/src
git clone https://github.com/BosphorusUAV/suruiha
cd ~/bosphorusuav
catkin_make
. ~/bosphorusuav/devel/setup.bash
```
Çalıştırmak için (5 iha kalkış ve iniş yapacak)
```
roslaunch sample_package sample_launch.launch
```

location.py konumu öğrenir.
speed.py ihanın pervane hızını ayarlar.