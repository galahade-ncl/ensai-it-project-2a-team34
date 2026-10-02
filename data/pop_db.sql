INSERT INTO user(username, password, email) VALUES
('admin',     '0000',  'admin@project.io'   ),
('a',         'a',     'a@ensai.fr'         ),
('maurice',   '1234',  'maurice@ensai.fr'   ),
('batricia',  '9876',  'bat@project.io'     ),
('miguel',    'abcd',  'miguel@project.io'  ),
('gilbert',   'toto',  'gilbert@project.io' ),
('junior',    'aaaa',  'junior@project.io'  );

INSERT INTO project(name_project, HMAC_key) VALUES
('projet_info',     'bGoa+V7g/yqDXvKRqq+JTFn4uQZbPiQJo4pf9RzJ'                              ),
('MIGUEL',          'VGVzdEtleUZvckhNQUNBcGlWYWxpZGF0aW9uMjAyNg=='                          ),
('tp4',             'secret-key-pour-les-tests-locaux'                                      ),
('voiture',         '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'      ),
('camion',          'TFn4uQa+4vcleUZV7IeyDXvKAyn4cNg=c=Zb/P'                                ),
('test_de_projet',  'fdslirgHR_rhoP3ZIJF5ruefiUREOIZPhflz568ro*àa_h5eAZEIjf')
(1,                 'proHV7g/apMFIeyr+JTFFARQZbGiQJo4*pf9RzJ'                               ),
("tp3",             []                                                                      );

INSERT INTO file(name_file, path, type_file, project_file) VALUES
('code1',           None,     "code",         3   ),
('roue',            None,     "code",         4   ),
('codetest',        None,     "code",         1   ),
('2e_fichier',      None,     "dependency",   1   ),
('miguel',          None,     "dependency",   2   ),
('code2',           None,     "dependency",   3   ),
('tp3_python',      None,     "code",         6   )
(5,                 None,     "dependency",   5   ),
('test_test_test',  None,     "miguel",       2   ),
('bonjour'          None,     "code",         "1" );

INSERT INTO audit(id_project, total_vulnerability, total_critical_vulnerability, complexity, energy_comsumption, carbon_emission_gco2e, status_qualitygate) VALUES
(1,         5,       1,        25,       120,         1584,      "passed"),
(2,         10,      blop,     20,       520,         126,       "passed"),
("miguel",  8,       8,        5,        870,         240,       "failed");