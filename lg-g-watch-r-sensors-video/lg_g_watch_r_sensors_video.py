#!/usr/bin/python
#
# The MIT License (MIT)
#
# Copyright (c) 2016 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

template = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="3840" height="2160" viewBox="0 0 3840 2160" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">

<defs>

<g id="altermarkive">
<path d="M90,0 A90,90 0 0,0 0,90 L0,422 A90,90 0 0,0 90,512 L422,512 A90,90 0 0,0 512,422 L512,90 A90,90 0 0,0 422,0 Z" fill="#FFFFFF"/>
<text x="256" y="440" fill="black" text-anchor="middle" style="font-weight:bold; font-size:480px">&#x2200;</text>
</g>

<linearGradient id="gradient" y2="0" x2="1">
<stop offset="0" stop-color="white" stop-opacity="0"/>
<stop offset="1" stop-color="white" stop-opacity="1"/>
</linearGradient>

<mask id="fade" maskContentUnits="objectBoundingBox">
<rect width="1" height="1" fill="url(#gradient)"/>
</mask>

<image id="background00" width="3672" height="4500" xlink:href="00.jpg" x="0" y="0"/>
<image id="background01" width="3672" height="4500" xlink:href="01.jpg" x="0" y="0"/>
<image id="background02" width="4896" height="3672" xlink:href="02.jpg" x="0" y="0"/>
<image id="background03" width="4896" height="3672" xlink:href="03.jpg" x="0" y="0"/>
<image id="background04" width="4896" height="3672" xlink:href="04.jpg" x="0" y="0"/>
<image id="background05" width="4896" height="3672" xlink:href="05.jpg" x="0" y="0"/>
<image id="background06" width="3672" height="3800" xlink:href="06.jpg" x="0" y="0"/>
<image id="background07" width="3672" height="3800" xlink:href="07.jpg" x="0" y="0"/>
<image id="background08" width="3672" height="3800" xlink:href="08.jpg" x="0" y="0"/>
<image id="background09" width="4896" height="3672" xlink:href="09.jpg" x="0" y="0"/>
<image id="background10" width="3672" height="4896" xlink:href="10.jpg" x="0" y="0"/>

<text id="labels" style="font-family:Roboto; font-size:52pt; fill:black; text-anchor:end;">
<tspan x="2100" y="164">Integer Type</tspan>
<tspan x="2100" y="308">String Type</tspan>
<tspan x="2100" y="452">Wake-Up</tspan>
<tspan x="2100" y="596">Reporting Mode</tspan>
<tspan x="2100" y="740">Name</tspan>
<tspan x="2100" y="884">Vendor</tspan>
<tspan x="2100" y="1028">Version</tspan>
<tspan x="2100" y="1172">Range</tspan>
<tspan x="2100" y="1316">Resolution</tspan>
<tspan x="2100" y="1460">Minimum Delay</tspan>
<tspan x="2100" y="1604">Maximum Delay</tspan>
<tspan x="2100" y="1748">Power</tspan>
<tspan x="2100" y="1892">FIFO Maximum</tspan>
<tspan x="2100" y="2036">FIFO Reserved</tspan>
</text>

<g id="foreground00">
<text style="font-family:Roboto; font-size:200pt; text-anchor:middle; font-weight:bold;">
<tspan x="2653" y="1080">LG G Watch R</tspan>
</text>
<text style="font-family:Roboto; font-size:100pt; text-anchor:middle; font-weight:bold;">
<tspan x="2653" y="1280">Sensor Specification</tspan>
</text>
</g>

<g id="foreground01">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_ACCELEROMETER</tspan>
<tspan x="2150" y="308">android.sensor.accelerometer</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">MPU6515 Accelerometer</tspan>
<tspan x="2150" y="884">InvenSense</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">19.613297</tspan>
<tspan x="2150" y="1316">5.950928E-4</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">0.4</tspan>
<tspan x="2150" y="1892">10000</tspan>
<tspan x="2150" y="2036">10000</tspan>
</text>
</g>

<g id="foreground02">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_MAGNETIC_FIELD</tspan>
<tspan x="2150" y="308">android.sensor.magnetic_field</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">AK8963 Magnetometer</tspan>
<tspan x="2150" y="884">AKM</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">4911.9995</tspan>
<tspan x="2150" y="1316">0.14953613</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">16666</tspan>
<tspan x="2150" y="1748">5.0</tspan>
<tspan x="2150" y="1892">1500</tspan>
<tspan x="2150" y="2036">1500</tspan>
</text>
</g>

<g id="foreground03">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_MAGNETIC_FIELD_UNCALIBRATED</tspan>
<tspan x="2150" y="308">android.sensor.magnetic_field_uncalibrated</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">AK8963 Magnetometer Uncalibrated</tspan>
<tspan x="2150" y="884">AKM</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">4911.9995</tspan>
<tspan x="2150" y="1316">0.14953613</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">16666</tspan>
<tspan x="2150" y="1748">5.0</tspan>
<tspan x="2150" y="1892">1500</tspan>
<tspan x="2150" y="2036">1500</tspan>
</text>
</g>

<g id="foreground04">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_GYROSCOPE</tspan>
<tspan x="2150" y="308">android.sensor.gyroscope</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">MPU6515 Gyroscope</tspan>
<tspan x="2150" y="884">InvenSense</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">34.906586</tspan>
<tspan x="2150" y="1316">0.0010681152</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">3.2</tspan>
<tspan x="2150" y="1892">1500</tspan>
<tspan x="2150" y="2036">1500</tspan>
</text>
</g>

<g id="foreground05">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_GYROSCOPE_UNCALIBRATED</tspan>
<tspan x="2150" y="308">android.sensor.gyroscope_uncalibrated</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">MPU6515 Gyroscope Uncalibrated</tspan>
<tspan x="2150" y="884">InvenSense</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">34.906586</tspan>
<tspan x="2150" y="1316">0.0010681152</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">3.2</tspan>
<tspan x="2150" y="1892">1500</tspan>
<tspan x="2150" y="2036">1500</tspan>
</text>
</g>

<g id="foreground06">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_PRESSURE</tspan>
<tspan x="2150" y="308">android.sensor.pressure</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">HSPPAD038 Pressure</tspan>
<tspan x="2150" y="884">ALPS ELECTRIC CO.,</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1100.0</tspan>
<tspan x="2150" y="1316">0.013122559</tspan>
<tspan x="2150" y="1460">1000000</tspan>
<tspan x="2150" y="1604">11111</tspan>
<tspan x="2150" y="1748">1.5</tspan>
<tspan x="2150" y="1892">1500</tspan>
<tspan x="2150" y="2036">1500</tspan>
</text>
</g>

<g id="foreground07">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_GRAVITY</tspan>
<tspan x="2150" y="308">android.sensor.gravity</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">Gravity</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">19.613297</tspan>
<tspan x="2150" y="1316">5.950928E-4</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">2850</tspan>
<tspan x="2150" y="2036">2850</tspan>
</text>
</g>

<g id="foreground08">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_LINEAR_ACCELERATION</tspan>
<tspan x="2150" y="308">android.sensor.linear_acceleration</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">Linear Acceleration</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">19.613297</tspan>
<tspan x="2150" y="1316">5.950928E-4</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">2850</tspan>
<tspan x="2150" y="2036">2850</tspan>
</text>
</g>

<g id="foreground09">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_ROTATION_VECTOR</tspan>
<tspan x="2150" y="308">android.sensor.rotation_vector</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">Rotation Vector</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">5.9604645E-8</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">5.399994</tspan>
<tspan x="2150" y="1892">4450</tspan>
<tspan x="2150" y="2036">4450</tspan>
</text>
</g>

<g id="foreground10">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_STEP_DETECTOR</tspan>
<tspan x="2150" y="308">android.sensor.step_detector</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_SPECIAL_TRIGGER</tspan>
<tspan x="2150" y="740">Step Detector</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">1.0</tspan>
<tspan x="2150" y="1460">0</tspan>
<tspan x="2150" y="1604">0</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">4900</tspan>
<tspan x="2150" y="2036">4900</tspan>
</text>
</g>

<g id="foreground11">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_STEP_COUNTER</tspan>
<tspan x="2150" y="308">android.sensor.step_counter</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_ON_CHANGE</tspan>
<tspan x="2150" y="740">Step Counter</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">1.0</tspan>
<tspan x="2150" y="1460">0</tspan>
<tspan x="2150" y="1604">0</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">4900</tspan>
<tspan x="2150" y="2036">4900</tspan>
</text>
</g>

<g id="foreground12">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_SIGNIFICANT_MOTION</tspan>
<tspan x="2150" y="308">android.sensor.significant_motion</tspan>
<tspan x="2150" y="452">YES</tspan>
<tspan x="2150" y="596">REPORTING_MODE_ONE_SHOT</tspan>
<tspan x="2150" y="740">Significant Motion Detector</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">1.0</tspan>
<tspan x="2150" y="1460">0</tspan>
<tspan x="2150" y="1604">-1</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">0</tspan>
<tspan x="2150" y="2036">0</tspan>
</text>
</g>

<g id="foreground13">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_GAME_ROTATION_VECTOR</tspan>
<tspan x="2150" y="308">android.sensor.game_rotation_vector</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">Game Rotation Vector</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">5.9604645E-8</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">0.3999939</tspan>
<tspan x="2150" y="1892">4450</tspan>
<tspan x="2150" y="2036">4450</tspan>
</text>
</g>

<g id="foreground14">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_GEOMAGNETIC_ROTATION_VECTOR</tspan>
<tspan x="2150" y="308">android.sensor.geomagnetic_rotation_vector</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">GeoMagnetic Rotation Vector</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">5.9604645E-8</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">16666</tspan>
<tspan x="2150" y="1748">5.399994</tspan>
<tspan x="2150" y="1892">2100</tspan>
<tspan x="2150" y="2036">2100</tspan>
</text>
</g>

<g id="foreground15">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">REPORTING_MODE_SPECIAL_TRIGGER</tspan>
<tspan x="2150" y="308">android.sensor.orientation</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_CONTINUOUS</tspan>
<tspan x="2150" y="740">Orientation</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">360.0</tspan>
<tspan x="2150" y="1316">0.1</tspan>
<tspan x="2150" y="1460">60014652</tspan>
<tspan x="2150" y="1604">5000</tspan>
<tspan x="2150" y="1748">5.399994</tspan>
<tspan x="2150" y="1892">4450</tspan>
<tspan x="2150" y="2036">4450</tspan>
</text>
</g>

<g id="foreground16">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">26</tspan>
<tspan x="2150" y="308">android.sensor.wrist_tilt_gesture</tspan>
<tspan x="2150" y="452">YES</tspan>
<tspan x="2150" y="596">REPORTING_MODE_SPECIAL_TRIGGER</tspan>
<tspan x="2150" y="740">Wrist Tilt Gesture</tspan>
<tspan x="2150" y="884">LGE</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">0.1</tspan>
<tspan x="2150" y="1460">0</tspan>
<tspan x="2150" y="1604">0</tspan>
<tspan x="2150" y="1748">1.0</tspan>
<tspan x="2150" y="1892">0</tspan>
<tspan x="2150" y="2036">0</tspan>
</text>
</g>

<g id="foreground17">
<use xlink:href="#labels"/>
<text style="font-family:Roboto; font-size:52pt; text-anchor:start; font-weight:bold;">
<tspan x="2150" y="164">TYPE_HEART_RATE</tspan>
<tspan x="2150" y="308">android.sensor.heart_rate</tspan>
<tspan x="2150" y="452">NO</tspan>
<tspan x="2150" y="596">REPORTING_MODE_ON_CHANGE</tspan>
<tspan x="2150" y="740">Heart Rate Monitor</tspan>
<tspan x="2150" y="884">QTI</tspan>
<tspan x="2150" y="1028">1</tspan>
<tspan x="2150" y="1172">1.0</tspan>
<tspan x="2150" y="1316">1.0</tspan>
<tspan x="2150" y="1460">0</tspan>
<tspan x="2150" y="1604">0</tspan>
<tspan x="2150" y="1748">1.0</tspan>
<tspan x="2150" y="1892">0</tspan>
<tspan x="2150" y="2036">0</tspan>
</text>
</g>

</defs>

%s

<use xlink:href="#altermarkive" transform="scale(0.25) translate(100, 100)"/>

<rect x="1366" y="0" width="100" height="2160" fill="white" stroke="none" mask="url(#fade)"/>
<rect x="1466" y="0" width="2372" height="2160" fill="white" stroke="none"/>

%s

</svg>
"""

backgrounds = [
    [733-1832, 1080-2424,   0.0,  75.0, 'http://i.imgur.com/QgLylPG.jpg'],
    [733-1848, 1080-2312,   0.0, -75.0, 'http://i.imgur.com/BPKwECl.jpg'],
    [733-1200, 1080-2400,  50.0,  25.0, 'http://i.imgur.com/65Psszr.jpg'],
    [733-3322, 1080-1666,  50.0, -25.0, 'http://i.imgur.com/uHSUZDu.jpg'],
    [733-2400, 1080-2100,   0.0,  50.0, 'http://i.imgur.com/h6S9a4h.jpg'],
    [733-2400, 1080-1300, -50.0,   0.0, 'http://i.imgur.com/HrwMA2S.jpg'],
    [733-2700, 1080-1800,  50.0,  50.0, 'http://i.imgur.com/JH28NrE.jpg'],
    [733-1850, 1080-2500,   0.0,  50.0, 'http://i.imgur.com/3xPACSj.jpg'],
    [733-1850, 1080-2550, -50.0, -50.0, 'http://i.imgur.com/GVj2mY3.jpg'],
    [733-2700, 1080-1200,  50.0,   0.0, 'http://i.imgur.com/IKRTATs.jpg'],
    [733-2000, 1080-2000, -50.0,  50.0, 'http://i.imgur.com/5gwId2e.jpg']]

fps = 100
fade = 1 * fps
count_backgrounds = len(backgrounds)
count_foregrounds = 18
show_foreground = 3 * fps
count_frames = count_foregrounds * show_foreground + (count_foregrounds - 1) * 2 * fade
show_background = (count_frames - (count_backgrounds - 1) * fade) / count_backgrounds

def select(prefix, index, fade, show, padding, frame):
    ante = index * (padding + show)
    post = ante + show
    opacity_ante = 1.0 - (1.0 / fade) * (ante - frame)
    opacity_post = 1.0 - (1.0 / fade) * (frame - post)
    opacity = min(opacity_ante, opacity_post)
    opacity = 1.0 if 1.0 < opacity else opacity
    opacity = 0.0 if opacity < 0.0 else opacity
    if opacity == 0:
        return ''
    else:
        return '<use xlink:href="#%s%02u" opacity="%f"/>' % (prefix, index, opacity)

def anchor(index, fade, show, padding):
    middle = (show / 2) + index * (padding + show)
    (offset_x, offset_y, delta_x, delta_y, drop) = backgrounds[index]
    return (offset_x - middle * delta_x / fps, offset_y - middle * delta_y / fps)

def align(item, index, frame):
    if '' == item:
        return ''
    else:
        (offset_x, offset_y, delta_x, delta_y, drop) = backgrounds[index]
        x = offset_x + frame * delta_x / fps
        y = offset_y + frame * delta_y / fps
        return '<g transform="translate(%f, %f)">%s</g>' % (x, y, item)

def jpg():
    print('JPG')
    for index in range(count_backgrounds):
        os.system('wget %s -O %02u.jpg' % (backgrounds[index][4], index))
        (anchored_x, anchored_y) = anchor(index, fade, show_background, fade)
        backgrounds[index][0] = anchored_x
        backgrounds[index][1] = anchored_y

def svg():
    print('SVG')
    for frame in range(count_frames):
        selected_backgrounds = ''
        for background in range(len(backgrounds)):
            selected = select('background', background, fade, show_background, fade, frame)
            selected_backgrounds += align(selected, background, frame)
        selected_foregrounds = ''
        for foreground in range(count_foregrounds):
            selected_foregrounds += select('foreground', foreground, fade, show_foreground, 2 * fade, frame)
        with open('frame.%05u.svg' % frame, 'wb') as file:
            file.write(template % (selected_backgrounds, selected_foregrounds))

def png():
    print('PNG')
    os.system('find . -name "frame.*.svg" -exec convert {} -resize 1920x1080 {}.png \\;')
    os.system('rm *.svg')
    os.system('rm *.jpg')

def mp4():
    print('MP4')
    os.system('ffmpeg -y -framerate %d -i frame.%%05d.svg.png -c:v libx264 -r %d -pix_fmt yuv420p lg.mp4' % (fps, fps))
    os.system('rm *.png')

if __name__ == "__main__":
    jpg()
    svg()
    png()
    mp4()
