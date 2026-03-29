DROP TABLE student;
CREATE TABLE student
(
    student_id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL UNIQUE ,
    major VARCHAR(20) DEFAULT 'not decided',
    PRIMARY KEY(student_id)
);
ALTER TABLE student ADD gpa DECIMAL(3,2);

DESCRIBE student;
SELECT * FROM student;




INSERT INTO student(name,major) VALUES('kate' , 'Biology');

INSERT INTO student(name) VALUES('mohy');
INSERT INTO student(name,major) VALUES('SAMEH','Biology');

UPDATE student
SET major = 'Bio'
WHERE major = 'Biology';

 

