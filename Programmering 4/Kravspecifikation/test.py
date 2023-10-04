    if pb1.value() == 0:
        sleep_ms(400)
        led1.value(not led1.value())
        npswitch = led1.value()
        print(npswitch)
    if npswitch == 1:
        blinke()
    if npswitch == 0:
        blinkestatisk()
    ...