urban_routes_url = 'https://cnt-58665e07-db9e-48ab-8f91-0784fc3d0d83.containerhub.tripleten-services.com/?lng=es'
address_from = 'East 2nd Street, 601'
address_to = '1300 1st St'
phone_number = '+11231231212'
card_number, card_code = '1234 5678 9100', '111'
message_for_driver = 'Muéstrame el camino al museo'


def test_choose_comfort(self):
    self.driver.get(data.urban_routes_url)
    self.test_set_route()
