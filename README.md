# SigmaDroid OTA repo

To officially support a device with SigmaDroid, you need to add OTA information. Follow these steps to get started.

## 1. Introduction

To be OTA compliant, there are a few things to know.

### 1.1 Device JSON Structure

The way the OTA Updater works is by checking this repository at [https://github.com/SigmaDroid-devices/OTA](https://github.com/SigmaDroid-devices/OTA) for a JSON file with a filename that matches the device codename. This JSON file contains the latest build information, including a download URL and other necessary information for the OTA Updater to function correctly. This JSON file is auto-generated during the build process and can be found in your OUT directory as *codename*.json.

Your JSON file should look something like this:

```json
{
  "response": [
    {
        "maintainer": "<Name (nickname)>",
        "oem": "<OEM>",
        "device": "<Device Name>",
        "filename": "SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device_codename>.zip",
        "download": "https://sigmadroid.xyz/downloads/Home/<device_codename>/OTAs/SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device_codename>.zip",
        "timestamp": 1672531199,
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "size": 104857600,
        "version": "<version>",
        "buildtype": "gapps",
        "forum": "<build_release_thread_url>",
        "gapps": "",
        "firmware": "",
        "modem": "",
        "bootloader": "",
        "recovery": "https://sigmadroid.xyz/downloads/Home/<device_codename>/Recovery/<recovery_image>",
        "paypal": "https://paypal.me/albinoman887",
        "telegram": "https://t.me/SigmaDroidROMChat",
        "dt": "https://github.com/SigmaDroid-devices/device_<oem>_<device_codename>",
        "common-dt": "https://github.com/SigmaDroid-devices/device_<oem>_<SOC>-common",
        "kernel": "<kernel_source_url>"
    }
  ]
}
```

* The `maintainer`, `oem`, `device`, `filename`, `download`, `timestamp`, `md5`, `sha256`, `size`, `version`, `buildtype`, `recovery`, `paypal`, `telegram`, `dt`, and `common-dt` fields are mandatory. The rest are optional.
* For the buildtype field, use `gapps` for builds with GApps and `vanilla` for builds without GApps.
* Most of these fields are populated during the build process. You only need to fill in the `forum`, `recovery`, and  `kernel` fields, and modify the paypal url to your own if you have one. Please still take care to review the generated JSON the first time for any errors.

### 1.2 Changelog Structure

The changelog is auto-generated during the build process and can be found in your OUT directory as SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device_codename>-Changelog.txt. It should look something like this:

```text
====================
     <date>
====================

   * <project>
<commit-id> - <commit-message> (by <commit-author>)

   * <project>
<commit-id> - <commit-message> (by <commit-author>)

====================
     <date>
====================

   * <project>
<commit-id> - <commit-message> (by <commit-author>)
```

## 2. Guidelines

* Check if the manufacturer already exists.
* Ensure the published link is official.
* Validate the JSON using online tools like [JSON Formatter by Curious Concept](https://jsonformatter.curiousconcept.com) or [JSON Formatter](https://jsonformatter.org).
* Ensure there are no extra or missing spaces.

## 3. Instructions

Replace *codename* with your device's codename in the instructions below.

### 3.1 Adding Initial Support

If you are adding support for a new device, follow these steps:

1. Fork this repository to your own GitHub account.
2. After building, a file named *codename*.json will be created in the OUT directory.
3. Copy that JSON file to the directory you cloned this repository.
4. Open the file and review and if required, modify the necessary entries (refer to section 1.1 for mandatory entries).
5. Copy the SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device_codename>-Changelog.txt file from your OUT directory (refer to section 1.2) to the cloned repository and rename it to `changelog_*codename*.txt`.
6. Commit your changes to this repository:

```bash
git add .
git commit -m "<device codename>: initial support"
git push
```

7. Submit a pull request to this repository. This allows us to validate your understanding of the requirements. If everything is correct, you will be granted direct push access to this repository.

### 3.2 Updating an Existing Device

If you are updating an existing device, follow these steps:

1. Navigate to the directory where this repository is cloned during the repo sync and git pull the latest changes if any:

```bash
cd vendor/OTA
git fetch --all
git pull sigma sigma-14.3
```

2. Copy the *codename*.json file from the OUT directory to this repository at vendor/OTA.
3. Copy the SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device_codename>-Changelog.txt file from your OUT directory (refer to section 1.2) to this repository at vendor/OTA and rename it to `changelog_*codename*.txt`.
4. Commit your changes to this repository:

```bash
git add .
git commit -m "<device codename>: update build"
```

5. Push your changes to this repository:

```bash
git push sigma sigma-14.3
```