INSERT INTO user(username, password, email, access_token) VALUES
('admin',     '0000',  'admin@project.io', 'GwXGr1IJVEjovcrKDT1Io0I10mWo-BMyx70UpOvniqQ'),
('a',         'a',     'a@ensai.fr', 'uokEUQhmJ3ptKKJ_ry9zwgJJZ10ctRFGdFS4A_w3A3M'),
('maurice',   '1234',  'maurice@ensai.fr', 'xNjLMwOI0KYt7IkSqYZ4t2AALDeHYKs1cs3E5WU3U7M'),
('batricia',  '9876',  'bat@project.io', '9pTGKrQYCsR_J9lIIxuw74K82t1U8QvJcjRsz5ByqXA'),
('miguel',    'abcd',  'miguel@project.io', null),
('gilbert',   'toto',  'gilbert@project.io', null),
('junior',    'aaaa',  'junior@project.io', null);

INSERT INTO file(name_file, id_user, HMAC_key) VALUES
('code1',     1,  'admin@project.io', hmac('code1', 'GwXGr1IJVEjovcrKDT1Io0I10mWo-BMyx70UpOvniqQ', 'sha256')),
('voiture',   1,     'a@ensai.fr', hmac('voiture', 'GwXGr1IJVEjovcrKDT1Io0I10mWo-BMyx70UpOvniqQ', 'sha256')),
('projet_info',   3,  'maurice@ensai.fr', hmac('projet_info', 'xNjLMwOI0KYt7IkSqYZ4t2AALDeHYKs1cs3E5WU3U7M', 'sha256')),
('projet_stat',  3,  'bat@project.io', hmac('projet_stat', 'xNjLMwOI0KYt7IkSqYZ4t2AALDeHYKs1cs3E5WU3U7M', 'sha256')),
('miguel',    3,  'miguel@project.io', hmac('miguel', 'xNjLMwOI0KYt7IkSqYZ4t2AALDeHYKs1cs3E5WU3U7M', 'sha256')),
('code2',   4,  'gilbert@project.io', hmac('code2', '9pTGKrQYCsR_J9lIIxuw74K82t1U8QvJcjRsz5ByqXA', 'sha256')),
('tp4',    4,  'junior@project.io'hmac('tp4', '9pTGKrQYCsR_J9lIIxuw74K82t1U8QvJcjRsz5ByqXA', 'sha256'))
;

'''
INSERT INTO audit(...) VALUES
()
;
'''