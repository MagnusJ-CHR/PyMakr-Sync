def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting")
        wlan.connect('HOTSPOT', 'Pass')
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig()[0])

do_connect()