#!/bin/bash
# 该脚本参考/kernel_platform/build/all-variants.sh
# 功能是对find的查找结果分别unpack并分析输出的文件，大小，md5sum等。
# 对于多个输入的统一分别处理的情况，该脚本架构可供参考
#
# 实际使用场景，find的输出结果为：
#   ../bootable/recovery/tests/testdata/boot.img
#   ../out/msm-kernel-bengal-consolidate/dist/boot.img
#   ../out/msm-kernel-bengal-consolidate/gki_kernel/dist/boot.img
#   ../out/target/product/bengal_515/obj/PACKAGING/target_files_intermediates/bengal_515-target_files-eng.fuzhongxin/IMAGES/boot.img
#   ../out/target/product/bengal_515/boot.img
#   ../kernel_platform/out/msm-kernel-bengal-consolidate/dist/boot.img
#   ../kernel_platform/out/msm-kernel-bengal-consolidate/gki_kernel/dist/boot.img
#   ../bootable/recovery/tests/testdata/boot.img



TOOL=../out/host/linux-x86/bin/unpack_bootimg

function do_find() (
	find ../ -name boot.img -type f
)

while read bootimg; do
	echo "============================================================"
	ls -l ${bootimg} | grep -v total
	md5sum ${bootimg}
	rm -r boot/* 
	${TOOL} --boot_img ${bootimg} --out boot/ #>> /dev/null
	ls -l boot/ | grep -v total
	md5sum boot/kernel
done < <(do_find)

