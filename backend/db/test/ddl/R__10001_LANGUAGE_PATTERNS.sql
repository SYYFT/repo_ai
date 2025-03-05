CREATE TABLE language_patterns (
    id SERIAL PRIMARY KEY,
    language TEXT NOT NULL,
    module_name TEXT NOT NULL,
    file_defined TEXT NOT NULL,
    file_used TEXT NOT NULL,
    reference_type TEXT NOT NULL,
    import_rule_id INT,
    FOREIGN KEY (import_rule_id) REFERENCES language_import_rules(id)
);


CREATE TABLE language_import_rules (
    id SERIAL PRIMARY KEY,
    language TEXT NOT NULL,
    pattern TEXT NOT NULL,
    reference_type TEXT NOT NULL
);


INSERT INTO language_import_rules (language, pattern, reference_type) VALUES
    ('HTML', '<script src="..."></script>', 'JavaScript Import'),
    ('HTML', '<link rel="stylesheet" href="...">', 'CSS Import'),
    ('HTML', '<link rel="icon" href="...">', 'Favicon'),
    ('JavaScript', 'import x from "./module.js"', 'ES6 Module Import'),
    ('JavaScript', 'require("./config.json")', 'CommonJS Import'),
    ('TypeScript', 'import { func } from "./utils.ts"', 'TypeScript Import'),
    ('CSS', '@import url("styles.css");', 'CSS Import'),
    ('Python', 'import module_name', 'Python Standard Import'),
    ('Python', 'from folder import script', 'Python Local Import'),
    ('Python', 'open("config.yaml")', 'File Read'),
    ('C++', '#include "file.hpp"', 'Header File'),
    ('C++', '#include <iostream>', 'Standard Library Import'),
    ('Java', 'import package.ClassName;', 'Java Import'),
    ('Go', 'import "package/file.go"', 'Go Import'),
    ('PHP', 'require "config.php";', 'PHP Import');
