# SigmaDroid OTA repo

To officially support a device with SigmaDroid, you need to add OTA information. Follow these steps to get started.

## 1. Introduction

To be OTA compliant, a device must meet the following requirements:

### 1.1 JSON Structure

Your JSON file should look like this:

```json
{
  "response": [
    {
        "maintainer": "Name (nickname)",
        "oem": "OEM",
        "device": "Device Name",
        "filename": "SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device codename>.zip",
        "download": "https://sigmadroid.xyz/downloads/Home/<device codename>/OTAs/SigmaDroid-v<version>-<date>-OFFICIAL-gapps-<device codename>.zip",
        "timestamp": 1672531199,
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "size": 104857600,
        "version": "<version>",
        "buildtype": "gapps",
        "forum": "https://forum link",
        "gapps": "",
        "firmware": "",
        "modem": "",
        "bootloader": "",
        "recovery": "https://recovery link",
        "paypal": "https://donation link",
        "telegram": "https://telegram link",
        "dt": "https://github.com/SigmaDroid-devices/device_<oem>_<device_codename>",
        "common-dt": "https://github.com/SigmaDroid-devices/device_<oem>_<SOC>-common",
        "kernel": "https://kernel link"
    }
  ]
}
```

### 1.2 Changelog Structure

The changelog is auto-generated during the build process and can be found in your OUT directory as Changelog.txt. It should look like this:

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

### 3.1 Initial Support

1. Fork this repository to your own GitHub account.
2. After building, a file named *codename*.json will be created in the OUT directory.
3. Copy this file to the cloned repository.
4. Open the file and modify the necessary entries (refer to section 1.1 for mandatory entries).
5. Copy the Changelog.txt file from your OUT directory (refer to section 1.2) to the cloned repository and rename it to `changelog_*codename*.txt`.
6. Submit a pull request to this repository. This allows us to validate your understanding of the requirements. If everything is correct, you will be granted direct push access to this repository.

### 3.2 Update Build

1. Navigate to the directory where this repository is cloned during the repo sync:

```bash
cd vendor/OTA
git fetch --all
git pull
```

2. Copy the *codename*.json file from the OUT directory to this repository.
3. Copy the `changelog_*codename*.txt` file from the OUT directory to this repository.
4. Commit your updates to this repository:

```bash
git add .
git commit -m "<device codename>: update build"
git push
```