INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
SELECT 'Corte Masculino', 'cortemasculino', 30, 50.00
WHERE NOT EXISTS (SELECT 1 FROM tb_servicos WHERE ser_tipo='cortemasculino');

INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
SELECT 'Corte Feminino', 'cortefeminino', 60, 80.00
WHERE NOT EXISTS (SELECT 1 FROM tb_servicos WHERE ser_tipo='cortefeminino');

INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
SELECT 'Barba', 'barba', 20, 35.00
WHERE NOT EXISTS (SELECT 1 FROM tb_servicos WHERE ser_tipo='barba');

INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
SELECT 'Pintar Cabelo', 'pintarcabelo', 120, 150.00
WHERE NOT EXISTS (SELECT 1 FROM tb_servicos WHERE ser_tipo='pintarcabelo');

INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
SELECT 'Sobrancelha', 'sobrancelha', 15, 25.00
WHERE NOT EXISTS (SELECT 1 FROM tb_servicos WHERE ser_tipo='sobrancelha');