from communication_library.frame import Frame
from communication_library import ids
from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError
from communication_library.tcp_transport import TcpSettings
from data import data
import asyncio

#1. receive_frames
#2. send_frame
#3. update_fuel_level
#4. update_ox_level
#5. update_altitude
#6. update_ox_pressure
#7. update_angle
#8. register_callbacks
#9. handle_relay
#10. handle_servo
#11. launch_rocket
#12. cm initizalization, change transport type, callbacks registration


ASYNC_SLEEP_TIME = 0.001 #[s]



async def receive_frames():
    cm.connect(TcpSettings("127.0.0.1", 3000))
    
    while True:
        try:
            frame = cm.receive()
        except TransportTimeoutError:
            pass
        except UnregisteredCallbackError:
            pass
        await asyncio.sleep(ASYNC_SLEEP_TIME)


def send_frame(priority: ids.PriorityID, device_type: ids.DeviceID, device: int, value: int = 100, operation: ids._RelayOperationID = ids._RelayOperationID.CLOSE) -> None:
    if device_type == ids.DeviceID.SERVO:
        frame = Frame(ids.BoardID.SOFTWARE,
                  priority,
                  ids.ActionID.SERVICE,
                  ids.BoardID.ROCKET,
                  device_type,
                  device,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (value, )
                  )
    elif device_type == ids.DeviceID.RELAY:
        frame = Frame(ids.BoardID.SOFTWARE,
                      priority,
                      ids.ActionID.SERVICE,
                      ids.BoardID.ROCKET,
                      device_type,
                      device,
                      ids.DataTypeID.NO_DATA,
                      operation,
                      tuple()
                      )

    cm.push(frame)
    cm.send()


def update_fuel_level(frame: Frame)->None:
    """updates fuel_level in data.py"""
    fuel_level = frame.as_dict()['payload'][0]
    data['fuel_level'] = round(fuel_level)


def update_ox_level(frame: Frame)->None:
    """updates ox_level in data.py"""
    ox_level = frame.as_dict()['payload'][0]
    data['ox_level']  = round(ox_level)


def update_altitude(frame: Frame)->None:
    """updates altitude in data.py"""
    altitude = frame.as_dict()['payload'][0]
    data['altitude'] = round(altitude)


def update_ox_pressure(frame: Frame)->None:
    """updates ox_pressure in data.py"""
    ox_pressure = frame.as_dict()['payload'][0]
    data['ox_pressure'] = round(ox_pressure, 2)


def update_angle(frame: Frame)->None:
    """updates angle in data.py"""
    angle = frame.as_dict()['payload'][0]
    data['angle'] = round(angle, 1)


def register_callbacks()->None:
    """register update functions as callbacks for each type of frame"""
    fuel_level_frame = Frame(ids.BoardID.SOFTWARE,
                            ids.PriorityID.LOW,
                            ids.ActionID.FEED,
                            ids.BoardID.ROCKET,
                            ids.DeviceID.SENSOR,
                            0, #fuel level
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.SENSOR.value.READ,
                            ()
                        )
    ox_level_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                1, #ox level
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    altitude_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                2, #altitude
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    ox_pressure_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                3, #ox pressure
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    angle_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                4, #angle
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    cm.register_callback(update_fuel_level, fuel_level_frame)
    cm.register_callback(update_ox_level, ox_level_frame)
    cm.register_callback(update_altitude, altitude_frame)
    cm.register_callback(update_ox_pressure, ox_pressure_frame)
    cm.register_callback(update_angle, angle_frame)


def handle_relay(e, device: int):
    """sends frame to relay"""
    operation = ids.OperationID.RELAY.value.OPEN if e.value else ids.OperationID.RELAY.value.CLOSE
    send_frame(ids.PriorityID.HIGH, ids.DeviceID.RELAY, device, operation = operation)


def handle_servo(e, device: int):
    """sends frame to servo"""
    send_frame(ids.PriorityID.HIGH, ids.DeviceID.SERVO, device, value = e.args)





async def launch_rocket(e):
    """activates launch rocket sequence"""
    btn = e.sender
    btn.disable()
    btn.text = 'LAUNCHED'
    btn.classes(
        replace='w-full py-4 rounded-2xl text-xl font-black tracking-widest '
                'border-2 border-slate-700 bg-slate-900/50 text-slate-600 '
                'cursor-not-allowed'
    )
    send_frame(ids.PriorityID.HIGH, ids.DeviceID.SERVO, 2, value = 0) #open fuel_main
    send_frame(ids.PriorityID.HIGH, ids.DeviceID.SERVO, 3, value = 0) #open oxidizer_main
    await asyncio.sleep(0.2) #to prevent error
    send_frame(ids.PriorityID.HIGH, ids.DeviceID.RELAY, 1, operation = ids.OperationID.RELAY.value.OPEN) #open igniter


cm = CommunicationManager()
cm.change_transport_type(TransportType.TCP)
register_callbacks()