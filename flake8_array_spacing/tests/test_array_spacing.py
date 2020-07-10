import subprocess
from textwrap import dedent
import pytest


def flake8(path, *args):
    """Run flake8."""
    import os
    os.chdir(str(path))
    proc = subprocess.run(
        ['flake8', '--select', 'F,A2',
         '--ignore', 'E201,E202,E203,E221,E222,E241,F821', '.'] + list(args),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = proc.stderr.decode().strip()
    assert stderr == ''
    return proc.stdout.decode().strip(), proc.returncode


def test_installed():
    """Test that flake8 is installed."""
    out, code = flake8('.', '--version')
    assert code == 0
    assert 'array-spacing' in out


@pytest.mark.parametrize('content, output', [
    ("""
     array([[x / 2.0,       0.],
            [0.,      -y / 2.0]])'""", ''),
    ("""
     np.array([[x / 2.0,       0.],
               [0.,      -y / 2.0]])'""", ''),
    ('[[x / 2.0,       0.], [0.,      -y / 2.0]]', """\
     ./bad.py:1:11: A241 multiple spaces after ','
     ./bad.py:1:27: A241 multiple spaces after ','"""),
    ('[ -3.  + 4.1j + 2,  -10e-2 +  20e+2j ]', ''),
    ('[[ 1  , 2 ]  ,  [3, 4]]', ''),
    ('[[ a  , b ]  ,  [a, b]]', """\
     ./bad.py:1:3: A201 whitespace after '['
     ./bad.py:1:10: A202 whitespace before ']'
     ./bad.py:1:15: A241 multiple spaces after ','"""),
    ('[ np.inf , 1  , 2 , numpy.nan , -inf  ]', ''),
    ('[a, b]', ''),
    ('[ a, b]', "./bad.py:1:2: A201 whitespace after '['"),
    ('[a, b ]', "./bad.py:1:6: A202 whitespace before ']'"),
    ('[a  + b, b]',
     "./bad.py:1:3: A221 multiple spaces before operator"),
    ('[a +  b, b]',
    "./bad.py:1:5: A222 multiple spaces after operator"),  # noqa: E501
    ('[ a,  b ]', """\
     ./bad.py:1:2: A201 whitespace after '['
     ./bad.py:1:5: A241 multiple spaces after ','
     ./bad.py:1:8: A202 whitespace before ']'"""),
    ('[a,  b]', "./bad.py:1:4: A241 multiple spaces after ','"),
    ('[a,  b]  # noqa', ''),
    ('[a,  b]  # noqa: E241', ''),
])
def test_array_spacing(content, output, tmpdir):
    """Test some cases."""
    content = dedent(content)
    output = dedent(output)
    fname = tmpdir.join('bad.py')
    with open(fname, 'w') as fid:
        fid.write(content)
    got_output, got_code = flake8(tmpdir)
    assert got_output == output
    assert got_code == (1 if output else 0)
