scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/device/qcom/bengal-kernel/dtbs/dtbo.img .
adb wait-for-device 
adb reboot bootloader
fastboot flash dtbo_a dtbo.img
fastboot reboot
