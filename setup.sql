-- Criação do banco de dados
CREATE DATABASE torneio_badminton;
USE torneio_badminton;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    tipo ENUM('usuario', 'administrador') NOT NULL DEFAULT 'usuario'
);

-- Inserção de usuário para teste
INSERT INTO usuarios (usuario, senha, email, tipo) VALUES
('ivanilson', 'krolanda', 'ivanilsonpc@outlook.com', 'usuario');

-- Tabela de partidas
CREATE TABLE partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria ENUM(
        'Simples Masculino', 
        'Simples Feminino', 
        'Duplas Masculinas', 
        'Duplas Femininas', 
        'Mista', 
        'Parabadminton'
    ) NOT NULL,
    jogador1 VARCHAR(100) NOT NULL,
    jogador2 VARCHAR(100) NOT NULL,
    horario TIME NOT NULL,
    resultado VARCHAR(50)
);

-- Tabela de classificação
CREATE TABLE classificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria ENUM(
        'Simples Masculino', 
        'Simples Feminino', 
        'Duplas Masculinas', 
        'Duplas Femininas', 
        'Mista', 
        'Parabadminton'
    ) NOT NULL,
    jogador VARCHAR(100) NOT NULL,
    pontos INT NOT NULL
);

-- Tabela de comentários
CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    comentario TEXT NOT NULL
);

-- Tabela de melhores do ano
CREATE TABLE melhores_do_ano (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    foto_url VARCHAR(255),
    video_url VARCHAR(255)
);

-- Tabela de eventos
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data DATE NOT NULL,
    descricao TEXT
);

-- Inserção de dados na tabela melhores_do_ano
INSERT INTO melhores_do_ano (categoria, nome, foto_url, video_url) VALUES
('Simples Masculino', 'Jogador A', '/static/img/jogador_a.jpg', '/static/videos/jogador_a.mp4'),
('Duplas Femininas', 'Jogadoras B & C', '/static/img/jogadoras_bc.jpg', NULL);