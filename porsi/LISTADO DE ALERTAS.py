import jlrpy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from datetime import datetime
#import mis_utilidades as util
from mis_utilidades import read_credentials_from_file


class Jaguar_AlarmApp(App):
    def __init__(self, config_file="config.txt"):
        
        #OJO QUE HACE ESTO?

        super(Jaguar_AlarmApp, self).__init__()
        self.config_file = config_file

    
    #construye el entorno grafico
    def build(self):

        # Configurar el icono de la aplicación
        self.icon = 'logo_jaguar.png'
        self.alarms = None
        layout = BoxLayout(orientation='vertical')

        button = Button(
            text='Listar Alarmas y Guardar en Archivo',
            size_hint=(1, 0.1)
        )
        button.bind(on_press=self.list_alarms_and_save)

        self.label = Label(
            size_hint=(1, 0.1),
            text='Presiona el botón para listar las alarmas y guardar en un archivo.'
        )

        self.label2 = Label(
            size_hint=(1, 0.8),
            text=''
        )

        button.background_color = (0.4, 0.4, 1, 1)
        button.border = (1, 0, 0, 0)
        button.border_radius = [50]

        layout.add_widget(self.label2)
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    #lista las alarmas y las salva
    def list_alarms_and_save(self, instance):

        #llama a la funcion read_credentials_from_file() 
        #credentials = self.read_credentials_from_file() esta es para cuando la funcion esta dentro
        credentials = read_credentials_from_file(self.config_file)

        #print ("credenciales: ",credentials)

        if credentials is not None:
            username, password = credentials
            c = jlrpy.Connection(username, password)
            v = c.vehicles[0]
            data = v.get_status()

            last_updated_time_vehicle_alert = data.get("lastUpdatedTimeVehicleAlert", "")
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

            current_datetime = datetime.now()
            filename = f"Alertas_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            fecha = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')


            #abre el archivo filename para escribir
            with open(filename, 'w') as file:
                
                #escribe encabezamiento
                file.write(f"ESTADO DE LAS ALERTAS A FECHA: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
                #escribe linea en blanco
                file.write(f"\n")
                #escribe las alarmas 
                file.write(alarm_text)

            #cambia el texto de la etiqueta 1 
            self.label.text = f"Las alarmas se han guardado en el archivo: {filename}"
            #cambia el texto de la etiqueta 2
            self.label2.text = "ESTADO DE LAS ALERTAS A FECHA: " + str(fecha) + "\n" + "\n" + alarm_text
        else:
            #si hay error lo pone en la etiqueta 1
            self.label.text = "Error en las credenciales."


if __name__ == '__main__':
    Jaguar_AlarmApp().run()
