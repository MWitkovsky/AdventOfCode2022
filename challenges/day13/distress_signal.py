# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class Packet:
    def __init__(self, data: list[int | list[int]]):
        self.__data = data

    def __eq__(self, other: "Packet"):
        if not isinstance(other, Packet):
            raise ValueError("Incomparable types")
        return self.__data == other.__data

    def __lt__(self, other: "Packet"):
        if not isinstance(other, Packet):
            raise ValueError("Incomparable types")

        other_data_len = len(other.data)
        for i, packet_segment in enumerate(self.__data):
            if i == other_data_len:
                return False
            other_segment = other.data[i]
            if packet_segment == other_segment:
                continue

            seg_type = type(packet_segment)
            other_type = type(other_segment)
            if seg_type != other_type:
                if seg_type == int:
                    packet_segment = [packet_segment]
                    seg_type = list
                else:
                    other_segment = [other_segment]
                    other_type = list

            if seg_type == other_type:
                if seg_type == int:
                    return packet_segment < other_segment
                else:
                    return Packet(packet_segment) < Packet(other_segment)
        return True

    @property
    def data(self) -> list[int | list[int]]:
        return self.__data


def _distress_signal(inp: list[list[int | list[int]]]):
    """
    Part 1:
        Determine which pairs of packets are already in the right order.
        What is the sum of the indices of those pairs?
    Part 2:

    """
    all_packets = []  # list[Packet]
    packet_pairs = []  # list[tuple[Packet, Packet]]
    for i in range(0, len(inp), 3):
        packet_pair = (Packet(inp[i]), Packet(inp[i+1]))
        all_packets.extend(packet_pair)
        packet_pairs.append(packet_pair)

    right_order_pairs = [i+1 for i, pair in enumerate(packet_pairs)
                         if pair[0] < pair[1]]
    print(f"Part 1: {sum(right_order_pairs)}")

    sorted_packets = sorted(all_packets)
    lo_signal_packet = Packet([[2]])
    hi_signal_packet = Packet([[6]])
    lo_packet_index = 0
    hi_packet_index = 0
    for i, packet in enumerate(sorted_packets):
        if lo_packet_index == 0:
            if lo_signal_packet > packet:
                continue
            lo_packet_index = i + 1
        else:
            if hi_signal_packet > packet:
                continue
            hi_packet_index = i + 2
            break
    print(f"Part 2: {lo_packet_index * hi_packet_index}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array(elem_type="json")
    parser.close()

    _distress_signal(inp)
