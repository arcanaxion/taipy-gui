from datetime import datetime
from typing import List

from taipy.cycle.cycle import Cycle
from taipy.cycle.cycle_model import CycleModel
from taipy.cycle.frequency import Frequency
from taipy.repository import FileSystemRepository


class CycleRepository(FileSystemRepository[CycleModel, Cycle]):
    def __init__(self, dir_name="cycles"):
        super().__init__(model=CycleModel, dir_name=dir_name)

    def to_model(self, cycle: Cycle) -> CycleModel:
        return CycleModel(
            id=cycle.id,
            name=cycle.name,
            frequency=cycle.frequency,
            creation_date=cycle.creation_date.isoformat(),
            start_date=cycle.start_date.isoformat() if cycle.start_date else None,
            end_date=cycle.end_date.isoformat() if cycle.end_date else None,
            properties=cycle.properties,
        )

    def from_model(self, model: CycleModel) -> Cycle:
        return Cycle(
            id=model.id,
            name=model.name,
            frequency=model.frequency,
            properties=model.properties,
            creation_date=datetime.fromisoformat(model.creation_date),
            start_date=datetime.fromisoformat(model.start_date) if model.start_date else None,
            end_date=datetime.fromisoformat(model.end_date) if model.end_date else None,
        )

    def get_cycles_by_frequency_and_creation_date(self, frequency: Frequency, creation_date: datetime) -> List[Cycle]:
        cycles_by_frequency = self.__get_cycles_by_frequency(frequency)
        cycles_by_creation_date = self.__get_cycles_by_creation_date(creation_date)
        return list(set(cycles_by_frequency) & set(cycles_by_creation_date))

    def get_cycles_by_frequency_and_overlapping_date(self, frequency: Frequency, date=datetime) -> List[Cycle]:
        cycles_by_frequency = self.__get_cycles_by_frequency(frequency)
        cycles_by_overlapping_date = self.__get_cycles_with_overlapping_date(date)
        return list(set(cycles_by_frequency) & set(cycles_by_overlapping_date))

    def __get_cycles_by_creation_date(self, creation_date: datetime) -> List[Cycle]:
        cycles_by_creation_date = []
        for cycle in self.load_all():
            if cycle.creation_date == creation_date:
                cycles_by_creation_date.append(cycle)
        return cycles_by_creation_date

    def __get_cycles_by_frequency(self, frequency: Frequency) -> List[Cycle]:
        cycles_by_frequency = []
        for cycle in self.load_all():
            if cycle.frequency == frequency:
                cycles_by_frequency.append(cycle)
        return cycles_by_frequency

    def __get_cycles_with_overlapping_date(self, date=datetime) -> List[Cycle]:
        cycles_by_overlapping_date = []
        for cycle in self.load_all():
            if cycle.start_date <= date <= cycle.end_date:
                cycles_by_overlapping_date.append(cycle)
        return cycles_by_overlapping_date