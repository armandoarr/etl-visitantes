CREATE TABLE IF NOT EXISTS visitantes (
    visitor_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    fechaPrimeraVisita DATETIME,
    fechaUltimaVisita DATETIME,
    visitasTotales INT,
    visitasAnioActual INT,
    visitasMesActual INT
)
;

CREATE TABLE IF NOT EXISTS errores (
  err_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(50),
  jyv VARCHAR(30),
  badmail VARCHAR(30),
  baja VARCHAR(30),
  fecha_envio VARCHAR(30),
  fecha_open VARCHAR(30),
  opens VARCHAR(30),
  opens_virales VARCHAR(30),
  fecha_click VARCHAR(30),
  clicks VARCHAR(30),
  clicks_virales VARCHAR(30),
  links VARCHAR(30),
  ips VARCHAR(30),
  navegadores VARCHAR(30),
  plataformas VARCHAR(30),
  error VARCHAR(50)
)
;

CREATE TABLE estadisticas(
  stat_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(50),
  jyv VARCHAR(30),
  badmail VARCHAR(30),
  baja VARCHAR(30),
  fecha_envio DATETIME,
  fecha_open DATETIME,
  opens INT,
  opens_virales INT,
  fecha_click DATETIME,
  clicks INT,
  clicks_virales INT,
  links FLOAT,
  ips VARCHAR(30),
  navegadores VARCHAR(30),
  plataformas VARCHAR(30),
  visitor_id INT UNSIGNED,
  FOREIGN KEY (visitor_id)
      REFERENCES visitantes(visitor_id)
)
;
