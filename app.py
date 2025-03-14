from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import mysql.connector

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'hotel_reservation_system'
}

class HotelApp(App):
    def build(self):
        layout = GridLayout(cols=2, padding=20, spacing=10, size_hint=(None, None), size=(600, 400), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        labels = ['Name', 'Room Number', 'Check-in Date', 'Check-out Date']
        self.text_inputs = []

        for label_text in labels:
            label = Label(text=label_text, size_hint_y=None, height=50, width=250, halign='right')
            text_input = TextInput(hint_text=label_text, size_hint_y=None, height=50, width=300)
            self.text_inputs.append(text_input)
            layout.add_widget(label)
            layout.add_widget(text_input)

        add_button = Button(text='Add Reservation', size_hint_y=None, height=50, width=250, background_color=(0.1, 0.5, 0.9, 1))
        add_button.bind(on_press=self.add_reservation)
        layout.add_widget(add_button)

        query_button = Button(text='Query Reservation', size_hint_y=None, height=50, width=250, background_color=(0.1, 0.5, 0.9, 1))
        query_button.bind(on_press=self.query_reservation)
        layout.add_widget(query_button)

        return layout
    
    def add_reservation(self, instance):
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        add_reservation_query = ("INSERT INTO reservations (name, room_number, check_in_date, check_out_date) "
                                 "VALUES (%s, %s, %s, %s)")
        reservation_data = (self.text_inputs[0].text, self.text_inputs[1].text,
                            self.text_inputs[2].text, self.text_inputs[3].text)

        # Check room availability
        check_availability_query = ("SELECT * FROM reservations WHERE room_number = %s AND "
                                    "(check_in_date < %s AND check_out_date > %s)")
        cursor.execute(check_availability_query, (self.text_inputs[1].text, self.text_inputs[3].text, self.text_inputs[2].text))
        reservations = cursor.fetchall()
        if reservations:
            popup = Popup(title='Error', content=Label(text='Room is already booked for this period.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            cursor.close()
            cnx.close()
            return

        cursor.execute(add_reservation_query, reservation_data)
        cnx.commit()
        cursor.close()
        cnx.close()


    def query_reservation(self, instance):
        def search_reservation(query_name):
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor()
            query = ("SELECT * FROM reservations WHERE name = %s ORDER BY name")
            cursor.execute(query, (query_name,))
            reservations = cursor.fetchall()
            cursor.close()
            cnx.close()

            popup = Popup(title='Reservations', size_hint=(None, None), size=(800, 400))
            layout = ScrollView()

            grid_layout = GridLayout(cols=5, spacing=10, size_hint_y=None)
            grid_layout.bind(minimum_height=grid_layout.setter('height'))

            # Add headers
            headers = ['ID', 'Name', 'Room Number', 'Check-in Date', 'Check-out Date']
            for header in headers:
                header_label = Label(text=header, size_hint_y=None, height=40, bold=True, font_size=16)
                grid_layout.add_widget(header_label)

            for reservation in reservations:
                for field in reservation:
                    field_label = Label(text=str(field), size_hint_y=None, height=40)
                    grid_layout.add_widget(field_label)

            layout.add_widget(grid_layout)
            popup.content = layout
            popup.open()

        popup = Popup(title='Query Reservation', size_hint=(None, None), size=(400, 150))
        query_layout = GridLayout(cols=2, padding=10, spacing=10)
        query_name_input = TextInput(hint_text='Enter Name', size_hint_x=None, width=150)
        query_button = Button(text='Search', size_hint_x=None, width=100)
        query_button.bind(on_press=lambda instance: search_reservation(query_name_input.text))
        query_layout.add_widget(query_name_input)
        query_layout.add_widget(query_button)
        popup.content = query_layout
        popup.open()

if __name__ == '__main__':
    HotelApp().run()