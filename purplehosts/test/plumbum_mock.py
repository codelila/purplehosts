from mock import Mock

from plumbum.commands.base import BaseCommand

commandMock = Mock(spec=BaseCommand)
commandMock.__getitem__ = Mock(return_value=commandMock)
commandMock.__lshift__ = Mock(return_value=commandMock)

import sys
import plumbum.cmd
plumbum.cmd.__class__.__getattr__ = Mock(return_value=commandMock)
sys.modules['plumbum.cmd'] = plumbum.cmd
