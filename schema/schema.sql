CREATE TABLE IF NOT EXISTS attacker (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS request_header (
    id SERIAL PRIMARY KEY,
    method VARCHAR(255) NULL,
    url VARCHAR(255) NULL,
    user_agent VARCHAR(512) NULL,
    sec_ch_ua TEXT NULL,
    sec_ch_ua_platform VARCHAR(255) NULL,
    client_ip VARCHAR(255) NULL,
    cookies TEXT NULL,
    attack_type VARCHAR(255) NULL,
    attacker_id INTEGER NULL,
    CONSTRAINT fk_attacker FOREIGN KEY (attacker_id) REFERENCES attacker(id) ON DELETE CASCADE
);


INSERT INTO attacker (name) VALUES
('Anonymous'),
('Script Kiddie'),
('Advanced Persistent Threat (APT)'),
('Botnet Operator'),
('Insider Threat')
ON CONFLICT (name) DO NOTHING;



INSERT INTO request_header (
    method, url, user_agent, sec_ch_ua, sec_ch_ua_platform,
    client_ip, cookies, attack_type, attacker_id
) VALUES
('GET', 'http://malicious.com/login', 'Mozilla/5.0', NULL, 'Windows', '192.168.1.10', 'sessionid=abc123', 'SQL Injection', 1),
('POST', 'http://victim.com/upload', 'Chrome/101.0.4951.64', '<script>alert(1)</script>', 'Linux', '10.0.0.5', 'auth=xyz987', 'XSS', 2),
('GET', 'http://banking.com/account', 'Mozilla/5.0 (Macintosh)', NULL, 'MacOS', '172.16.0.2', 'token=secure', 'Brute Force', 3),
('POST', 'http://api.victim.com/data', 'Opera/9.80', NULL, 'Android', '203.0.113.45', 'PHPSESSID=deadbeef', 'API Abuse', 4),
('PUT', 'http://shop.com/cart', 'Safari/537.36', NULL, 'iOS', '192.0.2.1', 'cart=exploit', 'Credential Stuffing', 5);
