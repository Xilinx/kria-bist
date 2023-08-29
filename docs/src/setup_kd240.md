# KD240 BIST Board Setup

## Hardware Requirements

1. KD240 Starter Kit [here](http://www.amd.com/kd240)
2. KD240 Power Supply & Adapter
3. KD240 Motor Kit [here](http://www.amd.com/kd240)
4. 24V Power Supply for Motor Kit
5. MicroSD Card
6. Host Machine (Windows or Ubuntu)
7. Three Ethernet Cables
8. Ethernet Switch
9. One [PMOD CAN](https://digilent.com/reference/pmod/pmodcan/start)
10. 10 Male to Male,Female to Female,Female to Male Jumper Wires
11. One RS485 Temperature and Humidity Sensor from [here](https://www.aliexpress.us/item/2251832868368800.html?gatewayAdapt=glo2usa4itemAdapt) or [here](https://www.amazon.com/Temperature-Humidity-Sensor-Display-Modbus/dp/B078NRYBVZ)
12. Two USB Flash Drives


## Board Setup

This page shows how to set up the KD240 before running the BIST application.

Refer to the KD240 Board and the Interface layout below for connector reference numbers:

![KD240-Interfaces](./media/KD240-Interfaces.png)

The following image shows a KD240 with all the hardware connected.

![KD240-Image](./media/KD240-Image.jpg)

The BIST application requires the following hardware setup to run
the full suite of hardware tests:

* USB Flash Drive (x2)

  ![KD240-SD](./media/KD240-SD.jpg)

  Connect a USB Flash Drive to each of the two USB ports.

* RS485 Temperature and Humidity Sensor (x1)

  ![KD240-RS485](./media/KD240-RS485-Connections.JPG)

  Connect the RS485 Temperature and Humidity sensor as below on the J22 Connector 
  on the KD240. 
  Obtain a separate 12V power supply to connect the two loose 
  jumpers as shown in the following image, one to GND(black wire in image) and the other to 12V Supply
  (white wire in image).

  ![KD240-RS485-Image](./media/KD240-RS485-Image.jpg)
  ![KD240-RS485-Close](./media/KD240-RS485-Close-Up.jpg)

  ***Note***: Make sure that the J21 jumper is on 1-2(RS485-AB) combination.

* Ethernet Cable (x3)

  ![KD240-Eth](./media/KD240-Eth.jpg)

  Connect an Ethernet cable from each of the three Ethernet ports on the KD240 to
  the host machine via a switch.

* PMOD CAN (x1)

  ![KD240-PMOD-CAN](./media/KD240-PMOD-CAN.jpg)

  Connect the PMOD-CAN test point headers to the J2 connector on the KD240. 
  Connect the PMOD-CAN(J2) to CAN 2.0(J18) using jumper wires as shown below:
  - Connect GND on J2 to GND on J18
  - Connect CANH on J2 to CANH on J18
  - Connect CANL on J2 to CANL on J18

* Brake and 1-wire
  
  ![KD240-Brake-1wire](./media/KD240-Brake-1Wire.jpg)

  Connect Pin1(Brake) on J46 to the pin2(Sense) on J47 in loopback.

* Motor Kit (x1)
  
  ![KD240-Motor-Kit](./media/KD240-Motor-Kit.jpg)

  * Connect 24V power supply to J39
  * Connect encoder header pins to J42
  * Connect Motor's AC power jack to J32


## Next Steps

* [Run the BIST Application](run.md)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
