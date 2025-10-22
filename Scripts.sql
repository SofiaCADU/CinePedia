-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema certificación_sofia
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `certificación_sofia` ;

-- -----------------------------------------------------
-- Schema certificación_sofia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `certificación_sofia` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `certificación_sofia` ;

-- -----------------------------------------------------
-- Table `certificación_sofia`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `certificación_sofia`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `certificación_sofia`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `certificación_sofia`.`peliculas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `certificación_sofia`.`peliculas` ;

CREATE TABLE IF NOT EXISTS `certificación_sofia`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `titulo` VARCHAR(50) NOT NULL,
  `sinopsis` TEXT NOT NULL,
  `director` VARCHAR(50) NOT NULL,
  `fecha_estreno` DATETIME NOT NULL,
  `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `titulo` (`titulo` ASC) VISIBLE,
  INDEX `fk_peliculas_usuario_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuario`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificación_sofia`.`usuarios` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `certificación_sofia`.`comentarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `certificación_sofia`.`comentarios` ;

CREATE TABLE IF NOT EXISTS `certificación_sofia`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pelicula_id` INT NOT NULL,
  `usuario_id` INT NOT NULL,
  `contenido` TEXT NOT NULL,
  `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `pelicula_id` (`pelicula_id` ASC) VISIBLE,
  INDEX `usuario_id` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `comentarios_ibfk_1`
    FOREIGN KEY (`pelicula_id`)
    REFERENCES `certificación_sofia`.`peliculas` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `comentarios_ibfk_2`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificación_sofia`.`usuarios` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
