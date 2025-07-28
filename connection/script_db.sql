SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `db_inventario` DEFAULT CHARACTER SET utf8 ;
USE `db_inventario` ;

-- -----------------------------------------------------
-- Table `db_inventario`.`direcciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`direcciones` (
  `iddirecciones` INT(11) NOT NULL AUTO_INCREMENT,
  `direccion` VARCHAR(100) NOT NULL,
  `numero` INT(11) NULL DEFAULT NULL,
  `piso` INT(11) NULL DEFAULT NULL,
  `dpto` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`iddirecciones`))
ENGINE = InnoDB
AUTO_INCREMENT = 52
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`personas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`personas` (
  `idpersonas` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `direcciones_iddirecciones` INT(11) NOT NULL,
  PRIMARY KEY (`idpersonas`),
  INDEX `fk_personas_direcciones1_idx` (`direcciones_iddirecciones` ASC),
  CONSTRAINT `fk_personas_direcciones1`
    FOREIGN KEY (`direcciones_iddirecciones`)
    REFERENCES `db_inventario`.`direcciones` (`iddirecciones`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 53
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`clientes` (
  `idClientes` INT(11) NOT NULL AUTO_INCREMENT,
  `personas_idpersonas` INT(11) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idClientes`),
  INDEX `fk_clientes_personas1_idx` (`personas_idpersonas` ASC),
  CONSTRAINT `fk_clientes_personas1`
    FOREIGN KEY (`personas_idpersonas`)
    REFERENCES `db_inventario`.`personas` (`idpersonas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`proveedores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`proveedores` (
  `idproveedores` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(255) NULL DEFAULT NULL,
  `personas_idpersonas` INT(11) NOT NULL,
  `web` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`idproveedores`),
  INDEX `fk_proveedores_personas1_idx` (`personas_idpersonas` ASC),
  CONSTRAINT `fk_proveedores_personas1`
    FOREIGN KEY (`personas_idpersonas`)
    REFERENCES `db_inventario`.`personas` (`idpersonas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 18
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`tipo_movimiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`tipo_movimiento` (
  `idtipo_movimiento` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` VARCHAR(45) NOT NULL,
  `proveedores_idproveedores` INT(11) NULL DEFAULT NULL,
  `clientes_idClientes` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idtipo_movimiento`),
  INDEX `fk_tipo_movimiento_proveedores1_idx` (`proveedores_idproveedores` ASC),
  INDEX `fk_tipo_movimiento_clientes1_idx` (`clientes_idClientes` ASC),
  CONSTRAINT `fk_tipo_movimiento_clientes1`
    FOREIGN KEY (`clientes_idClientes`)
    REFERENCES `db_inventario`.`clientes` (`idClientes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tipo_movimiento_proveedores1`
    FOREIGN KEY (`proveedores_idproveedores`)
    REFERENCES `db_inventario`.`proveedores` (`idproveedores`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 209
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`movimiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`movimiento` (
  `idMovimiento` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL DEFAULT NULL,
  `tipo_movimiento_idtipo_movimiento` INT(11) NOT NULL,
  PRIMARY KEY (`idMovimiento`),
  INDEX `fk_movimiento_tipo_movimiento1_idx` (`tipo_movimiento_idtipo_movimiento` ASC),
  CONSTRAINT `fk_movimiento_tipo_movimiento1`
    FOREIGN KEY (`tipo_movimiento_idtipo_movimiento`)
    REFERENCES `db_inventario`.`tipo_movimiento` (`idtipo_movimiento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 209
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`marcas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`marcas` (
  `idmarcas` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`idmarcas`))
ENGINE = InnoDB
AUTO_INCREMENT = 49
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`rubros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`rubros` (
  `idrubros` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idrubros`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`productos` (
  `idproductos` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `cantidad` INT(11) NOT NULL,
  `descripcion` VARCHAR(255) NULL DEFAULT NULL,
  `rubros_idrubros` INT(11) NOT NULL,
  `proveedores_idproveedores` INT(11) NULL DEFAULT NULL,
  `marcas_idmarcas` INT(11) NOT NULL,
  `pCompra` DOUBLE NOT NULL,
  `pVenta` DOUBLE NOT NULL,
  `estado` INT(11) NOT NULL,
  `cant_minima` INT(11) NOT NULL,
  `genero` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idproductos`),
  INDEX `fk_productos_rubros1_idx` (`rubros_idrubros` ASC),
  INDEX `fk_productos_proveedores1_idx` (`proveedores_idproveedores` ASC),
  INDEX `fk_productos_marcas1_idx` (`marcas_idmarcas` ASC),
  CONSTRAINT `fk_productos_marcas1`
    FOREIGN KEY (`marcas_idmarcas`)
    REFERENCES `db_inventario`.`marcas` (`idmarcas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_productos_proveedores1`
    FOREIGN KEY (`proveedores_idproveedores`)
    REFERENCES `db_inventario`.`proveedores` (`idproveedores`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_productos_rubros1`
    FOREIGN KEY (`rubros_idrubros`)
    REFERENCES `db_inventario`.`rubros` (`idrubros`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`detalle_movimiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`detalle_movimiento` (
  `iddetalle_movimiento` INT(11) NOT NULL AUTO_INCREMENT,
  `cantidad` INT(11) NULL DEFAULT NULL,
  `precio_unitario` DOUBLE NULL DEFAULT NULL,
  `productos_idproductos` INT(11) NOT NULL,
  `movimiento_idMovimiento` INT(11) NOT NULL,
  PRIMARY KEY (`iddetalle_movimiento`),
  INDEX `fk_detalle_movimiento_productos1_idx` (`productos_idproductos` ASC),
  INDEX `fk_detalle_movimiento_movimiento1_idx` (`movimiento_idMovimiento` ASC),
  CONSTRAINT `fk_detalle_movimiento_movimiento1`
    FOREIGN KEY (`movimiento_idMovimiento`)
    REFERENCES `db_inventario`.`movimiento` (`idMovimiento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_movimiento_productos1`
    FOREIGN KEY (`productos_idproductos`)
    REFERENCES `db_inventario`.`productos` (`idproductos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 245
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`generos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`generos` (
  `idgeneros` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idgeneros`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`modelos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`modelos` (
  `idmodelos` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(50) NOT NULL,
  `marcas_idmarcas` INT(11) NOT NULL,
  PRIMARY KEY (`idmodelos`),
  INDEX `fk_modelos_marcas1_idx` (`marcas_idmarcas` ASC),
  CONSTRAINT `fk_modelos_marcas1`
    FOREIGN KEY (`marcas_idmarcas`)
    REFERENCES `db_inventario`.`marcas` (`idmarcas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`pagos` (
  `idpagos` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `monto` DOUBLE NOT NULL,
  `tipo_movimiento_idtipo_movimiento` INT(11) NOT NULL,
  PRIMARY KEY (`idpagos`),
  INDEX `fk_pagos_tipo_movimiento1_idx` (`tipo_movimiento_idtipo_movimiento` ASC),
  CONSTRAINT `fk_pagos_tipo_movimiento1`
    FOREIGN KEY (`tipo_movimiento_idtipo_movimiento`)
    REFERENCES `db_inventario`.`tipo_movimiento` (`idtipo_movimiento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`telefonos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`telefonos` (
  `idtelefono` INT(11) NOT NULL AUTO_INCREMENT,
  `numero` BIGINT(20) NOT NULL,
  `tipo` VARCHAR(45) NOT NULL,
  `personas_idpersonas` INT(11) NOT NULL,
  PRIMARY KEY (`idtelefono`),
  INDEX `fk_telefonos_personas1_idx` (`personas_idpersonas` ASC),
  CONSTRAINT `fk_telefonos_personas1`
    FOREIGN KEY (`personas_idpersonas`)
    REFERENCES `db_inventario`.`personas` (`idpersonas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 54
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`tipos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`tipos` (
  `idtipos` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NOT NULL,
  `rubros_idrubros` INT(11) NOT NULL,
  PRIMARY KEY (`idtipos`),
  INDEX `fk_tipos_rubros1_idx` (`rubros_idrubros` ASC),
  CONSTRAINT `fk_tipos_rubros1`
    FOREIGN KEY (`rubros_idrubros`)
    REFERENCES `db_inventario`.`rubros` (`idrubros`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_inventario`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_inventario`.`usuarios` (
  `idusuarios` INT(11) NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NOT NULL,
  `personas_idpersonas` INT(11) NOT NULL,
  `contraseña` VARCHAR(45) NOT NULL,
  `usuario` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idusuarios`),
  INDEX `fk_usuarios_personas1_idx` (`personas_idpersonas` ASC),
  CONSTRAINT `fk_usuarios_personas1`
    FOREIGN KEY (`personas_idpersonas`)
    REFERENCES `db_inventario`.`personas` (`idpersonas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
