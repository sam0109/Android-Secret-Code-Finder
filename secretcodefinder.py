import subprocess
import os
import re

subprocess.call("adb push /home/device/Desktop/secretcodefinder/busybox /data/local/tmp/busybox", shell=True)
subprocess.call("adb shell chmod 777 /data/local/tmp/busybox", shell = True)
secret_codes = []
i = 1
next_line_secret_code = False
for app in subprocess.check_output('adb shell pm list packages -f', shell = True).splitlines():
	path = re.sub('package:', '', app)
	path = re.sub("=.*", "", path)
	subprocess.call('adb shell mkdir /data/local/tmp/unzipped_app_' + str(i) + '/', shell=True)
	subprocess.call("adb shell /data/local/tmp/busybox unzip -o " + path + " AndroidManifest.xml -d /data/local/tmp/unzipped_app_" + str(i) + '/', shell=True)
	subprocess.call("adb pull /data/local/tmp/unzipped_app_" + str(i) + '/AndroidManifest.xml /home/device/Desktop/secretcodefinder/manifest_' + str(i) + '/AndroidManifest.xml', shell=True)
	subprocess.call('cp /home/device/Desktop/secretcodefinder/manifest_' + str(i) + '/AndroidManifest.xml ./AndroidManifest.xml', shell=True)
	subprocess.call('zip /home/device/Desktop/secretcodefinder/manifest_' + str(i) + '/test.apk AndroidManifest.xml', shell=True)
	subprocess.call('rm ./AndroidManifest.xml', shell=True)
	Manifest_Contents = subprocess.check_output('/home/device/android-sdk-linux_x86/platform-tools/aapt d xmltree /home/device/Desktop/secretcodefinder/manifest_' + str(i) + '/test.apk AndroidManifest.xml', shell=True)
	i += 1
	for line in Manifest_Contents.splitlines():
		if next_line_secret_code == True:
			a = re.search('Raw: "[0-9]{1,100}', line)
			if a != None:
				code = a.group(0)
				secret_codes.append(code[6:])
				next_line_secret_code = False
		if re.search('android_secret_code', line):
			next_line_secret_code = True
secret_codes.sort()
secret_codes = reduce(lambda x, y: x if y in x else x + [y], secret_codes, [])
for i in secret_codes:
	print i
