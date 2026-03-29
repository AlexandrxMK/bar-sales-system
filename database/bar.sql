CREATE DATABASE IF NOT EXISTS bar;
USE bar;

-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bar
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cidade` varchar(100) NOT NULL,
  `torce_flamengo` tinyint(1) DEFAULT 0,
  `assiste_one_piece` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itens_venda`
--

DROP TABLE IF EXISTS `itens_venda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itens_venda` (
  `id_venda` int(11) NOT NULL,
  `id_produto` int(11) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_venda`,`id_produto`),
  KEY `id_produto` (`id_produto`),
  CONSTRAINT `itens_venda_ibfk_1` FOREIGN KEY (`id_venda`) REFERENCES `vendas` (`id_venda`),
  CONSTRAINT `itens_venda_ibfk_2` FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itens_venda`
--

LOCK TABLES `itens_venda` WRITE;
/*!40000 ALTER TABLE `itens_venda` DISABLE KEYS */;
/*!40000 ALTER TABLE `itens_venda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagamentos`
--

DROP TABLE IF EXISTS `pagamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamentos` (
  `id_pagamento` int(11) NOT NULL AUTO_INCREMENT,
  `id_venda` int(11) NOT NULL,
  `metodo` enum('cartao','boleto','pix','berries') NOT NULL,
  `status_confirmacao` enum('pendente','aprovado','recusado') DEFAULT 'pendente',
  PRIMARY KEY (`id_pagamento`),
  KEY `id_venda` (`id_venda`),
  CONSTRAINT `pagamentos_ibfk_1` FOREIGN KEY (`id_venda`) REFERENCES `vendas` (`id_venda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamentos`
--

LOCK TABLES `pagamentos` WRITE;
/*!40000 ALTER TABLE `pagamentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id_produto` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `estoque` int(11) DEFAULT 0,
  `preco` decimal(10,2) NOT NULL,
  `validade` date DEFAULT NULL,
  `categoria` varchar(50) NOT NULL,
  `fabricado_em` varchar(100) NOT NULL,
  PRIMARY KEY (`id_produto`),
  KEY `idx_produto_busca` (`nome`,`preco`,`categoria`,`fabricado_em`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (2,'Heineken','Heineken',4,99.00,'2027-01-01','',''),(4,'corona','indef',5,15.00,'2028-12-12','',''),(5,'refri','coca',2,10.00,'2029-01-01','','');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas` (
  `id_venda` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `id_vendedor` int(11) NOT NULL,
  `data_venda` datetime DEFAULT current_timestamp(),
  `valor_total` decimal(10,2) DEFAULT 0.00,
  PRIMARY KEY (`id_venda`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_vendedor` (`id_vendedor`),
  CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `vendas_ibfk_2` FOREIGN KEY (`id_vendedor`) REFERENCES `vendedores` (`id_vendedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

LOCK TABLES `vendas` WRITE;
/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendedores`
--

DROP TABLE IF EXISTS `vendedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendedores` (
  `id_vendedor` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id_vendedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendedores`
--

LOCK TABLES `vendedores` WRITE;
/*!40000 ALTER TABLE `vendedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendedores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-27 13:16:24

-- Trigger para impedir estoque negativo
DELIMITER //
CREATE TRIGGER trg_estoque_negativo BEFORE UPDATE ON produtos
FOR EACH ROW
BEGIN
    IF NEW.estoque < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque não pode ser negativo';
    END IF;
END;
//
DELIMITER ;

-- Stored Procedure para checkout (validar estoque, aplicar desconto, finalizar venda)
DELIMITER //
CREATE PROCEDURE finalizar_venda(
    IN p_id_cliente INT,
    IN p_id_vendedor INT,
    IN p_itens JSON,  -- Ex: '[{"id_produto":1, "quantidade":2}, {"id_produto":2, "quantidade":1}]'
    IN p_metodo_pagamento VARCHAR(20)
)
BEGIN
    DECLARE v_id_venda INT;
    DECLARE v_valor_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_desconto_pct INT DEFAULT 0;
    DECLARE v_desconto_valor DECIMAL(10,2);
    DECLARE v_valor_final DECIMAL(10,2);
    DECLARE v_estoque_atual INT;
    DECLARE i INT DEFAULT 0;
    DECLARE item_count INT;
    DECLARE item_id_produto INT;
    DECLARE item_quantidade INT;
    DECLARE item_preco DECIMAL(10,2);

    -- Calcular desconto baseado no cliente
    SELECT 
        CASE 
            WHEN cidade = 'Sousa' THEN 10 ELSE 0 END +
        CASE WHEN torce_flamengo = 1 THEN 10 ELSE 0 END +
        CASE WHEN assiste_one_piece = 1 THEN 10 ELSE 0 END
    INTO v_desconto_pct
    FROM clientes WHERE id_cliente = p_id_cliente;

    SET v_desconto_pct = LEAST(v_desconto_pct, 30);  -- Máximo 30%

    -- Verificar estoque para todos os itens
    SET item_count = JSON_LENGTH(p_itens);
    WHILE i < item_count DO
        SET item_id_produto = JSON_EXTRACT(p_itens, CONCAT('$[', i, '].id_produto'));
        SET item_quantidade = JSON_EXTRACT(p_itens, CONCAT('$[', i, '].quantidade'));
        
        SELECT estoque INTO v_estoque_atual FROM produtos WHERE id_produto = item_id_produto;
        IF v_estoque_atual < item_quantidade THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente';
        END IF;
        
        SET i = i + 1;
    END WHILE;

    -- Inserir venda
    INSERT INTO vendas (id_cliente, id_vendedor) VALUES (p_id_cliente, p_id_vendedor);
    SET v_id_venda = LAST_INSERT_ID();

    -- Processar itens
    SET i = 0;
    WHILE i < item_count DO
        SET item_id_produto = JSON_EXTRACT(p_itens, CONCAT('$[', i, '].id_produto'));
        SET item_quantidade = JSON_EXTRACT(p_itens, CONCAT('$[', i, '].quantidade'));
        
        SELECT preco INTO item_preco FROM produtos WHERE id_produto = item_id_produto;
        SET v_valor_total = v_valor_total + (item_preco * item_quantidade);
        
        INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario) 
        VALUES (v_id_venda, item_id_produto, item_quantidade, item_preco);
        
        UPDATE produtos SET estoque = estoque - item_quantidade WHERE id_produto = item_id_produto;
        
        SET i = i + 1;
    END WHILE;

    -- Aplicar desconto
    SET v_desconto_valor = v_valor_total * (v_desconto_pct / 100);
    SET v_valor_final = v_valor_total - v_desconto_valor;

    -- Atualizar valor total na venda
    UPDATE vendas SET valor_total = v_valor_final WHERE id_venda = v_id_venda;

    -- Inserir pagamento
    INSERT INTO pagamentos (id_venda, metodo) VALUES (v_id_venda, p_metodo_pagamento);

END;
//
DELIMITER ;

-- View para relatório mensal de vendas por vendedor
CREATE VIEW relatorio_vendas_mensal AS
SELECT 
    YEAR(v.data_venda) AS ano,
    MONTH(v.data_venda) AS mes,
    ve.nome AS vendedor,
    COUNT(v.id_venda) AS total_vendas,
    SUM(v.valor_total) AS valor_total_vendas
FROM vendas v
JOIN vendedores ve ON v.id_vendedor = ve.id_vendedor
GROUP BY YEAR(v.data_venda), MONTH(v.data_venda), ve.id_vendedor, ve.nome
ORDER BY ano DESC, mes DESC, valor_total_vendas DESC;
