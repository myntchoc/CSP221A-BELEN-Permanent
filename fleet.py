from abc import ABC, abstractmethod
from functools import wraps
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def log_action(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        logging.info("Starting %s", method.__name__)
        result = method(*args, **kwargs)
        logging.info("Finished %s", method.__name__)
        return result

    return wrapper


class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        message = (
            f"{robot_name} needs {required}% battery for this task "
            f"but only has {available}%."
        )
        super().__init__(message)


class Robot(ABC):
    manufacturer = "Fleet Robotics"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, battery={self.battery})"

    def use_battery(self, amount):
        if self.battery < amount:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @abstractmethod
    def perform_task(self):
        pass


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=10):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    def perform_task(self):
        self.use_battery(15)
        return f"{self.name} is cleaning the area."


class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    @log_action
    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} is surveying the area from the air."


def fleet_report(robots):
    for robot in robots:
        print(str(robot))


def run_task_safely(robot, **kwargs):
    try:
        task_result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as error:
        logging.error(error)
    else:
        print(task_result)
    finally:
        print(f"{robot.name} current battery: {robot.battery}%")


class SharedListExample:
    some_list = []


class IndependentListExample:
    def __init__(self):
        self.some_list = []


if __name__ == "__main__":
    print("Mutable class attribute demonstration:")

    first_shared = SharedListExample()
    second_shared = SharedListExample()
    first_shared.some_list.append("changed by first object")
    print("Shared list:", first_shared.some_list)
    print("Second object sees:", second_shared.some_list)

    first_independent = IndependentListExample()
    second_independent = IndependentListExample()
    first_independent.some_list.append("changed by first object")
    print("Independent first list:", first_independent.some_list)
    print("Independent second list:", second_independent.some_list)
