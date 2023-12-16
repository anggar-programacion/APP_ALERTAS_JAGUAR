import jlrpy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class AlarmApp(App):
    def build(self):
        self.alarms = None
        layout = BoxLayout(orientation='vertical')

        # Cambiar el tamaño del botón al 10% de la altura de la pantalla
        button = Button(
            text='Listar Alarmas',
            size_hint=(1, 0.1)  # 10% de la altura de la pantalla
        )
        button.bind(on_press=self.list_alarms)
        self.label = Label(text='Presiona el botón para listar las alarmas.')

        # Redondear el botón
        button.background_color = (0.4, 0.4, 1, 1)
        button.border = (0, 0, 0, 0)
        button.border_radius = [20]

        
        layout.add_widget(self.label)

        # Colocar el botón en la parte inferior de la pantalla
        layout.add_widget(button)

        return layout

    def list_alarms(self, instance):
        # Autenticación usando nombre de usuario y contraseña
        c = jlrpy.Connection('agarrido@agarquitectura.es', 'Quilla2502Quilla')
        v = c.vehicles[0]
        data = v.get_status()

        # Extraer la clave lastUpdatedTimeVehicleAlert del diccionario original
        last_updated_time_vehicle_alert = data.get("lastUpdatedTimeVehicleAlert", "")


        # Extraer y ordenar las alertas por lastUpdatedTime
        vehicle_alerts = data.get("vehicleAlerts", [])
        sorted_alerts = sorted(vehicle_alerts, key=lambda x: x.get("lastUpdatedTime", ""))

        alarm_text = ''
        for alert in sorted_alerts:
            key = alert.get("key", "")
            value = alert.get("value", "")
            active = alert.get("active", "")
            last_updated_time = alert.get("lastUpdatedTime", "")
            date, time = last_updated_time.split('T')
            alarm_text += f"{date} {time} {key} {value} {active}\n"

        
        self.label.text = alarm_text
        


if __name__ == '__main__':
    AlarmApp().run()