import mtpy
import time
import os.path


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# mtpy.get_raw_devices()
# Device 0 (VID=091e and PID=4cd8) is a Garmin Fenix 6S Pro/Sapphire.

# This works even if Android MTP app is also running

# But the following does not, exit the app first, otherwise error:
#   ibusb_detach_kernel_driver() failed, continuing anyway...: No such file or directory
#   error returned by libusb_claim_interface() = -3LIBMTP PANIC: Unable to initialize device
#   [1]    27619 segmentation fault  python main.py

retryCount = 0
while True:
    try:
        devices = mtpy.get_raw_devices()
        if len(devices) == 0:
            time.sleep(1)
            retryCount += 1
        else:
            break
    except Exception:
        time.sleep(1)
        retryCount += 1

    if retryCount > 30:
        print("no device seen for 30s, exiting")
        exit(1)

dev = devices[0].open()
# children = dev.get_children()
# print(children)

# garminFolder = dev.get_descendant_by_path("/GARMIN")
# garminChildren = garminFolder.get_children()
# print(garminChildren)

garminActivitiesFolder = dev.get_descendant_by_path("/GARMIN/Activity")

garminActivitiesChildrenByItemID = garminActivitiesFolder.get_children()
garminActivitiesChildrenByName = new_list = sorted(garminActivitiesChildrenByItemID,
                                                   key=lambda x: x.name,
                                                   reverse=False)

years = ["2021", "2022", "2023"]
for year in years:
    for fileItem in garminActivitiesChildrenByName:
        if fileItem.name.startswith("%s-" % year):
            rel_file_path = os.path.join("activities", year, fileItem.name)
            file_exists = os.path.exists(rel_file_path)
            if not file_exists:
                print("Downloading", fileItem.name, sizeof_fmt(fileItem.filesize))

                fileToDownload = garminActivitiesFolder.get_child_by_name(fileItem.name)
                fileToDownload.retrieve_to_file(rel_file_path)

# for fileItem in garminActivitiesChildrenByName:
#     print(fileItem.name, sizeof_fmt(fileItem.filesize))

# fileToDownload = garminActivitiesFolder.get_child_by_name("2023-02-28-16-23-28.fit")
# fileToDownload.retrieve_to_file("my_activity.fit")

dev.close()
