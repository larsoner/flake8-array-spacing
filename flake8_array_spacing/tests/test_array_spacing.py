import subprocess
import pytest


def flake8(path, *args):
    """Run flake8."""
    import os
    os.chdir(str(path))
    proc = subprocess.run(
        ['flake8', '--select', 'A2',
         '--ignore', 'E201,E202,E203,E221,E222,E241', '.'] + list(args),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = proc.stderr.decode().strip()
    assert stderr == ''
    return proc.stdout.decode().strip(), proc.returncode


def test_installed():
    """Test that flake8 is installed."""
    out, code = flake8('.', '--version')
    assert code == 0
    assert 'array-spacing' in out


a_b_pre = 'a = 1\nb = 2\n'


@pytest.mark.parametrize('line, want_output, want_code', [
    ('[ -3  + 4j ,  -10 +  20j ]', '', 0),
    (a_b_pre + '[a, b]', '', 0),
    (a_b_pre + '[ a, b]', "./bad.py:3:2: A201 whitespace after '['", 1),
    (a_b_pre + '[a, b ]', "./bad.py:3:6: A202 whitespace before ']'", 1),
    (a_b_pre + '[a  + b, b]', "./bad.py:3:3: A221 multiple spaces before operator", 1),  # noqa: E501
    (a_b_pre + '[a +  b, b]', "./bad.py:3:5: A222 multiple spaces after operator", 1),  # noqa: E501
    (a_b_pre + '[a,  b]', "./bad.py:3:4: A241 multiple spaces after ','", 1),
    (a_b_pre + '[a,  b]  # noqa', '', 0),
    (a_b_pre + '[a,  b]  # noqa: E241', '', 0),
])
def test_array_spacing(line, want_output, want_code, tmpdir):
    """Test some cases."""
    fname = tmpdir.join('bad.py')
    with open(fname, 'w') as fid:
        fid.write(line)
    got_output, got_code = flake8(tmpdir)
    assert got_output == want_output
    assert got_code == want_code
