CREATE TABLE `games`
(
    `pk`            INT NOT NULL AUTO_INCREMENT,
    user_pk          INT,
    `date_played`   DATETIME,
    PRIMARY KEY (`pk`),
    FOREIGN KEY (user_pk) REFERENCES `users`(`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci