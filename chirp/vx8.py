#!/usr/bin/python
#
# Copyright 2010 Dan Smith <dsmith@danplanet.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from chirp import chirp_common, yaesu_clone, vx8_ll

class VX8Radio(yaesu_clone.YaesuCloneModeRadio):
    BAUD_RATE = 38400
    VENDOR = "Yaesu"
    MODEL = "VX-8"

    _memsize = 65227

    _block_lengths = [ 10, 65217 ]
    _block_size = 32

    def get_features(self):
        rf = chirp_common.RadioFeatures()
        rf.has_bank = False
        rf.has_dtcs_polarity = False
        rf.valid_modes = ["FM", "WFM", "AM"]
        return rf

    def get_raw_memory(self, number):
        return vx8_ll.get_raw_memory(self._mmap, number)

    def _update_checksum(self):
        vx8_ll.update_checksum(self._mmap)

    def get_memory(self, number):
        return vx8_ll.get_memory(self._mmap, number)

    def set_memory(self, memory):
        if not self._mmap:
            self.sync_in()

        if memory.empty:
            self._mmap = vx8_ll.erase_memory(self._mmap, memory.number)
        else:
            self._mmap = vx8_ll.set_memory(self._mmap, memory)

    def get_banks(self):
        return []

    def get_memory_upper(self):
        return 900

    def filter_name(self, name):
        return chirp_common.name16(name)