import os
from xmm.util import file_is_empty
from xmm.util import convert_size
from xmm.util import parse_config
from xmm.util import check_if_not_create
from xmm.util import replace_last


def test_file_is_empty():
    assert file_is_empty('README.md') is False


def test_convert_size():
    assert convert_size(1) == '1B'
    assert convert_size(1023) == '1023B'
    assert convert_size(1024) == '1KB'
    assert convert_size(1025) == '1KB'
    assert convert_size(1048575) == '1023KB'
    assert convert_size(1048576) == '1MB'
    assert convert_size(1048577) == '1MB'
    assert convert_size(1073741823) == '1023MB'
    assert convert_size(1073741824) == '1GB'
    assert convert_size(1073741825) == '1GB'
    assert convert_size(1099511627775) == '1023GB'
    assert convert_size(1099511627776) == '1.0TB'
    assert convert_size(1099511627777) == '1.0TB'


def test_parse_config():
    _conf = parse_config(os.path.expanduser('~/.xmm.cfg'))
    assert 'target_dir' in _conf


def test_replace_last():
    _string = replace_last('one, two, three,', ',', ';')
    assert _string == 'one, two, three;'
