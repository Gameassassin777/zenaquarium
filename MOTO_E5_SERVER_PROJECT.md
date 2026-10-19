# Project: Repurposing a Moto e5 Cruise as a Headless Micro-Server

## 📱 Device Overview
**Model:** Motorola Moto e5 Cruise (Cricket Wireless Edition, ~2018)
**Specs:** Snapdragon 425 processor, 2GB RAM, 16GB Storage
**Condition:** Heavy screen wear, scratches, and a completely unresponsive touchscreen.

## 🎯 Project Goal
Transform the old, unresponsive Moto e5 Cruise into a remote, headless micro-server. The device will be deployed at a remote location (parents' house) on local Wi-Fi, acting as a node on an existing Tailscale network.

### Intended Use Cases
1. **Personal Server & Data Storage:** Using Syncthing or similar tools to act as a secure, decentralized remote backup node for personal data and projects.
2. **Adblocker:** Running a network-wide adblocker (like AdGuard Home) to filter traffic for the remote local network.
3. **Tailscale Node / Subnet Router:** Acting as a bridge between the remote local network and the primary apartment network.

*Note: Initially, hosting GitHub repositories (like `zenaquarium` or `workoutlog`) on the device was considered, but since those are easily hosted via GitHub/Vercel, the phone's limited storage and processing power are better utilized for the utility services listed above.*

---

## 🚧 The Problem: The Broken Screen Catch-22
To use an Android device as a purely headless server, it must be controllable from a PC terminal via **ADB (Android Debug Bridge)**. However, for security reasons, USB Debugging is disabled by default after a factory reset. To enable it, a user must physically tap through the Android setup menu and developer options. Because the touchscreen is broken, this is impossible through standard means.

**The Easy (but boring) Solution:** Purchase a Micro-USB OTG (On-The-Go) adapter and plug in a standard USB computer mouse. A cursor appears on the screen, allowing the user to click through the setup and enable USB debugging.

---

## 🧠 The Creative Solution: The Bootloader Breakout Plan
To bypass the need for a mouse and completely subvert the restricted Cricket Wireless environment, the following advanced plan was devised:

### Phase 1: The "Breakout" (Bootloader Exploit)
- **Goal:** Bypass the Cricket Wireless lock to gain low-level system access.
- **Method A (Soft):** Attempt to extract the OEM unlock data via `fastboot oem get_unlock_data` and force it through the Motorola Unlock Portal.
- **Method B (Hard/Hardware):** If Cricket blocks Method A, physically open the back of the Moto e5 Cruise, locate the **Qualcomm Test Points** on the motherboard, and short them with tweezers. This forces the phone into **EDL (Emergency Download) Mode (Qualcomm 9008)**. From there, use a leaked Snapdragon 425 "Firehose" programmer file to overwrite the restricted bootloader with an unlocked engineering bootloader.

### Phase 2: ADB Injection (Bypassing the Broken Screen)
- **Goal:** Enable USB debugging so the phone can be controlled purely via a PC terminal, completely bypassing the broken touchscreen.
- **Action:** Flash a custom recovery like **TWRP (Team Win Recovery Project)** via fastboot.
- **Action:** Boot into TWRP, mount the system partition via the PC terminal, and modify the `build.prop` file to include:
  ```properties
  ro.adb.secure=0
  persist.sys.usb.config=adb
  ```
  *Result: This forces the phone to trust all connected computers and turns on USB debugging by default, no screen taps required.*

### Phase 3: Headless Server Conversion
- **Goal:** Strip the Android OS and convert it into a lean Linux server.
- **Action:** Boot the phone normally. Plug it into the PC and open a terminal using `adb shell`.
- **Action:** Run extreme debloat scripts via ADB to uninstall the Android UI (launcher), Cricket bloatware, and unnecessary background services to free up RAM and CPU cycles.
- **Action:** Use ADB to push and install the APKs for **Termux** (the Linux environment) and **Tailscale**.

### Phase 4: Network & Storage Deployment
- **Goal:** Set up the utility services on the now-headless device.
- **Action:** Configure Termux to run OpenSSH and acquire a permanent Wakelock (preventing Android from putting the CPU to sleep).
- **Action:** Install and configure **AdGuard Home** via Termux to handle network-wide adblocking for the parents' house.
- **Action:** Install **Syncthing** for secure, decentralized remote data backups from the apartment node to the phone.
- **Action:** Authenticate Tailscale via the terminal and configure the phone as a Subnet Router to bridge the two locations securely.