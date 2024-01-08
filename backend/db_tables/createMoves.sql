CREATE TABLE `moves`
(
    `pk` int NOT NULL AUTO_INCREMENT,
    `game_pk` int,
    `move_idx` int NOT NULL,        # index of move in string array
    `move` varchar(4) NOT NULL,  # move string
    PRIMARY KEY (`pk`),
    FOREIGN KEY (`game_pk`) REFERENCES `games`(`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci