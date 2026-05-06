scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/vendor/bin/hw/android.hardware.health-service.qti .

adb wait-for-device
adb root
adb remount

adb push android.hardware.health-service.qti /vendor/bin/hw/android.hardware.health-service.qti
adb reboot
