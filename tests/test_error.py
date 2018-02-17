#########################################################################
# Tests for module pymunge.error
# Copyright (C) 2017-2018 nomadictype <nomadictype AT tutanota.com>
#
# pymunge is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  Additionally, you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# pymunge is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# and GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with pymunge.  If not, see
# <http://www.gnu.org/licenses/>.
#########################################################################

from pymunge.error import MungeErrorCode, MungeError

def test_construct_munge_error():
    e = MungeError(MungeErrorCode.EMUNGE_SNAFU.value,
            'Something bad happened', 42)
    assert e.code == MungeErrorCode.EMUNGE_SNAFU
    assert e.message == 'Something bad happened'
    assert e.result == 42
