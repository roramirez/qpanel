## QPanel Change Log

All notable changes to QPanel will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 1.1.1  (2022-07-17)


### Changed
 - Upgrade sqlalchemy from 0.9.10 to 1.3.0 in /requirements





## 1.1.0  (2022-07-17)


### Changed
 - Drop support Python 3.4
 - Upgrade Flask 1.1.14



## 1.0.1  (2022-06-05)


### Changed
 - Update doc to install in FusionPBX for Python 3
 - Re format the config sample to prevent error in ConfigIni parser

### Fixed
 - Bugfix has_key for Python 3: Close #231
   The support for Python2 was remove so, the has_key is not require to use
   in this wsgi
 - Fix issue Close #235



## 1.0.0  (2020-03-28)

### Added
- Docker support File
- Add script command to run reset stats 
- Sample configuration file for supervisord and reset stats
- Guide for FreePBX 15 as Service
- Support to filter and login by external service
- Sample e integration by domain filter for FusionPBX

### Changed
- Remove Python2.7 Support
- Use realname_queue for reset_stats_queue
- Split requirements for FreeSWITCH

### Fixed
- Support Redis version >= 3.0 for Reset stats jobs
- Remove member from a renamed Queue
- Format time for reset queue stats
- Fix reset stats for Queues


## 0.16.1  (2019-10-13)

### Fixed
-  Bugfix version dumped the failure in `/check_new_version`


## 0.16.0  (2019-10-13)

### Added
- [7d010a5] Add French translations, ref: [#199](https://github.com/roramirez/qpanel/pull/199)
- [294e1ae] Add howto install Centos 7 with FusionPBX
- [afd0b75] Add availability to enable a determined queues for users
- [e796769] Adding python-ESL to prevent using the own compiling module for Freeswitch

### Changed
- [650e597] The old theme is deprecated
- [bf02613] Upgrade Flask to 0.12.4

### Fixed
- [d441532] Bugfix: Update data of callers in the  all_queues.html
- [9adaf38] Fix url root for href for theme qpanel in the logo
- [056a87c] Fix Python 2.x Socket Error Broken Pipe, [#179](https://github.com/roramirez/qpanel/issues/179)
- [bd1e19b] Bugfix for Python 3 to set utf-8 and sys.reload

## 0.15.1  (2019-03-30)

### Added
- [f7114e5](https://github.com/roramirez/qpanel/commit/f7114e54cb20236292955f4ef3954676ae391f09) Add upgrade/update instructions
- [0aee6f0](https://github.com/roramirez/qpanel/commit/0aee6f0dd3da8e838595d7ac9e6d6072e9c8a0ac) Add docu-comment for VirtualEnv in sample file for Apache+Wsgi

### Fixed
- [#194](https://github.com/roramirez/qpanel/pull/194)  base_url fix  by @litnimax
- [268b92b](https://github.com/roramirez/qpanel/commit/268b92b2d2a9cea21229a4f370d69ea4ee442452) Update requests dependency
- [05db7b8](https://github.com/roramirez/qpanel/commit/05db7b83c51c815ed51cf99d08275d68a4a7b05d) handle events Spy, Whisper and Barge when the agent is added after the load queue/layout
- [af473fe](https://github.com/roramirez/qpanel/commit/af473fe535b92c335ef60f4bec2f2255642eb86e) Bugfix for Actions button Spy, Whispher and Barge: Close #180
- [4bd5a38](https://github.com/roramirez/qpanel/commit/4bd5a381df4d6977529ef85662a010700ca3c497) Fix $ not define for footer JS code


## 0.15.0  (2018-09-07)

### Added
- [861f41e](https://github.com/roramirez/qpanel/commit/861f41e6d12e3c55bb356c16f90481d688c9338b) Add theme support (@roramirez and @bilson)
- [8079f00](https://github.com/roramirez/qpanel/commit/8079f00ef50e7c4f0059fb94cb51c8c49f69b7f2) Add documentation for queue_log database connections.
- [#152](https://github.com/roramirez/qpanel/pull/152) Add flake8 to travis (@bilson)
- [f098908](https://github.com/roramirez/qpanel/commit/f098908ee30041560b52549dfb955d162f63492a) Add test to fix when the config.ini is present in root path
- [496dbfc](https://github.com/roramirez/qpanel/commit/496dbfca0c64d7533442ba7b6662ad822f456f93) refactor config.has_section and add tests
- [#150](https://github.com/roramirez/qpanel/pull/150) Config: Enable set configuration file path by enviroment variable
- [bed119f](https://github.com/roramirez/qpanel/commit/bed119f4887bd6168dd68da1aa8c9764d1755e27) Add support for wsgi (@bilson)
- [#147](https://github.com/roramirez/qpanel/pull/147) Support RPM spec for Issabel (@bilson)

### Changed
- [dc07772](https://github.com/roramirez/qpanel/commit/dc0777293bf31eb87f40985cb56b91a0743abd25) disable DEBUG_TB_INTERCEPT_REDIRECTS for Flask-DebugToolbar
- [6520919](https://github.com/roramirez/qpanel/commit/6520919d31334ad3168919853b7b9cc5a4369cd9) README: Update branches related about of separation for master and develop
- [#148](https://github.com/roramirez/qpanel/pull/148) Run travis with docker (@bilson)
- [#149](https://github.com/roramirez/qpanel/pull/149) Add python3.6 to tox/travis (@bilson)

### Fixed
- Fix hangup for caller into the table for the button by close td
- [#157](https://github.com/roramirez/qpanel/pull/157) Fix i18n: Close #96 Close #122 (@bilson)
- [#153](https://github.com/roramirez/qpanel/pull/153) Clean some pep8 errors (@bilson)

### 0.14.1 (2018-06-19)
- [#146](https://github.com/roramirez/qpanel/pull/146) Fix run wsgi (@bilson)

### 0.14.0 (2018-06-09)
- [3231fea](https://github.com/roramirez/qpanel/commit/3231fea6d65b7e7e0ba99cc4993805179842ee8f) Update bower version (@roramirez)
- [7a78b05](https://github.com/roramirez/qpanel/commit/7a78b05117a6aaf696fe63e1ad13030699aab980) Fix CentOS Linux release 7.2.1511 (Core) (@pathcl)
- [#88](https://github.com/roramirez/qpanel/pull/88) fix extconfig.conf (@DoM1niC)
- [9a0cc96](https://github.com/roramirez/qpanel/commit/9a0cc964b721eb48836df1e83b3c0307a88fd699) fix nginx port Elastix 2.5 with Centos update 5.10+ 
- [fe98a8e](https://github.com/roramirez/qpanel/commit/fe98a8eb890e6fbaf8ce8134320f3c7736f3a771) move parser_queuelog for run like script
- [fa170f4](https://github.com/roramirez/qpanel/commit/fa170f4707831290fb488e16836d56adf0b45710) fix some import for py3 (@roramirez)
- [3835aac](https://github.com/roramirez/qpanel/commit/3835aace53249a5545f357db95f2db644bdf492e) update AMI roles the enable some functions into .spec for RPM of Elastix 4
- [a0b8943](https://github.com/roramirez/qpanel/commit/a0b89438fea46caf125a59edf581fa2fb00310c4) set use_reloader to False
- [ab78158](https://github.com/roramirez/qpanel/commit/ab78158adacb53c2d039f028ecf5955bb02f450b) add .travis.yml
- [3b27e45](https://github.com/roramirez/qpanel/commit/3b27e45c72a33acefc3fc7397a90acf9cb034c02) add tox.ini
- [ce34785](https://github.com/roramirez/qpanel/commit/ce3478530611d6a05a644e25cc3358fa03df4d98) remove code not used into upgrader module
- [ca7435c](https://github.com/roramirez/qpanel/commit/ca7435c415589b662dda43ca206d85bc99fc61c9) remove the file .gitmodules is not use anymore.
- [637847a](https://github.com/roramirez/qpanel/commit/637847a0a7df8233bc101e8ef97a19329dc0b777) refactor code. Mode code into package module called qpanel
- [fbb5a94](https://github.com/roramirez/qpanel/commit/fbb5a942eb246435ed77d6a291541a5d0df6fa7f) improve function convert_time_when_param
- [#95](https://github.com/roramirez/qpanel/pull/95) Feature Reset stats
- [083f874](https://github.com/roramirez/qpanel/commit/083f87485f87f1dcc9d03513e460d0cfbf5d95dc) update doc Python26source to 2.6.9 Python version
- [b871991](https://github.com/roramirez/qpanel/commit/b871991df23a9c0ffffbe2e529bef295f2b101f1) SPEC for create a RPM for Elastix 4
- [4104daa](https://github.com/roramirez/qpanel/commit/4104daaffa6ef8f88cd0445fb582f7f5ee58cbe7) support Python 3
- [5c91f7c](https://github.com/roramirez/qpanel/commit/5c91f7cdec0ba75484321da5d8c266140a84d0dc) ignore .bak files
- [03fba0a](https://github.com/roramirez/qpanel/commit/03fba0a2adaf60108e2bd33a9b0c9189c97146b3) little format fix
- [52ef477](https://github.com/roramirez/qpanel/commit/52ef47703efbc0c1ebd2037c4ee9faf6f55e1708) Add sample config for apache2 and wsgi
- [457ae17](https://github.com/roramirez/qpanel/commit/457ae1728ddcd5714d896fa657a847ff4a9cf13e) Remove submodule instruction for create RPM
- [5cc61fa](https://github.com/roramirez/qpanel/commit/5cc61fab5e6fc3c28786526d2acadc25807013ad) add show config parameter.


### 0.13.1 (2016-09-20)
- [aa035cb](https://github.com/roramirez/qpanel/commit/aa035cb6b336c74129fcb83e81acc915f7ee392e) Fix bug when present space between separator of config for hide (@roramirez)


### 0.13.0 (2016-09-15)
- [590df92](https://github.com/roramirez/qpanel/commit/590df92131e9d70e7a25b6b5fa42fbdae1527519) Minor fix background logo header
- [f4067c7](https://github.com/roramirez/qpanel/commit/f4067c7a8de72ff7e6cc2d2e49a2699d59e5cc8f) restructure requirements files for dependencies
- [dfbf19d](https://github.com/roramirez/qpanel/commit/dfbf19d46e022afec844dec36b885e5c679183f9) new update pt_BR translations
- [059884a](https://github.com/roramirez/qpanel/commit/059884ad6215ca863ce6a0b12e5d7e96bc2addb3) add logo in vector format
- [7f68b95](https://github.com/roramirez/qpanel/commit/7f68b9506680ac017a02c508cb8aa97314cf86e7) Add script for WSGI support
- [35422b0](https://github.com/roramirez/qpanel/commit/35422b0517bef52b06c9f429ad4a986df8eb3994) sample config for apache2 + uwsgi
- [1767ef4](https://github.com/roramirez/qpanel/commit/1767ef4be13d107fe6ea37f87ea796f62c051798) Change use urlib2 by requests library
- [#84](https://github.com/roramirez/qpanel/pull/84) Use bower for manager of dependencies packages of JS and CSS utilities
- [dd42cf0](https://github.com/roramirez/qpanel/commit/dd42cf0f534408505f57b0d387dffee2f3688711) Use py-asterisk into requirement file
- [399a3d7](https://github.com/roramirez/qpanel/commit/399a3d7cf9ad68a35669884a156d845ab48ebcaa) Set time for pool_recycle to database connection on queuelog
- [#82](https://github.com/roramirez/qpanel/pull/82) Russian translation update

### 0.12.0 (2016-08-15)
- [22d2f1d](https://github.com/roramirez/qpanel/commit/22d2f1d359378de86e48f41ea582a792f7af0616) Add Stats from queue_log
- [0c9634c](https://github.com/roramirez/qpanel/commit/0c9634cb2dc4731b97c28e97b328983527367384) Add feature for hangup incoming calls
- [4a0657f](https://github.com/roramirez/qpanel/commit/4a0657f874750e5bd246c3e6a68de40622aebe7c) fix ExtDeprecationWarning for flask_login and flask_babel
- [#69](https://github.com/roramirez/qpanel/pull/69) move babel.cfg and messages.pot into translations directory for clean
- [#68](https://github.com/roramirez/qpanel/pull/68) Update Flask version to 0.11
- [c8d6113](https://github.com/roramirez/qpanel/commit/c8d6113b44fd84df2f687219ad4292e3433b672e) add feature remove agent from a queue

### 0.11.1 (2016-07-20)
- [a22c0f7](https://github.com/roramirez/qpanel/commit/a22c0f7230914f3ec6aebc2eddd6c91a3e1cd740) Fix import logging detect for issue #56 (@roramirez)

### 0.11.0 (2016-07-15)
- [#66](https://github.com/roramirez/qpanel/pull/66) Move file sample config.ini-dist into samples
- [#64](https://github.com/roramirez/qpanel/pull/64) Add In call Feature
- [a4c0fdb](https://github.com/roramirez/qpanel/commit/a4c0fdbaacfe6aba4d80801846fe76eee8d299f8) Fix a bug for update color label when new agent is added
- [af36976](https://github.com/roramirez/qpanel/commit/af36976a9dbc6ae6257edf69fabedabf4e1f1093) Add features Spy, Whisper and Barge
- [#63](https://github.com/roramirez/qpanel/pull/63) Show version id in footer
- [#62](https://github.com/roramirez/qpanel/pull/62) Add Tests
- [#61](https://github.com/roramirez/qpanel/pull/61) Refactor init app. Add __init__ and __main__ file

### 0.10.0 (2016-06-16)
- [c77edc9](https://github.com/roramirez/qpanel/commit/c77edc9658664ea6fad3d47174aa70d80b79d701) Install dependencies by requirements.txt file.
- [#60](https://github.com/roramirez/qpanel/pull/60) Change URL stable version.
- [24bd42d](https://github.com/roramirez/qpanel/commit/24bd42db7f84ac9acb30fd1caa20861db824cd3a) fix camelcase name GitHub keyword.
- [3035a0c](https://github.com/roramirez/qpanel/commit/3035a0c630e4516872fffee9259b23d8b648ebce) Change icon for tooltip notice of new stable version.
- [f09176f](https://github.com/roramirez/qpanel/commit/f09176f9033bade7046b9c2f28a34a16e723fcbf) remove deprecated function format_id_agent.
- [44cc4ef](https://github.com/roramirez/qpanel/commit/44cc4ef57b0adb99fbd560023af17e62201632d5) fix set name var for seconds ago into utils function.
- [4ce32ed](https://github.com/roramirez/qpanel/commit/4ce32ed5321f2bc24fc28df45e6cabdd24a7d0c8) remove deprecated Javascript function.
- [#55](https://github.com/roramirez/qpanel/pull/55) Add consolidated view feature.
- [303e08b](https://github.com/roramirez/qpanel/commit/303e08b53f8ddf53f38d758ab52e554e9442fa0e) Change port nginx close issue #56

### 0.9.1 (2016-05-30)
- [ed7f2ff](https://github.com/roramirez/qpanel/commit/ed7f2ff8db52ec886e861c870e7dce48d1674673) fixbug remove feature hide and rename queue names

### 0.9.0  (2016-05-09)
- [011d675](https://github.com/roramirez/qpanel/commit/011d675bde87bbcc231e52bb2c2e9c96cfcfde6a) fixbug when sections is defined in config original and not into template
- [48a0296](https://github.com/roramirez/qpanel/commit/48a0296e16d1277ac675d221f1709a9ea87dccd4) Refactor. Use function from QPanelConfig class for unified configs
- [ca042dd](https://github.com/roramirez/qpanel/commit/ca042dde1e99112c5c5992a2d298b0224e9ef8ca) add requirements file to install dependencies
- [1dd11b8](https://github.com/roramirez/qpanel/commit/1dd11b8ffd50208ba4139dd344f2742c625cfef2) refactor exception for not file config
- [ea145c2](https://github.com/roramirez/qpanel/commit/ea145c204add6382b0b83b531f6dbd4dd1f0b306) add Port patches Asterisk 11.X for app_queue
- [29d183a](https://github.com/roramirez/qpanel/commit/29d183a53b06734c4c2382df74aeb51d456d5f42) Change behavior when the members (agent) is paused set counter as busy
- [#50](https://github.com/roramirez/qpanel/pull/50) Update repository of  py-asterisk submodule.
- [#49](https://github.com/roramirez/qpanel/pull/49) massive fix format space for open/close brackets in templates
- [#48](https://github.com/roramirez/qpanel/pull/48) Refactor loops into templates and minimal fix format code bracket

### 0.8.1 (2016-04-11)
- [9abe336](https://github.com/roramirez/qpanel/commit/be33697b13ef5a544e3ea51e3f7674eb5f31cf) Add missing section into script migrate configs

### 0.8.0 (2016-03-17)
- [ca98b39](https://github.com/roramirez/qpanel/commit/ca98b39512e0235d0e76d917ef37db4d78c5c9c4) Add FreeSWITCH support.

### 0.7.3 (2016-03-02)
- [242e53e](https://github.com/roramirez/qpanel/commit/242e53eb302b94e1990c44c3184af7db61ac5af0) Fix a bug missing language for automatic best match

### 0.7.2 (2016-02-19)
- [59260cf](https://github.com/roramirez/qpanel/commit/59260cf3c732bbd014110a5f1f8ed362bb151118) Fix current_time parameter by default in function
- [77dd847](https://github.com/roramirez/qpanel/commit/77dd8472e910f634db1cdcb6d0b85e6ebab9c19e) fix refresh data call and last_call for new agents add in the list.
- [fbc3c6c](https://github.com/roramirez/qpanel/commit/fbc3c6cc105ee6ff6557bcef83949e017bdcf6f9) Fix wait time for a call

### 0.7.1 (2016-02-17)
- [9666392](https://github.com/roramirez/qpanel/commit/9666392c348457123b8daa8479d4b980156481da) Fix a bug not reload when used base_url /
- [#40](https://github.com/roramirez/qpanel/pull/40) Update german Translations by @DoM1niC

###0.7.0 (2016-02-12)
- [aafe5c1](https://github.com/roramirez/qpanel/commit/aafe5c1286d58ec15377fe0de35d0e8dc8f07384) Improved message error to connect Asterisk Manager API.
- [b55940e](https://github.com/roramirez/qpanel/commit/b55940e0d4b795be73b71e032af5290c2cb0268e) Add Port patches Asterisk 13.7.X for app_queue.
- [585adcf](https://github.com/roramirez/qpanel/commit/585adcf86f0808a613f782a16fd4d8c70d927c76) Add pause time of a pause of agent.
- [f514279](https://github.com/roramirez/qpanel/commit/f5142794259d51e2a8a0b0a6a7b1e851aa0daa27) Add a code of conduct.
- [cb942b3](https://github.com/roramirez/qpanel/commit/cb942b3322ce6d0431ab663131afb54f5719330d) Create patches directory add partches for Asterisk.
- [f8cc1ff](https://github.com/roramirez/qpanel/commit/f8cc1ffccc9b6e088aa191368b9a441585c2a846) Create package libs.qpanel.
- [9a55ce4](https://github.com/roramirez/qpanel/commit/9a55ce40a03d412751f9a821b14be39b880696df) Add information about queue strategy.
- [0c3a2fd](https://github.com/roramirez/qpanel/commit/0c3a2fda8e9cb78d4ff5064ef8e015e3133023b3) Update chart.js.
- [2f820df](https://github.com/roramirez/qpanel/commit/2f820df49ab98e0df53d37b83d0406d436e6ea55) add API documentation.
- [93c2f39](https://github.com/roramirez/qpanel/commit/93c2f39e2d02c1f2b54ff34c5100b22e37d7276c) add tooltips [\#23](https://github.com/roramirez/qpanel/issues/23)

### 0.6.1 (2016-01-23)
- [d2fa842](https://github.com/roramirez/qpanel/commit/d2fa842e36cec7b2f6fb12d27b3c9a667bde082a) Fix a bug for preserver old values in update_config

### 0.6.0 (2016-01-05)
- [6333e75](https://github.com/roramirez/qpanel/commit/6333e753de3b1c008fee32c39e9d6bd21166da3c) Add pt_BR translations
- [6262ccc](https://github.com/roramirez/qpanel/commit/6262ccc490f60c7fffceb75bb75e5cdcb875430a) Fix a bug in value NaN by division by 0 for Service Level
- [f830a5b](https://github.com/roramirez/qpanel/commit/f830a5bb3225fa345f54f3ec6f49f263529392b9) Improve prevent if set to 0 interval many requests
- [ce63c33](https://github.com/roramirez/qpanel/commit/ce63c33e84281fd758ec7fc516b6ff87661e75c8) Add feature login auth Issue [\#34](https://github.com/roramirez/qpanel/issues/34)


### 0.5.0 (2015-11-30)
- [47f4c10](https://github.com/roramirez/qpanel/commit/47f4c10e38dd40d41eeea5e810725879c4e31f09) Add feature show Service Level.  Issue [\#5](https://github.com/roramirez/qpanel/issues/5)
- [89b07c4](https://github.com/roramirez/qpanel/commit/89b07c4ce06026a36090c10208d788d7c1d06356) Add favicon.
- [99db9f2](https://github.com/roramirez/qpanel/commit/99db9f296965d8abaae05177a459aec3fd7ab9db) Refactor and add function get boolean value from config.
- [5334dd0](https://github.com/roramirez/qpanel/commit/5334dd008f4311c2089d98a46d94f5fa4e6ed5d7) Add script to create RPM for Elastix.
- [6ef1c8a](https://github.com/roramirez/qpanel/commit/6ef1c8ad31ea35d771d8313e4fb577d2a4b90fb4) Add feature check new stable releases.
- [5aed9d9](https://github.com/roramirez/qpanel/commit/5aed9d96a0fcae04fd90e1b04cbfaac3f545eb16) Add pause reason for Asterisk with change https://goo.gl/Njm6H5
- [26a8fc4](https://github.com/roramirez/qpanel/commit/26a8fc43773e6920c74f262670c7a6a65d25479a) Add callers in queue view Issue [\#12](https://github.com/roramirez/qpanel/issues/12)
- [b36c538](https://github.com/roramirez/qpanel/commit/b36c5381a57dd5c3624330294e2a7d2c54e312ff) Add number of agents on table for show queue.
- [63e694f](https://github.com/roramirez/qpanel/commit/63e694f6ad55cf5d4a9a4211ee494772f0d961e3) Add reload app when configuration file is changed.

### 0.4.3 (2015-11-20)
- [204659c](https://github.com/roramirez/qpanel/commit/204659ccc030767675aff11dab45a7db55df40b3) Add backwards compatibility for Elastix on config file
- [00588f6](https://github.com/roramirez/qpanel/commit/00588f67e0c58ad607ca054b87f9487be4b8791c) Fixed a bug for set config secret_key owhen is used wsgi

### 0.4.2 (2015-11-16)
- [350f86b](https://github.com/roramirez/qpanel/commit/350f86b17b077df80ad174dd9255dea31880c003) Fixed a bug on refresh data field incoming call for section queue on general view. Issue [\#26](https://github.com/roramirez/qpanel/issues/26)
- [92a75c7](https://github.com/roramirez/qpanel/commit/92a75c7fea210412d09547e94a0d06b676a5f531) Fixed a bug for path where is menu file for Elastix.

### 0.4.1 (2015-11-05)
- [14e2d10](https://github.com/roramirez/qpanel/commit/14e2d1061048465d40e58118bdcb340d77df8bbf) Fixed a bug remove agent from list if not in queue after added on list view for queues.
- [a3ff2cb](https://github.com/roramirez/qpanel/commit/a3ff2cb5d4a4be390e53994d638ee643ed54f174) Fixed a bug add new member when the list of agent on queue view dont have member.
- [ff73668](https://github.com/roramirez/qpanel/commit/ff73668c83e3bf0a8455a37378457795ddd5a64f) Fixed a bug for  close tr on table agents when is add a new


### 0.4.0 (2015-10-31)
- [c4fab97](https://github.com/roramirez/qpanel/commit/c4fab97b94b4bcf2324c3fd2f1078c3d41bc0d08) Add last_call agent on queue
- [d7b7571](https://github.com/roramirez/qpanel/commit/d7b757173874d61ddbaabbd383ff27f5f0809daa) add Russian translation (@alexcr-telecom)
- [0320525](https://github.com/roramirez/qpanel/commit/03205250ba6adbe80b7c67b91af78d325b55312b) Add german translation
- [#16](https://github.com/roramirez/qpanel/pull/16) Add Changelog
- [83792a6](https://github.com/roramirez/qpanel/commit/83792a6a9946b1222f084feb4a951ceaf979743a) Feature translations issue [\#8](https://github.com/roramirez/qpanel/issues/3) language english and spanish
- [550b548](https://github.com/roramirez/qpanel/commit/550b5487dd9945d05f92418a05abe173718d3b5f) Feature set by config secret_key
- [b1b79ff](https://github.com/roramirez/qpanel/commit/b1b79ff1eeb314e2863e5dc2d0e0c641d4ee7f31) Improve update jQuery version to v1.11.3
- [57a61b0](https://github.com/roramirez/qpanel/commit/57a61b0749bf89eea66f4832559f4d5514338077) Create dir for documentation
- [e95d066](https://github.com/roramirez/qpanel/commit/e95d0668aea46d2575a7195dd2d4c76920abe5d2) Added Logo


### 0.3.2 (2015-10-17)
- [58e650e](https://github.com/roramirez/qpanel/commit/58e650e1d7bd523c664f7ba61867975f28a3bcff) Fixed a bug on link to up on footer
- [7507174](https://github.com/roramirez/qpanel/commit/7507174d748b532bd02e3836940e76260793401d) Fixed a bug for add agent on table if not present after load the page for queue

### 0.3.1 (2015-10-14)
- [ee38b04](https://github.com/roramirez/qpanel/commit/ee38b0419eb822cd5be8fb652a5661e83026bc64) Improve: prevent multi special character for / and @ on div convert name
- [56138a3](https://github.com/roramirez/qpanel/commit/56138a3c51b6527c5eecc5ae53dc815eb1e79a8f) Add 404 HTTP response
- [f1deedd](https://github.com/roramirez/qpanel/commit/f1deedd4d57a437fe53a1a03e61f762c82582ea0) Fixed a bug Elastix Spec: Seted manager config for qpanel on   /etc/asterisk/manager_additional.conf file
- [af1ce0a](https://github.com/roramirez/qpanel/commit/af1ce0a52c78773e31a370dd874c4601f7a889a1) Fixed a bug en .spec for RPM to Elastix when uwsgi after start service.
- [bd03dc4](https://github.com/roramirez/qpanel/commit/bd03dc4ec40eeda6c2e74a6a108b46ec0c9d8cfc) Fixed a bug for NaN division by 0
- [2f47b9f](https://github.com/roramirez/qpanel/commit/2f47b9f8e46b4c8229ac3ca11baa53da1c4db17a) Add config RPM for Elastix Addons
- [35b7334](https://github.com/roramirez/qpanel/commit/35b7334e684485a4c41b3270512aa08c2be5cd62) Add base_url support
- [4d182d7](https://github.com/roramirez/qpanel/commit/4d182d706ba3eb7e2887c952d3429d48fa60a482) Add sample config for Asterisk manager
- [bd2de49](https://github.com/roramirez/qpanel/commit/bd2de4983b09cd43a194b11955123050937bd62b) Round agent percent for total agents

### 0.3.0 (2015-10-03)
- [0406f4f](https://github.com/roramirez/qpanel/commit/0406f4fe361b5bc16f4430fa3687ac553df12625) Fixed a bug on refresh data when queue has name with a space character
- [8e43a4c](https://github.com/roramirez/qpanel/commit/8e43a4c0557dcd6127dce9ec2437072c91b69e87) Fixed a bug for reconnect AMI manager
- [a243f39](https://github.com/roramirez/qpanel/commit/a243f392883fc8f4b8c5c783f1775073078d252f) Add feature set request interval by config [\#3](https://github.com/roramirez/qpanel/issues/3)
- [b61fb9c](https://github.com/roramirez/qpanel/commit/b61fb9c16fa149cbc791d68a5380b718be51ccac) Add feature rename queue name issue [\#4](https://github.com/roramirez/qpanel/issues/4)
- [2937d83](https://github.com/roramirez/qpanel/commit/2937d834d1f0e45350af4d0c288fd60585d8ef73) Add feature hide queue by config issue [\#4](https://github.com/roramirez/qpanel/issues/4)
- [92c8061](https://github.com/roramirez/qpanel/commit/92c806135d1759dfa3defbc35c3916a77eadaa4e) Add change to color status agent on queue by status
- [93eb372](https://github.com/roramirez/qpanel/commit/93eb3729a38a2896dc252d5af5a3f367de5ea995) Fixed a bug when the interface name containt a @ character

### 0.2.4 (2015-09-24)
- [2ebc6eb](https://github.com/roramirez/qpanel/commit/2ebc6eb53754175b23723e812bbd42650b4620eb) Fixed a bug introduced in commit 91d2be497e76ae886171ecdab80590df9bb66a84 issue [#\2](https://github.com/roramirez/qpanel/issues/2)

### 0.2.3 (2015-09-10)
- [6efb62d](https://github.com/roramirez/qpanel/commit/6efb62d9f50a812dcba90480049a7fb22701935b) Fixed a bug for StateInterface var in Asterisk 1.8 Close [\#1] (https://github.com/roramirez/qpanel/issues/1)

### 0.2.2 (2015-09-09)
- [2ce55be](https://github.com/roramirez/qpanel/commit/2ce55be9f7f3ed6c34ea02913f707bc1bf9a4829) Add sample animation.gif of QPanel
- [266334c](https://github.com/roramirez/qpanel/commit/266334c4f9cd18ec6729b4c7e0643a890e6e28f2) Add Licence
- [ec27975](https://github.com/roramirez/qpanel/commit/ec27975581fb128ea3ab23c5eabd4fd068a59cde) Add host config

### 0.2.1 (2015-09-01)
- [fd2aa2f](https://github.com/roramirez/qpanel/commit/fd2aa2f7d0b91e07b177dd201bf0dde982807ea7) Fixed a bug in agent status
- [010b499](https://github.com/roramirez/qpanel/commit/010b4991c78f2c8b79e59ffd2a1a438f25535e32) Improve in  validation if config.ini exists

### 0.2.0 (2015-08-29)
- [9bae5e8](https://github.com/roramirez/qpanel/commit/9bae5e84854dd31e6441cdfc5e98c47a9f92cb8d) Add README for Centos 5.x and Elastix Distributions
- [031b752](https://github.com/roramirez/qpanel/commit/031b7525f0546144de714912097a04e283a8dc2e) Add status pause on queue for agent
- [8b45f85](https://github.com/roramirez/qpanel/commit/8b45f853014503fa9fd940c2908bffbc1d98525d) Add setting for port number
- [e0ef5f6](https://github.com/roramirez/qpanel/commit/e0ef5f6c32dc94b3c182ae167cc9c61682a6faec) Add info agents on show info for queue
- [961cda8](https://github.com/roramirez/qpanel/commit/961cda8488badcc2322d3bad5f7cdf713bbdfe62) Update bootstrap version to 3.3.5
- [c8415d4](https://github.com/roramirez/qpanel/commit/c8415d46f5792c4c94364abceb14ce80152a9067) Show info by queue
- [b416cab](https://github.com/roramirez/qpanel/commit/b416cabd387ecfd8628c8c08f1f9b517a18d16d2) Improve control exception when is not connect to Asterisk manager
- [8ff6db7](https://github.com/roramirez/qpanel/commit/8ff6db7a154ec9af821ccfdca5c1fa20d096aa2a) Add examples config for nginx and uwsgi

### 0.1.1 (2015-08-06)
- [d204378](https://github.com/roramirez/qpanel/commit/d204378860ae79407d10ef3a6ad70a5193178249) Add manager and Asterisk requirement to Readme
- [7fbf296](https://github.com/roramirez/qpanel/commit/7fbf2964a0daad03fe0a0a7c8f677aaabe704778) Add update for data graph after request page
- [dd738eb](https://github.com/roramirez/qpanel/commit/dd738eb035dfccbb51a0d137832023835ecfc0ef) prevent NaN value on cero

### 0.1.0 (2015-08-02)
-  Init Version
