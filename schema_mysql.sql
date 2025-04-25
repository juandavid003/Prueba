CREATE DATABASE IF NOT EXISTS BioNetDB;
USE BioNetDB;

CREATE TABLE IF NOT EXISTS resultados_examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    laboratorio_id INT NOT NULL,
    paciente_id INT NOT NULL,
    tipo_examen VARCHAR(100) NOT NULL,
    resultado VARCHAR(100) NOT NULL,
    fecha_examen DATE NOT NULL,
    UNIQUE (paciente_id, tipo_examen, fecha_examen)
);

CREATE TABLE IF NOT EXISTS log_cambios_resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operacion VARCHAR(10),
    paciente_id INT,
    tipo_examen VARCHAR(100),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



DELIMITER //
CREATE TRIGGER trg_log_cambios
AFTER INSERT ON resultados_examenes
FOR EACH ROW
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen)
    VALUES ('INSERT', NEW.paciente_id, NEW.tipo_examen);
END;
//
DELIMITER ;

INSERT IGNORE INTO resultados_examenes (laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen)
VALUES
(1, 1001, 'Hemoglobina', '13.5', '2024-04-20'),
(1, 1002, 'Glucosa', '95', '2024-04-20');

SELECT * FROM resultados_examenes;
SELECT * FROM log_cambios_resultados;
