from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError
from nicegui import ui
from functions import send_frame, register_callbacks

# def update_chart(frame: Frame):
#     echart.options['series'][0]['data'] = frame.as_dict()['payload'][0]

#ui.label("Control Panel")



cm = CommunicationManager()
cm.change_transport_type(TransportType.TCP)

register_callbacks(cm)




cm.connect(TcpSettings("127.0.0.1", 3000))

# send_frame(cm, ids.PriorityID.LOW, ids.DeviceID.SERVO, 1, 0)
# send_frame(cm, ids.PriorityID.LOW, ids.DeviceID.SERVO, 0, 0)

while True:
        try:
            frame = cm.receive() # We can handle frames using callbacks or by getting frame right from receive() call
        except TransportTimeoutError:
            pass
        except UnregisteredCallbackError as e:
            pass
            #print(f"unregistered frame received: {e.frame}")

