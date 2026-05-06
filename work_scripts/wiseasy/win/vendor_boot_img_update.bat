scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/vendor_boot.img .
adb wait-for-device
adb reboot bootloader
fastboot flash vendor_boot_a vendor_boot.img
fastboot reboot
