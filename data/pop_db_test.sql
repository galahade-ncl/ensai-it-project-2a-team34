INSERT INTO user_table(username, password, email) VALUES
('admin',     '0000',     'admin@project.io'   ),
('a',         'a',        'a@ensai.fr'         ),
('maurice',   '1234',     'maurice@ensai.fr'   ),
('batricia',  '9876',     'bat@project.io'     ),
('miguel',    'abcd',     'miguel@project.io'  ),
('gilbert',   'toto',     'gilbert@project.io' ),
('junior',    'aaaa',     'junior@project.io'  ),
(5,           'kelkel',   '5@gmail.com'        ),
('bonjour',    5438,      'bonjour@test.fr'    ),
('arty',      'password', TRUE                 );

INSERT INTO project_table(name_project, id_user, HMAC_key) VALUES
('projet_info',       3,      'bGoa+V7g/yqDXvKRqq+JTFn4uQZbPiQJo4pf9RzJ'                              ),
('MIGUEL',            5,      'VGVzdEtleUZvckhNQUNBcGlWYWxpZGF0aW9uMjAyNg=='                          ),
('tp4',               4,      'secret-key-pour-les-tests-locaux'                                      ),
('voiture',           8,      '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'      ),
('camion',            8,      'TFn4uQa+4vcleUZV7IeyDXvKAyn4cNg=c=Zb/P'                                ),
('test_de_projet',    6,      'fdslirgHR_rhoP3ZIJF5ruefiUREOIZPhflz568ro*àa_h5eAZEIjf'                ),
(1,                   2,      'proHV7g/apMFIeyr+JTFFARJo4*pf9RzJ'                                     ),
('aurevoir',          10,     'cka+GV4v5rhQZ3eyZIrgHiIR_fbGiQUREOJF'                                  ),
('tp3',               3,      'petite_cle'                                                            );

INSERT INTO audit_table(id_project, total_vulnerability, total_critical_vulnerability, complexity, energy_comsumption, carbon_emission_gco2e, status_qualitygate) VALUES
(1,         5,       1,        25,       120,         1584,      'passed'),
(2,         10,      0,        20,       520,         126,       'passed'),
(7,         10,      2,        10,       200,         126,       'passed'),
(3,         8,       8,        5,        870,         240,       'failed');