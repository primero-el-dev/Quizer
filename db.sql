CREATE TABLE user(
	id VARCHAR(50) PRIMARY KEY,
	email VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,
	role VARCHAR(50) NOT NULL
);

INSERT INTO user(id, email, password, role) VALUES('715634f3-711e-4c04-b6de-a7de4881e637', 'abc@mail.com', '$2a$12$pktZwRr8kFtNj4QYj3M0qO7cOeZfTp9gDgs5fCyXvzzZir.Lg6xxO', 'admin');

CREATE TABLE test(
	id VARCHAR(50) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	estimated_minutes INT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	show_all_result_categories BOOLEAN DEFAULT FALSE,
	show_results_as_percent BOOLEAN DEFAULT TRUE,
	created_by VARCHAR(50) NOT NULL,
	is_published BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE NO ACTION
);

CREATE TABLE question(
	id VARCHAR(50) PRIMARY KEY,
	`order` INT NOT NULL,
	content TEXT NOT NULL,
	answer_type VARCHAR(255) NOT NULL,
	test_id VARCHAR(50) NOT NULL,
	FOREIGN KEY (test_id) REFERENCES test(id) ON DELETE CASCADE
);

CREATE TABLE point_category(
	id VARCHAR(50) PRIMARY KEY,
	`order` INT NOT NULL,
	name VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	test_id VARCHAR(50) NOT NULL,
	FOREIGN KEY (test_id) REFERENCES test(id) ON DELETE CASCADE
);

CREATE TABLE answer(
	id VARCHAR(50) PRIMARY KEY,
	`order` INT NOT NULL,
	min_points INT DEFAULT 0,
	max_points INT DEFAULT 1,
	first_label VARCHAR(255) NOT NULL,
	second_label VARCHAR(255),
	step INT DEFAULT 1,
	question_id VARCHAR(50) NOT NULL,
	negative_point_category_id VARCHAR(50) NOT NULL,
	positive_point_category_id VARCHAR(50) NOT NULL,
	content VARCHAR(255) NOT NULL,
	FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
	FOREIGN KEY (negative_point_category_id) REFERENCES point_category(id) ON DELETE CASCADE,
	FOREIGN KEY (positive_point_category_id) REFERENCES point_category(id) ON DELETE CASCADE
);