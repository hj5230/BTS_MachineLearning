from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
import pandas as pd

# FILE_PATH = "../Auxiliaration/SourceData/"
FILE_PATH = "./SourceData/"

class WBS:
    def __init__(self, *fileName: str) -> None:
        self.wbs = [load_workbook(FILE_PATH + _ + ".xlsx") for _ in fileName]

    def wclose(self) -> None:
        [_.close() for _ in self.wbs]


class SensorData:
    def __init__(self, wbs: WBS, state: str) -> None:
        if wbs == None:
            self.state = state
            self.x1 = None
            self.y1 = None
            self.z1 = None
            self.x2 = None
            self.y2 = None
            self.z2 = None
            self.x3 = None
            self.y3 = None
            self.z3 = None
        else:
            self.state = state
            self.x1 = wbs.wbs[0][state + "_1X"]["A"][3:]
            self.y1 = wbs.wbs[0][state + "_1Y"]["A"][3:]
            self.z1 = wbs.wbs[0][state + "_1Z"]["A"][3:]
            self.x2 = wbs.wbs[1][state + "_2X"]["A"][3:]
            self.y2 = wbs.wbs[1][state + "_2Y"]["A"][3:]
            self.z2 = wbs.wbs[1][state + "_2Z"]["A"][3:]
            self.x3 = wbs.wbs[2][state + "_3X"]["A"][3:]
            self.y3 = wbs.wbs[2][state + "_3Y"]["A"][3:]
            self.z3 = wbs.wbs[2][state + "_3Z"]["A"][3:]

    def dataframing(self) -> pd.DataFrame:
        x1_series = pd.Series([cell.value for cell in self.x1], name="x1")
        y1_series = pd.Series([cell.value for cell in self.y1], name="y1")
        z1_series = pd.Series([cell.value for cell in self.z1], name="z1")
        x2_series = pd.Series([cell.value for cell in self.x2], name="x2")
        y2_series = pd.Series([cell.value for cell in self.y2], name="y2")
        z2_series = pd.Series([cell.value for cell in self.z2], name="z2")
        x3_series = pd.Series([cell.value for cell in self.x3], name="x3")
        y3_series = pd.Series([cell.value for cell in self.y3], name="y3")
        z3_series = pd.Series([cell.value for cell in self.z3], name="z3")
        df = pd.concat(
            [
                x1_series,
                y1_series,
                z1_series,
                x2_series,
                y2_series,
                z2_series,
                x3_series,
                y3_series,
                z3_series,
            ],
            axis=1,
        )
        return df


class Ranger:
    def __init__(
        self,
        start: int = None,
        end: int = None,
        length: int = None,
    ) -> None:
        counter = 0
        counter += 1 if start != None else 0
        counter += 1 if end != None else 0
        counter += 1 if length != None else 0
        if counter != 2 or (length and length < 0):
            raise Exception("Invalid Parameters")
        elif start != None and end != None:
            self.start = start
            self.end = end
        elif start != None and length != None:
            self.start = start
            self.end = start + length
        elif end != None and length != None:
            self.start = end - length
            self.end = end


class Utils:
    def subconstructor(*attr: Cell, state: str) -> SensorData:
        sd = SensorData(None, state)
        sd.x1 = attr[0]
        sd.y1 = attr[1]
        sd.z1 = attr[2]
        sd.x2 = attr[3]
        sd.y2 = attr[4]
        sd.z2 = attr[5]
        sd.x3 = attr[6]
        sd.y3 = attr[7]
        sd.z3 = attr[8]
        return sd

    def paragraphing(sd: SensorData, ranger: Ranger) -> tuple[SensorData, SensorData]:
        if ranger.start >= ranger.end or ranger.start < 0 or ranger.end > 204800:
            raise Exception("Index Out of Range")

        mid_x1 = sd.x1[ranger.start: ranger.end]
        mid_y1 = sd.y1[ranger.start: ranger.end]
        mid_z1 = sd.z1[ranger.start: ranger.end]
        mid_x2 = sd.x2[ranger.start: ranger.end]
        mid_y2 = sd.y2[ranger.start: ranger.end]
        mid_z2 = sd.z2[ranger.start: ranger.end]
        mid_x3 = sd.x3[ranger.start: ranger.end]
        mid_y3 = sd.y3[ranger.start: ranger.end]
        mid_z3 = sd.z3[ranger.start: ranger.end]

        rem_x1 = sd.x1[: ranger.start] + sd.x1[ranger.end :]
        rem_y1 = sd.y1[: ranger.start] + sd.y1[ranger.end :]
        rem_z1 = sd.z1[: ranger.start] + sd.z1[ranger.end :]
        rem_x2 = sd.x2[: ranger.start] + sd.x2[ranger.end :]
        rem_y2 = sd.y2[: ranger.start] + sd.y2[ranger.end :]
        rem_z2 = sd.z2[: ranger.start] + sd.z2[ranger.end :]
        rem_x3 = sd.x3[: ranger.start] + sd.x3[ranger.end :]
        rem_y3 = sd.y3[: ranger.start] + sd.y3[ranger.end :]
        rem_z3 = sd.z3[: ranger.start] + sd.z3[ranger.end :]

        mid_sensor_data = Utils.subconstructor(
            mid_x1,
            mid_y1,
            mid_z1,
            mid_x2,
            mid_y2,
            mid_z2,
            mid_x3,
            mid_y3,
            mid_z3,
            state=sd.state,
        )
        rem_sensor_data = Utils.subconstructor(
            rem_x1,
            rem_y1,
            rem_z1,
            rem_x2,
            rem_y2,
            rem_z2,
            rem_x3,
            rem_y3,
            rem_z3,
            state=sd.state,
        )
        
        return mid_sensor_data, rem_sensor_data


if __name__ == "__main__":
    workbooks_of_1st_machine = WBS("sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1")
    state_off_output = SensorData(workbooks_of_1st_machine, "3")
    # state_turbo_jump = SensorData(wbs, "9")
    mid, rem = Utils.paragraphing(state_off_output, Ranger(start=102400, end=122880))
    print(mid.dataframing().tail())
    print(rem.dataframing().head())
    print(type(rem.x1[0]))
    # print(state_off_output.head())
    # print(state_turbo_jump.head())
    workbooks_of_1st_machine.wclose()
