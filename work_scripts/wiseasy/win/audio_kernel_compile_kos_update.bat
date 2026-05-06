ssh fuzhongxin@10.30.0.52 "cd /home/workspace_sda/fuzhongxin/sm6115/workspace && ./build_audio_kernel.sh"
scp -r fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/sm6115/QSSI13/out/target/product/bengal_515/obj/DLKM_OBJ/vendor/qcom/opensource/audio-kernel/ .

adb wait-for-device
adb root
adb shell vdc checkpoint commitChanges
adb remount

adb push audio-kernel/dsp/q6_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/adsp_loader_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/q6_pdr_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/spf_core_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/q6_notifier_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/audio_prm_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/dsp/audpkt_ion_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/ipc/gpr_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/ipc/audio_pkt_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/soc/pinctrl_lpi_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/soc/swr_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/soc/snd_event_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/soc/swr_ctrl_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/platform_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/machine_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/wcd_core_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/wcd9xxx_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/wsa881x_analog_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/stub_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/mbhc_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/bolero/bolero_cdc_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/bolero/va_macro_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/bolero/tx_macro_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/bolero/rx_macro_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/wcd937x/wcd937x_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/wcd937x/wcd937x_slave_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/rouleur/rouleur_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/rouleur/rouleur_slave_dlkm.ko /vendor_dlkm/lib/modules
adb push audio-kernel/asoc/codecs/rouleur/pm2250_spmi_dlkm.ko /vendor_dlkm/lib/modules
adb reboot
