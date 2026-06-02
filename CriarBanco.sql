-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS tb_clientes (
    cli_id        SERIAL          PRIMARY KEY,
    cli_nome      VARCHAR(100)    NOT NULL,
    cli_cpf       CHAR(11)        UNIQUE NOT NULL,
    cli_telefone  VARCHAR(20)     NOT NULL,
    cli_email     VARCHAR(100)    NOT NULL
);

-- Tabela de Profissionais
CREATE TABLE IF NOT EXISTS tb_profissionais (
    pro_id            SERIAL          PRIMARY KEY,
    pro_nome          VARCHAR(100)    NOT NULL,
    pro_cpf           CHAR(11)        UNIQUE NOT NULL,
    pro_especialidade VARCHAR(100)    NOT NULL,
    pro_disponivel    BOOLEAN         NOT NULL DEFAULT TRUE
);

-- Tabela de Servicos
CREATE TABLE IF NOT EXISTS tb_servicos (
    ser_id      SERIAL          PRIMARY KEY,
    ser_nome    VARCHAR(100)    NOT NULL,
    ser_tipo    VARCHAR(50)     NOT NULL,
    ser_duracao INTEGER         NOT NULL CHECK (ser_duracao > 0),
    ser_preco   NUMERIC(10, 2)  NOT NULL CHECK (ser_preco > 0),

    CONSTRAINT chk_tipo_servico
        CHECK (ser_tipo IN ('cortemasculino', 'cortefeminino', 'barba',
                            'pintarcabelo', 'sobrancelha'))
);

-- Tabela de Agendamentos
CREATE TABLE IF NOT EXISTS tb_agendamentos (
    age_id         SERIAL       PRIMARY KEY,
    age_cli_id     INTEGER      NOT NULL,
    age_pro_id     INTEGER      NOT NULL,
    age_ser_id     INTEGER      NOT NULL,
    age_data_hora  TIMESTAMP    NOT NULL,
    age_status     VARCHAR(20)  NOT NULL DEFAULT 'agendado',
    age_estrategia VARCHAR(20)  NOT NULL DEFAULT 'normal',

    CONSTRAINT fk_cliente
        FOREIGN KEY (age_cli_id) REFERENCES tb_clientes(cli_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_profissional
        FOREIGN KEY (age_pro_id) REFERENCES tb_profissionais(pro_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_servico
        FOREIGN KEY (age_ser_id) REFERENCES tb_servicos(ser_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_status
        CHECK (age_status IN ('agendado', 'concluido', 'cancelado')),

    CONSTRAINT chk_estrategia
        CHECK (age_estrategia IN ('normal', 'promocional', 'fidelidade'))
);