# CTF: Examining EXIF Metadata

__MASTER HANDBOOK 2026.02__

DESCRIPTION: Digital images often contain hidden metadata such as device information, timestamps, and GPS coordinates. Exchangeable Image File Format (EXIF) tags can unintentionally expose sensitive information when images and documents are shared online.

In this challenge, you will analyze image metadata to extract identifying and geolocation information using common tools.

DIFFICULTY: Novice

ESTIMATED TIME: 5 minutes

TARGET: [cat.jpg](cat.jpg)

OBJECTIVES:
+ Extract EXIF metadata from a JPG image
+ Identify ownership information
+ Recovery embedded GPS coordinates
+ Use OSINT techniques to determine where the picture was taken

## PART 0x00 -- Metadata Enumeration

Inspect the image and determine what metadata is embedded within it.

_Questions:_
+ Who is the owner of the image?

_Commands:_

```
$ exif --tag=CameraOwnerName ./cat.jpg #OR
$ exiftool -OwnerName ./cat.jpg
```

_Flag\_01:_

```
FLAG{c1ean_y0ur_m3tad@ta}
```

## PART 0x01 -- Geolocation Analysis

Determine whether this image contains location data.

_Question(s):_
+ What city and country was the image taken in?
+ BONUS: What famous statue is nearby?

_Command(s):_

```
$ exif ./cat.jpg # OR
$ exiftool -GPSPosition ./cat.jpg # OR
$ exiflooter --image ./cat.jpg
```

_Expected Output:_

```
GPS Latitude:  45 deg 26' 31.7" N
GPS Longitude: 10 deg 59' 55.4" E
```

_Flag_02 (City, Country):_

```
Verona, Italy
```

_Bonus:_

```
Statua di Giulietta
```

----

EOF
