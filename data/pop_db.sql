INSERT INTO user(username, password, email) VALUES
('admin',     '0000',  'admin@project.io'   ),
('a',         'a',     'a@ensai.fr'         ),
('maurice',   '1234',  'maurice@ensai.fr'   ),
('batricia',  '9876',  'bat@project.io'     ),
('miguel',    'abcd',  'miguel@project.io'  ),
('gilbert',   'toto',  'gilbert@project.io' ),
('junior',    'aaaa',  'junior@project.io'  );

INSERT INTO project(name_project, id_user, HMAC_key) VALUES
('projet_info',       3,      'bGoa+V7g/yqDXvKRqq+JTFn4uQZbPiQJo4pf9RzJ'                              ),
('MIGUEL',            5,      'VGVzdEtleUZvckhNQUNBcGlWYWxpZGF0aW9uMjAyNg=='                          ),
('tp4',               4,      'secret-key-pour-les-tests-locaux'                                      ),
('voiture',           8,      '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'      ),
('camion',            8,      'TFn4uQa+4vcleUZV7IeyDXvKAyn4cNg=c=Zb/P'                                ),
('test_de_projet',    6,      'fdslirgHR_rhoP3ZIJF5ruefiUREOIZPhflz568ro*àa_h5eAZEIjf'                );


INSERT INTO file(name_file, path, type_file, project_file) VALUES
('code1',           None,     "code",         3   ),
('roue',            None,     "code",         4   ),
('codetest',        None,     "code",         1   ),
('2e_fichier',      None,     "dependency",   1   ),
('miguel',          None,     "dependency",   2   ),
('code2',           None,     "dependency",   3   ),

INSERT INTO audit(id_project, total_vulnerability, total_critical_vulnerability, complexity, energy_comsumption, carbon_emission_gco2e, status_qualitygate) VALUES
(1,         5,       1,        25,       120,         1584,      "passed"),
(7,         10,      2,        10,       200,         126,       "passed");