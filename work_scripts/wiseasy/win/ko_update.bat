REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/power/supply/sgm41528_charger.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/obj/DLKM_OBJ/vendor/wiseasy/drivers/typec_hub/typec/tcpc/typec_hub_dlkm.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/obj/DLKM_OBJ/vendor/wiseasy/drivers/wis_sp/wis_sp_dlkm.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/obj/DLKM_OBJ/vendor/qcom/opensource/securemsm-kernel/qseecom_dlkm.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/misc/wis-devinfo.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/obj/DLKM_OBJ/vendor/wiseasy/drivers/scan/scan_dlkm.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/tty/serial/msm_geni_serial.ko .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/usb/dwc3/dwc3-msm.ko .

adb wait-for-device
adb root
adb remount

adb push wis_sp_dlkm.ko /vendor_dlkm/lib/modules
REM adb push sgm41528_charger.ko /vendor_dlkm/lib/modules
REM adb push typec_hub_dlkm.ko /vendor_dlkm/lib/modules
REM adb push qseecom_dlkm.ko /vendor_dlkm/lib/modules
REM adb push wis-devinfo.ko /vendor_dlkm/lib/modules
REM adb push scan_dlkm.ko /vendor_dlkm/lib/modules
REM adb push msm_geni_serial.ko /vendor_dlkm/lib/modules
REM adb push dwc3-msm.ko /vendor_dlkm/lib/modules

adb reboot
