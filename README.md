# Functional-Hub
It's is a 3.0 USB Hub X Macro Pad.

Yeah its a Fusion dish of some of the most needed things in one , designed by me aka Shaurya a 17 Y/O from India

# Zine

<img width="540" height="828" alt="Frame 2" src="https://github.com/user-attachments/assets/62edc3e1-51ce-46cf-bb7e-75b6a00ebc68" />

# Why i build it 
I was going through the guided project files when i discover about a guide to build a USB Hub , but its was kinda simple so i thoungh why not build some thing complex . Then i came to this conclusion to build a 3.0 fast (kinda) USB Hub with a in-built Macro Pad .

# Schematics

<img width="4698" height="3326" alt="SCH_Schematic1_1-P1_2026-06-13" src="https://github.com/user-attachments/assets/6d001341-aad1-4724-8a9f-fc067b202dfc" />

So let's begain with the tech talk

I have used TUSB8041RGCT IC from Texas industries comes in a 64-Pin QFN Package, it is a 5Gbps high speed 1x stream & 4x downstream USB hub IC.
It took me a long time to figure out connection and working of this IC , I've spent hours reading the datasheet . It also supports external powered for downstream USBs with Over current detection and auto shut down of downstream ports.
<img width="508" height="418" alt="Screenshot 2026-06-13 at 2 13 01 AM" src="https://github.com/user-attachments/assets/0d2e54a5-27fa-424b-9ef2-f632f95d5012" />

For over current protection, I've used another IC from Texas industries i.e. TPS2561DRCR .
I saw this in one of the datasheet of a high speed USB hub. It allows maximum of 2 A per downstream port.
<img width="752" height="149" alt="Screenshot 2026-06-13 at 2 16 48 AM" src="https://github.com/user-attachments/assets/40a00f97-191d-4041-bc31-692b54b51add" />


The four down port are divided as:
--> 2x USB-C
--> 1x USB-A
--> RP2040 (directly connected)

This is a separate IC for ESD protection on every downstream & upstream port .


Upstream port :
<img width="221" height="110" alt="Screenshot 2026-06-13 at 2 21 19 AM" src="https://github.com/user-attachments/assets/58e3da33-4f99-4e86-ab31-31de04c1b4ea" />


Downstream port's :
<img width="592" height="107" alt="Screenshot 2026-06-13 at 2 21 02 AM" src="https://github.com/user-attachments/assets/1dc66215-f22e-419f-a7f6-ceb363a8d567" />


There is a separate USB-C for powering the downstream ports .I have also added a switch to change between the upstream power source and external power source.
<img width="514" height="145" alt="Screenshot 2026-06-13 at 2 25 24 AM" src="https://github.com/user-attachments/assets/51248df0-e5c5-4c25-b284-e5eba449ea30" />


Now the Macro Pad 

The main mcu for this is a RP2040 which is the chepest and most reliable mcu for this application .
It's from our fav company raspberry pi . It requires a separate memory to flash code as it doesn't have one in-built. Also, I have connected the USB interface of RP2040 directly to the fourth downstream port of the USB hub IC.
<img width="330" height="321" alt="Screenshot 2026-06-13 at 2 30 04 AM" src="https://github.com/user-attachments/assets/1a075bfb-7b6c-4504-84cb-b509e411c132" />

This macro pad has:
--> 3x Push Button
--> 0.91 OLED 128X32
--> Magnetic Rotary Encoder

<img width="186" height="335" alt="Screenshot 2026-06-13 at 2 32 47 AM" src="https://github.com/user-attachments/assets/84945145-fed6-4361-9b49-7224d05bcde1" />


# PCB 

It's a 4 layer pcb with top and bottom layers signal and inner layers as ground and power.

The wiring was the most difficult part in this project, I was going through many Dattasheets and read post, but was not able to figure out what was the impedance and proper track width and lenght so, there it's the major flow of my design as it will not provide the maximum speed (5Gbps) but should have better speed than a normal 2.0 USB hub.

Top layer:
<img width="939" height="388" alt="Screenshot 2026-06-13 at 2 38 58 AM" src="https://github.com/user-attachments/assets/c1bf25a3-f48f-4fb0-8eb6-f5c3d6a23800" />

Bottom layer:
<img width="949" height="386" alt="Screenshot 2026-06-13 at 2 39 19 AM" src="https://github.com/user-attachments/assets/b5c43a65-cc35-49fe-b87a-b93696eae4df" />

Inner GND layer:
<img width="937" height="378" alt="Screenshot 2026-06-13 at 2 40 05 AM" src="https://github.com/user-attachments/assets/108037f8-6126-4a00-a5a8-98871c38345f" />

Inner Power layer:
<img width="931" height="370" alt="Screenshot 2026-06-13 at 2 40 42 AM" src="https://github.com/user-attachments/assets/01936ad1-9d66-4025-a3ee-0436a25b6028" />

power one had mulltiple different power line so i simply used traces to connect them while the rest of the macro pad had a common power source so I used a copper fill region there.

# CAD 

I used Fusion 360 stu. License version to create the enclosure for this USB hub.
The base will be a simple 3D printed part with screw holes to properly secure the PCB.
The top will be a custom cut translucent acrylic sheet which will be glued to the bottom case.

Here are some of the rendering of the final product.

<img width="2880" height="1226" alt="Untitled_2026-Jun-12_02-11-34PM-000_CustomizedView20562888345_png_alpha" src="https://github.com/user-attachments/assets/b4d8ce1d-d3ed-4790-85bb-d2b4ce31ae51" />
<img width="2880" height="1226" alt="Untitled_2026-Jun-12_02-12-34PM-000_CustomizedView5272772413_png_alpha" src="https://github.com/user-attachments/assets/c709263d-9b41-42bc-b253-56bf69ba10f3" />
<img width="2880" height="1226" alt="Untitled_2026-Jun-12_02-24-10PM-000_CustomizedView5463506446_png_alpha" src="https://github.com/user-attachments/assets/b478861d-cf10-413d-8457-8b54a57d624b" />

# Assembly

<img width="1508" height="1036" alt="Bottom Base" src="https://github.com/user-attachments/assets/63eb3ff7-36da-48dc-8a3e-ea4f1592107d" />

Those are M2 Screw's & the top acrylic sheet will be glued .
















