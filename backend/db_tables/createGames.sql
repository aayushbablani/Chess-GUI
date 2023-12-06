CREATE TABLE `games`
(
    `pk`      int NOT NULL AUTO_INCREMENT,
    `user` int,
    PRIMARY KEY (`pk`),
    FOREIGN KEY (`user`) REFERENCES `users`(`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci