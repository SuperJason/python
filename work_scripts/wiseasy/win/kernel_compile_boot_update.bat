ssh fuzhongxin@10.30.0.52 "cd /home/workspace_sda/fuzhongxin/sm6115 && time . build_wiseasy.sh --kernel 2>&1 | tee build__kernel__log_remote.txt"
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/sm6115/QSSI13/out/msm-kernel-bengal-consolidate/dist/boot.img .
adb reboot bootloader
fastboot flash boot_a boot.img
fastboot reboot
