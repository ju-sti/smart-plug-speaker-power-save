import time
import ctypes
import comtypes
import pycaw.pycaw
import urllib.request


# magic win32 voodoo I found on the internet
class IAudioMeterInformation(comtypes.IUnknown):
    _iid_ = comtypes.GUID('{C02216F6-8C67-4B5B-9D00-D008E73E0064}')
    _methods_ = (
        # HRESULT GetPeakValue([out] c_float *pfPeak);
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetPeakValue',
                           (['out'], ctypes.POINTER(ctypes.c_float), 'pfPeak')),)


devices = pycaw.pycaw.AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioMeterInformation._iid_, comtypes.CLSCTX_ALL, None)
meter = ctypes.cast(interface, ctypes.POINTER(IAudioMeterInformation))


BASE_URL = "http://192.168.1.55"
on = False


def main():
    # get current state
    response = urllib.request.urlopen(BASE_URL + "/index").read(500)
    if b'input class="g"' in response:
        # speaker (smart plug) is enabled => electricity is flowing
        on = True
    else:
        on = False

    while True:
        time.sleep(1 / 1000)  # 15ms or so in reality
        if meter.GetPeakValue() > 0.0001:  # enable speaker as soon as possible when audio is playing
            if not on:
                on = True
                print("on")
                urllib.request.urlopen(BASE_URL + "/index?tgl=0")  # don't read: connection is not closed properly
        else:
            if on:
                volume = 0
                for i in range(120):
                    time.sleep(1)
                    volume += meter.GetPeakValue()
                if volume < 0.0001:  # turn off speaker when no sound was played for 2 minutes
                    on = False
                    print("off")
                    urllib.request.urlopen(BASE_URL + "/index?tgl=0")  # don't read: connection is not closed properly


# when windows is shutdown the speaker is not set to off because detecting a shutdown would need some more win32 api voodoo
main()