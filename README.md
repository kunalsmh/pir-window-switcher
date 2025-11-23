## Using PIR motion sensor to change tabs
The motion sensor sends an API request to the local hosted server if someone is detected and opens the defined file/app.

### Hardware used
- ESP32 (5$)
- hc-sr501 (1$)

The board is powered with my personal 10,000Mah spare power bank but it can be powered with a cheap lipo battery or directly through your laptop/pc.

### Flashing the code into the board and hosting a local API server

1. Clone this repo and open the src file
2. Configure the platform.ini according to your board
3. Inside server.py, replace `pdf_path` with your file path
4. Go to main.cpp, replace your `WIFI_SSID`, `WIFI_PASSWORD`, `API_URL` with your credentials
5. Place the device where you want the sensor to detect presence

- The API server runs in the background, close it from system tray to end the process.

###### I use this so my parents think i'm always studying but you can use this however you want haha

<table>
  <tr>
    <td><img src="https://github.com/kunalsmh/pir-window-switcher/blob/master/src/1.png" width="350"/></td>
    <td><img src="https://github.com/kunalsmh/pir-window-switcher/blob/master/src/eee.png" width="350"/></td>
  </tr>
</table>
