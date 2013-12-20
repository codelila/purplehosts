from mock import Mock

import purplehosts.config

get = purplehosts.config.get = Mock(return_value={})
getFile = purplehosts.config.getFile = Mock(return_value='')
