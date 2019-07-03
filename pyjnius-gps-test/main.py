from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.logger import Logger

from jnius import PythonJavaClass, java_method, autoclass


Looper = autoclass('android.os.Looper')
LocationManager = autoclass('android.location.LocationManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity
Context = autoclass('android.content.Context')


class GpsListener(PythonJavaClass):
    __javainterfaces__ = ['android/location/LocationListener']

    def __init__(self, callback):
        super(GpsListener, self).__init__()
        self.callback = callback
        self.locationManager = PythonActivity.getSystemService(Context.LOCATION_SERVICE)

    def start(self):
        self.locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 10000, 10, self, Looper.getMainLooper())

    def stop(self):
        self.locationManager.removeUpdates(self)

    @java_method('()I')
    def hashCode(self):
        return id(self)%2147483647

    @java_method('(Landroid/location/Location;)V')
    def onLocationChanged(self, location):
        self.callback(self, 'location', location)

    @java_method('(Ljava/lang/String;ILandroid/os/Bundle;)V')
    def onStatusChanged(self, *args):
        self.callback(self, 'status-change', *args)

    @java_method('(Ljava/lang/String;)V')
    def onProviderDisabled(self, status):
        self.callback(self, 'provider-disabled', status)

    @java_method('(Ljava/lang/Object;)Z')
    def equals(self, obj):
        return obj.hashCode() == self.hashCode()


class GpstestRoot(BoxLayout):
    pass


class GpstestApp(App):

    def gps_callback(self, provider, eventname, *args):
        if provider is not self.provider:
            return
        Logger.info("GPS Happened: {}".format((provider, eventname, args)))
        if eventname == 'provider-disabled':
            self.gps_values[1] = args[0]
            self.trigger_gps_update_values()
        elif eventname == 'location':
            location = args[0]
            Logger.info("Latitude: {}".format(location.getLatitude()))
            Logger.info("Longitude: {}".format(location.getLongitude()))
            self.gps_values[2:] = [location.getLatitude(),
                                location.getLongitude()]
            self.trigger_gps_update_values()

    def gps_update_values(self, *args):
        Logger.info("GPS Values Updated: {}".format(*args))
        values = self.gps_values
        self.root.ids.gps_label.text = str(values)

    def on_stop(self):
        if self.provider:
            self.provider.stop()
        super(GpstestApp, self).on_stop()

    def on_pause(self):
        if self.provider:
            self.provider.stop()
        return True

    def on_resume(self):
        if self.provider:
            self.provider.start()

    def build(self):
        self.provider = GpsListener(self.gps_callback)
        self.gps_values = ['', '', 0, 0] 
        self.trigger_gps_update_values = Clock.create_trigger(self.gps_update_values, 0)
        #self.provider.start()

        return(GpstestRoot())


if __name__ == "__main__":
    GpstestApp().run()
