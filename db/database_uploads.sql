CREATE TABLE uploads (
    upload_id INT NOT NULL AUTO_INCREMENT,
    image_name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (upload_id)
);